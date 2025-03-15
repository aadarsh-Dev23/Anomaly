import streamlit as st
import influxdb_client_3 as InfluxDBClient3
import pandas as pd
import numpy as np
from influxdb_client_3 import flight_client_options
import certifi
from adtk.detector import QuantileAD
from adtk.data import validate_series
import matplotlib.pyplot as plt
import time
import telegram
from sklearn.ensemble import IsolationForest
import pygwalker as pyg

# Streamlit UI
st.set_page_config(page_title="Real-time Anomaly Detection & Dashboard", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["📊 Anomaly Detection", "📈 Dashboard"])

# Telegram configuration (Replace with secure handling)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_alert(message):
    """Send an alert via Telegram."""
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        st.error(f"Failed to send Telegram alert: {e}")

# Read certificate
with open(certifi.where(), "r") as fh:
    cert = fh.read()

# Connect to InfluxDB
client = InfluxDBClient3.InfluxDBClient3(
    token="QUWVifwLdA6x0BI2A1iQJbpZVeOTQkLTk8yi5Kr9ronQX3NWWWuH67A99Ic99lA66uM0Vr_VyEpWHgrQ_gdtNA==",
    org="None",
    host="https://us-east-1-1.aws.cloud2.influxdata.com",
    database="test",
    flight_client_options=flight_client_options(tls_root_certs=cert)
)

def fetch_data():
    """Fetch data from InfluxDB."""
    query = """
        SELECT * FROM "win_net"
        WHERE "instance" != 'Realtek PCIe GbE Family Controller'
    """
    table = client.query(query=query, language="sql")
    df = table.to_pandas()

    if df.empty:
        return None

    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time").sort_index()
    df = df.loc[~df.index.duplicated(keep='first')]
    return df

# Main Page: Anomaly Detection
if page == "📊 Anomaly Detection":
    st.title("📊 Real-time Anomaly Detection with InfluxDB")

    model_choice = st.sidebar.selectbox("Select Anomaly Detection Model", ["QuantileAD", "IsolationForest"])
    enable_alerts = st.sidebar.checkbox("Enable Telegram Alerts", value=False)

    # Placeholders
    chart_placeholder = st.empty()
    data_placeholder = st.empty()

    # Initialize last alert time
    if 'last_alert_time' not in st.session_state:
        st.session_state.last_alert_time = 0

    # Refresh interval (seconds)
    REFRESH_INTERVAL = 5

    while True:
        df = fetch_data()

        if df is None:
            st.warning("⚠️ No data retrieved from InfluxDB.")
            time.sleep(REFRESH_INTERVAL)
            continue

        if "Bytes_Received_persec" in df.columns:
            data_temp = df["Bytes_Received_persec"]
            data_temp = validate_series(data_temp)

            # Anomaly detection
            if model_choice == "QuantileAD":
                detector = QuantileAD(low=0.01, high=0.99)
                anomalies = detector.fit_detect(data_temp)
            else:  # IsolationForest
                X = data_temp.values.reshape(-1, 1)
                iso = IsolationForest(contamination=0.01, random_state=42)
                y_pred = iso.fit_predict(X)
                anomalies = pd.Series(y_pred, index=data_temp.index) == -1

            # Alert if anomalies are detected
            if enable_alerts:
                current_time = time.time()
                ALERT_INTERVAL = 60  # seconds
                if anomalies.any() and (current_time - st.session_state.last_alert_time > ALERT_INTERVAL):
                    send_telegram_alert("🚨 Anomaly detected in Bytes_Received_persec!")
                    st.session_state.last_alert_time = current_time

            # Plot Anomaly Detection
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data_temp.index, data_temp, label="Bytes_Received_persec", color="blue")
            ax.scatter(anomalies[anomalies].index, data_temp[anomalies], color="red", label="Anomalies", marker="x")
            ax.set_title("Real-time Anomaly Detection")
            ax.set_xlabel("Time")
            ax.set_ylabel("Bytes_Received_persec")
            ax.legend()
            chart_placeholder.pyplot(fig)
            plt.close(fig)

        # Update data table
        data_placeholder.dataframe(df)

        # Wait before the next refresh
        time.sleep(REFRESH_INTERVAL)

# Dashboard Page: Pygwalker
elif page == "📈 Dashboard":
    st.title("📈 Interactive Data Dashboard")

    # Fetch Data
    df = fetch_data()

    if df is None or df.empty:
        st.warning("⚠️ No data available for visualization.")
    else:
        # Display Pygwalker Dashboard
        pyg_html = pyg.walk(df, return_html=True)
        st.components.v1.html(pyg_html, height=800, scrolling=True)
