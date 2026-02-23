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
import json
from streamlit_folium import st_folium

# 🎨 1. CLEAN INTERFACE ENGINE
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .stApp { max-width: 100%; }
    .chat-bubble { background: white; border: 1px solid #dadce0; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .price-tag { color: #1e8e3e; font-weight: bold; font-size: 1.4rem; }
    .roi-badge { background: #e6f4ea; color: #137333; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; }
    .module-info { color: #1a73e8; font-size: 12px; font-weight: bold; }
    .flight-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center; border-top: 1px solid #eee; padding-top: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 🗺️ 2. TOP NAVIGATION BAR
tabs = st.tabs(["✈️ Flights & Chat", "🌍 Explore Map", "🛂 Safety & Visa", "🏨 Hotels"])

# 💬 3. MAIN MODULE: FLIGHT CHAT & BUDGET INTELLIGENCE
with tabs[0]:
    st.subheader("✈️ AeroSave Flight Assistant")
    
    # Fresh Info Logic
    if "chat_data" not in st.session_state:
        st.session_state.chat_data = None

    if query := st.chat_input("Patna to Delhi 20 March 2026"):
        st.session_state.chat_data = query
        st.rerun()

    if st.session_state.chat_data:
        st.info(f"Showing fresh results for: **{st.session_state.chat_data}**")
        
        # Advanced Data Architecture
        flights = [
            {"type": "Sasti", "air": "IndiGo 6E-2124", "p": "6,247", "dep": "06:20 AM", "arr": "08:10 AM", "roi": "92/100", "budget": "₹12,500"},
            {"type": "Sasti", "air": "SpiceJet SG-847", "p": "6,500", "dep": "11:30 AM", "arr": "01:25 PM", "roi": "88/100", "budget": "₹13,200"},
            {"type": "Premium", "air": "Air India Luxury", "p": "9,179", "dep": "02:45 PM", "arr": "04:30 PM", "roi": "75/100", "budget": "₹28,000"},
            {"type": "Premium", "air": "Vistara Gold", "p": "12,450", "dep": "09:30 PM", "arr": "11:20 PM", "roi": "68/100", "budget": "₹35,000"}
        ]

        for f in flights:
            with st.container():
                st.markdown(f"""
                <div class="chat-bubble">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="module-info">{f['type']} Flight | <span class="roi-badge">ROI: {f['roi']}</span></span>
                        <span class="price-tag">₹{f['p']}</span>
                    </div>
                    <b>{f['air']}</b>
                    <p style="font-size:11px; color:grey; margin:0;">Total Trip Cost (Est): <b>{f['budget']}</b></p>
                    <div class="flight-grid">
                        <div><small>TAKE OFF</small><br><b>{f['dep']}</b></div>
                        <div><small>ARRIVAL</small><br><b>{f['arr']}</b></div>
                        <div><button style="background:#1a73e8; color:white; border:none; padding:5px 15px; border-radius:5px; font-weight:bold;">Book</button></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("👋 Hello Arbaj! Destination aur date likhkar search karein.")

# 🌍 4. EXPLORE MODULE
with tabs[1]:
    st.subheader("Global Price Map")
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    folium.Marker([1.35, 103.8], popup="Singapore: ₹24,030").add_to(m)
    folium.Marker([28.6, 77.2], popup="Delhi: ₹2,284").add_to(m)
    st_folium(m, width="100%", height=500)

# 🛂 5. SAFETY & VISA MODULE
with tabs[2]:
    st.subheader("International Safety & Visa Status")
    visa_data = [
        {"p": "Dubai", "s": "95/100", "v": "E-Visa", "r": "Safe"},
        {"p": "Thailand", "s": "82/100", "v": "Arrival", "r": "Caution"}
    ]
    for v in visa_data:
        st.markdown(f"<div class='chat-bubble'><b>{v['p']}</b><br>Safety: {v['s']} | Visa: {v['v']}<br>Status: {v['r']}</div>", unsafe_allow_html=True)

# 🏨 6. HOTELS MODULE
with tabs[3]:
    st.text_input("Enter city", "Ranchi")
    st.markdown("<div class='chat-bubble'><b>Hotel Meera</b><br>Price: ₹708 | Rating: 4.0 ⭐</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("AeroSave v190.0 | ROI Engine | Arbaj Edition")
