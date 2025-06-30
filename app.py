import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="OTT Churn Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_OTT_Dataset.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter the Data")
gender = st.sidebar.multiselect("Gender", options=[0, 1], default=[0, 1])
family = st.sidebar.multiselect("Family Subscription", options=[0, 1], default=[0, 1])
billing = st.sidebar.multiselect("Billing Cycle (1=Monthly, 2=Yearly)", options=[1, 2], default=[1, 2])

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["FamilySubscription"].isin(family)) &
    (df["BillingCycle"].isin(billing))
]

# KPIs
st.title("📺 OTT Subscription Churn Dashboard")
st.markdown("Use this dashboard to understand churn patterns in OTT customers. The visualizations provide macro and micro trends for stakeholders to act on.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Churned", df["CancelledSubscription"].sum())
col3.metric("Churn Rate", f"{df['CancelledSubscription'].mean()*100:.2f}%")

# Tabs
tabs = st.tabs(["Overview", "Demographics", "Usage & Support", "Pricing & Plans", "Ratings & Feedback", "Correlation"])

# Tab 1: Overview
with tabs[0]:
    st.subheader("Churn by Billing Cycle")
    st.markdown("Shows how churn differs by billing cycle preferences.")
    fig1 = px.histogram(filtered_df, x="BillingCycle", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Monthly Plan Price Distribution")
    st.markdown("Higher pricing tiers may influence cancellation.")
    fig2 = px.box(filtered_df, x="CancelledSubscription", y="MonthlyPlanPrice", color="CancelledSubscription")
    st.plotly_chart(fig2, use_container_width=True)

# Tab 2: Demographics
with tabs[1]:
    st.subheader("Gender vs Churn")
    st.markdown("Check if churn is higher for a specific gender.")
    fig = px.histogram(filtered_df, x="Gender", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Group vs Churn")
    fig = px.histogram(filtered_df, x="AgeGroup", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Usage & Support
with tabs[2]:
    st.subheader("Average Watch Time vs Churn")
    fig = px.box(filtered_df, x="CancelledSubscription", y="AvgWatchTimePerWeek", color="CancelledSubscription")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Support Rating Distribution")
    fig = px.histogram(filtered_df, x="CustomerSupportRating", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Streaming Quality Preference vs Churn")
    fig = px.histogram(filtered_df, x="StreamingQuality", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Pricing & Plans
with tabs[3]:
    st.subheader("Monthly Plan Price vs Churn")
    fig = px.scatter(filtered_df, x="MonthlyPlanPrice", y="MonthsSubscribed", color="CancelledSubscription")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Subscription Duration vs Churn")
    fig = px.histogram(filtered_df, x="MonthsSubscribed", color="CancelledSubscription", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Family Plan Impact")
    fig = px.histogram(filtered_df, x="FamilySubscription", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 5: Ratings & Feedback
with tabs[4]:
    st.subheader("App Rating vs Churn")
    fig = px.box(filtered_df, x="CancelledSubscription", y="AppRating", color="CancelledSubscription")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Preferred Genre vs Churn")
    fig = px.histogram(filtered_df, x="PreferredGenre", color="CancelledSubscription", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 6: Correlation
with tabs[5]:
    st.subheader("Correlation Heatmap")
    st.markdown("Explore relationships between numerical features.")
    numeric_df = filtered_df.select_dtypes(include='number')
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.subheader("Churn Breakdown")
    st.dataframe(filtered_df["CancelledSubscription"].value_counts())

