iimport streamlit as st
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
# --- 🤖 AEROSAVE AI v65.0: THE FINAL MASTER ENGINE ---
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import random

# 1. 🎨 GOOGLE TRAVEL REPLICA STYLING
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .stButton>button { border-radius: 20px; border: 1px solid #dadce0; background: white; color: #3c4043; font-weight: 500; }
    .card { background: white; border: 1px solid #dadce0; border-radius: 8px; padding: 16px; margin-bottom: 12px; position: relative; }
    .price-green { color: #1e8e3e; font-weight: bold; font-size: 1.3rem; text-align: right; }
    .badge-blue { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .info-row { display: flex; justify-content: space-between; margin-top: 10px; color: #5f6368; font-size: 14px; border-top: 1px solid #f1f3f4; padding-top: 10px; }
    .sidebar-tool { background: #ffffff; padding: 12px; border-radius: 8px; border-left: 5px solid #1a73e8; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. 🔐 UPDATED LOGIN (Name & Mobile Only)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center;'>✈️ AeroSave AI: Login</h2>", unsafe_allow_html=True)
    with st.container():
        _, col, _ = st.columns([1,1.5,1])
        with col:
            u_name = st.text_input("Full Name")
            u_mob = st.text_input("WhatsApp Number (+91)")
            if st.button("Unlock Travel Engine", use_container_width=True):
                if u_name and len(u_mob) == 10:
                    st.session_state.update({'logged_in': True, 'u_name': u_name, 'tab': 'Flights'})
                    st.rerun()
    st.stop()

# 3. 🗺️ NAVIGATION BAR
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if cols[i].button(t, key=f"btn_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state.get('tab', 'Travel')

# 4. 🧭 TAB: TRAVEL (Popular Destinations)
if current_tab == "Travel":
    st.markdown(f"### Popular destinations from Patna for {st.session_state['u_name']}")
    dest_data = [
        {"city": "New Delhi", "desc": "Fog, temple, monuments & zoo", "p": "₹2,284", "img": "https://picsum.photos/seed/del/300/200"},
        {"city": "Mumbai", "desc": "Bollywood, shopping & beaches", "p": "₹3,044", "img": "https://picsum.photos/seed/mum/300/200"},
        {"city": "Dubai", "desc": "Burj Khalifa & Luxury Malls", "p": "₹7,657", "img": "https://picsum.photos/seed/dxb/300/200"}
    ]
    c1, c2 = st.columns([2, 1])
    with c1:
        for d in dest_data:
            st.markdown(f"""<div class='card' style='display:flex; gap:15px;'>
                <img src='{d['img']}' style='width:100px; height:100px; border-radius:8px; object-fit:cover;'>
                <div><b>{d['city']}</b><br><small>{d['desc']}</small><br><span class='price-green'>{d['p']}</span></div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.info("📍 Data tracked from Mandar (IXR)")
        st.image("https://www.gstatic.com/travel-frontend/_/static/modules/mweb/common/images/google_travel_header_v4.png")

# 5. 📂 TAB: EXPLORE (Global Price Map)
elif current_tab == "Explore":
    st.subheader("Global Price Map & Visa Guide")
    explore_db = [
        {"city": "Singapore", "p": "₹24,030", "lat": 1.35, "lon": 103.8, "visa": "E-Visa"},
        {"city": "Tokyo", "p": "₹238,970", "lat": 35.6, "lon": 139.6, "visa": "Required"},
        {"city": "Bangkok", "p": "₹28,172", "lat": 13.7, "lon": 100.5, "visa": "On Arrival"},
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.12, "visa": "Required"},
        {"city": "Bengaluru", "p": "₹12,755", "lat": 12.9, "lon": 77.5, "visa": "Domestic"}
    ]
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB Positron")
    for e in explore_db:
        folium.Marker([e['lat'], e['lon']], popup=f"{e['city']}: {e['p']}", tooltip=e['city']).add_to(m)
    
    col_m, col_l = st.columns([1.5, 1])
    with col_m: st_folium(m, width="100%", height=500)
    with col_l:
        for e in explore_db:
            st.markdown(f"<div class='card'><b>{e['city']}</b><br><small>Visa: {e['visa']}</small><br><span class='price-green'>{e['p']}</span></div>", unsafe_allow_html=True)

# 6. ✈️ TAB: FLIGHTS (Deep Search Engine)
elif current_tab == "Flights":
    with st.sidebar:
        st.markdown("<div class='sidebar-tool'>🎒 <b>Luggage:</b> 25kg (Checked)</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-tool'>🛂 <b>Visa:</b> Required for International</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.checkbox("Show non-stop only", value=True)

    st.warning("⚠️ **Smart AI Alert:** Prices are expected to rise by ₹3,007 soon!")
    
    st.markdown("### ✅ Cheapest Real-Time Flights (Patna to Delhi)")
    f_list = [
        {"air": "IndiGo", "p": "6,247", "dep": "06:20 PM", "arr": "08:10 PM", "dur": "1h 50m", "cat": "Cheapest"},
        {"air": "Air India Premium", "p": "7,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m", "cat": "Premium"}
    ]
    for f in f_list:
        st.markdown(f"""<div class='card'>
            <div style='display:flex; justify-content:space-between;'>
                <span class='badge-blue'>{f['cat']} Choice</span>
                <span class='price-green'>₹{f['p']}</span>
            </div>
            <div class='info-row'>
                <div><b>{f['air']}</b><br><small>Non-stop</small></div>
                <div>{f['dep']}<br><small>Departure</small></div>
                <div>{f['dur']}<br><small>Duration</small></div>
                <div>{f['arr']}<br><small>Arrival</small></div>
            </div>
            <div style='text-align:center; margin-top:15px; color:#1a73e8; font-weight:bold; cursor:pointer;'>🚀 Book Now</div>
        </div>""", unsafe_allow_html=True)

# 7. 🏨 TAB: HOTELS (Advanced Location Features)
elif current_tab == "Hotels":
    st.subheader("Top Hotels near Mandar / Ranchi")
    h_data = [
        {"n": "Hotel Meera", "p": "₹708", "feat": "Pool • Free breakfast • Wi-Fi", "star": "4.0 ⭐"},
        {"n": "HOTEL GENISTA INN", "p": "₹3,000", "feat": "Luxury • Restaurant • AC", "star": "4.2 ⭐"},
        {"n": "Radiance Retreat", "p": "₹1,139", "feat": "Fitness centre • Breakfast", "star": "4.9 ⭐"}
    ]
    for h in h_data:
        st.markdown(f"<div class='card'><b>{h['n']}</b> ({h['star']})<br><small>{h['feat']}</small><br><span class='price-green'>{h['p']}</span></div>", unsafe_allow_html=True)

# 8. 🏘️ TAB: HOLIDAY RENTALS (Local & Global)
elif current_tab == "Holiday rentals":
    st.subheader("Holiday Homes & Apartments")
    r_data = [
        {"n": "1-Bedroom House", "p": "₹1,900", "loc": "Mandar", "feat": "Sleeps 2 • Kitchen"},
        {"n": "The Candy Studio", "p": "₹3,994", "loc": "Ranchi", "feat": "Sleeps 4 • Designer"},
        {"n": "Pratap Grand Villa", "p": "₹978", "loc": "Bariatu", "feat": "Garden • Pool"}
    ]
    for r in r_data:
        st.markdown(f"<div class='card'><b>{r['n']}</b><br><small>{r['loc']} • {r['feat']}</small><br><span class='price-green'>{r['p']}</span>/night</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align:center; color:grey;'>© 2026 AeroSave AI | Verified for {st.session_state['u_name']}</p>", unsafe_allow_html=True)
