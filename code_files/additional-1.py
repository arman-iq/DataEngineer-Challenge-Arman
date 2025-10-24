# Additional #1
import pandas as pd

# csv file paths + key columns
datasets = {
    "/Lilly/results.csv": ["date", "home_team", "away_team", "home_score", "away_score", "tournament", "city", "country", "neutral"],
    "/Lilly/goalscorers.csv": ["date", "home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"],
    "/Lilly/shootouts.csv": ["date", "home_team", "away_team", "winner", "first_shooter"]
}

# check each dataset
for file, cols in datasets.items():
    print(f"{file}...")
    
    # load csv and treat "NA", "NULL", "NONE", etc as missing
    df = pd.read_csv(file, na_values=["NA", "NaN", "N/A", "NULL","NONE", " "])
    
    # add new column to flag missing values
    df["data_quality_issue"] = df[cols].isna().any(axis=1)
    
    # filter only rows with issues
    bad_rows = df[df["data_quality_issue"] == True]
    
    # show results
    if len(bad_rows) > 0:
        print(f"{len(bad_rows)} rows have data quality issues.")
        print(bad_rows.head(15))  # show 15 rows
    else:
        print("0 rows have data quality issues.")
