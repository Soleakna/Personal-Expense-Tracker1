
import os
import hashlib

PASSWORD_FILE = "password.txt"

def hash_password(password):
    """Hash the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def set_password():
    """Set a new password."""
    password = input("Create your password: ")
    confirm_password = input("Confirm your password: ")
    if password == confirm_password:
        with open(PASSWORD_FILE, "w") as f:
            f.write(hash_password(password))
        print("Password set successfully!")
        return True
    print("Passwords do not match.")
    return False

def verify_password():
    """Verify the user's password."""
    if not os.path.exists(PASSWORD_FILE):
        print("No password found. Please set one first.")
        return False
    entered_password = input("Enter your password: ")
    with open(PASSWORD_FILE, "r") as f:
        stored_password = f.read().strip()
    if hash_password(entered_password) == stored_password:
        return True
    print("Incorrect password.")
    return False


def main():
    """
    Main function to simulate the app.
    """
    if not os.path.exists(PASSWORD_FILE):
        print("Welcome! Let's set up your password.")
        if set_password():
            print("You can now use the app!")
    else:
        print("Welcome back! Please log in.")
        if verify_password():
            print("You are now logged in.")
        else:
            print("Please try again.")

if __name__ == "__main__":
    main()
