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

# -------------------------
# DARK MODE TOGGLE
# -------------------------

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# MULTI LANGUAGE
# -------------------------

language = st.sidebar.selectbox(
    "🌍 Language",
    ["English", "Hindi"]
)

def translate(text):

    hindi = {
        "Home":"होम",
        "Calculator":"कैलकुलेटर",
        "Converter":"कन्वर्टर",
        "Engineering Tools":"इंजीनियरिंग टूल्स"
    }

    if language == "Hindi":
        return hindi.get(text,text)

    return text


# -------------------------
# LOGO + BRANDING
# -------------------------

st.markdown("""
# 🧠 EngiCore
### Engineering Super Platform
---
""")

# -------------------------
# NAVIGATION
# -------------------------

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

# -------------------------
# HOME
# -------------------------

if menu == "🏠 Home":

    st.header("Welcome to EngiCore")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("Smart Assistant")

    with col2:
        st.success("Calculator")

    with col3:
        st.success("Converter")

# -------------------------
# SMART ASSISTANT
# -------------------------

elif menu == "🧠 Smart Assistant":

    st.header("Smart Assistant")

    query = st.text_input("Ask anything")

    audio = mic_recorder(
        start_prompt="🎤 Start",
        stop_prompt="Stop"
    )

    if audio:
        st.info("Voice captured")

    if st.button("Solve"):

        try:
            result = sp.sympify(query)
            st.success(result)
        except:
            st.info("Try math or engineering question")


# -------------------------
# CALCULATOR
# -------------------------

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

# -------------------------
# CONVERTER
# -------------------------

elif menu == "🔄 Converter":

    st.header("Converter")

    value = st.number_input("Value", 1.0)

    from_unit = st.text_input("From", "meter")
    to_unit = st.text_input("To", "kilometer")

    if st.button("Convert"):

        result = (value * ureg(from_unit)).to(to_unit)
        st.success(result)

# -------------------------
# DOCUMENT
# -------------------------

elif menu == "📄 Document Tools":

    st.header("Document Tools")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf:
        reader = PdfReader(pdf)
        st.success(f"Pages: {len(reader.pages)}")


# -------------------------
# ENGINEERING TOOLS
# -------------------------

elif menu == "⚙️ Engineering Tools":

    st.header("Engineering Tools")

    tool = st.selectbox(
        "Select Tool",
        [
            "Tank Volume",
            "Pipe Velocity",
            "Pump Power"
        ]
    )

    if tool == "Tank Volume":

        dia = st.number_input("Diameter")
        height = st.number_input("Height")

        if st.button("Calculate"):
            volume = 3.14 * (dia/2)**2 * height
            st.success(volume)

# -------------------------
# FOOTER
# -------------------------

st.markdown("""
---
### EngiCore Platform  
Made for Students • Engineers • Professionals
""")
