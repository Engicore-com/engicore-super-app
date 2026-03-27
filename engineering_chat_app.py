import streamlit as st
import json
import os
import math
import numpy as np
import pandas as pd
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="EngiCore",
    page_icon="⚙️",
    layout="wide"
)

# Header
st.title("⚙️ EngiCore Professional Engineering Platform")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Engineering Tools",
        "Plant Simulator",
        "Save Project",
        "Export PFD PDF",
        "Team Collaboration",
        "AI Auto Design",
        "Cloud Deployment"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.header("🚀 EngiCore Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tools", "50+")
    col2.metric("Version", "Professional")
    col3.metric("Mode", "Offline + Online")

# Engineering Tools
elif menu == "Engineering Tools":

    st.header("📐 Engineering Calculations")

    calc = st.selectbox(
        "Select Calculation",
        [
            "Pipe Sizing",
            "Pump Power",
            "Heat Duty"
        ]
    )

    if calc == "Pipe Sizing":

        flow = st.number_input("Flow (m3/s)")
        velocity = st.number_input("Velocity (m/s)")

        if st.button("Calculate"):

            diameter = (4*flow/(3.14*velocity))**0.5

            st.success(f"Pipe Diameter = {diameter:.3f} m")

    elif calc == "Pump Power":

        flow = st.number_input("Flow rate")
        head = st.number_input("Head")

        if st.button("Calculate Pump"):

            power = flow*head/367

            st.success(f"Power = {power:.2f} kW")

# Plant Simulator
elif menu == "Plant Simulator":

    st.header("🏭 Plant Simulator")

    flow = st.number_input("Flow")
    temp = st.number_input("Temperature")
    pressure = st.number_input("Pressure")

    if st.button("Run Simulation"):

        new_temp = temp + 5
        new_pressure = pressure - 1

        st.success("Simulation Complete")

        st.write(f"Outlet Temp = {new_temp}")
        st.write(f"Outlet Pressure = {new_pressure}")

# Save Project
elif menu == "Save Project":

    st.header("💾 Save Project")

    project = st.text_input("Project Name")

    flow = st.number_input("Flow")
    pressure = st.number_input("Pressure")
    temp = st.number_input("Temperature")

    if st.button("Save"):

        os.makedirs("projects", exist_ok=True)

        data = {
            "flow": flow,
            "pressure": pressure,
            "temp": temp
        }

        with open(f"projects/{project}.json","w") as f:
            json.dump(data,f)

        st.success("Project Saved")

    if st.button("Load"):

        try:
            with open(f"projects/{project}.json") as f:
                data=json.load(f)

            st.write(data)

        except:
            st.error("Project not found")

# Export PDF
elif menu == "Export PFD PDF":

    st.header("📄 Export PFD")

    name = st.text_input("File Name")

    if st.button("Export"):

        c = canvas.Canvas(f"{name}.pdf")

        c.drawString(100,750,"EngiCore PFD")
        c.drawString(100,700,"Tank → Pump → Heat Exchanger")

        c.save()

        st.success("PDF Exported")

# Team Collaboration
elif menu == "Team Collaboration":

    st.header("👥 Team Chat")

    user = st.text_input("User")

    msg = st.text_input("Message")

    if st.button("Send"):

        st.write(f"{user}: {msg}")

# AI Auto Design
elif menu == "AI Auto Design":

    st.header("🤖 AI Plant Design")

    plant = st.selectbox(
        "Plant Type",
        [
            "Cooling Water",
            "Steam System",
            "Pump System"
        ]
    )

    if st.button("Generate"):

        if plant == "Cooling Water":

            st.success("Generated Design")
            st.write("Cooling Tower → Pump → Users")

        elif plant == "Steam System":

            st.success("Generated Design")
            st.write("Boiler → Steam Header → Users")

        elif plant == "Pump System":

            st.success("Generated Design")
            st.write("Tank → Pump → Pipeline")

# Cloud Deployment
elif menu == "Cloud Deployment":

    st.header("☁️ Cloud Deployment")

    st.write("Deploy using:")

    st.write("• Streamlit Cloud")
    st.write("• AWS")
    st.write("• Azure")

    st.info("Upload project to GitHub then deploy")
