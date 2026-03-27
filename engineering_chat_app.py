import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from pint import UnitRegistry
import networkx as nx

ureg = UnitRegistry()

st.set_page_config(layout="wide")

st.title("⚙️ EngiCore Enterprise Engineering Platform")

# Menu
menu = st.sidebar.selectbox(
    "EngiCore",
    [
        "Dashboard",
        "Advanced Calculator",
        "Unit Converter",
        "Industrial Calculators",
        "Engineering Database",
        "Engineering Standards",
        "Plant Builder",
        "Equipment Sizing AI",
        "PDF Tools (iLovePDF Clone)",
        "Save Project"
    ]
)

# Dashboard
if menu == "Dashboard":

    col1,col2,col3 = st.columns(3)

    col1.metric("Modules","60+")
    col2.metric("Version","Enterprise")
    col3.metric("Platform","Industrial Suite")


# Calculator
elif menu == "Advanced Calculator":

    expr = st.text_input("Expression")

    if st.button("Calculate"):

        try:
            st.success(eval(expr))
        except:
            st.error("Invalid")


# Unit Converter
elif menu == "Unit Converter":

    value = st.number_input("Value")

    from_unit = st.text_input("From","meter")
    to_unit = st.text_input("To","feet")

    if st.button("Convert"):

        try:
            result = (value * ureg(from_unit)).to(to_unit)
            st.success(result)
        except:
            st.error("Error")


# Industrial Calculators
elif menu == "Industrial Calculators":

    calc = st.selectbox(
        "Calculator",
        [
            "Pipe Sizing",
            "Pump Power",
            "Heat Duty"
        ]
    )

    if calc == "Pipe Sizing":

        flow = st.number_input("Flow")
        vel = st.number_input("Velocity")

        if st.button("Calculate"):

            d = (4*flow/(3.14*vel))**0.5
            st.success(d)


# Engineering Database
elif menu == "Engineering Database":

    df = pd.DataFrame({
        "Material":["Steel","SS304","Aluminum"],
        "Density":[7850,8000,2700]
    })

    st.dataframe(df)


# Engineering Standards
elif menu == "Engineering Standards":

    df = pd.DataFrame({
        "Standard":["ASME B31.3","API 610","ASTM A106"]
    })

    st.dataframe(df)


# Plant Builder
elif menu == "Plant Builder":

    st.header("🏭 Plant Builder")

    equipment = st.selectbox(
        "Add Equipment",
        [
            "Pump",
            "Heat Exchanger",
            "Tank",
            "Valve",
            "Compressor"
        ]
    )

    if "plant" not in st.session_state:
        st.session_state.plant = []

    if st.button("Add Equipment"):
        st.session_state.plant.append(equipment)

    st.subheader("Plant Layout")

    for i, eq in enumerate(st.session_state.plant):
        st.write(f"{i+1}. {eq}")

    # Auto pipe
    st.subheader("Auto Pipe Connections")

    if st.button("Connect Automatically"):

        for i in range(len(st.session_state.plant)-1):
            st.write(
                f"{st.session_state.plant[i]} → {st.session_state.plant[i+1]}"
            )

    # Canvas
    st.subheader("PFD Canvas")

    canvas = st_canvas(
        fill_color="rgba(0,0,255,0.3)",
        stroke_width=2,
        background_color="#fff",
        height=500,
        drawing_mode="rect",
        key="canvas"
    )

    # Plant Simulator
    st.subheader("Plant Simulator")

    flow = st.number_input("Flow")
    temp = st.number_input("Temperature")
    pressure = st.number_input("Pressure")

    if st.button("Run Simulation"):

        st.success("Simulation Complete")

        st.write("Outlet Temp:", temp+5)
        st.write("Outlet Pressure:", pressure-1)


    # Save Layout
    st.subheader("Save Plant Layout")

    name = st.text_input("Layout Name")

    if st.button("Save Layout"):

        os.makedirs("layouts",exist_ok=True)

        with open(f"layouts/{name}.json","w") as f:
            json.dump(st.session_state.plant,f)

        st.success("Saved")


    # Load Layout
    if st.button("Load Layout"):

        with open(f"layouts/{name}.json") as f:
            st.session_state.plant = json.load(f)

        st.success("Loaded")


    # Export PDF
    st.subheader("Export PFD PDF")

    if st.button("Export PDF"):

        c = canvas.Canvas("PFD.pdf")

        y = 750

        for eq in st.session_state.plant:
            c.drawString(100,y,eq)
            y -= 30

        c.save()

        st.success("PFD Exported")


# Equipment Sizing AI
elif menu == "Equipment Sizing AI":

    st.header("🤖 Equipment Sizing AI")

    eq = st.selectbox(
        "Equipment",
        [
            "Pump",
            "Heat Exchanger",
            "Tank"
        ]
    )

    if eq == "Pump":

        flow = st.number_input("Flow")
        head = st.number_input("Head")
        eff = st.number_input("Efficiency",70)

        if st.button("Size"):

            power = (flow*head)/(367*(eff/100))

            st.success(f"Pump Power {power:.2f} kW")


    elif eq == "Tank":

        d = st.number_input("Diameter")
        h = st.number_input("Height")

        if st.button("Size"):

            vol = 3.14*(d/2)**2*h

            st.success(f"Volume {vol:.2f} m3")


# PDF Tools
elif menu == "PDF Tools (iLovePDF Clone)":

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

            for file in files:
                merger.append(file)

            merger.write("merged.pdf")

            st.success("Merged")


# Save Project
elif menu == "Save Project":

    name = st.text_input("Project Name")

    if st.button("Save"):

        os.makedirs("projects",exist_ok=True)

        with open(f"projects/{name}.json","w") as f:
            json.dump({"project":name},f)

        st.success("Saved")
