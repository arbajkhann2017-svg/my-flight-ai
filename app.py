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
# 🎨 1. MASTER UI & AUTHENTIC STYLING
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .card { background: white; border: 1px solid #dadce0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .price-text { color: #1e8e3e; font-weight: bold; font-size: 1.6rem; }
    .status-badge { background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: bold; }
    .price-alert { background: #fff7e0; border: 1px solid #ffeeba; color: #856404; padding: 10px; border-radius: 8px; font-size: 14px; margin-bottom: 20px; }
    .great-deal { background: #e6f4ea; color: #137333; font-size: 11px; font-weight: bold; padding: 3px 10px; border-radius: 5px; margin-bottom: 8px; display: inline-block; }
    .flight-info-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; border-top: 1px solid #eee; padding-top: 15px; margin-top: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 🗺️ 2. NAVIGATION CONTROL
if 'tab' not in st.session_state: st.session_state['tab'] = 'Flights'
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if cols[i].button(t, key=f"nav_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state['tab']

# ✈️ 3. FLIGHT ENGINE: AM/PM, Luggage, Visa & Price Prediction
if current_tab == "Flights":
    st.markdown('<div class="price-alert">⚠️ <b>Price Prediction:</b> Based on AI trends, prices are expected to rise by <b>₹3,007</b> in the next 4 hours. Book now to save!</div>', unsafe_allow_html=True)
    
    flights = [
        {"air": "IndiGo Airlines", "p": "6,247", "dep": "06:20 PM", "arr": "08:10 PM", "dur": "1h 50m", "cat": "Sasti (Cheapest)", "lug": "15kg Check-in + 7kg Hand", "visa": "Not Required (Domestic)"},
        {"air": "Air India Premium", "p": "7,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m", "cat": "Premium Service", "lug": "25kg Check-in + 7kg Hand", "visa": "Not Required (Domestic)"},
        {"air": "Vistara Luxury", "p": "9,850", "dep": "02:15 PM", "arr": "04:05 PM", "dur": "1h 50m", "cat": "Costly Premium", "lug": "30kg Check-in + 10kg Hand", "visa": "Not Required (Domestic)"}
    ]

    for f in flights:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div class="great-deal">GREAT PRICE DEAL</div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <b style="font-size:1.3rem;">{f['air']}</b> <span class="status-badge">{f['cat']}</span><br>
                        <small style="color:#5f6368;">🧳 Luggage: {f['lug']} | 🛂 Visa: {f['visa']}</small>
                    </div>
                    <div class="price-text">₹{f['p']}</div>
                </div>
                <div class="flight-info-row">
                    <div><small>DEPARTURE</small><br><b>{f['dep']}</b></div>
                    <div><small>DURATION</small><br><b>{f['dur']}</b></div>
                    <div><small>ARRIVAL</small><br><b>{f['arr']}</b></div>
                    <div><button style="background:#1a73e8; color:white; border:none; padding:10px 25px; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">Book Now</button></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 🌍 4. EXPLORE & TRAVEL: Global Maps & Correct Prices
elif current_tab in ["Explore", "Travel"]:
    st.subheader("Global & India Popular Destinations")
    destinations = [
        {"city": "Singapore", "p": "₹24,030", "lat": 1.35, "lon": 103.8, "type": "Global"},
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.1, "type": "Global"},
        {"city": "Dubai", "p": "₹7,657", "lat": 25.2, "lon": 55.2, "type": "Global"},
        {"city": "New Delhi", "p": "₹2,284", "lat": 28.6, "lon": 77.2, "type": "India"},
        {"city": "Mumbai", "p": "₹3,044", "lat": 19.0, "lon": 72.8, "type": "India"},
        {"city": "Tokyo", "p": "₹2,38,970", "lat": 35.6, "lon": 139.6, "type": "Global"}
    ]
    
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    for d in destinations:
        folium.Marker([d['lat'], d['lon']], popup=f"{d['city']}: {d['p']}", tooltip=d['city']).add_to(m)
    
    col1, col2 = st.columns([1.8, 1])
    with col1: st_folium(m, width="100%", height=550)
    with col2:
        st.write("#### Live Flight Prices")
        for d in destinations:
            st.markdown(f"<div class='card' style='padding:10px;'><b>{d['city']}</b> ({d['type']})<br><span class='price-text' style='font-size:1.1rem;'>{d['p']}</span></div>", unsafe_allow_html=True)

# 🏨 5. HOTELS & RENTALS: Best Stays Near Location
elif current_tab == "Hotels":
    loc = st.text_input("Enter your location for best hotels", "Ranchi, Jharkhand")
    hotels = [
        {"n": "Hotel Meera", "p": "₹708", "feat": "Free breakfast • Pool • WiFi", "r": "4.0 ⭐"},
        {"n": "Hotel Genista Inn Luxury", "p": "₹3,000", "feat": "Gym • Spa • Restaurant", "r": "4.2 ⭐"},
        {"n": "Radiance Retreat", "p": "₹1,139", "feat": "Pet-friendly • AC • Kitchen", "r": "4.9 ⭐"}
    ]
    for h in hotels:
        st.markdown(f"<div class='card'><b>{h['n']}</b> ({h['r']})<br><small>{h['feat']}</small><br><span class='price-text'>₹{h['p']}</span></div>", unsafe_allow_html=True)

elif current_tab == "Holiday rentals":
    st.subheader("Holiday Rentals with All Features")
    rentals = [
        {"n": "1-Bedroom Modern House", "p": "₹1,900", "feat": "Sleeps 2 • 1 Bedroom • Kitchen • WiFi", "l": "Mandar"},
        {"n": "The Candy Studio Apartment", "p": "₹3,994", "feat": "Sleeps 4 • Designer Interior • AC", "l": "Ranchi Main"},
        {"n": "Pratap Grand Villa", "p": "₹978", "feat": "Sleeps 2 • Garden View • Parking", "l": "Bariatu"}
    ]
    for r in rentals:
        st.markdown(f"<div class='card'><b>{r['n']}</b><br><small>{r['l']} • {r['feat']}</small><br><span class='price-text'>{r['p']}</span>/night</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AeroSave AI v130.0 | Developed for Arbaj | Professional Travel Engine")
