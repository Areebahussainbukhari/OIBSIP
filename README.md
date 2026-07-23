# BMI Calculator

**Oasis Infobyte AICTE SIP — Python Programming Track — Task 2**

## What This Project Does

This is a command-line program that calculates a user's Body Mass Index (BMI)
from their weight and height, then classifies the result into one of four
standard health categories: Underweight, Normal, Overweight, or Obese.

## Features

- Takes weight (kg) and height as input
- Accepts height in **either meters or centimeters** — automatically detects
  and converts centimeter input (e.g. entering `160` is treated as 160 cm and
  converted to 1.60 m)
- Validates input: rejects non-numeric entries and negative/zero values,
  and asks again instead of crashing
- Calculates BMI using the standard formula: weight (kg) / height (m)²
- Displays the BMI rounded to 2 decimal places, along with its category

## How to Run

1. Make sure Python is installed on your computer.
2. Open a terminal in this folder.
3. Run:
   ```
   python bmi_calculator.py
   ```
4. Enter your weight in kilograms when prompted.
5. Enter your height in meters (e.g. `1.70`) or centimeters (e.g. `170`).
6. The program will display your BMI and category.

## Example

```
Enter your weight in kilograms (kg): 70
Enter your height in meters (e.g. 1.70) OR centimeters (e.g. 170): 175

--- Result ---
Your BMI is: 22.86
Category: Normal
```

## BMI Category Reference

| BMI Range     | Category     |
|---------------|--------------|
| Below 18.5    | Underweight  |
| 18.5 – 24.9   | Normal       |
| 25.0 – 29.9   | Overweight   |
| 30.0 and above| Obese        |

## Technologies Used

- Python 3 (no external libraries required — built entirely with Python's
  core features: `input()`, `try/except`, functions, and conditionals)

## What I Learned

Building this project helped me practice input validation (handling both
invalid text and out-of-range numbers gracefully), writing reusable
functions, and thinking through a real-world edge case — many people
naturally type their height in centimeters, so I added automatic detection
and conversion instead of just expecting the "correct" format.
