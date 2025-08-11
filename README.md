# 📊 Gaza Food Market Supply & Demand Analysis 

## Description :
 
This project provides an interactive dashboard for analyzing food market supply and demand trends in Gaza,
using data collected from Telegram channels where people post buying and selling offers.

The system uses:

   * ■ Telethon – to fetch raw posts from Telegram
   * ■ pandas – for data filtering and aggregation
   * ■ matplotlib – for chart generation
   * ■ Streamlit – for the interactive dashboard
    
## Data Range Used in This Project:

 * 1 March 2025 → 1 August 2025
 
## Project Structure
 
```
.
├── Data/
│   ├── RawData.csv             # All raw Telegram posts from selected time range (1/3/2025 → 1/8/2025)
│   ├── Demand.csv              # Posts identified as demand-related before filtering for food-only items
│   ├── Sellers.csv             # Posts identified as supply-related before filtering for food-only items
│   ├── DailyDemand.csv         # Demand.csv after filtering for food-related posts and calculating daily percentages
│   ├── DailySellers.csv        # Sellers.csv after filtering for food-related posts and calculating daily percentages
│
├── Src/
│   ├── RawData.py               # Uses Telethon to scrape Telegram posts and save to RawData.csv
│   ├── BuyersPosts.py           # Extracts demand posts, filters for food, saves to DailyDemand.csv
│   ├── SellersPosts.py          # Extracts supply posts, filters for food, saves to DailySellers.csv
│   ├── Daily_Data_percntage.py  # Converts raw counts to daily percentage values
│   ├── visualizer.py            # Generates all plots (line, bar, pie, correlation)
│   ├── food_market_UI.py # Streamlit dashboard for interactive analysis
│
├── visualizations/              # Auto-generated plots
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignore unnecessary files
└── README.md                    # Documentation

```
## Data Collection & Processing :
 
This project turns raw Telegram posts into clean, visual, month‑by‑month insights. Below is exactly how each file is produced and used.

#### 1) Collect raw posts → RawData.csv

   * ■ Script: Src/RawData.py
   * ■ How: Uses the Telegram API via Telethon to fetch posts from a target group/channel within the range 2025‑03‑01 → 2025‑08‑01.
   * ■ What’s saved: All posts (buyers & sellers, any category) with their timestamp and text to Data/RawData.csv.

#### 2) Split by intent (demand / supply)
   
   We split raw posts into demand and supply using Arabic keyword rules.

   * 2.a) Demand posts → Demand.csv
   
        * ■ Script: Src/BuyersPosts.py
        * ■ Rule: Posts containing words like "مطلوب" (wanted).
        * ■ Output: Data/Demand.csv — still includes non‑food posts at this stage.

   * 2.b) Supply posts → Sellers.csv
   
        * ■ Script: Src/SellersPosts.py
        * ■ Rule : Posts containing "للبيع", "موجود", "متوفر" (for sale/available).
        * ■ Output: Data/Sellers.csv — still includes non‑food posts at this stage.
        * ■ These two files (Demand.csv, Sellers.csv) are intermediate:
           * They record all demand/supply posts before restricting to food.

#### 3) Keep only food items & compute daily percentages :
   
   * ■ Now we filter the two intermediate files down to food posts and convert the daily counts into percentages per day.
   * ■ Script: Src/Daily_Data_percntage.py
   * ■ Input: A CSV (Demand.csv or Sellers.csv)

   * Process:

        * Filter to food‑related posts.

        * Aggregate by day and food item.
   
        * For each day, compute the share of each item as a percentage of that day’s total.

        * Outputs (overwrite):

            * Data/DailyDemand.csv → percentages per food item per day (demand)
            * Data/DailySellers.csv → percentages per food item per day (supply)

#### 4) Visualize in Streamlit :
   
   * App: Src/food_market_streamlit.py

   * Engine: Src/visualizer.py

   * What you can view:

      + Daily Demand vs Supply

      + Difference (shortage/surplus)

      + Food share pie chart

      + Correlation matrix (top 10 items)

      + Daily comparison bars by month


## File Cheat Sheet :

   * Data/RawData.csv — all posts in the time range (mixed topics, mixed intents)
       
   * Data/Demand.csv — posts that match demand keywords (may include non‑food)
            
   * Data/Sellers.csv — posts that match supply keywords (may include non‑food)
            
   * Data/DailyDemand.csv — demand food‑only, converted to daily percentages
            
   * Data/DailySellers.csv — supply food‑only, converted to daily percentages

## Installation :
```
# Clone the repository
git clone https://github.com/AhmadKhtib/supply-demand-analysis2025.git

# Navigate into the folder
cd supply-demand-analysis2025

# Install dependencies
pip install -r requirements.txt

```

## How to run the Dashboard :
    streamlit run Src/food_market_UI.py

##  Developer :
### Ahmed I. Alkhateeb – Data Science & AI Engineer

* Email : akh6@smail.ucas.edu.ps
* Linkedin : https://www.linkedin.com/in/ahmedai
