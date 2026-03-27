import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from pint import UnitRegistry

try:
    from streamlit_drawable_canvas import st_canvas
    canvas_available = True
except:
    canvas_available = False

ureg = UnitRegistry()

st.set_page_config(layout="wide")

st.title("⚙️ EngiCore Enterprise Engineering Platform")

# Sidebar buttons

st.sidebar.title("⚙️ EngiCore")

if "page" not in st.session_state:
    st.session_state.page = "calc"

if st.sidebar.button("🧮 Advanced Calculator"):
    st.session_state.page = "calc"

if st.sidebar.button("📐 Unit Converter"):
    st.session_state.page = "unit"

if st.sidebar.button("🏭 Industrial Calculators"):
    st.session_state.page = "industrial"

if st.sidebar.button("🏭 Plant Builder"):
    st.session_state.page = "plant"

if st.sidebar.button("📄 Doc Converter"):
    st.session_state.page = "doc"

if st.sidebar.button("🤖 Equipment AI"):
    st.session_state.page = "ai"


# Advanced Calculator

if st.session_state.page == "calc":

    st.header("🧮 Advanced Calculator")

    expr = st.text_input("Expression")

    if st.button("Calculate"):

        try:
            st.success(eval(expr))
        except:
            st.error("Invalid Expression")


# Unit Converter

elif st.session_state.page == "unit":

    st.header("📐 Unit Converter")

    value = st.number_input("Value")

    from_unit = st.text_input("From", "meter")
    to_unit = st.text_input("To", "feet")

    if st.button("Convert"):

        try:
            result = (value * ureg(from_unit)).to(to_unit)
            st.success(result)
        except:
            st.error("Conversion Error")


# Industrial Calculators

elif st.session_state.page == "industrial":

    st.header("🏭 Industrial Calculators")

    flow = st.number_input("Flow")
    vel = st.number_input("Velocity")

    if st.button("Pipe Size"):

        d = (4*flow/(3.14*vel))**0.5
        st.success(f"Diameter {d}")


# Plant Builder

elif st.session_state.page == "plant":

    st.header("🏭 Plant Builder")

    if "plant" not in st.session_state:
        st.session_state.plant = []

    st.subheader("Drag Equipment")

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("⚙️ Pump"):
        st.session_state.plant.append("Pump")

    if col2.button("🔥 Heat Exchanger"):
        st.session_state.plant.append("Heat Exchanger")

    if col3.button("🛢 Tank"):
        st.session_state.plant.append("Tank")

    if col4.button("🔧 Valve"):
        st.session_state.plant.append("Valve")

    st.subheader("Plant Layout")

    for eq in st.session_state.plant:
        st.write(eq)

    # Pipe drawing

    st.subheader("Pipe Drawing")

    start = st.text_input("From")
    end = st.text_input("To")

    if st.button("Draw Pipe"):

        st.write(f"{start} → {end}")

    # PFD Canvas

    st.subheader("PFD Drawing")

    if canvas_available:

        canvas = st_canvas(
            fill_color="rgba(0,0,255,0.3)",
            stroke_width=2,
            background_color="#fff",
            height=500,
            drawing_mode="rect",
            key="canvas"
        )

    else:
        st.warning("Canvas not available")

    # Save Layout

    st.subheader("Save Layout")

    name = st.text_input("Layout Name")

    if st.button("Save"):

        os.makedirs("layouts", exist_ok=True)

        with open(f"layouts/{name}.json","w") as f:
            json.dump(st.session_state.plant, f)

        st.success("Saved")

    # Export PDF

    st.subheader("Export PFD PDF")

    if st.button("Export"):

        c = canvas.Canvas("PFD.pdf")

        y = 750

        for eq in st.session_state.plant:

            c.drawString(100,y,eq)
            y -= 30

        c.save()

        st.success("Exported")


# Doc Converter

elif st.session_state.page == "doc":

    st.header("📄 Doc Converter & iLovePDF")

    tool = st.selectbox(
        "Tool",
        [
            "Merge PDF",
            "Split PDF",
            "Image to PDF"
        ]
    )

    if tool == "Merge PDF":

        files = st.file_uploader(
            "Upload PDFs",
            accept_multiple_files=True
        )

        if st.button("Merge"):

            merger = PdfMerger()

            for f in files:
                merger.append(f)

            merger.write("merged.pdf")

            st.success("Merged")

    elif tool == "Split PDF":

        file = st.file_uploader("Upload PDF")

        if st.button("Split"):

            reader = PdfReader(file)
            writer = PdfWriter()

            writer.add_page(reader.pages[0])

            with open("split.pdf","wb") as f:
                writer.write(f)

            st.success("Split")


# Equipment AI

elif st.session_state.page == "ai":

    st.header("🤖 Equipment Sizing AI")

    eq = st.selectbox(
        "Equipment",
        ["Pump","Tank"]
    )

    if eq == "Pump":

        flow = st.number_input("Flow")
        head = st.number_input("Head")

        if st.button("Size"):

            power = flow*head/367

            st.success(f"Power {power:.2f} kW")

    elif eq == "Tank":

        d = st.number_input("Diameter")
        h = st.number_input("Height")

        if st.button("Size"):

            vol = 3.14*(d/2)**2*h

            st.success(f"Volume {vol:.2f} m3")


# Footer Dashboard

st.markdown("---")

st.write("⚙️ EngiCore Enterprise | Engineering Platform")
