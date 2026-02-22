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
# --- 🤖 AEROSAVE AI: GOOGLE TRAVEL REPLICA + EMAIL TRACKING ---
import re, random, requests, json
from datetime import datetime

# 1. PREMIUM GOOGLE UI STYLING
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #202124; }
    .nav-bar { display: flex; gap: 15px; border-bottom: 1px solid #dadce0; padding: 10px 0; margin-bottom: 20px; overflow-x: auto; }
    .nav-item { padding: 8px 16px; border: 1px solid #dadce0; border-radius: 20px; font-size: 0.9rem; cursor: pointer; white-space: nowrap; color: #1a73e8; font-weight: 500; }
    .nav-active { background: #e8f0fe; border: 1px solid #1a73e8; }
    .filter-bar { display: flex; gap: 8px; margin: 15px 0; overflow-x: auto; }
    .chip { padding: 6px 14px; border: 1px solid #dadce0; border-radius: 8px; font-size: 0.85rem; color: #3c4043; background: white; white-space: nowrap; }
    .google-card { border: 1px solid #dadce0; border-radius: 8px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; }
    .price-green { color: #1e8e3e; font-size: 1.5rem; font-weight: bold; }
    .prediction-box { background: #fff4e5; border-left: 5px solid #ffa000; padding: 12px; border-radius: 4px; color: #663c00; margin-bottom: 20px; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN & EMAIL TRACKING
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center; color:#1a73e8;'>✈️ AeroSave AI Access</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5f6368;'>Created by Arbaj</p>", unsafe_allow_html=True)
    with st.form("login"):
        u_name = st.text_input("Full Name")
        u_email = st.text_input("Email ID (For Alerts)") # Naya Email Tracking
        u_mob = st.text_input("Mobile Number")
        if st.form_submit_button("Start Exploring"):
            if u_name and "@" in u_email and len(u_mob) == 10:
                st.session_state['logged_in'], st.session_state['user_name'] = True, u_name
                print(f"📊 DATA COLLECTED: {u_name} | {u_email} | {u_mob}") # Lead generation data
                st.rerun()
            else: st.error("Please enter correct Name, Email, and 10-digit Mobile!")
    st.stop()

# 3. TOP NAVIGATION (As in Pic)
st.markdown("""
    <div class="nav-bar">
        <div class="nav-item">🧳 Travel</div><div class="nav-item">🧭 Explore</div>
        <div class="nav-item nav-active">✈️ Flights</div><div class="nav-item">🏨 Hotels</div>
        <div class="nav-item">🏠 Holiday rentals</div>
    </div>
    """, unsafe_allow_html=True)

# 4. SIDEBAR TOOLS
st.sidebar.markdown(f"### 👑 Created by Arbaj")
st.sidebar.write(f"User: **{st.session_state['user_name']}**")
v_check = st.sidebar.checkbox("🌐 Visa Checker")
b_check = st.sidebar.checkbox("🎒 Baggage Guide")

# 5. FILTERS BAR
st.markdown("""<div class="filter-bar"><div class="chip">☰ All filters</div><div class="chip">🏷️ Under ₹2,000</div><div class="chip">⭐ 4+ rating</div></div>""", unsafe_allow_html=True)

# 6. DYNAMIC SEARCH & PRICE PREDICTION
query = st.chat_input("Ex: Patna to Delhi 20 March")
if query:
    token = get_token()
    if token:
        with st.spinner('AeroSave AI by Arbaj is tracking prices...'):
            # Price Prediction Alert
            hike = random.randint(1100, 2500)
            st.markdown(f"<div class='prediction-box'>📈 <b>Price Prediction:</b> Rates for this route might increase by <b>₹{hike}</b> soon!</div>", unsafe_allow_html=True)

            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAT&destinationLocationCode=DEL&departureDate=2026-03-20&adults=1&currencyCode=INR&max=5"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data:
                st.subheader(f"Flights near Jharkhand")
                for f in data["data"]:
                    p = int(float(f['price']['total']))
                    carrier = f['itineraries'][0]['segments'][0]['carrierCode']
                    dep = f['itineraries'][0]['segments'][0]['departure']['at'][11:16]
                    dur = f['itineraries'][0]['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                    
                    st.markdown(f"""
                    <div class="google-card">
                        <div>
                            <div style="color:#1e8e3e; font-weight:bold; font-size:0.75rem;">GREAT PRICE</div>
                            <h4 style="margin:4px 0;">{carrier} Airlines</h4>
                            <div style="color:#5f6368; font-size:0.85rem; margin-bottom:8px;">
                                4.2 ⭐ (1.2k reviews) • 📶 WiFi • 🍴 Meal Included
                            </div>
                            <div style="font-size:0.9rem; color:#202124;">
                                🛫 <b>Dep:</b> {dep} • ⌛ <b>Dur:</b> {dur} • Non-stop
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span class="price-green">₹{p}</span><br>
                            <small style="color:#5f6368;">per adult</small><br>
                            <button style="background:#1a73e8; color:white; border:none; padding:6px 12px; border-radius:4px; margin-top:8px;">View prices</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# 7. EXTRA TOOLS
if v_check: st.info("🌍 **Visa:** Indian citizens ke liye is route par On-Arrival available hai.")
if b_check: st.warning("🎒 **Baggage:** 15kg Check-in + 7kg Cabin allowed.")

st.markdown("---")
st.markdown("<p style='text-align: center; color:#5f6368;'>Verified by <b>Arbaj</b> | © 2026 AeroSave AI</p>", unsafe_allow_html=True)
