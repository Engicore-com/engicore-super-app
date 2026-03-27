import streamlit as st
import sympy as sp
import pint
import re
from PyPDF2 import PdfReader
from streamlit_mic_recorder import mic_recorder

# Setup
ureg = pint.UnitRegistry()

st.set_page_config(
    page_title="EngiCore Platform",
    layout="wide"
)

# Branding
st.markdown("""
# 🧠 EngiCore
### Engineering Super Platform
---
""")

# Navigation Bar
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🧠 Smart Assistant",
        "🧮 Calculator",
        "🔄 Converter",
        "📄 Document Tools",
        "⚙️ Engineering Tools"
    ]
)

# -----------------------------
# HOME PAGE
# -----------------------------

if menu == "🏠 Home":

    st.header("Welcome to EngiCore")

    st.write("All-in-One Engineering Platform")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("🧠 Smart Assistant")
        st.write("Ask engineering questions")

    with col2:
        st.success("🧮 Calculator")
        st.write("Scientific & engineering calculator")

    with col3:
        st.success("🔄 Converter")
        st.write("Universal unit converter")

    st.markdown("---")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.success("📄 Document Tools")

    with col5:
        st.success("⚙️ Engineering Tools")

    with col6:
        st.success("🤖 AI Assistant")


# -----------------------------
# SMART ASSISTANT
# -----------------------------

elif menu == "🧠 Smart Assistant":

    st.header("Smart Assistant")

    query = st.text_input("Ask anything")

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="Stop Recording"
    )

    if audio:
        st.info("Voice captured")

    if st.button("Solve"):

        try:
            result = sp.sympify(query)
            st.success(result)
        except:
            st.info("Try math or engineering question")


# -----------------------------
# CALCULATOR
# -----------------------------

elif menu == "🧮 Calculator":

    st.header("Calculator")

    num1 = st.number_input("Number 1")
    num2 = st.number_input("Number 2")

    operation = st.selectbox(
        "Operation",
        ["Add", "Subtract", "Multiply", "Divide"]
    )

    if st.button("Calculate"):

        if operation == "Add":
            st.success(num1 + num2)

        elif operation == "Subtract":
            st.success(num1 - num2)

        elif operation == "Multiply":
            st.success(num1 * num2)

        elif operation == "Divide":
            st.success(num1 / num2)


# -----------------------------
# CONVERTER
# -----------------------------

elif menu == "🔄 Converter":

    st.header("Unit Converter")

    value = st.number_input("Value", 1.0)

    from_unit = st.text_input("From", "meter")
    to_unit = st.text_input("To", "kilometer")

    if st.button("Convert"):

        result = (value * ureg(from_unit)).to(to_unit)
        st.success(result)


# -----------------------------
# DOCUMENT TOOLS
# -----------------------------

elif menu == "📄 Document Tools":

    st.header("Document Tools")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf:
        reader = PdfReader(pdf)
        st.success(f"Pages: {len(reader.pages)}")


# -----------------------------
# ENGINEERING TOOLS
# -----------------------------

elif menu == "⚙️ Engineering Tools":

    st.header("Engineering Tools")

    tool = st.selectbox(
        "Select Tool",
        [
            "Tank Volume",
            "Pipe Velocity",
            "Pump Power",
            "Reynolds Number"
        ]
    )

    if tool == "Tank Volume":

        dia = st.number_input("Diameter (m)")
        height = st.number_input("Height (m)")

        if st.button("Calculate Volume"):
            volume = 3.14 * (dia/2)**2 * height
            st.success(volume)

    elif tool == "Pipe Velocity":

        flow = st.number_input("Flow (m3/hr)")
        dia = st.number_input("Diameter (mm)")

        if st.button("Calculate Velocity"):
            velocity = flow/(3.14*(dia/1000)**2/4)/3600
            st.success(velocity)

    elif tool == "Pump Power":

        flow = st.number_input("Flow")
        head = st.number_input("Head")
        eff = st.number_input("Efficiency")

        if st.button("Calculate Power"):
            power = (flow * head * 9.81) / (367 * (eff/100))
            st.success(power)

    elif tool == "Reynolds Number":

        density = st.number_input("Density")
        velocity = st.number_input("Velocity")
        diameter = st.number_input("Diameter")
        viscosity = st.number_input("Viscosity")

        if st.button("Calculate Reynolds"):
            re = (density * velocity * diameter) / viscosity
            st.success(re)


# Footer
st.markdown("""
---
### EngiCore Engineering Platform  
Built for Students • Engineers • Professionals
""")
