# 📊 Real-time Anomaly Detection & Dashboard

**Python** version - 3.8

## Overview
This project is a **real-time anomaly detection and data visualization** tool using:
- **Streamlit** for UI
- **InfluxDB** for time-series data storage
- **Pygwalker** for interactive dashboard
- **QuantileAD & IsolationForest** for anomaly detection
- **Telegram Bot** for alerts

## Features
✅ Real-time data retrieval from **InfluxDB**  
✅ **Anomaly Detection** with **QuantileAD & IsolationForest**  
✅ **Live Charts** for real-time monitoring  
✅ **Telegram Alerts** for anomalies  
✅ **Interactive Dashboard** powered by **Pygwalker**  
✅ **Multipage Navigation** with Streamlit  

## Installation
### 1️⃣ Install Dependencies
Ensure you have **Python 3.8+** installed, then run:
```bash
pip install streamlit influxdb-client-3 pandas numpy matplotlib adtk scikit-learn pygwalker telegram
```

### 2️⃣ Set Up InfluxDB
- Create an **InfluxDB account** at [InfluxData](https://www.influxdata.com/)
- Replace your **InfluxDB token, host, and database name** in `app.py`:
  ```python
  client = InfluxDBClient3.InfluxDBClient3(
      token="YOUR_INFLUXDB_TOKEN",
      org="None",
      host="https://us-east-1-1.aws.cloud2.influxdata.com",
      database="test"
  )
  ```

### 3️⃣ Set Up Telegram Alerts (Optional)
- Create a Telegram bot via [@BotFather](https://t.me/BotFather)
- Get your **Bot Token** and **Chat ID**
- Replace them in `app.py`:
  ```python
  TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
  TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
  ```

## Running the Application
```bash
streamlit run app.py
```

## How to Use
1️⃣ **Select a Page from Sidebar**:
   - 📊 **Anomaly Detection** → Live data monitoring & alerts  
   - 📈 **Dashboard** → Interactive Pygwalker visualization  

2️⃣ **Choose Model for Anomaly Detection**:
   - **QuantileAD** (Statistical)
   - **IsolationForest** (ML-based)

3️⃣ **Enable Telegram Alerts** (Optional)
   - Get alerts when anomalies are detected

## Example Screenshots
🎯 **Anomaly Detection Page:**  
🚀 **Interactive Dashboard:**  
_(Add images here)_

## Next Steps
- ✅ Secure credentials using `.env` file
- ✅ Deploy to cloud (Streamlit Sharing / Docker)
- ✅ Add more ML models for anomaly detection

## License
📜 MIT License

---
💡 **Need help?** Feel free to open an issue or reach out! 🚀
