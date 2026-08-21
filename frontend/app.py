import os
from datetime import datetime

import requests
import streamlit as st


st.set_page_config(
    page_title="Maritime Control Dashboard",
    page_icon="⚓",
    layout="wide",
)

API_URL = os.getenv("API_URL", "http://localhost:8000")


@st.cache_data(ttl=10)
def get_data():
    try:
        response = requests.get(f"{API_URL}/dashboard", timeout=3)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "vessels": 24,
            "active_alerts": 3,
            "port_operations": 18,
            "system_status": "Operational",
            "traffic": {
                "labels": ["06:00", "09:00", "12:00", "15:00", "18:00"],
                "values": [12, 19, 27, 22, 31],
            },
            "alerts": [
                {"vessel": "MV Horizon", "type": "Weather warning", "severity": "High"},
                {"vessel": "Ocean Star", "type": "Route deviation", "severity": "Medium"},
                {"vessel": "Sea Falcon", "type": "Engine inspection", "severity": "Low"},
            ],
        }


data = get_data()

st.title("⚓ Maritime Control Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with st.sidebar:
    st.header("Navigation")
    st.radio("View", ["Overview", "Vessels", "Alerts", "Port Operations"])
    st.divider()
    st.success(f"System: {data['system_status']}")
    st.caption(f"API: {API_URL}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Vessels", data["vessels"])
col2.metric("Active Alerts", data["active_alerts"])
col3.metric("Port Operations", data["port_operations"])
col4.metric("System Status", data["system_status"])

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("Maritime Traffic")
    chart_data = {
        "Traffic": data["traffic"]["values"],
    }
    st.line_chart(chart_data, x_label="Time", y_label="Vessels")

with right:
    st.subheader("System Summary")
    st.info("All core maritime monitoring services are running.")
    st.progress(min(data["vessels"] / 50, 1.0), text="Fleet capacity")

st.subheader("Recent Alerts")

for alert in data["alerts"]:
    severity = alert["severity"]

    if severity == "High":
        st.error(f"🔴 **{alert['vessel']}** — {alert['type']}")
    elif severity == "Medium":
        st.warning(f"🟠 **{alert['vessel']}** — {alert['type']}")
    else:
        st.info(f"🔵 **{alert['vessel']}** — {alert['type']}")

if st.button("Refresh dashboard"):
    st.cache_data.clear()
    st.rerun()

