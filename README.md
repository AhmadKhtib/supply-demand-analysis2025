# Gaza Food Market Analysis 🇵🇸

This project analyzes supply and demand of food items in Gaza using public Telegram posts.
It fetches data using Telethon, classifies "demand" and "supply" messages, calculates daily percentages, and visualizes patterns.

## Folder Structure
- `src/`: Python scripts
- `data/`: Collected and processed CSV files
- `visualizations/`: Charts and images

## How to Run

```bash
pip install -r requirements.txt
python src/RawData.py
python src/BuyersPosts.py
python src/SellersPosts.py
python src/DailyLineChart.py
