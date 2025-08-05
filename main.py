# main.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from camera.camera_handler import start_camera, stop_camera, get_latest_frame
from detection.alert_logger import log_detection, get_recent_alerts, clear_alerts

# === Page Config ===
st.set_page_config(layout="wide")
st.title("🤖 DOBI: Autonomous Inspection System")

# === STATE ===
if 'nav_mode' not in st.session_state:
    st.session_state.nav_mode = "manual"  # Default mode

# === TOP BAR ===
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚗 Navigation Mode")
    nav_choice = st.radio("Choose Mode:", ["Manual", "Autonomous"], horizontal=True)

    if nav_choice.lower() != st.session_state.nav_mode:
        st.session_state.nav_mode = nav_choice.lower()
    # === MANUAL CONTROL SECTION ===
    if st.session_state.nav_mode == "manual":
        st.subheader("🎮 Manual Control")

        from control.manual_control import (
            connect_serial, is_connected, send_command
        )

        if st.button("🔌 Connect to Robot"):
            success, msg = connect_serial()
            if success:
                st.success(msg)
            else:
                st.error(msg)

        if is_connected():
            col_wasd = st.columns(3)
            if col_wasd[1].button("⬆️ Forward (W)"):
                send_command('w')
            if col_wasd[0].button("⬅️ Left (A)"):
                send_command('a')
            if col_wasd[2].button("➡️ Right (D)"):
                send_command('d')
            if col_wasd[1].button("⬇️ Backward (S)"):
                send_command('s')
            if col_wasd[1].button("⛔ Stop (X)"):
                send_command('x')

            manual_input = st.text_input("Send Manual Command (w/a/s/d/x):").strip().lower()
            if manual_input in ['w', 'a', 's', 'd', 'x']:
                send_command(manual_input)
        else:
            st.warning("Not connected to robot.")

with col2:
    st.subheader("🎮 Camera Control")
    cam_col1, cam_col2 = st.columns(2)

    with cam_col1:
        if st.button("▶️ Start Camera"):
            start_camera(log_detection)
    with cam_col2:
        if st.button("⏹ Stop Camera"):
            stop_camera()

# === LIVE CAMERA FEED ===
st.subheader("📷 Live Feed with Detection")

frame = get_latest_frame()
if frame is not None:
    st.image(frame, channels="BGR", caption="Live Annotated Feed")
else:
    st.info("Camera not active. Click 'Start Camera' to begin.")

# === ALERTS PANEL ===
with st.sidebar:
    st.header("🚨 Detection Alerts")

    if st.button("🧹 Clear Alerts"):
        clear_alerts()

    alerts = get_recent_alerts(10)
    if alerts:
        for alert in alerts:
            st.markdown(
                f"**[{alert['time']}]** `{alert['label'].upper()}` - *Severity:* {alert['severity']} | *Location:* {alert['location']}"
            )
    else:
        st.markdown("No alerts yet.")

# === AUTO REFRESH ===
if frame is not None:
    st_autorefresh(interval=1000, limit=None, key="feed-refresh")

# === FOOTER ===
st.markdown("---")
st.caption("DOBI BETA | Modular Autonomous Navigation + Real-Time Detection")
