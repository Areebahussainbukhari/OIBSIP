"""
Random Password Generator
Oasis Infobyte AICTE SIP - Python Programming Track - Task 3

Generates a random password based on the user's chosen length
and character types (uppercase, lowercase, numbers, symbols).
"""

import random
import string


def get_length():
    """Asks for password length, enforcing a minimum of 8 characters."""
    while True:
        user_input = input("Enter desired password length (minimum 8): ")
        try:
            length = int(user_input)
        except ValueError:
            print("Error: Please enter a whole number (e.g. 12).")
            continue

        if length < 8:
            print("Error: Length must be at least 8 characters.")
            continue

        return length


def ask_yes_no(prompt):
    """
    Asks a yes/no question. Accepts full words like 'yes' or 'no',
    as well as short forms like 'y' or 'n' - not case sensitive.
    Keeps asking until it gets a recognizable answer.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type 'yes' or 'no'.")


def get_character_types():
    """
    Asks the user which character types to include.
    Requires at least 2 types to be selected.
    """
    while True:
        print("\nWhich character types do you want to include?")
        print("Answer 'yes' or 'no' for each.")

        use_upper = ask_yes_no("Include uppercase letters (A-Z)? (yes/no): ")
        use_lower = ask_yes_no("Include lowercase letters (a-z)? (yes/no): ")
        use_digits = ask_yes_no("Include numbers (0-9)? (yes/no): ")
        use_symbols = ask_yes_no("Include symbols (!@#$...)? (yes/no): ")

        selected_count = sum([use_upper, use_lower, use_digits, use_symbols])

        if selected_count < 2:
            print("Error: Please select at least 2 character types.\n")
            continue

        return use_upper, use_lower, use_digits, use_symbols


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """Builds the pool of characters to randomly choose from."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    return pool


def generate_password(length, pool):
    """Randomly picks 'length' characters from the pool to form a password."""
    return "".join(random.choice(pool) for _ in range(length))


def main():
    print("=== Random Password Generator ===")
    print("This tool creates a random password based on your preferences.\n")

    while True:
        length = get_length()
        use_upper, use_lower, use_digits, use_symbols = get_character_types()
        pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

        password = generate_password(length, pool)

        print("\n--- Generated Password ---")
        print(password)

        again = ask_yes_no("\nGenerate another password? (yes/no): ")
        if not again:
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
