import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="E-Commerce Customer Dashboard", page_icon="🛍️", layout="wide")

# Title and Description
st.title("🛍️ E-Commerce Customer Behavior & Purchase Pattern Dashboard")
st.write("This interactive dashboard analyzes customer behavior, digital platform engagement, and spending patterns for our online store.")

# Cache data loading
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customers.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Customer Data")
min_membership = float(df['Length of Membership'].min())
max_membership = float(df['Length of Membership'].max())
membership_range = st.sidebar.slider("Select Length of Membership (Years)", min_membership, max_membership, (min_membership, max_membership))

min_spend = float(df['Yearly Amount Spent'].min())
max_spend = float(df['Yearly Amount Spent'].max())
spend_range = st.sidebar.slider("Select Yearly Amount Spent ($)", min_spend, max_spend, (min_spend, max_spend))

# Filtered DataFrame
filtered_df = df[
    (df['Length of Membership'] >= membership_range[0]) & 
    (df['Length of Membership'] <= membership_range[1]) &
    (df['Yearly Amount Spent'] >= spend_range[0]) & 
    (df['Yearly Amount Spent'] <= spend_range[1])
]

# 4 Key Numbers on Top (Metrics)
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(filtered_df):,}")
col2.metric("Average Yearly Spend", f"${filtered_df['Yearly Amount Spent'].mean():,.2f}")
col3.metric("Avg Membership Length", f"{filtered_df['Length of Membership'].mean():.1f} Years")
col4.metric("Highest Yearly Spend", f"${filtered_df['Yearly Amount Spent'].max():,.2f}")
st.markdown("---")

# Graphs Section (At least 5 graphs including univariate, bivariate, and heatmap)
st.subheader("📊 Data Visualizations & Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("### 1. Univariate: Yearly Amount Spent Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df['Yearly Amount Spent'], kde=True, ax=ax, color='teal')
    ax.set_title("Distribution of Yearly Spend")
    st.pyplot(fig)

with chart_col2:
    st.write("### 2. Univariate: Length of Membership Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df['Length of Membership'], kde=True, ax=ax, color='coral')
    ax.set_title("Distribution of Membership Length")
    st.pyplot(fig)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.write("### 3. Bivariate: Time on App vs Yearly Spend")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='Time on App', y='Yearly Amount Spent', alpha=0.7, ax=ax, color='purple')
    ax.set_title("Time on App vs Spending")
    st.pyplot(fig)

with chart_col4:
    st.write("### 4. Bivariate: Time on Website vs Yearly Spend")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='Time on Website', y='Yearly Amount Spent', alpha=0.7, ax=ax, color='green')
    ax.set_title("Time on Website vs Spending")
    st.pyplot(fig)

# Correlation Heatmap (5th graph requirement)
st.write("### 5. Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8, 5))
numeric_df = filtered_df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Correlation Matrix of Numeric Features")
st.pyplot(fig)

# Checkbox to show raw data table
if st.checkbox("Show Raw Filtered Data Table"):
    st.subheader("Raw Customer Data Preview")
    st.dataframe(filtered_df)

# Main Findings Section
st.markdown("---")
st.subheader("📝 Key Findings & Insights")
st.markdown("""
- **Primary Spending Driver:** **Length of Membership** exhibits the strongest positive correlation with yearly spending, indicating that long-term retention is critical for revenue growth.
- **App vs Website Performance:** Customer engagement on the mobile application shows a stronger positive pattern with high spending compared to the website.
- **Strategic Recommendation:** The company should invest more in enhancing mobile app features and launching loyalty programs targeting customers approaching their second year of membership.
""")