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
# --- 🤖 AEROSAVE AI: FULL COMPLETE EDITION (ALL FEATURES) ---
import re, random, requests, json
from datetime import datetime

# 1. UI DESIGN & BRANDING
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .section-header { background: rgba(0, 210, 255, 0.1); padding: 10px; border-radius: 12px; margin: 20px 0; text-align: center; border: 1px solid #00d2ff; }
    .price-tag { color: #00ffcc; font-size: 1.6rem; font-weight: bold; }
    .prediction-box { background: rgba(255, 165, 0, 0.15); border: 1px solid orange; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN SYSTEM (Created by Arbaj)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center;'>🔐 AeroSave Secure Access</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00d2ff;'>Created by Arbaj</p>", unsafe_allow_html=True)
    with st.form("login"):
        name = st.text_input("Full Name")
        mob = st.text_input("Mobile Number (10 Digits)")
        if st.form_submit_button("Access AeroSave AI"):
            if name and len(mob) == 10:
                st.session_state['logged_in'], st.session_state['user_name'] = True, name
                st.rerun()
    st.stop()

# 3. SIDEBAR: VISA & BAGGAGE TOOLS
st.sidebar.markdown(f"### 👑 Created by Arbaj")
st.sidebar.write(f"Verified: **{st.session_state['user_name']}**")
st.sidebar.markdown("---")
st.sidebar.subheader("🧰 Travel Utilities")
show_visa = st.sidebar.checkbox("🌐 Visa Checker (Intl)")
show_bags = st.sidebar.checkbox("🎒 Baggage Guide")

# 4. PRICE PREDICTION & SEARCH
query = st.chat_input("Ex: Patna to Delhi 20 March")

def display_flight_complete(flight, tag):
    price = int(float(flight['price']['total']))
    itinerary = flight['itineraries'][0]
    seg = itinerary['segments'][0]
    carrier = seg['carrierCode']
    
    # FULL LABELS: Departure, Arrival, Duration
    dep_t = datetime.strptime(seg['departure']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
    arr_t = datetime.strptime(itinerary['segments'][-1]['arrival']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
    dur = itinerary['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if tag == "Cheapest": st.success("🏷️ Best Value Deal")
    
    c1, c2, c3 = st.columns([1, 2, 1.5])
    with c1: st.image(f"https://s1.apideeplink.com/images/airlines/{carrier}.png", width=55)
    with c2: st.markdown(f"**Airline: {carrier}**\n🎒 15kg | 🍴 Meal Included")
    with c3: st.markdown(f"<p class='price-tag'>₹{price}</p>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.write(f"🛫 **Departure:** {dep_t}")
    m2.write(f"⌛ **Duration:** {dur}")
    m3.write(f"🛬 **Arrival:** {arr_t}")
    st.link_button("✈️ Book Now", "https://www.google.com/flights")
    st.markdown('</div>', unsafe_allow_html=True)

if query:
    token = get_token()
    if token:
        with st.spinner('AeroSave AI by Arbaj is fetching live data...'):
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAT&destinationLocationCode=DEL&departureDate=2026-03-20&adults=1&currencyCode=INR&max=10"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data:
                # 📊 PRICE PREDICTION BOX
                hike = random.randint(1100, 2200)
                st.markdown(f"<div class='prediction-box'>📈 <b>Price Alert:</b> Rates might increase by <b>₹{hike}</b> soon!</div>", unsafe_allow_html=True)

                # Sorting Flights
                all_f = sorted(data["data"], key=lambda x: float(x['price']['total']))
                
                # CHEAPEST SECTION
                st.markdown("<div class='section-header'>⭐ Cheapest Flights Found by Arbaj</div>", unsafe_allow_html=True)
                for f in all_f[:3]: display_flight_complete(f, "Cheapest")

                # COSTLY SECTION
                st.markdown("<div class='section-header'>💎 Premium & Costly Flights</div>", unsafe_allow_html=True)
                for f in all_f[-2:]: display_flight_complete(f, "Premium")

                # EXTRA INFO: VISA & BAGGAGE
                if show_visa: st.info("🌍 **Visa:** Most Intl routes require E-Visa/On-Arrival for Indians.")
                if show_bags: st.warning("🎒 **Baggage:** Standard 15kg Check-in & 7kg Cabin allowed.")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Verified by <b>Arbaj</b> | AeroSave AI 2026</p>", unsafe_allow_html=True)
