import pandas as pd
import re

print("Loading data...")
df = pd.read_csv("fifa21_raw_data.csv", low_memory=False)
print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")

def height_to_cm(value):
    value = str(value).strip().lower()
    if "'" in value:
        feet = int(re.search(r"(\d+)'", value).group(1))
        inches_match = re.search(r"(\d+)\"", value)
        inches = int(inches_match.group(1)) if inches_match else 0
        return round(feet * 30.48 + inches * 2.54)
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None

df["Height_cm"] = df["Height"].apply(height_to_cm)
print("\n=== HEIGHT CHECK ===")
print(df[["Height", "Height_cm"]].head(5))

def weight_to_kg(value):
    value = str(value).strip().lower()
    num = int(re.search(r"(\d+)", value).group(1))
    if "lbs" in value:
        return round(num * 0.453592)
    return num

df["Weight_kg"] = df["Weight"].apply(weight_to_kg)
print("\n=== WEIGHT CHECK ===")
print(df[["Weight", "Weight_kg"]].head(5))

def money_to_number(value):
    value = str(value).strip().replace("€", "")
    multiplier = 1
    if value.endswith("K"):
        multiplier = 1000
        value = value[:-1]
    elif value.endswith("M"):
        multiplier = 1000000
        value = value[:-1]
    try:
        return float(value) * multiplier
    except ValueError:
        return None

for col in ["Value", "Wage", "Release Clause"]:
    if col in df.columns:
        df[col + "_clean"] = df[col].apply(money_to_number)

print("\n=== MONEY CHECK ===")
print(df[["Value", "Value_clean", "Wage", "Wage_clean"]].head(5))

for col in ["SM", "W/F", "IR"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace("★", "", regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

print("\n=== STAR CHECK ===")
print(df[["SM", "W/F", "IR"]].head(5))

def parse_team_contract(value):
    value = str(value).strip()
    team = None
    contract = None
    status = "Unknown"
    
    if "\n" in value:
        parts = value.split("\n")
        team = parts[0].strip()
        contract = parts[1].strip() if len(parts) > 1 else None
    else:
        contract = value
    
    if contract and " ~ " in contract:
        start_end = contract.split(" ~ ")
        return (team, start_end[0].strip(), start_end[1].strip(), "Contract")
    if contract == "Free":
        return (team, None, None, "Free")
    if contract and "Loan" in contract:
        return (team, None, None, "Loan")
    return (team, None, None, "Unknown")

split = df["Team & Contract"].apply(lambda x: pd.Series(parse_team_contract(x)))
split.columns = ["Team", "Contract_Start", "Contract_End", "Contract_Status"]
df = pd.concat([df, split], axis=1)

print("\n=== CONTRACT CHECK ===")
print(df[["Team & Contract", "Team", "Contract_Start", "Contract_End", "Contract_Status"]].head(5))
df.to_csv("fifa21_cleaned.csv", index=False)
print("\nDONE - Saved as fifa21_cleaned.csv")