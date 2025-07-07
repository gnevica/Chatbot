import streamlit as st
import pandas as pd
import requests
from utils.data_viz import plot_uploaded_csv
from utils.forecast import forecast_with_prophet
from utils.memory import ChatMemory
from utils.weather_loc import get_weather
from utils.img_gen import generate_place_image

# Load API Key from Streamlit secrets
api_key = st.secrets["openrouter"]["api_key"]

st.set_page_config("AI Chatbot")

# Session management
session = st.session_state
if "memory" not in session:
    session.memory = ChatMemory()

# Page title
st.title("24/7 AI Chatbot")

# Sidebar options
st.sidebar.header("Options")

uploaded = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if st.sidebar.button("Get Local Weather :"):
    weather = get_weather()
    st.write(weather)

st.sidebar.subheader("Generate Place Image")
place = st.sidebar.text_input("Enter place name")
if st.sidebar.button("Generate Image"):
    img = generate_place_image(place)
    st.image(img, caption=f"AI visualization: {place}")

# Chat section
st.header("Chat with me:")
user_input = st.text_input("You:")

if user_input:
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
        # GPT-4 via OpenRouter
        messages = session.memory.get()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "openai/gpt-4",
            "messages": messages
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
            res.raise_for_status()
            reply = res.json()["choices"][0]["message"]["content"]
            session.memory.add("assistant", reply)
            st.markdown(f"**GPT‑4:** {reply}")
        except Exception as e:
            st.error(f"Error: {str(e)}")


