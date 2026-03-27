import streamlit as st
import sympy as sp
import pint
import re

# Setup
ureg = pint.UnitRegistry()

st.set_page_config(
    page_title="EngiCore Super App",
    layout="wide"
)

st.title("🧠 EngiCore Super App")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Smart Assistant",
        "Calculator",
        "Converter",
        "Document Tools",
        "Engineering Tools"
    ]
)

# -----------------------
# SMART ASSISTANT
# -----------------------

if menu == "Smart Assistant":

    st.header("Smart Assistant")

    query = st.text_input("Ask anything")

    if st.button("Solve"):

        try:
            result = sp.sympify(query)
            st.success(result)
        except:
            st.info("Try math or engineering question")


# -----------------------
# CALCULATOR
# -----------------------

elif menu == "Calculator":

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


# -----------------------
# CONVERTER
# -----------------------

elif menu == "Converter":

    st.header("Unit Converter")

    value = st.number_input("Value", 1.0)

    from_unit = st.text_input("From", "meter")
    to_unit = st.text_input("To", "kilometer")

    if st.button("Convert"):

        result = (value * ureg(from_unit)).to(to_unit)
        st.success(result)


# -----------------------
# DOCUMENT TOOLS
# -----------------------

elif menu == "Document Tools":

    st.header("Document Tools")

    st.info("PDF tools coming next update")


# -----------------------
# ENGINEERING TOOLS
# -----------------------

elif menu == "Engineering Tools":

    st.header("Engineering Tools")

    tool = st.selectbox(
        "Select Tool",
        [
            "Tank Volume",
            "Pipe Velocity"
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
