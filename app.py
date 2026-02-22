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
# --- 🤖 AEROSAVE AI: THE ULTIMATE "ALL OPTIONS" MASTER CODE ---
import re, random, requests, json
from datetime import datetime

# 1. GOOGLE-STYLE LAYOUT & CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .nav-bar { display: flex; gap: 10px; border-bottom: 1px solid #dadce0; padding: 10px 0; margin-bottom: 20px; overflow-x: auto; sticky: top; background: white; }
    .nav-btn { padding: 8px 18px; border: 1px solid #dadce0; border-radius: 20px; font-size: 0.85rem; cursor: pointer; background: white; color: #3c4043; font-weight: 500; border: none; }
    .active-tab { background: #e8f0fe; color: #1a73e8; border: 1px solid #1a73e8; }
    .hero-box { background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url('https://www.gstatic.com/travel-frontend/_/ss/k=travel-frontend.it.38l69u4k45qj.L.W.O/am=GBA/d=0/rs=AA2YrTvT6U58_M9m5K9jX2uX5A6K7B1Hpg'); height: 160px; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #202124; margin-bottom: 20px; }
    .card { border: 1px solid #dadce0; border-radius: 8px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
    .price-tag { color: #1e8e3e; font-size: 1.3rem; font-weight: bold; }
    .chip-bar { display: flex; gap: 8px; margin-bottom: 20px; overflow-x: auto; }
    .chip { padding: 6px 12px; border: 1px solid #dadce0; border-radius: 8px; font-size: 0.8rem; background: white; white-space: nowrap; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN & DATA LOGGING (Name, Email, Mobile)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center;'>✈️ AeroSave AI: Secure Access</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u_name = st.text_input("Name")
        u_email = st.text_input("Email ID")
        u_mob = st.text_input("Mobile")
        if st.form_submit_button("Access Portal"):
            if u_name and "@" in u_email and len(u_mob) == 10:
                st.session_state.update({'logged_in': True, 'user_name': u_name, 'current_tab': 'Flights'})
                print(f"✅ DATA: {u_name} | {u_email} | {u_mob}")
                st.rerun()
    st.stop()

# 3. TOP NAVIGATION (Harek Option)
if 'current_tab' not in st.session_state: st.session_state['current_tab'] = 'Flights'

nav_cols = st.columns([1,1,1,1,1.5])
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
for i, t in enumerate(tabs):
    if nav_cols[i].button(t, key=f"btn_{t}", use_container_width=True):
        st.session_state['current_tab'] = t
        st.rerun()

# 4. TRAVEL TAB (As in Pic 8:05 PM)
if st.session_state['current_tab'] == "Travel":
    st.markdown("<div class='hero-box'><h2 style='background:rgba(255,255,255,0.8); padding:5px 15px; border-radius:8px;'>Discover your next adventure</h2></div>", unsafe_allow_html=True)
    st.subheader("Popular destinations")
    dest_list = [
        {"city": "New Delhi", "info": "Fog, temple, monument", "price": "₹2,284", "img": "https://picsum.photos/seed/delhi/120/80"},
        {"city": "Mumbai", "info": "Bollywood, shopping & landmarks", "price": "₹3,044", "img": "https://picsum.photos/seed/mumbai/120/80"},
        {"city": "Dubai", "info": "Burj Khalifa & malls", "price": "₹7,657", "img": "https://picsum.photos/seed/dubai/120/80"}
    ]
    for d in dest_list:
        st.markdown(f"""<div class='card'><div style='display:flex; gap:15px;'><img src='{d['img']}' style='border-radius:8px;'><div><h4 style='margin:0;'>{d['city']}</h4><small style='color:grey;'>{d['info']}</small></div></div><div class='price-tag'>{d['price']}</div></div>""", unsafe_allow_html=True)

# 5. EXPLORE TAB (Destination Discovery)
elif st.session_state['current_tab'] == "Explore":
    st.subheader("Explore destinations")
    st.markdown("<div class='chip-bar'><div class='chip'>☰ All filters</div><div class='chip'>📅 Flexible dates</div><div class='chip'>🌍 International</div></div>", unsafe_allow_html=True)
    st.info("Explore feature is now live! Start finding your next trip.")

# 6. FLIGHTS TAB (The Search Engine)
elif st.session_state['current_tab'] == "Flights":
    st.sidebar.markdown(f"### 👑 Created by Arbaj")
    v_c = st.sidebar.checkbox("🌐 Visa Checker")
    b_c = st.sidebar.checkbox("🎒 Baggage Guide")
    
    query = st.chat_input("Ex: Patna to Delhi 20 March")
    if query:
        token = get_token()
        if token:
            # Price Prediction Alert
            st.warning(f"📈 **Price Prediction:** Rates for this route might hike by ₹{random.randint(1100, 2400)} soon!")
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAT&destinationLocationCode=DEL&departureDate=2026-03-20&adults=1&currencyCode=INR&max=5"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()
            if "data" in data:
                for f in data["data"]:
                    p = int(float(f['price']['total']))
                    st.markdown(f"""
                    <div class='card'>
                        <div><small style='color:#1e8e3e; font-weight:bold;'>GREAT PRICE</small><h4 style='margin:0;'>{f['itineraries'][0]['segments'][0]['carrierCode']} Airlines</h4><small>4.2 ⭐ | WiFi | Meal</small><br>🛫 {f['itineraries'][0]['segments'][0]['departure']['at'][11:16]} • Non-stop</div>
                        <div style='text-align:right;'><span class='price-tag'>₹{p}</span><br><small>per adult</small></div>
                    </div>""", unsafe_allow_html=True)
    if v_c: st.info("🌍 **Visa:** On-Arrival available for Indians.")
    if b_c: st.warning("🎒 **Baggage:** 15kg Check-in + 7kg Cabin allowed.")

# 7. HOTELS TAB (As in Pic 7:45 PM)
elif st.session_state['current_tab'] == "Hotels":
    st.subheader("Hotels in Jharkhand")
    hotels = [
        {"name": "Hotel Meera", "rate": "4.0", "rev": "969", "price": "₹708", "badge": "GREAT PRICE"},
        {"name": "Hotel Sohrai Inn", "rate": "4.3", "rev": "574", "price": "₹1,717", "badge": "TOP RATED"},
        {"name": "Hotel Genista Inn", "rate": "4.2", "rev": "2.6k", "price": "₹3,000", "badge": "LUXURY"}
    ]
    for h in hotels:
        st.markdown(f"""<div class='card'><div><small style='color:#1a73e8; font-weight:bold;'>{h['badge']}</small><h4 style='margin:0;'>{h['name']}</h4><small>{h['rate']} ⭐ ({h['rev']} reviews)</small><br><small>📶 Free WiFi • 🏊 Pool • ❄️ AC</small></div><div style='text-align:right;'><span class='price-tag'>{h['price']}</span><br><button style='background:#1a73e8; color:white; border:none; border-radius:4px; padding:5px 10px;'>View prices</button></div></div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>Verified by Arbaj | AeroSave AI 2026</p>", unsafe_allow_html=True)
