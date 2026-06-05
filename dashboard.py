import streamlit as st
import sqlite3
import pandas as pd

# Set page configuration
st.set_page_config(page_title="AI Security Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ AI-Powered Log Monitoring & Threat Response")
st.markdown("Real-time monitoring of system logins and potential security threats.")

# Fetch data from Database
def load_data():
    conn = sqlite3.connect('security_logs.db')
    query = """
    SELECT 
        id, 
        datetime(timestamp, 'localtime') as timestamp, 
        ip_address, 
        username, 
        threat_type, 
        severity 
    FROM alerts 
    ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = load_data()

# Display Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Threats Detected", value=len(data))
with col2:
    high_risk = len(data[data['severity'] >= 7])
    st.metric(label="High Risk (Severity >= 7)", value=high_risk)
with col3:
    st.metric(label="Last Detection Time", value=data['timestamp'].max() if not data.empty else "N/A")

st.divider()

# Display Charts and Tables
col_chart, col_table = st.columns([1, 2])

with col_chart:
    st.subheader("Threat Types")
    if not data.empty:
        threat_counts = data['threat_type'].value_counts()
        st.bar_chart(threat_counts)
    else:
        st.write("No data available.")

with col_table:
    st.subheader("🚨 Latest Alert Records")
    if not data.empty:
        # Color coding for severity
        def color_severity(val):
            color = 'red' if val >= 7 else 'orange' if val >= 4 else 'green'
            return f'color: {color}; font-weight: bold;'
        
        st.dataframe(data.style.map(color_severity, subset=['severity']), use_container_width=True)
    else:
        st.write("No security records found.")