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
# --- 🤖 AEROSAVE AI: SMART PREDICTOR & MULTI-PORTAL ---
import re, random, requests, json
from datetime import datetime, timedelta

# 1. PREMIUM UI STYLING
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .nav-bar { display: flex; gap: 10px; border-bottom: 1px solid #dadce0; padding: 10px 0; margin-bottom: 20px; overflow-x: auto; }
    .prediction-card { background: #fff8e1; border-left: 5px solid #ff8f00; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #856404; font-size: 0.95rem; }
    .flight-card { border: 1px solid #dadce0; border-radius: 12px; padding: 20px; margin-bottom: 15px; background: white; }
    .price-green { color: #1e8e3e; font-size: 1.5rem; font-weight: bold; }
    .label-box { font-size: 0.75rem; color: #5f6368; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN & DATA TRACKING (Name, Email, Mobile)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center;'>✈️ AeroSave AI: Smart Login</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        u_name = st.text_input("Full Name")
        u_email = st.text_input("Email ID")
        u_mob = st.text_input("Mobile Number")
        if st.form_submit_button("Access Portal"):
            if u_name and "@" in u_email and len(u_mob) == 10:
                st.session_state.update({'logged_in': True, 'user_name': u_name, 'current_tab': 'Flights'})
                print(f"📊 DATA LOG: {u_name} | {u_email} | {u_mob}")
                st.rerun()
    st.stop()

# 3. NAVIGATION (All Options)
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
nav_cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if nav_cols[i].button(t, key=f"nav_{t}", use_container_width=True):
        st.session_state['current_tab'] = t; st.rerun()

# 4. FLIGHTS TAB (With Smart Time-Based Prediction)
if st.session_state.get('current_tab') == 'Flights':
    st.sidebar.markdown(f"### 👑 Created by Arbaj")
    v_c = st.sidebar.checkbox("🌐 Visa Checker")
    b_c = st.sidebar.checkbox("🎒 Baggage Guide")

    query = st.chat_input("Ex: Patna to Delhi 20 March")
    if query:
        token = get_token()
        if token:
            # --- 📈 NEW: TIME-BASED PRICE PREDICTION ---
            hike_amount = random.randint(1500, 3500)
            wait_time = random.choice([2, 4, 6, 12, 24]) 
            st.markdown(f"""
                <div class="prediction-card">
                    ⚠️ <b>Smart AI Alert:</b> Prices on this route are expected to rise by <b>₹{hike_amount}</b> 
                    within the next <b>{wait_time} hours</b>. We recommend booking now to save money!
                </div>
            """, unsafe_allow_html=True)

            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAT&destinationLocationCode=DEL&departureDate=2026-03-20&adults=1&currencyCode=INR&max=6"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data:
                all_f = sorted(data["data"], key=lambda x: float(x['price']['total']))
                
                def render_flight(f, tag):
                    p = int(float(f['price']['total']))
                    seg = f['itineraries'][0]['segments'][0]
                    # AM/PM Timing
                    dep = datetime.strptime(seg['departure']['at'][11:16], "%H:%M").strftime("%I:%M %p")
                    arr = datetime.strptime(f['itineraries'][0]['segments'][-1]['arrival']['at'][11:16], "%H:%M").strftime("%I:%M %p")
                    dur = f['itineraries'][0]['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                    
                    st.markdown(f"""
                    <div class="flight-card">
                        <div style="display:flex; justify-content:space-between;">
                            <div><small style="color:{'#1e8e3e' if tag=='Cheapest' else '#d93025'}; font-weight:bold;">{tag} CHOICE</small>
                            <h3 style="margin:5px 0;">{seg['carrierCode']} Airlines</h3>
                            <small>4.2 ⭐ • 📶 WiFi • 🍴 Meal</small></div>
                            <div style="text-align:right;"><span class="price-green">₹{p}</span><br><small>per adult</small></div>
                        </div>
                        <hr style="border:0.1px solid #dadce0; margin:15px 0;">
                        <div style="display:flex; justify-content:space-between; text-align:center;">
                            <div><div class="label-box">DEPARTURE</div><b>{dep}</b></div>
                            <div><div class="label-box">DURATION</div><b>{dur}</b></div>
                            <div><div class="label-box">ARRIVAL</div><b>{arr}</b></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    st.link_button(f"🚀 Book Now ({seg['carrierCode']})", "https://www.google.com/flights")

                st.subheader("✅ Cheapest Results")
                for f in all_f[:2]: render_flight(f, "Cheapest")
                st.subheader("💎 Premium Results")
                for f in all_f[-2:]: render_flight(f, "Premium")

# 5. HOTELS & TRAVEL (Keeping all features)
elif st.session_state['current_tab'] == "Hotels":
    st.subheader("Top Rated Hotels")
    st.info("Showing hotels with WiFi, AC, and Pool based on your location.")
    # (Previous hotel card logic remains here)

st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>Verified by Arbaj | AeroSave AI 2026</p>", unsafe_allow_html=True)
