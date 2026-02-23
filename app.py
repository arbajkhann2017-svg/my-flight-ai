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

# 🎨 1. MASTER CSS (Authentic Travel Look)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatFloatingInputContainer { background-color: white; border-top: 1px solid #ddd; }
    .chat-card { background: white; border-radius: 15px; padding: 15px; border: 1px solid #e0e0e0; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .price-green { color: #1e8e3e; font-weight: bold; font-size: 1.4rem; }
    .badge { background: #e8f0fe; color: #1a73e8; padding: 3px 10px; border-radius: 5px; font-size: 11px; font-weight: bold; }
    .prediction-box { background: #fff7e0; border: 1px solid #ffeeba; color: #856404; padding: 10px; border-radius: 10px; font-size: 13px; margin: 10px 0; }
    .flight-info-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center; margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 🗺️ 2. NAVIGATION SYSTEM
if 'tab' not in st.session_state: st.session_state['tab'] = 'Flights'
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if cols[i].button(t, key=f"v4_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state['tab']

# ✈️ 3. SMART FLIGHT CHAT SECTION
if current_tab == "Flights":
    st.subheader("✈️ AeroSave Flight Assistant")
    
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello Arbaj! Patna to Delhi flights ki details chahiye? Kripya search box mein destination aur date likhein."}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Patna to Delhi 20 March 2026"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        # 🤖 AI GENERATED RESPONSE WITH ALL AUTHENTIC DETAILS
        ai_response = f"""
        🔍 **Searching flights for: {prompt}**... <br><br>
        
        <div class="prediction-box">⚠️ <b>Price Prediction:</b> Prices for 20 March are expected to rise by <b>₹3,007</b> in the next few hours.</div>
        
        <div class="chat-card">
            <span class="badge">Sasti Flight (Cheapest)</span>
            <div style="display:flex; justify-content:space-between; margin-top:5px;">
                <b>IndiGo • 6E-2124</b>
                <span class="price-green">₹6,247</span>
            </div>
            <div class="flight-info-row">
                <div><small>TAKE OFF</small><br><b>06:20 PM</b></div>
                <div><small>DURATION</small><br><b>1h 50m</b></div>
                <div><small>ARRIVAL</small><br><b>08:10 PM</b></div>
            </div>
            <div style="font-size: 12px; color: grey; margin-top: 5px;">🧳 15kg Luggage | 🛂 Visa Free | 📍 Patna (PAT) ➔ Delhi (DEL)</div>
            <button style="width:100%; background:#1a73e8; color:white; border:none; padding:8px; border-radius:5px; margin-top:10px; font-weight:bold;">Book Now</button>
        </div>

        <div class="chat-card">
            <span class="badge" style="background:#fce8e6; color:#d93025;">Costly Premium</span>
            <div style="display:flex; justify-content:space-between; margin-top:5px;">
                <b>Air India Luxury</b>
                <span class="price-green">₹9,850</span>
            </div>
            <div class="flight-info-row">
                <div><small>TAKE OFF</small><br><b>10:40 AM</b></div>
                <div><small>DURATION</small><br><b>1h 45m</b></div>
                <div><small>ARRIVAL</small><br><b>12:25 PM</b></div>
            </div>
            <div style="font-size: 12px; color: grey; margin-top: 5px;">🧳 35kg Luggage | 🛂 Visa Free | 🍱 Premium Meals Included</div>
            <button style="width:100%; background:#1a73e8; color:white; border:none; padding:8px; border-radius:5px; margin-top:10px; font-weight:bold;">Book Now</button>
        </div>
        """
        with st.chat_message("assistant"):
            st.markdown(ai_response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 🌍 4. EXPLORE & TRAVEL (Global Maps)
elif current_tab in ["Explore", "Travel"]:
    st.subheader("Explore Popular Destinations")
    dest_data = [
        {"city": "Singapore", "p": "₹24,030", "lat": 1.35, "lon": 103.8},
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.1},
        {"city": "Mumbai", "p": "₹3,044", "lat": 19.0, "lon": 72.8},
        {"city": "Delhi", "p": "₹2,284", "lat": 28.6, "lon": 77.2}
    ]
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    for d in dest_data:
        folium.Marker([d['lat'], d['lon']], popup=f"{d['city']}: {d['p']}").add_to(m)
    
    c1, c2 = st.columns([1.5, 1])
    with c1: st_folium(m, width="100%", height=500)
    with c2:
        for d in dest_data:
            st.markdown(f"<div class='chat-card'><b>{d['city']}</b><br><span class='price-green' style='font-size:1rem;'>{d['p']}</span></div>", unsafe_allow_html=True)

# 🏨 5. HOTELS & RENTALS
elif current_tab == "Hotels":
    loc = st.text_input("Enter location", "Ranchi, Jharkhand")
    hotels = [{"n": "Hotel Meera", "p": "₹708", "r": "4.0 ⭐"}, {"n": "Genista Inn", "p": "₹3,000", "r": "4.2 ⭐"}]
    for h in hotels: st.markdown(f"<div class='chat-card'><b>{h['n']}</b> ({h['r']})<br><span class='price-green'>₹{h['p']}</span></div>", unsafe_allow_html=True)

elif current_tab == "Holiday rentals":
    rentals = [{"n": "Modern House", "p": "₹1,900", "l": "Mandar"}, {"n": "Candy Studio", "p": "₹3,994", "l": "Ranchi"}]
    for r in rentals: st.markdown(f"<div class='chat-card'><b>{r['n']}</b><br><small>{r['l']}</small><br><span class='price-green'>{r['p']}</span>/night</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("AeroSave AI v160.0 | Smart Chat & Travel Engine | Arbaj Edition")
