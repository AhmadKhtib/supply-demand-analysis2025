import streamlit as st
import pandas as pd
from datetime import datetime
from visualizer import FoodMarketVisualizer

st.set_page_config(page_title="Food Market Visualizer", layout="wide")
st.title("\U0001F4CA Food Market Visualizer")

# Load data
@st.cache_data
def load_data():
    try:
        demand_df = pd.read_csv("Data/DailyDemand.csv", encoding="utf-8-sig")
        supply_df = pd.read_csv("Data/DailySellers.csv", encoding="utf-8-sig")
        return demand_df, supply_df
    except FileNotFoundError:
        st.error("❌ Data files not found. Please check the 'Data/' folder.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        st.stop()

demand_df, supply_df = load_data()
viz = FoodMarketVisualizer(demand_df, supply_df)

# UI controls
chart_type = st.selectbox("Select Chart Type", [
    "Daily Demand vs Supply",
    "Difference Between Demand and Supply",
    "Total Food Percentages (Pie Chart)",
    "Correlation Matrix",
    "Daily Comparison for Month"
])

year = 2025
start_month = st.number_input("Start Month", min_value=3, max_value=7, value=6, step=1)

if chart_type != "Daily Comparison for Month":
    end_month = st.number_input("End Month", min_value=start_month, max_value=8, value=start_month, step=1)
    start_date = datetime(year, start_month, 1)
    end_date = pd.Timestamp(datetime(year, end_month, 1)) + pd.offsets.MonthEnd(1)
    st.markdown(f"**Date Range:** {start_date.date()} → {end_date.date()}")
else:
    start_date = datetime(year, start_month, 1)
    end_date = start_date

if chart_type != "Correlation Matrix" and chart_type != "Total Food Percentages (Pie Chart)":
    column = st.selectbox("Select Food Item", demand_df.columns[1:])

# Chart actions
if chart_type == "Daily Demand vs Supply":
    if st.button("Generate Chart"):
        try:
            viz.plot_daily(column, start_date=start_date, end_date=end_date)
            st.image(f"visualizations/daily_{column}_{start_date.date()}_{end_date.date()}.png")
        except KeyError:
            st.error("❌ Selected column does not exist in the data.")
        except ValueError as ve:
            st.error(f"❌ Date error: {ve}")
        except FileNotFoundError:
            st.error("❌ Data file missing during chart generation.")
        except TypeError:
            st.error("❌ Invalid type used for plotting. Check date or column selection.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

elif chart_type == "Difference Between Demand and Supply":
    if st.button("Generate Chart"):
        try:
            viz.plot_difference(column, start_date=start_date, end_date=end_date)
            st.image(f"visualizations/difference_{column}_{start_date.date()}_{end_date.date()}.png")
        except KeyError:
            st.error("❌ Selected column does not exist.")
        except ValueError:
            st.error("❌ Invalid value encountered.")
        except FileNotFoundError:
            st.error("❌ Data file missing.")
        except TypeError:
            st.error("❌ Invalid input types.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

elif chart_type == "Total Food Percentages (Pie Chart)":
    if st.button("Generate Chart"):
        try:
            viz.plot_total_food_percentages("Data/DailyDemand.csv", start_date=start_date, end_date=end_date)
            st.image(f"visualizations/piechart_{start_date.date()}_{end_date.date()}.png")
        except FileNotFoundError:
            st.error("❌ CSV file not found.")
        except ValueError:
            st.error("❌ No food data found in selected range.")
        except TypeError:
            st.error("❌ Date range error or input mismatch.")
        except KeyError:
            st.error("❌ One or more required columns are missing.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

elif chart_type == "Correlation Matrix":
    data_type = st.radio("Select Data Source", ["demand", "supply"], horizontal=True)
    if st.button("Generate Chart"):
        try:
            viz.plot_correlation_matrix(data_type=data_type)
            st.image(f"visualizations/correlation_top10_{data_type}.png")
        except ValueError:
            st.error("❌ Correlation calculation failed. Not enough numeric data.")
        except KeyError:
            st.error("❌ Missing expected columns for correlation.")
        except TypeError:
            st.error("❌ Non-numeric data type encountered.")
        except FileNotFoundError:
            st.error("❌ Required data not found.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

elif chart_type == "Daily Comparison for Month":
    if st.button("Generate Chart"):
        try:
            viz.plot_daily_comparison_bar_for_month(column, year=year, month=start_month)
            st.image(f"visualizations/daily_bar_{column}_{year}_{start_month:02d}.png")
        except KeyError:
            st.error("❌ Column not found in data.")
        except ValueError:
            st.error("❌ Invalid or empty data for the selected month.")
        except FileNotFoundError:
            st.error("❌ Required dataset missing.")
        except TypeError:
            st.error("❌ Invalid date or input format.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
