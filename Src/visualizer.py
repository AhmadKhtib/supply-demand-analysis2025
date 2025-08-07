import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
import seaborn as sns

# Output directory
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

class FoodMarketVisualizer:
    def __init__(self, demand_df, supply_df):
        self.demand_df = demand_df.copy()
        self.supply_df = supply_df.copy()
        self.demand_df['day'] = pd.to_datetime(self.demand_df['day'])
        self.supply_df['day'] = pd.to_datetime(self.supply_df['day'])
        self.arabic_font = fm.findfont(fm.FontProperties(family='Arial'))
        self.font_prop = fm.FontProperties(fname=self.arabic_font)

    def reshape(self, text):
        return get_display(arabic_reshaper.reshape(text))

    def save_plot(self, filename):
        """Helper to save the current matplotlib figure to the output directory."""
        path = os.path.join(output_dir, filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
                # Explaination of the methods:

    # Plotting methods , 
    # No.01 plot daily demand vs supply

    def plot_daily(self, column, start_date=None, end_date=None):
        df1 = self.demand_df.copy()
        df2 = self.supply_df.copy()

        if start_date and end_date:
            start_date = pd.Timestamp(start_date)
            end_date = pd.Timestamp(end_date)
            df1 = df1[(df1['day'] >= start_date) & (df1['day'] <= end_date)]
            df2 = df2[(df2['day'] >= start_date) & (df2['day'] <= end_date)]

        if df1.empty:
            print("No demand data available for the selected period.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(df1['day'], df1[column], marker='o', linewidth=2, label=self.reshape(f"الطلب على ال{column}"))

        if not df2.empty:
            plt.plot(df2['day'], df2[column], marker='s', linewidth=2, linestyle='--',
                    label=self.reshape(f"العرض على ال{column}"))

        # Safely show the date range only if both are set
        if start_date and end_date:
            date_range_text = f" ({start_date.date()} → {end_date.date()})"
        else:
            date_range_text = ""

        plt.title(self.reshape(f"مقارنة الطلب والعرض على {column}{date_range_text}"),
                fontsize=20, fontproperties=self.font_prop)
        plt.xlabel(self.reshape("اليوم"), fontsize=14, fontproperties=self.font_prop)
        plt.ylabel(self.reshape("النسبة المئوية"), fontsize=14, fontproperties=self.font_prop)
        plt.legend(prop=self.font_prop)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        if start_date and end_date:
            filename = f"daily_{column}_{start_date.date()}_{end_date.date()}.png"
        else:
            filename = f"daily_{column}_full.png"

        self.save_plot(filename)


    def plot_difference(self, column, start_date=None, end_date=None):
        merged = pd.merge(
            self.demand_df[['day', column]],
            self.supply_df[['day', column]],
            on='day', suffixes=('_demand', '_supply')
        )

        # Convert date safely
        if start_date and end_date:
            start_date = pd.Timestamp(start_date)
            end_date = pd.Timestamp(end_date)
            merged = merged[(merged['day'] >= start_date) & (merged['day'] <= end_date)]

        if merged.empty:
            print("No data available for the selected period.")
            return

        merged['difference'] = merged[f'{column}_demand'] - merged[f'{column}_supply']

        plt.figure(figsize=(12, 6))
        plt.plot(merged['day'], merged['difference'], color='black', linewidth=2,
                label=self.reshape('الفرق بين الطلب والعرض'))
        plt.axhline(0, color='gray', linestyle='--')
        plt.fill_between(merged['day'], merged['difference'], 0, where=merged['difference'] > 0,
                        color='red', alpha=0.3, label=self.reshape('عجز'))
        plt.fill_between(merged['day'], merged['difference'], 0, where=merged['difference'] < 0,
                        color='green', alpha=0.3, label=self.reshape('فائض'))

        title_text = f"الفرق بين الطلب والعرض على {column}"
        if start_date and end_date:
            title_text += f" ({start_date.date()} → {end_date.date()})"

        plt.title(self.reshape(title_text), fontsize=20, fontproperties=self.font_prop)
        plt.xlabel(self.reshape("اليوم"), fontsize=14, fontproperties=self.font_prop)
        plt.ylabel(self.reshape("الفرق (٪)"), fontsize=14, fontproperties=self.font_prop)
        plt.legend(prop=self.font_prop)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        if start_date and end_date:
            filename = f"difference_{column}_{start_date.date()}_{end_date.date()}.png"
        else:
            filename = f"difference_{column}_full.png"

        self.save_plot(filename)


    # No.02 plot total food percentages

    def plot_total_food_percentages(self, csv_path, start_date, end_date, title="نسبة ظهور المواد الغذائية"):
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        df['day'] = pd.to_datetime(df['day'])

        df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
        if df.empty:
            print("No data for selected period.")
            return

        food_sums = df.drop(columns=['day']).sum().sort_values(ascending=False)
        food_sums = food_sums[food_sums > 0]
        total = food_sums.sum()
        labels, sizes = [], []
        others = 0

        for food, val in food_sums.items():
            if val / total >= 0.03:
                labels.append(self.reshape(food))
                sizes.append(val)
            else:
                others += val

        if others > 0:
            labels.append(self.reshape("أخرى"))
            sizes.append(others)

        plt.figure(figsize=(10, 10))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 13})
        plt.axis('equal')
        range_text = f"{start_date.date()} → {end_date.date()}"
        plt.title(self.reshape(f"{title} ({range_text})"), fontsize=18, fontproperties=self.font_prop)
        plt.tight_layout()

        # Save plot
        filename = f"piechart_{start_date.date()}_{end_date.date()}.png"
        self.save_plot(filename)

    # No.03 plot correlation matrix

    def plot_correlation_matrix(self, data_type='demand', top_n=10):
        # Choose dataframe
        df = self.demand_df.copy() if data_type == 'demand' else self.supply_df.copy()
        # Drop non-numeric or non-food columns
        df_numeric = df.drop(columns=['day'], errors='ignore').select_dtypes(include='number')
        if df_numeric.empty:
            print("No numeric data found for correlation.")
            return
        # Select top N items by total sum
        top_items = df_numeric.sum().sort_values(ascending=False).head(top_n).index.tolist()
        df_top = df_numeric[top_items]
        corr = df_top.corr()
        # Reshape Arabic labels
        reshaped_labels = [self.reshape(col) for col in corr.columns]
        # Plot heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f",
                    xticklabels=reshaped_labels, yticklabels=reshaped_labels,
                    cbar_kws={'label': self.reshape('Correlation Coefficient')})
        title_text = f"Correlation Matrix of Top {top_n} Items  ({'الطلب' if data_type == 'demand' else 'العرض'})"
        plt.title(self.reshape(title_text), fontsize=18, fontproperties=self.font_prop)
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        # Save
        filename = f"correlation_top{top_n}_{data_type}.png"
        self.save_plot(filename)

    # No.04 plot daily comparison bar for month

    def plot_daily_comparison_bar_for_month(self, column, year, month):
        # Filter the month from both demand and supply
        df_demand = self.demand_df.copy()
        df_supply = self.supply_df.copy()

        # Filter by selected year and month
        df_demand = df_demand[(df_demand['day'].dt.year == year) & (df_demand['day'].dt.month == month)]
        df_supply = df_supply[(df_supply['day'].dt.year == year) & (df_supply['day'].dt.month == month)]

        if df_demand.empty or df_supply.empty:
            print("No data available for the selected month.")
            return

        # Check if the column exists
        if column not in df_demand.columns or column not in df_supply.columns:
            print(f"Column '{column}' does not exist in the data.")
            return

        # Group by day
        demand_daily = df_demand.groupby(df_demand['day'].dt.day)[column].sum()
        supply_daily = df_supply.groupby(df_supply['day'].dt.day)[column].sum()

        days = sorted(set(demand_daily.index) | set(supply_daily.index))
        demand_values = [demand_daily.get(day, 0) for day in days]
        supply_values = [supply_daily.get(day, 0) for day in days]

        # Plot
        x = range(len(days))
        width = 0.4

        plt.figure(figsize=(14, 6))
        plt.bar([i - width/2 for i in x], demand_values, width=width, label=self.reshape(f"الطلب على {column}"))
        plt.bar([i + width/2 for i in x], supply_values, width=width, label=self.reshape(f"العرض على {column}"))

        day_labels = [self.reshape(str(day)) for day in days]
        plt.xticks(ticks=x, labels=day_labels, rotation=0, fontsize=12)
        month_name = datetime(year, month, 1).strftime("%B %Y")
        plt.title(self.reshape(f"مقارنة يومية بين العرض والطلب على {column} في شهر {month_name}"), fontsize=18, fontproperties=self.font_prop)
        plt.xlabel(self.reshape("اليوم"), fontsize=14, fontproperties=self.font_prop)
        plt.ylabel(self.reshape("الإجمالي"), fontsize=14, fontproperties=self.font_prop)
        plt.legend(prop=self.font_prop)
        plt.grid(axis='y')
        plt.tight_layout()

        # Save
        filename = f"daily_bar_{column}_{year}_{month:02d}.png"
        self.save_plot(filename)





# cleaned CSVs
demand_df = pd.read_csv("Data/DailyDemand.csv", encoding="utf-8-sig")
supply_df = pd.read_csv("Data/DailySellers.csv", encoding="utf-8-sig")

# the visualizer
viz = FoodMarketVisualizer(demand_df, supply_df)

# Plot daily demand vs supply for suger
viz.plot_daily("سكر", start_date=datetime(2025, 6, 1), end_date=datetime(2025, 6, 30))

# Plot difference chart for suger
viz.plot_difference("سكر", start_date=datetime(2025, 6, 1), end_date=datetime(2025, 6, 30))

# Pie chart of total demand percentages
viz.plot_total_food_percentages("Data/DailyDemand.csv", start_date=datetime(2025, 6, 1), end_date=datetime(2025, 7, 15),title='نسبة الطلب على المواد الغذائية')

viz.plot_correlation_matrix(data_type='supply')

viz.plot_daily_comparison_bar_for_month(
    column="طحين",
    year=2025,
    month=6
)

