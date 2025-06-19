import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.config import TRAINING_DATA_PATH, KNOWLEDGE_FILE, MODEL_PATH, STATIC_DATA_FILE


def load_training_examples():
    with open(TRAINING_DATA_PATH, "r") as f:
        training_data = json.load(f)

    examples = []
    labels = []
    for item in training_data:
        intent = item["intent"]
        if intent == "dynamic_knowledge":
            intent = "question"
        for example in item["examples"]:
            examples.append(example)
            labels.append(intent)
    return examples, labels


def load_knowledge_examples():
    if not os.path.exists(KNOWLEDGE_FILE):
        return [], []
    with open(KNOWLEDGE_FILE, "r") as f:
        knowledge = json.load(f)

    examples = [term for term, value in knowledge.items()
                if not (isinstance(value, str) and value.startswith("__alias__:"))]
    labels = ["question"] * len(examples)
    return examples, labels


def train_intent_model():
    train_x, train_y = load_training_examples()
    knowledge_x, knowledge_y = load_knowledge_examples()

    # Combine both training sets
    texts = train_x + knowledge_x
    labels = train_y + knowledge_y

    # Split into train/test for validation
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Create pipeline
    pipeline = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), stop_words="english"),
        LogisticRegression(max_iter=500)
    )

    # Train the model
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the pipeline
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Intent classifier trained and saved as '{MODEL_PATH}'")


# Run manually only if this file is executed directly
if __name__ == "__main__":
    train_intent_model()
