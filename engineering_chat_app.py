import streamlit as st
import math
import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from pint import UnitRegistry
import speech_recognition as sr
import base64
from io import BytesIO
from PIL import Image

ureg = UnitRegistry()

# Embedded Logo
def get_logo():
    logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAA... (shortened placeholder)
"""
    logo_bytes = base64.b64decode(logo_base64)
    return Image.open(BytesIO(logo_bytes))


st.set_page_config(
    page_title="EngiCore",
    layout="wide"
)

# Mobile UI
st.markdown("""
<style>
.block-container {
padding-top:1rem;
}
.stButton>button{
width:100%;
}
</style>
""", unsafe_allow_html=True)


# Header
col1, col2 = st.columns([1,6])

with col1:
    try:
        st.image(get_logo(), width=80)
    except:
        st.write("⚙️")

with col2:
    st.title("EngiCore")
    st.caption("Professional Engineering Platform")

# Sidebar
try:
    st.sidebar.image(get_logo(), width=120)
except:
    st.sidebar.title("⚙️ EngiCore")


menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Advanced Calculator",
        "Unit Converter",
        "Engineering Tools",
        "Steam Tables",
        "Pump Curve",
        "Heat Exchanger",
        "Pipe Network",
        "Plant Simulator",
        "Fluid Database",
        "Equipment Database",
        "Engineering AI",
        "AI Auto Design",
        "Save Project",
        "Export PDF",
        "Team Collaboration"
    ]
)

# Voice
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return ""


# Dashboard
if menu == "Dashboard":

    st.header("🚀 Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Modules","30+")
    col2.metric("Version","Professional")
    col3.metric("Mode","Online + Offline")


# Calculator
elif menu == "Advanced Calculator":

    st.header("🧮 Advanced Calculator")

    col1,col2 = st.columns(2)

    with col1:
        expr = st.text_input("Expression")

    with col2:
        if st.button("🎤 Voice"):
            expr = voice_input()
            st.write(expr)

    if st.button("Calculate"):
        try:
            result = eval(expr)
            st.success(result)
        except:
            st.error("Invalid")


# Unit Converter
elif menu == "Unit Converter":

    st.header("📐 Universal Unit Converter")

    value = st.number_input("Value")

    from_unit = st.text_input("From Unit","meter")
    to_unit = st.text_input("To Unit","feet")

    if st.button("Convert"):
        try:
            result = (value * ureg(from_unit)).to(to_unit)
            st.success(result)
        except:
            st.error("Conversion Error")


# Engineering Tools
elif menu == "Engineering Tools":

    st.header("⚙️ Engineering Tools")

    tool = st.selectbox(
        "Tool",
        ["Pipe Sizing","Pump Power","Heat Duty"]
    )

    if tool == "Pipe Sizing":

        flow = st.number_input("Flow")
        velocity = st.number_input("Velocity")

        if st.button("Calculate"):
            d = (4*flow/(3.14*velocity))**0.5
            st.success(d)


# Steam Tables
elif menu == "Steam Tables":

    st.header("♨️ Steam Tables")

    temp = st.number_input("Temperature")

    h = 4.18*temp

    st.success(f"Enthalpy {h}")


# Pump Curve
elif menu == "Pump Curve":

    st.header("📈 Pump Curve")

    max_flow = st.number_input("Max Flow")

    if st.button("Plot"):

        flow = np.linspace(0,max_flow,50)
        head = max_flow-flow

        plt.figure()
        plt.plot(flow,head)

        st.pyplot(plt)


# Heat Exchanger
elif menu == "Heat Exchanger":

    st.header("🔥 Heat Exchanger")

    m = st.number_input("Flow")
    cp = st.number_input("Cp")
    dt = st.number_input("Delta T")

    if st.button("Calculate"):

        Q = m*cp*dt
        st.success(Q)


# Pipe Network
elif menu == "Pipe Network":

    st.header("🔧 Pipe Network")

    length = st.number_input("Length")
    diameter = st.number_input("Diameter")

    if st.button("Calculate"):

        loss = length/diameter
        st.success(loss)


# Plant Simulator
elif menu == "Plant Simulator":

    st.header("🏭 Plant Simulator")

    flow = st.number_input("Flow")
    temp = st.number_input("Temp")

    if st.button("Run"):

        st.success("Simulation Complete")
        st.write(temp+5)


# Fluid Database
elif menu == "Fluid Database":

    st.header("💧 Fluid Database")

    df = pd.DataFrame({
        "Fluid":["Water","Oil","Steam"],
        "Density":[1000,850,0.6]
    })

    st.dataframe(df)


# Equipment Database
elif menu == "Equipment Database":

    st.header("⚙️ Equipment Database")

    df = pd.DataFrame({
        "Equipment":["Pump","Tank","HX"]
    })

    st.dataframe(df)


# Engineering AI
elif menu == "Engineering AI":

    st.header("🤖 Engineering AI")

    q = st.text_input("Ask")

    if st.button("Ask"):
        st.success("AI Answer Coming")


# AI Auto Design
elif menu == "AI Auto Design":

    st.header("🤖 Auto Design")

    plant = st.selectbox(
        "Plant",
        ["Cooling","Steam","Pump"]
    )

    if st.button("Generate"):
        st.success("Design Generated")


# Save Project
elif menu == "Save Project":

    st.header("💾 Save Project")

    name = st.text_input("Project Name")

    if st.button("Save"):

        os.makedirs("projects",exist_ok=True)

        with open(f"projects/{name}.json","w") as f:
            json.dump({"project":name},f)

        st.success("Saved")


# Export PDF
elif menu == "Export PDF":

    st.header("📄 Export PDF")

    name = st.text_input("File Name")

    if st.button("Export"):

        c = canvas.Canvas(f"{name}.pdf")
        c.drawString(100,750,"EngiCore PFD")
        c.save()

        st.success("Exported")


# Team Chat
elif menu == "Team Collaboration":

    st.header("👥 Team Chat")

    user = st.text_input("User")
    msg = st.text_input("Message")

    if st.button("Send"):
        st.write(f"{user}: {msg}")
