import joblib

# Load the trained model
classifier = joblib.load("intent_classifier.joblib")

# Test examples
examples = [
    "hello",
    "how are you?",
    "teach: cloud = serverless",
    "what is a reserved instance?",
    "thanks a lot",
    "delete: alias",
    "show: budgets",
    "finops definition from gcp"
]

# Predict intent for each example
for example in examples:
    intent = classifier.predict([example])[0]
    print(f"Input: {example}\nPredicted Intent: {intent}\n")
