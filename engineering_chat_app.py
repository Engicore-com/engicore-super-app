import streamlit as st
import sympy as sp
import pint
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import wikipedia
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas

# Setup
ureg = pint.UnitRegistry()

st.set_page_config(
    page_title="EngiCore Platform",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🧠 EngiCore Engineering Platform")
st.markdown("---")

# -----------------------------
# MODULE BUTTONS
# -----------------------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    home = st.button("🏠 Home")

with col2:
    smart = st.button("🧠 Smart Assistant")

with col3:
    calc = st.button("🧮 Calculator")

with col4:
    convert = st.button("🔄 Converter")

with col5:
    docs = st.button("📄 Docs")

with col6:
    eng = st.button("⚙️ Engineering")


# -----------------------------
# HOME
# -----------------------------

if home:

    st.header("Welcome to EngiCore")

    st.write("All in One Engineering Platform")

# -----------------------------
# SMART ASSISTANT
# -----------------------------

if smart:

    st.header("Smart Assistant")

    query = st.text_input("Ask anything")

    def smart_engine(q):

        # Math
        try:
            return sp.sympify(q)
        except:
            pass

        # Unit conversion
        try:
            pattern = r'(\d+\.?\d*)\s*(\w+)\s*(to)\s*(\w+)'
            match = re.search(pattern, q)

            if match:
                value = float(match.group(1))
                from_unit = match.group(2)
                to_unit = match.group(4)

                return (value * ureg(from_unit)).to(to_unit)

        except:
            pass

        # Wikipedia
        try:
            return wikipedia.summary(q, sentences=2)
        except:
            pass

        return "Try math, engineering or unit conversion"

    if st.button("Ask"):
        result = smart_engine(query)
        st.success(result)


# -----------------------------
# CALCULATOR
# -----------------------------

if calc:

    st.header("Calculator")

    num1 = st.number_input("Number 1")
    num2 = st.number_input("Number 2")

    op = st.selectbox(
        "Operation",
        ["Add","Subtract","Multiply","Divide"]
    )

    if st.button("Calculate"):

        if op == "Add":
            st.success(num1 + num2)

        elif op == "Subtract":
            st.success(num1 - num2)

        elif op == "Multiply":
            st.success(num1 * num2)

        elif op == "Divide":
            st.success(num1 / num2)

# -----------------------------
# CONVERTER
# -----------------------------

if convert:

    st.header("Converter")

    value = st.number_input("Value",1.0)
    from_unit = st.text_input("From")
    to_unit = st.text_input("To")

    if st.button("Convert"):
        result = (value * ureg(from_unit)).to(to_unit)
        st.success(result)

# -----------------------------
# DOCUMENT
# -----------------------------

if docs:

    st.header("Document Tools")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf:
        reader = PdfReader(pdf)
        st.success(f"Pages: {len(reader.pages)}")

# -----------------------------
# ENGINEERING
# -----------------------------

if eng:

    st.header("Engineering Tools")

    tool = st.selectbox(
        "Select Tool",
        [
        "Pump Curve",
        "Pipe Sizing",
        "Fluid Database",
        "Plant Simulation",
        "Engineering Report"
        ]
    )

# Pump Curve

    if tool == "Pump Curve":

        flow = np.linspace(0,100,50)
        head = 50 - 0.01*(flow**2)

        fig, ax = plt.subplots()
        ax.plot(flow,head)

        st.pyplot(fig)

# Pipe Sizing

    elif tool == "Pipe Sizing":

        flow = st.number_input("Flow")
        velocity = st.number_input("Velocity")

        if st.button("Calculate"):

            area = flow/(velocity*3600)
            dia = ((4*area)/3.14)**0.5

            st.success(dia*1000)

# Fluid Database

    elif tool == "Fluid Database":

        fluids = {
            "Water":{"Density":1000},
            "Oil":{"Density":850},
            "Air":{"Density":1.2}
        }

        fluid = st.selectbox("Fluid",fluids.keys())

        st.write(fluids[fluid])

# Plant Simulation

    elif tool == "Plant Simulation":

        eq = st.multiselect(
            "Equipment",
            ["Pump","Tank","Pipe"]
        )

        for e in eq:
            st.success(f"{e} added")

# Report

    elif tool == "Engineering Report":

        project = st.text_input("Project")

        if st.button("Generate"):

            c = canvas.Canvas("report.pdf")

            c.drawString(100,750,"EngiCore Report")
            c.drawString(100,720,project)

            c.save()

            st.success("Report Generated")


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")
st.write("EngiCore Engineering Platform")
