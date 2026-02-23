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

# 🎨 1. ADVANCED UI ENGINE (Master Frontend)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card { background: white; border-radius: 12px; padding: 20px; border: 1px solid #dadce0; margin-bottom: 15px; }
    .price-roi { color: #1e8e3e; font-weight: bold; font-size: 1.5rem; }
    .module-tag { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-right: 5px; }
    .budget-pill { background: #e6f4ea; color: #137333; padding: 2px 8px; border-radius: 20px; font-size: 10px; font-weight: bold; }
    .itinerary-step { border-left: 2px solid #1a73e8; padding-left: 15px; margin-bottom: 10px; position: relative; }
    </style>
    """, unsafe_allow_html=True)

# 🗺️ 2. SYSTEM NAVIGATION
tabs = ["Flights", "Explore", "Hotels", "Safety & Visa", "AI Planner"]
selected_tab = st.sidebar.radio("Navigation Menu", tabs)

# ✈️ 3. FLIGHT EXPLORE & BUDGET MODULE
if selected_tab == "Flights":
    st.subheader("✈️ Flight & Budget Intelligence")
    colA, colB = st.columns(2)
    with colA: origin = st.text_input("Origin", "Patna")
    with colB: budget_mode = st.selectbox("Budget Mode", ["Student", "Economy", "Luxury"])
    
    # Advanced Data Structure (Authentic Organize)
    flights = [
        {
            "airline": "IndiGo 6E-2124", "price": "6,247", "dep": "06:20 PM", "arr": "08:10 PM",
            "budget": {"total": "₹12,500", "roi": 92, "breakdown": "F: 6k, H: 4k, T: 2.5k"},
            "type": "Sasti Flight"
        },
        {
            "airline": "Vistara Gold", "price": "9,850", "dep": "10:40 AM", "arr": "12:25 PM",
            "budget": {"total": "₹28,000", "roi": 78, "breakdown": "F: 10k, H: 15k, T: 3k"},
            "type": "Premium"
        }
    ]

    for f in flights:
        st.markdown(f"""
        <div class="card">
            <span class="module-tag">{f['type']}</span> <span class="budget-pill">ROI: {f['budget']['roi']}/100</span>
            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                <b>{f['airline']}</b>
                <span class="price-roi">₹{f['price']}</span>
            </div>
            <p style="font-size:12px; color:grey;">Estimated Total Trip Cost ({budget_mode}): <b>{f['budget']['total']}</b></p>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); text-align:center; border-top:1px solid #eee; padding-top:10px;">
                <div><small>DEPARTURE</small><br><b>{f['dep']}</b></div>
                <div><small>ARRIVAL</small><br><b>{f['arr']}</b></div>
                <div><button style="background:#1a73e8; color:white; border:none; border-radius:4px; padding:5px 15px;">Book</button></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 🌍 4. EXPLORE & TRENDING MODULE
elif selected_tab == "Explore":
    st.subheader("🌍 Trending Destinations & Visual Preview")
    dest = [
        {"city": "Singapore", "price": "₹24,030", "lat": 1.35, "lon": 103.8, "trend": "+12% Growth"},
        {"city": "London", "price": "₹73,650", "lat": 51.5, "lon": -0.1, "trend": "+5% Growth"}
    ]
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    for d in dest: folium.Marker([d['lat'], d['lon']], popup=d['city']).add_to(m)
    st_folium(m, width="100%", height=400)
    
    for d in dest:
        st.markdown(f"<div class='card'><b>{d['city']}</b> | <small>{d['trend']}</small><br><span class='price-roi'>Starting {d['price']}</span></div>", unsafe_allow_html=True)

# 🛂 5. SAFETY & VISA MODULE
elif selected_tab == "Safety & Visa":
    st.subheader("🛂 Safety Scores & Entry Rules")
    data = [
        {"place": "Dubai", "safety": "95/100", "visa": "E-Visa (48h)", "rules": "No COVID restrictions"},
        {"place": "Thailand", "safety": "82/100", "visa": "Visa on Arrival", "rules": "Passport validity 6 months"}
    ]
    for d in data:
        st.markdown(f"""
        <div class="card">
            <b>{d['place']}</b> <span class="module-tag" style="float:right;">Safety: {d['safety']}</span><br>
            <small>🛂 Visa: {d['visa']}</small><br>
            <small>📝 Entry Rules: {d['rules']}</small>
        </div>
        """, unsafe_allow_html=True)

# 🗓️ 6. AI TRIP PLANNER MODULE
elif selected_tab == "AI Planner":
    st.subheader("🗓️ AI Personalized Itinerary")
    days = [
        {"day": "Day 1", "task": "Arrive at Delhi, Check-in at Hotel Meera, Evening at India Gate."},
        {"day": "Day 2", "task": "Visit Red Fort & Chandni Chowk. Afternoon Flight back to Patna."},
    ]
    for d in days:
        st.markdown(f"""
        <div class="itinerary-step">
            <b>{d['day']}</b><br><small>{d['task']}</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("AeroSave v180.0 | ROI Engine | Arbaj Edition")
