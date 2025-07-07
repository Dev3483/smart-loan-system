import streamlit as st
import pandas as pd
import pickle

# scripts/alerts.py

from twilio.rest import Client
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
ALERT_PHONE = os.getenv("ALERT_PHONE")


def send_sms_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=ALERT_PHONE
    )
    print("📨 SMS Sent:", msg.sid)


# App title
st.title("💰 Smart Loan Recovery System")

# Sidebar input fields
st.sidebar.header("📋 Input Borrower Info")

# Collect inputs for the 9 selected features
delinq_2yrs = st.sidebar.number_input(
    "Delinquencies in past 2 years", min_value=0, step=1)
last_fico_range_high = st.sidebar.slider(
    "FICO Score (High)", 300, 850, step=10)
last_fico_range_low = st.sidebar.slider("FICO Score (Low)", 300, 850, step=10)
acc_now_delinq = st.sidebar.number_input(
    "Current Delinquencies", min_value=0, step=1)
open_acc_6m = st.sidebar.number_input(
    "Open Accounts in last 6 months", min_value=0, step=1)
total_bal_il = st.sidebar.number_input(
    "Total Installment Balance", min_value=0.0, step=100.0)
il_util = st.sidebar.slider(
    "Installment Loan Utilization (%)", 0.0, 200.0, step=1.0)
open_rv_12m = st.sidebar.number_input(
    "Open Revolving Accounts (12M)", min_value=0, step=1)
all_util = st.sidebar.slider("All Utilization (%)", 0.0, 200.0, step=1.0)

# Predict button
if st.sidebar.button("🔍 Predict Default Risk"):
    try:
        # Load the model
        model = pickle.load(open("models/loan_default_model1.pkl", "rb"))

        # Create a DataFrame with correct feature names and order
        user_df = pd.DataFrame([[
            delinq_2yrs,
            last_fico_range_high,
            last_fico_range_low,
            acc_now_delinq,
            open_acc_6m,
            total_bal_il,
            il_util,
            open_rv_12m,
            all_util
        ]], columns=[
            'delinq_2yrs',
            'last_fico_range_high',
            'last_fico_range_low',
            'acc_now_delinq',
            'open_acc_6m',
            'total_bal_il',
            'il_util',
            'open_rv_12m',
            'all_util'
        ])

        # Make prediction
        prediction = model.predict(user_df)
        if prediction[0] == 0:  # 0 means "Bad Loan" or "High Risk"
            risk = "🔴 High Risk of Default"
            st.error(f"Prediction: {risk}")

            send_sms_alert("⚠️ ALERT: This borrower has a HIGH risk of default.")
        else:
            risk = "🟢 Low Risk (Good Loan)"
            st.success(f"Prediction: {risk}")


    except Exception as e:
        st.error(f"❌ Error occurred during prediction: {e}")
