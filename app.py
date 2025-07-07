import streamlit as st
from utils.data_viz import plot_uploaded_csv
from utils.forecast import forecast_with_prophet
from utils.memory import ChatMemory
from utils.weather_loc import get_weather
from utils.img_gen import generate_place_image
import os
import pandas as pd
from openai import OpenAI
api_key = st.secrets["openrouter"]["api_key"]

st.set_page_config("AI Chatbot")

session = st.session_state
if "memory" not in session:
    session.memory = ChatMemory()

st.title("24/7 AI Chatbot")
st.sidebar.header("Options")
uploaded = st.sidebar.file_uploader("Upload CSV for viz/forecast", type=["csv"])
location_button = st.sidebar.button("Get Local Weather :")

if location_button:
    weather = get_weather()
    st.write(weather)

st.sidebar.subheader("Generate Place Image")
place = st.sidebar.text_input("Enter place name")
if st.sidebar.button("Generate Image"):
    img = generate_place_image(place)
    st.image(img, caption=f"AI visualization: {place}")

# Chat area
st.header("Chat with me:")
if user_input := st.text_input("You:"):
    session.memory.add("user", user_input)
    if uploaded is not None and "plot" in user_input.lower():
        df = pd.read_csv(uploaded)
        chart = plot_uploaded_csv(df, user_input)
        st.plotly_chart(chart)
    elif uploaded is not None and "forecast" in user_input.lower():
        df = pd.read_csv(uploaded)
        fc = forecast_with_prophet(df, user_input)
        st.plotly_chart(fc)
    else:
        messages = session.memory.get()
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages
        ).choices[0].message.content
        session.memory.add("assistant", response)
        st.markdown(f"**GPT‑4:** {response}")

