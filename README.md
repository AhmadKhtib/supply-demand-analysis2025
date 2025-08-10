# 📊 Gaza Food Market Supply & Demand Analysis 

# Description :
 
This project provides an interactive dashboard for analyzing food market supply and demand trends in Gaza,
using data collected from Telegram channels where people post buying and selling offers.

The system uses:

    ■ Telethon – to fetch raw posts from Telegram
    
    ■ pandas – for data filtering and aggregation
    
    ■ matplotlib – for chart generation
    
    ■ Streamlit – for the interactive dashboard
    
# Data Range Used in This Project:

  1 March 2025 → 1 August 2025
 
# Project Structure
 
<img width="992" height="505" alt="image" src="https://github.com/user-attachments/assets/f272fc39-464c-4901-a823-6b45ad32ce30" />

# Data Collection & Processing :
 
This project turns raw Telegram posts into clean, visual, month‑by‑month insights. Below is exactly how each file is produced and used.

1) Collect raw posts → RawData.csv

        ■ Script: Src/RawData.py
        ■ How: Uses the Telegram API via Telethon to fetch posts from a target group/channel within the range 2025‑03‑01 → 2025‑08‑01.
        ■ What’s saved: All posts (buyers & sellers, any category) with their timestamp and text to Data/RawData.csv.

2) Split by intent (demand / supply)
   
    We split raw posts into demand and supply using Arabic keyword rules.

    2.a) Demand posts → Demand.csv
   
        ■ Script: Src/BuyersPosts.py
        ■ Rule: Posts containing words like "مطلوب" (wanted).
        ■ Output: Data/Demand.csv — still includes non‑food posts at this stage.

    2.b) Supply posts → Sellers.csv
   
        ■ Script: Src/SellersPosts.py
        ■ Rule : Posts containing "للبيع", "موجود", "متوفر" (for sale/available).
        ■ Output: Data/Sellers.csv — still includes non‑food posts at this stage.
        ■ These two files (Demand.csv, Sellers.csv) are intermediate:
            They record all demand/supply posts before restricting to food.

3) Keep only food items & compute daily percentages :
   
        ■ Now we filter the two intermediate files down to food posts and convert the daily counts into percentages per day.
        ■ Script: Src/Daily_Data_percntage.py
        ■ Input: A CSV (Demand.csv or Sellers.csv)

    Process:

        Filter to food‑related posts.

        Aggregate by day and food item.
   
        For each day, compute the share of each item as a percentage of that day’s total.

        Outputs (overwrite):

            Data/DailyDemand.csv → percentages per food item per day (demand)
            Data/DailySellers.csv → percentages per food item per day (supply)

4) Visualize in Streamlit :
   
        App: Src/food_market_streamlit.py

        Engine: Src/visualizer.py

        What you can view:

            Daily Demand vs Supply

            Difference (shortage/surplus)

            Food share pie chart

            Correlation matrix (top 10 items)

            Daily comparison bars by month


# File Cheat Sheet

            Data/RawData.csv — all posts in the time range (mixed topics, mixed intents)
            
            Data/Demand.csv — posts that match demand keywords (may include non‑food)
            
            Data/Sellers.csv — posts that match supply keywords (may include non‑food)
            
            Data/DailyDemand.csv — demand food‑only, converted to daily percentages
            
            Data/DailySellers.csv — supply food‑only, converted to daily percentages
