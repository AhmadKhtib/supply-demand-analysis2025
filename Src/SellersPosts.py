import pandas as pd
from Daily_Data_percntage import calculate_daily_food_percentages

# Load raw data
df = pd.read_csv(r"Data\RawData.csv", encoding="utf-8-sig")
# Filter posts that contain supply-related keywords
supply_keywords = "متوفر|للبيع|موجود|المعنيس"
wanted_mask = df['text'].str.contains(supply_keywords, case=False, na=False)
wanted_df = df[wanted_mask].copy()

if not wanted_df.empty:
    # Extract 'day' from datetime
    wanted_df['day'] = pd.to_datetime(wanted_df['date']).dt.date
    wanted_df = wanted_df[['day', 'text']]
    # Save filtered seller posts
    wanted_csv_path = r"Data\Sellers.csv"
    wanted_df.to_csv(wanted_csv_path, index=False, encoding="utf-8-sig")
    print(f" Saved {len(wanted_df)} seller posts to Sellers.csv")
    # Generate daily percentages
    calculate_daily_food_percentages(wanted_csv_path, r'Data\DailySellers.csv')
    print(" Daily supply percentages saved to DailySellers.csv")
else:
    print(" No seller posts found in RawData.csv.")
