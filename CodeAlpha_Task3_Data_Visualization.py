"""
CodeAlpha Data Analytics Internship
Task 3: Data Visualization & Storytelling
Project: CodeAlpha_DataVisualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

def generate_sales_data():
    np.random.seed(101)
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    n = len(dates) * 4
    
    transaction_dates = np.random.choice(dates, size=n)
    regions = np.random.choice(["North", "South", "East", "West"], size=n, p=[0.3, 0.25, 0.2, 0.25])
    categories = np.random.choice(["Technology", "Furniture", "Office Supplies"], size=n, p=[0.35, 0.25, 0.40])
    segments = np.random.choice(["Consumer", "Corporate", "Home Office"], size=n, p=[0.50, 0.30, 0.20])
    
    sales = np.random.gamma(shape=2.5, scale=80, size=n).clip(15, 1200)
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.20, 0.30, 0.40], size=n, p=[0.35, 0.25, 0.20, 0.10, 0.06, 0.04])
    base_margin = np.random.normal(0.28, 0.05, size=n)
    effective_margin = base_margin - (discounts * 1.35)
    profits = sales * effective_margin

    df = pd.DataFrame({
        "OrderDate": transaction_dates,
        "Region": regions,
        "Category": categories,
        "Segment": segments,
        "Sales": np.round(sales, 2),
        "Discount": discounts,
        "Profit": np.round(profits, 2)
    })
    
    df["Month"] = df["OrderDate"].dt.to_period("M").dt.to_timestamp()
    df["ProfitMargin"] = df["Profit"] / df["Sales"]
    return df

def build_data_storytelling_dashboard(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    overall_margin = (total_profit / total_sales) * 100
    
    print("="*65)
    print(f"Total Revenue: ${total_sales:,.2f} | Net Profit: ${total_profit:,.2f} | Margin: {overall_margin:.2f}%")
    print("="*65)

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25)
    fig.suptitle("CodeAlpha Task 3 - Executive Sales Performance & Profitability Dashboard", 
                 fontsize=18, fontweight='bold', y=0.98)

    # 1. Monthly Revenue & Profit
    ax1 = fig.add_subplot(gs[0, :2])
    monthly_data = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
    ax1.plot(monthly_data["Month"], monthly_data["Sales"], marker='o', linewidth=2.5, color='#1f77b4', label='Revenue ($)')
    ax1.plot(monthly_data["Month"], monthly_data["Profit"], marker='s', linewidth=2, color='#2ca02c', label='Net Profit ($)')
    ax1.set_title("Monthly Revenue & Profit Growth Trends", fontsize=13, fontweight='bold')
    ax1.set_ylabel("USD ($)")
    ax1.legend(loc="upper left")
    
    # 2. Donut Chart
    ax2 = fig.add_subplot(gs[0, 2])
    segment_sales = df.groupby("Segment")["Sales"].sum()
    colors = ['#4e79a7', '#f28e2b', '#e15759']
    wedges, texts, autotexts = ax2.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%',
                                       startangle=140, colors=colors, pctdistance=0.75,
                                       wedgeprops=dict(width=0.4, edgecolor='w'))
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax2.set_title("Revenue by Customer Segment", fontsize=13, fontweight='bold')

    # 3. Horizontal Bar
    ax3 = fig.add_subplot(gs[1, 0])
    cat_summary = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    y_pos = np.arange(len(cat_summary))
    bar_width = 0.35
    ax3.barh(y_pos - bar_width/2, cat_summary["Sales"], height=bar_width, color='#3470a3', label='Sales')
    ax3.barh(y_pos + bar_width/2, cat_summary["Profit"], height=bar_width, color='#66c2a5', label='Profit')
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(cat_summary["Category"], fontweight='medium')
    ax3.set_title("Category Revenue vs. Profit", fontsize=13, fontweight='bold')
    ax3.legend(loc="lower right")

    # 4. Boxplot
    ax4 = fig.add_subplot(gs[1, 1])
    sns.boxplot(x="Region", y="ProfitMargin", data=df, ax=ax4, palette="Pastel1", showmeans=True)
    ax4.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax4.set_title("Profit Margin Spread by Region", fontsize=13, fontweight='bold')

    # 5. Scatter Plot
    ax5 = fig.add_subplot(gs[1, 2])
    sns.regplot(x="Discount", y="Profit", data=df.sample(500, random_state=42), ax=ax5, 
                scatter_kws={'alpha':0.4, 'color':'#d95f02'}, line_kws={'color':'#7570b3', 'linewidth':2})
    ax5.axhline(0, color='black', linestyle=':', linewidth=1)
    ax5.set_title("Discount Impact on Profitability", fontsize=13, fontweight='bold')

    dashboard_file = "sales_bi_dashboard.png"
    plt.savefig(dashboard_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    df.to_csv("visualized_sales_dataset.csv", index=False)
    print(f"[+] Saved dashboard visual to '{dashboard_file}' and exported dataset.")

if __name__ == "__main__":
    df = generate_sales_data()
    build_data_storytelling_dashboard(df)
