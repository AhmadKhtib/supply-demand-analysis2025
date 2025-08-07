import pandas as pd
from Daily_Data_percntage import calculate_daily_food_percentages

# Load raw data
df = pd.read_csv(r"Data\RawData.csv", encoding="utf-8-sig")
# Filter for demand posts (containing "مطلوب")
wanted_mask = df['text'].str.contains("مطلوب", case=False, na=False)
wanted_df = df[wanted_mask].copy()

if not wanted_df.empty:
    # Extract day from datetime and clean columns
    wanted_df['day'] = pd.to_datetime(wanted_df['date']).dt.date
    wanted_df = wanted_df[['day', 'text']]
    # Save the filtered posts
    wanted_csv_path = r"Data\Demand.csv"
    wanted_df.to_csv(wanted_csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved {len(wanted_df)} demand posts to Demand.csv")
    # Generate daily percentages
    calculate_daily_food_percentages(wanted_csv_path, r"Data\DailyDemand.csv")
    print("Daily demand percentages saved to DailyDemand.csv")
else:
    print("No demand posts found in RawData.csv.")
