import re

def check_password_strength(password):
    """
    Checks the strength of the given password based on several criteria:
    - Minimum length of 8 characters
    - Contains both uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character

    Returns True if all criteria are met, otherwise False.
    """
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one digit.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain at least one special character.")
        return False

    return True


# Script to take user input and validate password strength
if __name__ == "__main__":
    user_password = input("Enter a password to check its strength: ")
    if check_password_strength(user_password):
        print("Password is strong.")
    else:
        print("Password is not strong enough.")
