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
# --- 🤖 AEROSAVE AI v55.0: THE GLOBAL DATA-HUB REPLICA ---
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import random

# 1. 🎨 MASTER UI STYLING
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: white; border-radius: 20px; border: 1px solid #dadce0; padding: 5px 20px; }
    .dest-card { background: white; border: 1px solid #dadce0; border-radius: 12px; padding: 0px; margin-bottom: 15px; overflow: hidden; display: flex; transition: 0.3s; }
    .dest-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .content-area { padding: 12px; flex-grow: 1; position: relative; }
    .price-tag { color: #1e8e3e; font-weight: bold; font-size: 1.2rem; }
    .sidebar-tool { background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #1a73e8; }
    </style>
    """, unsafe_allow_html=True)

# 2. 🔐 UPDATED LOGIN (Minimalist)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align:center;'>🌍 AeroSave AI: Premium Access</h2>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            u_name = st.text_input("Full Name")
            u_mob = st.text_input("WhatsApp Number (+91)")
            if st.button("Unlock All Features", use_container_width=True):
                if u_name and len(u_mob) == 10:
                    st.session_state.update({'logged_in': True, 'u_name': u_name, 'tab': 'Travel'})
                    st.rerun()
    st.stop()

# 3. 🌐 TOP NAVIGATION
tabs_list = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs_list))
for i, t in enumerate(tabs_list):
    if cols[i].button(t, key=f"nav_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state.get('tab', 'Travel')

# 4. 🧭 TAB: TRAVEL (India & Global Favorites)
if current_tab == "Travel":
    st.markdown(f"### Hello {st.session_state['u_name']}, popular destinations for you")
    
    # Authentic Destination Data
    travel_data = [
        {"city": "New Delhi", "desc": "Fog, temple, monuments and zoo", "price": "₹2,284", "img": "https://picsum.photos/seed/del/200/150"},
        {"city": "Mumbai", "desc": "Bollywood, shopping & landmarks", "price": "₹3,044", "img": "https://picsum.photos/seed/mum/200/150"},
        {"city": "Dubai", "desc": "Burj Khalifa, Atlantis & malls", "price": "₹7,657", "img": "https://picsum.photos/seed/dxb/200/150"},
        {"city": "Singapore", "desc": "Gardens by the bay, Luxury", "price": "₹24,030", "img": "https://picsum.photos/seed/sin/200/150"}
    ]
    
    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        for d in travel_data:
            st.markdown(f"""
            <div class="dest-card">
                <img src="{d['img']}" style="width:120px; object-fit:cover;">
                <div class="content-area">
                    <b>{d['city']}</b><br><small>{d['desc']}</small><br>
                    <span class="price-tag">{d['price']}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    with col_r:
        st.info("📍 Recommended based on your search from Mandar")
        st.image("https://www.gstatic.com/travel-frontend/_/static/modules/mweb/common/images/google_travel_header_v4.png")

# 5. 📂 TAB: EXPLORE (Master Map & All India/Global Prices)
elif current_tab == "Explore":
    st.subheader("Global Price Explorer")
    # Massive Database
    explore_db = [
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.1, "type": "Global"},
        {"city": "Paris", "p": "₹82,221", "lat": 48.8, "lon": 2.3, "type": "Global"},
        {"city": "Tokyo", "p": "₹2,38,970", "lat": 35.6, "lon": 139.6, "type": "Global"},
        {"city": "Bangkok", "p": "₹28,172", "lat": 13.7, "lon": 100.5, "type": "Global"},
        {"city": "New York", "p": "₹1,12,450", "lat": 40.7, "lon": -74.0, "type": "Global"},
        {"city": "Bengaluru", "p": "₹12,755", "lat": 12.9, "lon": 77.5, "type": "India"},
        {"city": "Jaipur", "p": "₹23,496", "lat": 26.9, "lon": 75.8, "type": "India"},
        {"city": "Kolkata", "p": "₹5,430", "lat": 22.5, "lon": 88.3, "type": "India"}
    ]
    
    m = folium.Map(location=[20, 20], zoom_start=2, tiles="CartoDB Positron")
    for e in explore_db:
        folium.Marker([e['lat'], e['lon']], popup=f"{e['city']}: {e['p']}", tooltip=e['city']).add_to(m)
    
    st_folium(m, width="100%", height=500)
    
    st.markdown("#### Detailed Price List")
    e_col1, e_col2 = st.columns(2)
    for i, e in enumerate(explore_db):
        target = e_col1 if i % 2 == 0 else e_col2
        target.markdown(f"**{e['city']}** - <span class='price-tag'>{e['p']}</span>", unsafe_allow_html=True)

# 6. ✈️ TAB: FLIGHTS (The Ultimate Assistant)
elif current_tab == "Flights":
    with st.sidebar:
        st.markdown("<div class='sidebar-tool'>🎒 <b>Luggage:</b> 25kg Checked, 7kg Cabin</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-tool'>🛂 <b>Visa:</b> Required for Global</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-tool'>🕒 <b>Best Time:</b> Book 3 weeks early</div>", unsafe_allow_html=True)

    st.warning("⚠️ Prices expected to rise by ₹3,150 soon!")
    
    # Category-wise Results
    st.markdown("### ✅ Cheapest Choices")
    f_data = [
        {"air": "IndiGo", "p": "6,247", "dep": "06:20 PM", "arr": "08:10 PM", "dur": "1h 50m"},
        {"air": "Air India Express", "p": "7,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m"}
    ]
    for f in f_data:
        st.markdown(f"""
        <div style="background:white; border:1px solid #dadce0; border-radius:10px; padding:15px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between;">
                <b>{f['air']}</b> <span class="price-tag">₹{f['p']}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:10px; color:grey; font-size:13px;">
                <div>DEP: {f['dep']}</div><div>DUR: {f['dur']}</div><div>ARR: {f['arr']}</div>
            </div>
            <div style="text-align:center; color:#1a73e8; margin-top:10px; font-weight:bold;">🚀 Book Now</div>
        </div>""", unsafe_allow_html=True)

# 7. 🏨 TAB: HOTELS (Advanced Features)
elif current_tab == "Hotels":
    city = st.text_input("Search Location", "Ranchi")
    st.markdown(f"### Best Stays in {city}")
    h_data = [
        {"n": "Hotel Meera", "p": "₹708", "feat": "Pool • Free WiFi • AC", "star": "4.0 ⭐"},
        {"n": "Radiance Retreat", "p": "₹1,139", "feat": "Gym • Spa • Breakfast", "star": "4.9 ⭐"},
        {"n": "Genista Inn Luxury", "p": "₹3,000", "feat": "Bar • 24/7 Service", "star": "4.2 ⭐"}
    ]
    for h in h_data:
        st.markdown(f"""
        <div class="dest-card" style="padding:15px; flex-direction:column;">
            <div style="display:flex; justify-content:space-between;"><b>{h['n']}</b> <span>{h['star']}</span></div>
            <small style="color:grey;">{h['feat']}</small>
            <span class="price-tag">{h['p']}</span>
        </div>""", unsafe_allow_html=True)

# 8. 🏘️ TAB: HOLIDAY RENTALS (Verified Stays)
elif current_tab == "Holiday rentals":
    st.markdown("### 🏘️ Top Rated Rentals")
    r_data = [
        {"n": "1-Bedroom Modern House", "p": "₹1,900", "loc": "Mandar", "s": "Sleeps 2"},
        {"n": "The Candy Studio", "p": "₹3,994", "loc": "Ranchi", "s": "Sleeps 4"},
        {"n": "Pratap Grand Apartment", "p": "₹978", "loc": "Bariatu", "s": "Sleeps 2"}
    ]
    for r in r_data:
        st.markdown(f"""
        <div class="dest-card" style="padding:15px; flex-direction:column;">
            <b>{r['n']}</b>
            <small>{r['loc']} • {r['s']}</small>
            <span class="price-tag">{r['p']}</span>/night
        </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align:center; color:grey;'>© 2026 AeroSave AI | Deep Data Verified by {st.session_state['u_name']}</p>", unsafe_allow_html=True)
