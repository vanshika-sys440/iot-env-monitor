import sqlite3
import time

import pandas as pd
import streamlit as st

st.set_page_config(page_title="IoT Environment Monitor", page_icon="🌡️")
st.title("IoT Environment Monitor")

db = sqlite3.connect("readings.db")
df = pd.read_sql_query(
    "SELECT * FROM readings ORDER BY id DESC LIMIT 100", db
)
db.close()

if df.empty:
    st.warning("No readings yet. Start the sensor and the subscriber.")
else:
    df = df.sort_values("id")
    df["time"] = pd.to_datetime(df["ts"], unit="s")
    latest = df.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric("Temperature (°C)", latest["temperature"])
    col2.metric("Humidity (%)", latest["humidity"])

    st.line_chart(df.set_index("time")[["temperature", "humidity"]])
    st.caption(f"Showing the last {len(df)} readings from {latest['device']}")

time.sleep(3)
st.rerun()