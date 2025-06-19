import json
from app.main.knowledge_base import save_knowledge, normalize, resolve, load_knowledge
from app.intent.intent_training_control import train_if_needed


def teach(term, definition, role, knowledge):
    term = term.lower().strip()

    if term in knowledge:
        if knowledge[term].startswith("__alias__"):
            return f"'{term}' is an alias. Please teach the original term '{resolve(term, knowledge)}'."
        return f"The term '{term}' already exists. Use update: to modify it."

    if role != "admin":
        return "Only admins can teach new terms."

    knowledge[term] = definition
    save_knowledge(knowledge)
    train_if_needed(force=True)
    return f"Taught new term: '{term}'"


def update(term, new_definition, user_role, knowledge):
    if user_role != "admin":
        return "Only admins can update terms."

    normalized = normalize(term)
    resolved_term = resolve(normalized, knowledge)

    if resolved_term not in knowledge:
        return f"Term '{term}' does not exist."

    if knowledge[resolved_term].startswith("__alias__"):
        return f"Cannot update alias term '{term}'. Update the original term '{resolved_term}' instead."

    knowledge[resolved_term] = new_definition
    save_knowledge(knowledge)
    train_if_needed(force=True)
    return f"Updated term: '{resolved_term}' with new definition."


def alias(new_term, existing_term, role, knowledge):
    new_term = new_term.lower().strip()
    existing_term = existing_term.lower().strip()

    if role != "admin":
        return "Only admins can create aliases."

    if existing_term not in knowledge:
        return f"The target term '{existing_term}' does not exist."

    if knowledge.get(existing_term, "").startswith("__alias__"):
        existing_term = resolve(existing_term, knowledge)

    if new_term == existing_term:
        return "You cannot alias a term to itself."

    if new_term in knowledge:
        return f"The term '{new_term}' already exists."

    knowledge[new_term] = f"__alias__: {existing_term}"
    save_knowledge(knowledge)
    return f"Alias created: '{new_term}' → '{existing_term}'"


def delete(term, role, knowledge):
    term = term.lower().strip()

    if role != "admin":
        return "Only admins can delete terms."

    if term not in knowledge:
        return f"The term '{term}' does not exist."

    del knowledge[term]
    aliases_removed = [
        alias for alias, value in list(knowledge.items())
        if isinstance(value, str) and value.startswith("__alias__:") and value.replace("__alias__:", "").strip() == term
    ]
    for alias_term in aliases_removed:
        del knowledge[alias_term]

    save_knowledge(knowledge)
    train_if_needed(force=True)

    msg = f"Deleted term '{term}'."
    if aliases_removed:
        msg += f" Also removed aliases: {', '.join(aliases_removed)}."
    return msg


def list_terms(knowledge):
    real_terms = [
        term for term, value in knowledge.items()
        if not (isinstance(value, str) and value.startswith("__alias__:"))
    ]
    return "\nKnown terms:\n" + "\n".join(f"- {term}" for term in sorted(real_terms))


def show(term, knowledge):
    term = term.lower().strip()
    resolved = resolve(term, knowledge)

    if resolved not in knowledge:
        return f"No entry found for '{term}'."

    if resolved != term:
        return f"'{term}' is an alias of '{resolved}':\n{knowledge[resolved]}"
    return f"{resolved}:\n{knowledge[resolved]}"


def help_menu(role, html=False):
    commands = [
        "• help: [show this list]",
        "• list: [show all known terms]",
        "• show: term [see definition or alias target]",
        "• exit: [close the bot]",
    ]
    if role == "admin":
        commands += [
            "• teach: term = definition [teach new term]",
            "• update: term = new definition [update existing term]",
            "• alias: new_term = existing_term [add alias to existing term]",
            "• delete: term [delete term and its aliases]",
        ]
    commands.append("You can also ask questions like: 'What is a saving plan?' or 'Explain RI'")

    return "<br>".join(commands) if html else "\n".join(commands)
