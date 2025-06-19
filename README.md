# FinOpsBot 🤖

A conversational AI assistant designed to help users with FinOps (Cloud Financial Management) tasks, leveraging a knowledge base, intent classification, semantic search, and user authentication.

## 🚀 Features

- **Natural Language Q&A**: Ask FinOps questions like "What is a savings plan?" or "Explain EC2 pricing".
- **Admin Commands**: Teach, update, alias, delete knowledge base entries.
- **Intent Classification**: Machine learning model to classify user intents.
- **Semantic Search**: FAISS-based fallback using Sentence Transformers.
- **User System**: Registration, login, email verification, password reset.
- **Chat Logging**: Logs user-bot interactions per user and date.
- **Cache Layer**: Speeds up repeated semantic searches.

## 🧱 Project Structure

```
finops_chatbot/
├── app/                    # Main Flask app with routes and config
│   ├── auth/               # User authentication & email verification
│   ├── intent/             # Intent classification logic & training
│   ├── main/               # Core bot logic and knowledge handling
│   └── config.py           # App configuration and secrets
├── core/                   # Semantic search, crawling, cache
├── data/                   # All saved and generated data files
├── static/                 # CSS styles
├── templates/              # Jinja2 HTML templates
├── logs/                   # Chat logs per user
├── run.py                  # Entry point
└── README.md               # Project description
```

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/finops-chatbot.git
   cd finops-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional):**
   You can configure SMTP settings and secret keys in `app/config.py`.

5. **Run the app:**
   ```bash
   python run.py
   ```

## 🛡️ Admin Features

Admin users can:
- `teach: term = definition`
- `update: term = new definition`
- `alias: new_term = existing_term`
- `delete: term`

## 🧠 Technologies Used

- Flask
- scikit-learn
- FAISS
- Sentence Transformers
- Jinja2
- JSON-based knowledge base

## 📨 Contact

Built by [Alex](https://github.com/Alexander-NO5) for educational and operational FinOps use cases.

---

*FinOpsBot: Making cloud costs conversational.* ☁️💬
