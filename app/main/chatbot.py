import re
import difflib
from app.main.chat_logger import log_chat
from app.main.knowledge_base import normalize, resolve, load_knowledge
from app.main.commands_list import teach, update, alias, delete, list_terms, show, help_menu
from app.main.web_lookup import semantic_search_cached as semantic_search
from app.main.utils import parse_term_and_source
from app.main.small_talk import handle_small_talk
from app.config import TRUSTED_SITES
from app.intent.intent_model import classify_intent
from app.intent.intent_training_control import train_if_needed
from app.intent.update_training_data import update_training_data_from_knowledge


def detect_trusted_site(user_input):
    user_input_lower = user_input.lower()
    for key in TRUSTED_SITES.keys():
        if re.search(rf"\b(according to|on|in)?\s*{key}\b", user_input_lower):
            return key
    return None


def format_multiline(text):
    return '<div class="multiline-response">' + '<br>'.join(text.splitlines()) + '</div>'


def answer_question(user_input, knowledge, user_email=None, user_role="user"):
    cleaned_input = user_input.strip().lower()
    response = None

    # === Commands ===
    if cleaned_input == "help:":
        response = format_multiline(f"{help_menu(user_role)}")

    elif cleaned_input == "list:":
        response = format_multiline(list_terms(knowledge))

    elif cleaned_input.startswith("show:"):
        term = user_input[5:].strip()
        response = format_multiline(show(term, knowledge))

    elif cleaned_input.startswith("teach:"):
        if "=" in user_input:
            term, definition = user_input[6:].split("=", 1)
            response = teach(term.strip(), definition.strip(), user_role, knowledge)
            knowledge.clear()
            knowledge.update(load_knowledge())
            update_training_data_from_knowledge()
            train_if_needed(force=True)
        else:
            response = "Format: teach: term = definition"

    elif cleaned_input.startswith("update:"):
        if "=" in user_input:
            term, definition = user_input[7:].split("=", 1)
            response = update(term.strip(), definition.strip(), user_role, knowledge)
            knowledge.clear()
            knowledge.update(load_knowledge())
            update_training_data_from_knowledge()
            train_if_needed(force=True)
        else:
            response = "Format: update: term = new definition"

    elif cleaned_input.startswith("alias:"):
        if "=" in user_input:
            new_term, existing_term = user_input[6:].split("=", 1)
            response = alias(new_term.strip(), existing_term.strip(), user_role, knowledge)
        else:
            response = "Format: alias: new_term = existing_term"

    elif cleaned_input.startswith("delete:"):
        term = user_input[7:].strip()
        response = delete(term, user_role, knowledge)
        knowledge.clear()
        knowledge.update(load_knowledge())
        update_training_data_from_knowledge()
        train_if_needed(force=True)

    # === Small Talk (after command detection!) ===
    elif handle_small_talk(cleaned_input):
        response = handle_small_talk(cleaned_input)

    # === Knowledge Matching ===
    else:
        intent = classify_intent(user_input)

        term, _ = parse_term_and_source(user_input)
        question_prefixes = [r"\bwhat is\b", r"\bdefine\b", r"\bexplain\b", r"\btell me about\b", r"\bwho is\b", r"\bdescribe\b", r"\bwhat is a\b"]
        for pattern in question_prefixes:
            term = re.sub(pattern, '', term, flags=re.IGNORECASE).strip()

        norm_term = normalize(term)
        resolved_term = resolve(norm_term, knowledge)

        if resolved_term in knowledge and not knowledge[resolved_term].startswith("__alias__"):
            response = knowledge[resolved_term]

        elif norm_term != resolved_term and norm_term in knowledge and not knowledge[norm_term].startswith("__alias__"):
            response = knowledge[norm_term]

        else:
            close_matches = difflib.get_close_matches(norm_term, knowledge.keys(), n=1, cutoff=0.7)
            if close_matches:
                closest = close_matches[0]
                if not knowledge[closest].startswith("__alias__"):
                    response = f"Did you mean '{closest}'?<br>{knowledge[closest]}"

    # === Semantic Search Fallback ===
    if response is None:
        response = semantic_search(user_input) or "I'm not sure how to help with that. Try asking a question or using a command like <code>help:</code>."

    # === Log all responses ===
    log_chat(user_email, user_input, response)
    return response
