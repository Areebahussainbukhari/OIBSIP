"""
BMI Calculator
Oasis Infobyte AICTE SIP - Python Programming Track - Task 2

Calculates a user's Body Mass Index (BMI) from weight and height,
and classifies the result into a standard health category.
"""

#Takes user input for weight and height
def get_positive_float(prompt):
    """
    Keeps asking the user for input until they type a valid,
    positive number. Rejects text and negative/zero values.
    """
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
        except ValueError:
            print("Error: Please enter a valid number (e.g. 65 or 65.5).")
            continue

        if value <= 0:
            print("Error: Value must be greater than zero. Please try again.")
            continue

        return value


def normalize_height(height):
    """
    Many people accidentally type their height in centimeters
    instead of meters so it have two options for user to enter in meters or centimeters.
    """
    if height > 3:
        converted = height / 100
        print(f"Note: {height} looks like centimeters, not meters. "
              f"Using {converted:.2f} m instead.")
        return converted
    return height


def calculate_bmi(weight_kg, height_m):
    """BMI formula: weight (kg) / height (m) squared."""
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    """Returns the standard BMI health category for a given BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    print("=== BMI Calculator ===")
    print("This tool calculates your Body Mass Index (BMI) and tells you")
    print("which health category it falls into.\n")

    weight = get_positive_float("Enter your weight in kilograms (kg): ")
    height = get_positive_float(
        "Enter your height in meters (e.g. 1.70) OR centimeters (e.g. 170): "
    )
    height = normalize_height(height)

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print("\n--- Result ---")
    print(f"Your BMI is: {bmi:.2f}")
    print(f"Category: {category}")


if __name__ == "__main__":
    main()
