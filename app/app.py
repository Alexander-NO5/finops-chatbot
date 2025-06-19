import datetime
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.main.knowledge_base import load_knowledge
from app.main.chatbot import answer_question
from app.auth.auth import register_user, authenticate_user, is_admin, mark_user_as_verified, get_user_by_email, reset_password
from app.auth.email_verification import send_verification_email, send_password_reset_email, serializer
from app.intent.intent_training_control import train_if_needed
from app.config import SECRET_KEY
from itsdangerous import SignatureExpired, BadSignature


# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'), static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.secret_key = SECRET_KEY

# Load the knowledge base into memory
knowledge = load_knowledge()

# Home page route, redirects to chat if logged in
@app.route('/')
def home():
    if 'user_email' in session:
        return redirect(url_for('chat'))
    return render_template('login.html')

# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        employee_id = request.form['employee_id']

        # Validate input data
        if not employee_id.isdigit():
            return render_template('register.html', message="Employee ID must contain only numbers.")

        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            return render_template('register.html', message="Please enter a valid email address.")

        if password != confirm_password:
            return render_template('register.html', message="Passwords do not match.")

        # Create user and send verification email
        message = register_user(full_name, email, password, employee_id)
        send_verification_email(full_name, email)
        return render_template('login.html', message="Registration successful. Please check your email to verify your account.")
    return render_template('register.html')

# Handle email verification links
@app.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        if mark_user_as_verified(email):
            return render_template('login.html', message="Email verified. You can now log in.")
        else:
            return "Verification failed: user not found."
    except SignatureExpired:
        return "Verification link expired."
    except BadSignature:
        return "Invalid verification link."

# Handle login logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user and get full user object if valid
        user = authenticate_user(email, password)

        if not user:
            return render_template('login.html', message="Invalid credentials or unverified email.")

        # Check if the user is verified (already checked in authenticate_user)
        if not user.get("verified", False):
            return render_template(
                'login.html',
                message="Your email is not verified. Please check your inbox.",
                show_verification=True,
                user_email=email
            )

        # Store session information including role (admin/user)
        session['user_email'] = email
        session['user_full_name'] = user['full_name']
        session['user_role'] = user.get('role', 'user')  # fallback to 'user'

        return redirect(url_for('chat'))

    return render_template('login.html')

# Handle code-based verification form
@app.route('/submit-verification', methods=['POST'])
def submit_verification():
    email = request.form['email']
    code = request.form['code']
    user = get_user_by_email(email)

    if not user:
        return render_template('login.html', message="User not found.")

    try:
        email_check = serializer.loads(code, salt='email-confirmation-salt', max_age=3600)
        if email_check == email:
            mark_user_as_verified(email)
            return render_template('login.html', message="Email verified successfully. You can now log in.")
    except Exception:
        return render_template('login.html', message="Invalid or expired verification code.", show_verification=True, user_email=email)

    return render_template('login.html', message="Verification failed.", show_verification=True, user_email=email)

# Handle forgotten password and send reset link
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = get_user_by_email(email)

        if user:
            send_password_reset_email(user["full_name"], email)

        return render_template("login.html", message="If this email is registered, a reset link was sent.")
    return render_template("forgot_password.html")

# Password reset form
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    try:
        email = serializer.loads(token, salt="reset-password-salt", max_age=3600)
    except SignatureExpired:
        return "Reset link expired."
    except BadSignature:
        return "Invalid reset link."

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            return render_template("reset_password.html", token=token, message="Passwords do not match.")
        if reset_password(email, new_password):
            return render_template("login.html", message="Password reset successful. You can now log in.")
        else:
            return "User not found."

    return render_template("reset_password.html", token=token)

# Handle logout and clear session
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_full_name', None)
    session.pop('user_role', None)
    session.pop('chat_history', None)
    return redirect(url_for('home'))

# Chat route handling conversation and commands
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    if 'chat_history' not in session:
        session['chat_history'] = []

    user_email = session['user_email']
    user_role = session['user_role']
    user_full_name = session.get('user_full_name', user_email)

    if request.method == 'POST':
        user_input = request.form['message']
        bot_response = answer_question(user_input, knowledge, user_email, user_role)

        timestamp = datetime.datetime.now().strftime("%I:%M %p")

        # Save user and bot message to chat history
        session['chat_history'].append({'sender': 'user', 'message': user_input, 'timestamp': timestamp})
        session['chat_history'].append({'sender': 'bot', 'message': bot_response, 'timestamp': timestamp})

        session.modified = True

    return render_template('chat.html', user_email=user_email, user_full_name=user_full_name, chat_history=session['chat_history'])

# Simple test route for CSS
@app.route('/test-css')
def test_css():
    return '''
    <html>
    <head>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body class="container">
        <div class="form-container">
            <h1 class="message">Styled CSS Works!</h1>
            <button class="btn">Test Button</button>
        </div>
    </body>
    </html>
    '''

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)


# Automatically retrain intent classifier if needed
train_if_needed()

if __name__ == "__main__":
    app.run(debug=True)  # or change to False for production

# OR if you want to import `main` in run.py:

def main():
    app.run(debug=True)
