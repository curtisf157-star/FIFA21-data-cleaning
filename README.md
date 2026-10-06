# FIFA 21 Data Cleaning Pipeline

A Python pipeline that transforms the raw, messy FIFA 21 player dataset into a clean, analysis-ready CSV.

## The Problem

The raw dataset contains 18,979 players across 77 columns, but the data is stored as text in ways that break analysis:

| Column | Problem | Example |
|---|---|---|
| Height | Mixed units | 5'11" and 180cm in the same column |
| Weight | Mixed units | 159lbs and 72kg in the same column |
| Value, Wage, Release Clause | Money stored as text with euro signs and K/M suffixes | 67.5M euro, 560K euro |
| SM, W/F, IR | Star ratings with a star symbol | 4 star |
| Team & Contract | Team name and contract dates mashed into one cell | Liverpool, 2020 ~ 2023 |

You cannot compute average salary, compare player heights, or filter by contract year without cleaning this first.

## What I Did

Wrote an end-to-end Python pipeline using pandas and regex that:

1. Standardized Height - converted feet/inches to centimeters
2. Standardized Weight - converted pounds to kilograms
3. Parsed money columns - stripped currency symbols and K/M suffixes, converted to floats
4. Cleaned star ratings - removed star symbols and converted to integers
5. Split the Team & Contract column into four clean columns: Team, Contract_Start, Contract_End, Contract_Status

## Before & After

Height:
- 5'7" becomes 170 cm
- 6'2" becomes 188 cm
- 5'11" becomes 180 cm

Weight:
- 159lbs becomes 72 kg
- 183lbs becomes 83 kg
- 192lbs becomes 87 kg

Money:
- 67.5M euro becomes 67500000.0
- 46M euro becomes 46000000.0
- 560K euro becomes 560000.0

Star ratings:
- 4 star becomes 4
- 5 star becomes 5
- 3 star becomes 3

Team & Contract:
- "Liverpool / 2020 ~ 2023" becomes Team: Liverpool, Start: 2020, End: 2023, Status: Contract

## The Result

A clean CSV (fifa21_cleaned.csv) with:
- All heights in centimeters
- All weights in kilograms
- All money columns as numeric floats
- All star ratings as integers
- Contract data split into 4 structured columns

Ready to plug into any dashboard, model, or SQL database.

## Tools Used

- Python 3.13
- pandas
- regex (re module)

## How to Run It

    git clone https://github.com/curtisf157-star/FIFA21-data-cleaning.git
    cd FIFA21-data-cleaning
    python -m venv venv
    venv\Scripts\activate
    pip install pandas
    python Clean.py

The cleaned file will appear as fifa21_cleaned.csv in the same folder.

## Files in This Repo

- Clean.py - the cleaning pipeline
- fifa21_cleaned.csv - the cleaned output dataset
- README.md - this file

## Author

Curtis - Data cleaning and analytics.

Dataset source: FIFA 21 Messy Raw Dataset on Kaggle (yagunnersya)