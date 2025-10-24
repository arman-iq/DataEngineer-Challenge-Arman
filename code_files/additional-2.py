# Additional #2 
import pandas as pd

# csv files/paths + columns
datasets = {
    "/Lilly/results.csv": ["date","home_team","away_team","home_score","away_score","tournament","city","country","neutral"],
    "/Lilly/goalscorers.csv": ["date","home_team","away_team","team","scorer","minute","own_goal","penalty"],
    "/Lilly/shootouts.csv": ["date","home_team","away_team","winner","first_shooter"]
}

# loop through each dataset
for file, cols in datasets.items():
    print(f"{file}...")

    # load csv, determine these values as missing
    df = pd.read_csv(file, na_values=["NA","NaN","N/A","NULL","NONE"," "])
    
    # check how many rows have issues before cleaning
    flag_cols = [c for c in cols if c in df.columns]
    before_mask = df[flag_cols].isna().any(axis=1)
    num_issues_before = int(before_mask.sum())
    print(f"Before cleaning: {num_issues_before} rows with issues.")

    # if clean then skip
    if num_issues_before == 0:
        print("No data quality issues found.")
        continue

    # fill missing text columns with 'Unknown'
    text_cols = [c for c in flag_cols if df[c].dtype == "object"]
    if text_cols:
        df[text_cols] = df[text_cols].fillna("Unknown")

    # fix numeric columns (replace missing or invalid with -1)
    for num_col in ["home_score", "away_score", "minute"]: # convert these columns to numbers
        if num_col in flag_cols:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce").fillna(-1) # if cannot be converted, mark as missing and fill with -1
    if "minute" in flag_cols:
        df.loc[(df["minute"] < -1) | (df["minute"] > 125), "minute"] = -1 # 125 minutes, matches rarely exceed 125 mins

    # re-flag and show only rows that had issues before (cleaned now)
    after_mask = df[flag_cols].isna().any(axis=1)
    print(f"After cleaning: {after_mask.sum()} rows with issues.")

    print(df.loc[before_mask, flag_cols].head(25)) # shows 25 rows
