import streamlit as st
import sympy as sp
import pint
import re

# Setup
ureg = pint.UnitRegistry()

st.set_page_config(
    page_title="EngiCore Super App",
    layout="centered"
)

st.title("🧠 EngiCore Engineering Super App")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Smart Math
def smart_math(query):
    try:
        return sp.sympify(query)
    except:
        return None


# Unit Converter
def smart_convert(text):
    try:
        pattern = r'(\d+\.?\d*)\s*([a-zA-Z/°/]+)\s*(to|in)\s*([a-zA-Z/°/]+)'
        match = re.search(pattern, text)

        if match:
            value = float(match.group(1))
            from_unit = match.group(2)
            to_unit = match.group(4)

            result = (value * ureg(from_unit)).to(to_unit)
            return result
    except:
        return None


# Engineering Formulas
def engineering_formula(query):

    if "area of circle" in query.lower():
        return "Area = π r²"

    if "reynolds" in query.lower():
        return "Re = ρVD / μ"

    if "velocity" in query.lower():
        return "Velocity = Flow / Area"

    return None


# Smart Engine
def smart_engine(query):

    math = smart_math(query)
    if math:
        return f"Math Result: {math}"

    convert = smart_convert(query)
    if convert:
        return f"Conversion: {convert}"

    formula = engineering_formula(query)
    if formula:
        return formula

    return "Ask math, unit conversion, or engineering question"


# Chat input
if prompt := st.chat_input("Ask anything..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    st.chat_message("user").write(prompt)

    response = smart_engine(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    st.chat_message("assistant").write(response)
