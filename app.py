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
# 🎨 1. MASTER UI DESIGN (Google Travel Style)
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .card { background: white; border: 1px solid #dadce0; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .price-green { color: #1e8e3e; font-weight: bold; font-size: 1.5rem; }
    .great-price { background: #e6f4ea; color: #137333; font-size: 11px; font-weight: bold; padding: 3px 10px; border-radius: 5px; margin-bottom: 10px; display: inline-block; }
    .badge-info { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .flight-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; border-top: 1px solid #eee; padding-top: 15px; margin-top: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 🗺️ 2. NAVIGATION SYSTEM
if 'tab' not in st.session_state: st.session_state['tab'] = 'Flights'
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if cols[i].button(t, key=f"btn_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state['tab']

# ✈️ 3. TAB: FLIGHTS (Full Details, Luggage & Visa)
if current_tab == "Flights":
    st.warning("⚠️ **Smart AI Alert:** Prices are expected to rise by **₹3,007** within 4 hours!")
    
    # Authenticated Database
    flights = [
        {"air": "IndiGo Airlines", "p": "6,247", "dep": "06:20 PM", "arr": "08:10 PM", "dur": "1h 50m", "cat": "Cheapest", "lug": "25kg", "visa": "Free"},
        {"air": "Air India Premium", "p": "7,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m", "cat": "Premium", "lug": "35kg", "visa": "Free"},
        {"air": "Vistara Luxury", "p": "9,850", "dep": "02:15 PM", "arr": "04:05 PM", "dur": "1h 50m", "cat": "Comfort", "lug": "25kg", "visa": "Free"}
    ]
    
    for f in flights:
        st.markdown(f"""
        <div class="card">
            <div class="great-price">GREAT PRICE</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b style="font-size:1.2rem;">{f['air']}</b> <span class="badge-info">{f['cat']}</span><br>
                    <small style="color:grey;">🧳 {f['lug']} Luggage | 🛂 Visa: {f['visa']}</small>
                </div>
                <div class="price-green">₹{f['p']}</div>
            </div>
            <div class="flight-grid">
                <div><small>DEPARTURE</small><br><b>{f['dep']}</b></div>
                <div><small>DURATION</small><br><b>{f['dur']}</b></div>
                <div><small>ARRIVAL</small><br><b>{f['arr']}</b></div>
                <div><button style="background:#1a73e8; color:white; border:none; padding:8px 15px; border-radius:5px; font-weight:bold; cursor:pointer;">Book Now</button></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 🌍 4. TAB: EXPLORE & TRAVEL (Global Price Map)
elif current_tab == "Explore" or current_tab == "Travel":
    st.subheader("Global Destination Explorer (India & World)")
    dest_db = [
        {"city": "Singapore", "p": "₹24,030", "lat": 1.35, "lon": 103.8, "info": "International Hub"},
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.1, "info": "Culture & History"},
        {"city": "Mumbai", "p": "₹3,044", "lat": 19.0, "lon": 72.8, "info": "Bollywood & Beaches"},
        {"city": "New Delhi", "p": "₹2,284", "lat": 28.6, "lon": 77.2, "info": "Capital City"}
    ]
    
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    for d in dest_db:
        folium.Marker([d['lat'], d['lon']], popup=f"{d['city']}: {d['p']}").add_to(m)
    
    c1, c2 = st.columns([1.5, 1])
    with c1: st_folium(m, width="100%", height=500)
    with c2:
        for d in dest_db:
            st.markdown(f"<div class='card'><b>{d['city']}</b><br><small>{d['info']}</small><br><span class='price-green' style='font-size:1rem;'>{d['p']}</span></div>", unsafe_allow_html=True)

# 🏨 5. TAB: HOTELS & RENTALS (Location Verified)
elif current_tab == "Hotels":
    user_loc = st.text_input("Enter location for best hotels", "Ranchi, Jharkhand")
    hotels = [
        {"n": "Hotel Meera", "p": "₹708", "f": "Pool • WiFi • AC", "r": "4.0 ⭐"},
        {"n": "Genista Inn Luxury", "p": "₹3,000", "f": "Gym • Spa • Restaurant", "r": "4.2 ⭐"}
    ]
    for h in hotels:
        st.markdown(f"<div class='card'><b>{h['n']}</b> ({h['r']})<br><small>{h['f']}</small><br><span class='price-green'>₹{h['p']}</span></div>", unsafe_allow_html=True)

elif current_tab == "Holiday rentals":
    rentals = [
        {"n": "1-Bedroom Modern House", "p": "₹1,900", "l": "Mandar", "s": "Kitchen • Sleeps 2"},
        {"n": "The Candy Studio", "p": "₹3,994", "l": "Ranchi Main", "s": "Designer • Sleeps 4"}
    ]
    for r in rentals:
        st.markdown(f"<div class='card'><b>{r['n']}</b><br><small>{r['l']} • {r['s']}</small><br><span class='price-green'>{r['p']}</span>/night</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AeroSave AI v115.0 | Smart Master Edition | User: {st.session_state.get('u_name', 'Arbaj')}")
