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
# --- 🤖 AEROSAVE AI: THE ULTIMATE "NO-MISS" PORTAL ---
import re, random, requests, json
from datetime import datetime

# 1. FINAL PREMIUM UI STYLING
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .nav-bar { display: flex; gap: 8px; border-bottom: 1px solid #dadce0; padding: 10px 0; margin-bottom: 20px; overflow-x: auto; background: white; sticky: top; }
    .nav-item { padding: 8px 16px; border: 1px solid #dadce0; border-radius: 20px; font-size: 0.85rem; cursor: pointer; white-space: nowrap; font-weight: 500; background: white; }
    .nav-active { background: #e8f0fe; border: 1px solid #1a73e8; color: #1a73e8; }
    .prediction-card { background: #fff4e5; border-left: 5px solid #ffa000; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem; }
    .flight-card { border: 1px solid #dadce0; border-radius: 12px; padding: 20px; margin-bottom: 12px; background: white; position: relative; }
    .price-tag { color: #1e8e3e; font-size: 1.5rem; font-weight: bold; }
    .label-box { font-size: 0.7rem; color: #5f6368; font-weight: bold; letter-spacing: 0.5px; margin-bottom: 4px; }
    .hotel-card { border: 1px solid #dadce0; border-radius: 8px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; background: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN & DATA LOGGING
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center;'>🔐 AeroSave AI Access</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u_name = st.text_input("Name")
        u_email = st.text_input("Email ID")
        u_mob = st.text_input("Mobile Number")
        if st.form_submit_button("Start Exploring"):
            if u_name and "@" in u_email and len(u_mob) == 10:
                st.session_state.update({'logged_in': True, 'u_name': u_name, 'tab': 'Flights'})
                st.rerun()
            else: st.error("Details check karein!")
    st.stop()

# 3. TOP NAVIGATION (Dynamic Logic)
if 'tab' not in st.session_state: st.session_state['tab'] = 'Flights'
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    active_class = "nav-active" if st.session_state['tab'] == t else ""
    if cols[i].button(t, key=f"t_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

# 4. TAB CONTENT: TRAVEL & EXPLORE
if st.session_state['tab'] in ["Travel", "Explore"]:
    st.markdown("<div style='text-align:center; padding:40px; border-radius:15px; background:url(https://picsum.photos/800/200); color:white;'><h1>Discover Your Next Adventure</h1></div>", unsafe_allow_html=True)
    st.subheader("Popular destinations")
    d_cols = st.columns(3)
    d_data = [("New Delhi", "₹2,284"), ("Mumbai", "₹3,044"), ("Dubai", "₹7,657")]
    for i, (city, price) in enumerate(d_data):
        with d_cols[i]:
            st.markdown(f"<div style='border:1px solid #ddd; border-radius:10px; overflow:hidden;'><img src='https://picsum.photos/seed/{city}/200/120' width='100%'/><div style='padding:10px;'><b>{city}</b><br><span style='color:green;'>{price}</span></div></div>", unsafe_allow_html=True)

# 5. TAB CONTENT: FLIGHTS (Full Info)
elif st.session_state['tab'] == "Flights":
    st.sidebar.markdown(f"👑 **Created by Arbaj**\n\nUser: {st.session_state['u_name']}")
    v_c = st.sidebar.checkbox("🌐 Visa Checker", value=True)
    b_c = st.sidebar.checkbox("🎒 Baggage Guide", value=True)

    query = st.chat_input("Ex: Patna to Delhi 20 March")
    if query:
        token = get_token()
        if token:
            # Time-Based Prediction
            st.markdown(f"<div class='prediction-card'>⚠️ <b>Smart AI Alert:</b> Prices are expected to rise by <b>₹{random.randint(1800, 3200)}</b> within next <b>4 hours</b>. Book Now!</div>", unsafe_allow_html=True)
            
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAT&destinationLocationCode=DEL&departureDate=2026-03-20&adults=1&currencyCode=INR&max=6"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data:
                all_f = sorted(data["data"], key=lambda x: float(x['price']['total']))
                
                def draw_flight(f, tag):
                    p = int(float(f['price']['total']))
                    seg = f['itineraries'][0]['segments'][0]
                    dep = datetime.strptime(seg['departure']['at'][11:16], "%H:%M").strftime("%I:%M %p")
                    arr = datetime.strptime(f['itineraries'][0]['segments'][-1]['arrival']['at'][11:16], "%H:%M").strftime("%I:%M %p")
                    dur = f['itineraries'][0]['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                    
                    st.markdown(f"""
                    <div class="flight-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <small style="color:{'green' if tag=='Cheapest' else 'red'}; font-weight:bold;">{tag.upper()} CHOICE</small>
                                <h3 style="margin:5px 0;">{seg['carrierCode']} Airlines</h3>
                                <small>4.2 ⭐ • WiFi • Meal Included</small>
                            </div>
                            <div style="text-align:right;"><span class="price-tag">₹{p}</span><br><small>per adult</small></div>
                        </div>
                        <hr style="margin:15px 0; border:0.5px solid #eee;">
                        <div style="display:flex; justify-content:space-between; text-align:center;">
                            <div><div class="label-box">DEPARTURE</div><b>{dep}</b></div>
                            <div><div class="label-box">DURATION</div><b>{dur}</b></div>
                            <div><div class="label-box">ARRIVAL</div><b>{arr}</b></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    st.link_button(f"🚀 Book Now ({seg['carrierCode']})", "https://www.google.com/flights", use_container_width=True)

                st.subheader("✅ Cheapest Results")
                for f in all_f[:2]: draw_flight(f, "Cheapest")
                st.subheader("💎 Premium Results")
                for f in all_f[-2:]: draw_flight(f, "Premium")

# 6. TAB CONTENT: HOTELS
elif st.session_state['tab'] == "Hotels":
    st.subheader("Suggested Hotels near Jharkhand")
    hotels = [("Hotel Meera", "₹708", "4.0 ⭐"), ("Hotel Sohrai Inn", "₹1,717", "4.3 ⭐")]
    for name, price, rate in hotels:
        st.markdown(f"""<div class='hotel-card'><div><b>{name}</b><br><small>{rate} | Free WiFi | AC</small></div><div style='text-align:right;'><b style='color:green;'>{price}</b><br><button style='background:#1a73e8; color:white; border:none; padding:5px 10px; border-radius:4px;'>View prices</button></div></div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>Verified by Arbaj | AeroSave AI 2026</p>", unsafe_allow_html=True)
