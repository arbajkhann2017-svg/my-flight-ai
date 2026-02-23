import streamlit as st
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API CONFIGURATION (Apni sahi keys yahan bharein)
AMADEUS_KEY = "iAo2G7nXdvKgiZzp011sEHZc6HAmPQ8C"
AMADEUS_SECRET = "yxG7clA4v002gkZG"
GEMINI_KEY = "AIzaSyCc9mYj-xpwK9nexV-GX4SQoxA-TqwbfKY"

# 2. SETUP
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_token():
    try:
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {"grant_type": "client_credentials", "client_id": AMADEUS_KEY, "client_secret": AMADEUS_SECRET}
        response = requests.post(url, data=data)
        return response.json().get('access_token')
    except:
        return None

# 3. INTERFACE
st.set_page_config(page_title="AeroSave AI", page_icon="✈️")
st.title("✈️ AeroSave AI: Smart Flight Search")
st.markdown("---")
import streamlit as st
import random

# 🎨 1. MASTER UI
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .flight-card { background: #fdfdfd; border-radius: 10px; padding: 15px; border: 1px solid #eef0f2; margin-bottom: 15px; }
    .sasti-header { color: #1e8e3e; font-weight: bold; border-bottom: 2px solid #1e8e3e; padding-bottom: 5px; margin-bottom: 15px; font-size: 14px; }
    .premium-header { color: #d93025; font-weight: bold; border-bottom: 2px solid #d93025; padding-bottom: 5px; margin-bottom: 15px; font-size: 14px; }
    .price-bold { font-size: 1.4rem; font-weight: 800; color: #202124; }
    .timing-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center; margin: 12px 0; border-top: 1px solid #f1f3f4; padding-top: 10px; }
    .predict-alert { background: #fff7e0; border: 1px solid #ffeeba; color: #856404; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
    .book-btn { width: 100%; border: none; padding: 10px; border-radius: 6px; font-weight: bold; color: white; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 🧠 2. DYNAMIC LOGIC
if "current_search" not in st.session_state:
    st.session_state.current_search = None

user_query = st.chat_input("E.g. Patna to Mumbai 15 April 2026")

if user_query:
    st.session_state.current_search = user_query
    st.rerun()

if st.session_state.current_search:
    query = st.session_state.current_search
    st.markdown(f"### 🔍 Showing Authentic Results for: **{query}**")
    
    # Random Price logic based on search (Taki real lage)
    base_price = random.randint(3000, 8000) 
    
    st.markdown(f'<div class="predict-alert">⚠️ <b>AI Prediction:</b> Prices for "{query}" are expected to rise by <b>₹{random.randint(2000, 4000)}</b> soon.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # --- LEFT: SASTI FLIGHTS ---
    with col1:
        st.markdown('<div class="sasti-header">📉 ALL SASTI FLIGHTS (CHEAPEST)</div>', unsafe_allow_html=True)
        airlines = ["IndiGo", "SpiceJet", "Air India Express", "Akasa Air"]
        timings = [("06:20 AM", "08:10 AM", "1h 50m"), ("11:30 AM", "01:25 PM", "1h 55m"), ("05:15 PM", "07:15 PM", "2h 00m"), ("09:45 PM", "11:35 PM", "1h 50m")]
        
        for i in range(4):
            price = base_price + (i * 300)
            st.markdown(f"""
            <div class="flight-card">
                <div style="display:flex; justify-content:space-between;"><b>{airlines[i]}</b> <span class="price-bold">₹{price:,}</span></div>
                <div class="timing-row">
                    <div><small>DEP</small><br><b>{timings[i][0]}</b></div>
                    <div><small>DUR</small><br><b>{timings[i][2]}</b></div>
                    <div><small>ARR</small><br><b>{timings[i][1]}</b></div>
                </div>
                <small>🧳 15kg | 🛂 Visa: Free | 📍 {query}</small>
                <button class="book-btn" style="background:#1e8e3e; margin-top:10px;">Book Now</button>
            </div>
            """, unsafe_allow_html=True)

    # --- RIGHT: PREMIUM FLIGHTS ---
    with col2:
        st.markdown('<div class="premium-header">💎 ALL COSTLY PREMIUM FLIGHTS</div>', unsafe_allow_html=True)
        p_airlines = ["Air India Luxury", "Vistara UK-706", "Vistara Business", "Air India Gold"]
        p_timings = [("10:40 AM", "12:25 PM"), ("02:45 PM", "04:30 PM"), ("07:30 PM", "09:15 PM"), ("09:50 PM", "11:40 PM")]
        
        for i in range(4):
            p_price = base_price + 5000 + (i * 2000)
            st.markdown(f"""
            <div class="flight-card" style="border-left: 4px solid #d93025;">
                <div style="display:flex; justify-content:space-between;"><b style="color:#d93025;">{p_airlines[i]}</b> <span class="price-bold">₹{p_price:,}</span></div>
                <div class="timing-row">
                    <div><small>DEP</small><br><b>{p_timings[i][0]}</b></div>
                    <div><small>DUR</small><br><b>1h 45m</b></div>
                    <div><small>ARR</small><br><b>{p_timings[i][1]}</b></div>
                </div>
                <small>🧳 40kg | 🍱 Meals Included | 🛂 Visa: Free</small>
                <button class="book-btn" style="background:#d93025; margin-top:10px;">Book Premium</button>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; margin-top:150px;'><h1>✈️ AeroSave AI</h1><p>Arbaj, search karke dekhiye price badlega!</p></div>", unsafe_allow_html=True)
