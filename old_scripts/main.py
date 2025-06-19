import json
from old_scripts.login_module import login_user
from old_scripts.register import register_user
from app.main.chatbot import start_chatbot
from app.config import KNOWLEDGE_FILE  # import path constant

def main():
    print("Welcome to the FinOps Chatbot!")

    while True:
        print("\nPlease choose an option:")
        print("  1. Login")
        print("  2. Register")
        print("  3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            user_info = login_user()
            if user_info:
                # Load knowledge.json ONCE here using path from config
                with open(KNOWLEDGE_FILE, "r") as f:
                    knowledge = json.load(f)

                # Pass knowledge dict to start_chatbot
                start_chatbot(user_info["email"], user_info["role"], knowledge)
            else:
                print("Login failed. Returning to main menu...")

        elif choice == "2":
            registered = register_user()
            if registered:
                print("Registration successful. You can now login.")
            else:
                print("Registration failed. Returning to main menu...")

        elif choice == "3":
            print("Exiting the chatbot. Goodbye!")
            break

        else:
            print("Invalid input. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
