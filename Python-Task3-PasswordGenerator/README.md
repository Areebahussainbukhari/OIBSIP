# Random Password Generator

**Oasis Infobyte AICTE SIP — Python Programming Track — Task 3**

## What This Project Does

This is a command-line program that generates a random password based on
the user's chosen length and preferred character types (uppercase,
lowercase, numbers, symbols).

## Features

- Asks for desired password length (minimum 8 characters enforced)
- Lets the user choose which character types to include: uppercase letters,
  lowercase letters, numbers, and symbols — requires at least 2 types to be
  selected for a stronger password
- Accepts answers as full words ("yes"/"no") in any capitalization, not
  just single letters, for clarity
- Validates all input: rejects invalid lengths, unrecognized answers, and
  fewer than 2 selected character types, asking again instead of crashing
- Generates a truly random password using Python's `random` module
- Lets the user generate additional passwords in the same session without
  restarting the program

## How to Run

1. Make sure Python is installed on your computer.
2. Open a terminal in this folder.
3. Run:
   ```
   python password_generator.py
   ```
4. Enter your desired password length (minimum 8).
5. Answer "yes" or "no" for each character type you want included.
6. Your randomly generated password will be displayed.
7. Choose whether to generate another password or exit.

## Example

```
Enter desired password length (minimum 8): 12
Which character types do you want to include?
Answer 'yes' or 'no' for each.
Include uppercase letters (A-Z)? (yes/no): yes
Include lowercase letters (a-z)? (yes/no): yes
Include numbers (0-9)? (yes/no): yes
Include symbols (!@#$...)? (yes/no): no

--- Generated Password ---
BuZGAabvmMLN

Generate another password? (yes/no): no
Goodbye!
```

## Technologies Used

- Python 3 (standard library only — `random` and `string` modules,
  no external dependencies required)

## What I Learned

Building this project helped me practice input validation across multiple
related questions at once, writing a reusable yes/no input handler, and
thinking about real user behavior — people don't always answer with a
single letter, so accepting full words like "yes"/"no" makes the tool
more forgiving and user-friendly.
