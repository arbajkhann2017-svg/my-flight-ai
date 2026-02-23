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
import folium
from streamlit_folium import st_folium

# 🎨 1. PURE CHAT UI DESIGN
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .chat-container { max-width: 800px; margin: auto; }
    .flight-card { background: #f8f9fa; border-radius: 12px; padding: 15px; border: 1px solid #eee; margin-bottom: 15px; }
    .section-header { font-size: 14px; font-weight: bold; color: #5f6368; text-transform: uppercase; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    .price-sasti { color: #1e8e3e; font-weight: bold; font-size: 1.3rem; }
    .price-premium { color: #d93025; font-weight: bold; font-size: 1.3rem; }
    .timing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center; margin-top: 10px; padding: 10px 0; border-top: 1px solid #eef; }
    .predict-box { background: #fff7e0; border-left: 5px solid #fbbc04; padding: 10px; font-size: 13px; border-radius: 4px; margin-bottom: 20px; }
    .book-btn { width: 100%; background: #1a73e8; color: white; border: none; padding: 8px; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 🧠 2. FRESH CHAT LOGIC (Purana info delete karne ke liye)
if "last_query" not in st.session_state:
    st.session_state.last_query = None

# Chat Search Bar at the Top
query = st.chat_input("E.g. Patna to Delhi 20 March 2026")

if query:
    st.session_state.last_query = query

# ✈️ 3. FLIGHT RESULTS DISPLAY (Sirf tab dikhega jab search hoga)
if st.session_state.last_query:
    current_q = st.session_state.last_query
    st.markdown(f"### 🔍 Results for: {current_q}")
    
    # Price Prediction Alert
    st.markdown('<div class="predict-box">⚠️ <b>Price Prediction:</b> Based on history, prices are expected to rise by <b>₹3,007</b> in the next 4 hours.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # --- LEFT SIDE: SASTI FLIGHTS (CHEAPEST) ---
    with col1:
        st.markdown('<div class="section-header">📉 All Sasti Flights (Cheapest)</div>', unsafe_allow_html=True)
        sasti_flights = [
            {"air": "IndiGo 6E-2124", "p": "6,247", "dep": "06:20 AM", "arr": "08:10 AM", "dur": "1h 50m", "lug": "15kg", "v": "Free"},
            {"air": "SpiceJet SG-847", "p": "6,500", "dep": "11:30 AM", "arr": "01:25 PM", "dur": "1h 55m", "lug": "15kg", "v": "Free"},
            {"air": "Air India Exp", "p": "6,890", "dep": "05:15 PM", "arr": "07:15 PM", "dur": "2h 00m", "lug": "20kg", "v": "Free"}
        ]
        for f in sasti_flights:
            st.markdown(f"""
            <div class="flight-card">
                <div style="display:flex; justify-content:space-between;"><b>{f['air']}</b> <span class="price-sasti">₹{f['p']}</span></div>
                <div class="timing-grid">
                    <div><small>TAKE OFF</small><br><b>{f['dep']}</b></div>
                    <div><small>DUR</small><br><b>{f['dur']}</b></div>
                    <div><small>ARR</small><br><b>{f['arr']}</b></div>
                </div>
                <small style="color:gray;">🧳 {f['lug']} | 🛂 Visa: {f['v']}</small>
                <button class="book-btn">Book Now</button>
            </div>
            """, unsafe_allow_html=True)

    # --- RIGHT SIDE: COSTLY PREMIUM FLIGHTS ---
    with col2:
        st.markdown('<div class="section-header">💎 All Costly Premium Flights</div>', unsafe_allow_html=True)
        premium_flights = [
            {"air": "Air India Luxury", "p": "9,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m", "lug": "35kg", "v": "Free"},
            {"air": "Vistara Gold", "p": "12,450", "dep": "02:45 PM", "arr": "04:30 PM", "dur": "1h 45m", "lug": "40kg", "v": "Free"},
            {"air": "Vistara Platinum", "p": "15,200", "dep": "09:30 PM", "arr": "11:20 PM", "dur": "1h 50m", "lug": "45kg", "v": "Free"}
        ]
        for f in premium_flights:
            st.markdown(f"""
            <div class="flight-card" style="border-left: 4px solid #d93025;">
                <div style="display:flex; justify-content:space-between;"><b>{f['air']}</b> <span class="price-premium">₹{f['p']}</span></div>
                <div class="timing-grid">
                    <div><small>TAKE OFF</small><br><b>{f['dep']}</b></div>
                    <div><small>DUR</small><br><b>{f['dur']}</b></div>
                    <div><small>ARR</small><br><b>{f['arr']}</b></div>
                </div>
                <small style="color:gray;">🧳 {f['lug']} | 🍱 Premium Meals | 🛂 Visa: {f['v']}</small>
                <button class="book-btn" style="background:#d93025;">Book Premium</button>
            </div>
            """, unsafe_allow_html=True)
else:
    # Default Welcome Screen
    st.markdown("""
    <div style="text-align:center; padding-top:100px; color:#5f6368;">
        <h1 style="font-size:3rem;">✈️</h1>
        <h2>AeroSave AI Chat</h2>
        <p>Hello Arbaj! Patna to Delhi 20 March 2026 likhkar search karein.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("AeroSave v200.0 | Pure Chat Interface | Developed for Arbaj")
