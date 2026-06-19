import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Config
st.set_page_config(
    page_title="Job Hunt Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("Job Hunt Dashboard")

# Create CSV if it doesn't exist
if not os.path.exists("applications.csv"):
    sample_df = pd.DataFrame({
        "Date": ["2026-06-19"],
        "Company": ["Deloitte"],
        "Role": ["Business Analyst"],
        "Status": ["Applied"],
        "Platform": ["LinkedIn"]
    })
    sample_df.to_csv("applications.csv", index=False)

# Load Data
df = pd.read_csv("applications.csv")

# Metrics
applications = len(df)
interviews = len(df[df["Status"] == "Interview"])
offers = len(df[df["Status"] == "Offer"])
rejections = len(df[df["Status"] == "Rejected"])

st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Applications", applications)

with col2:
    st.metric("Interviews", interviews)

with col3:
    st.metric("Offers", offers)

with col4:
    st.metric("Rejections", rejections)

st.divider()

# Applications Table
st.subheader("📋 Application Tracker")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# Status Chart
st.subheader("📈 Application Pipeline")

status_count = (
    df["Status"]
    .value_counts()
    .reset_index()
)

status_count.columns = ["Status", "Count"]

fig = px.pie(
    status_count,
    names="Status",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# Add New Application
st.subheader("➕ Add New Application")

with st.form("application_form"):

    date = st.text_input("Date")

    company = st.text_input("Company")

    role = st.text_input("Role")

    status = st.selectbox(
        "Status",
        [
            "Applied",
            "Recruiter Contacted",
            "Interview",
            "Offer",
            "Rejected"
        ]
    )

    platform = st.selectbox(
        "Platform",
        [
            "LinkedIn",
            "Naukri",
            "Wellfound",
            "Instahyre",
            "Referral"
        ]
    )

    submit = st.form_submit_button("Save Application")

    if submit:

        new_row = pd.DataFrame({
            "Date": [date],
            "Company": [company],
            "Role": [role],
            "Status": [status],
            "Platform": [platform]
        })

        updated_df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        updated_df.to_csv(
            "applications.csv",
            index=False
        )

        st.success("Application Added Successfully!")

        st.rerun()