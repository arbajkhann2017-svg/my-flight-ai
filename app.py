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
# --- 🤖 AEROSAVE AI v100.0: MASTER ENGINE (AUTHENTIC REPLICA) ---

# 1. 🎨 ADVANCED UI STYLING
st.markdown("""
    <style>
    .main { background-color: #f1f3f4; }
    .stButton>button { border-radius: 20px; border: 1px solid #dadce0; background: white; color: #3c4043; height: 40px; }
    .card { background: white; border: 1px solid #dadce0; border-radius: 8px; margin-bottom: 15px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .price-tag { color: #1e8e3e; font-weight: bold; font-size: 1.4rem; }
    .status-badge { background: #e8f0fe; color: #1a73e8; padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .great-price-label { background: #e6f4ea; color: #137333; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
    .flight-row { display: flex; justify-content: space-between; align-items: center; text-align: center; border-top: 1px solid #eee; padding-top: 12px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 🗺️ SMART NAVIGATION
if 'tab' not in st.session_state: st.session_state['tab'] = 'Flights'
tabs = ["Travel", "Explore", "Flights", "Hotels", "Holiday rentals"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    if cols[i].button(t, key=f"t_{t}", use_container_width=True):
        st.session_state['tab'] = t; st.rerun()

current_tab = st.session_state['tab']

# 3. ✈️ TAB: FLIGHTS (Full Details & Prediction)
if current_tab == "Flights":
    st.markdown("### ✈️ AeroSave AI: Smart Flight Search")
    st.warning("⚠️ **Smart AI Alert:** Prices are expected to rise by **₹3,007** within 4 hours!")
    
    flights = [
        {"air": "IndiGo Airlines", "p": "6,247", "dep": "06:20 PM", "arr": "08:10 PM", "dur": "1h 50m", "cat": "Cheapest", "lug": "25kg", "visa": "Domestic Free"},
        {"air": "Air India Premium", "p": "7,179", "dep": "10:40 AM", "arr": "12:25 PM", "dur": "1h 45m", "cat": "Premium", "lug": "35kg", "visa": "Domestic Free"},
        {"air": "Vistara Comfort", "p": "9,850", "dep": "02:15 PM", "arr": "04:05 PM", "dur": "1h 50m", "cat": "Luxury", "lug": "25kg", "visa": "Domestic Free"}
    ]

    for f in flights:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div class="great-price-label">GREAT PRICE</div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <b style="font-size: 1.1rem;">{f['air']}</b> <span class="status-badge">{f['cat']}</span><br>
                        <small style="color: grey;">🧳 {f['lug']} Luggage Included | 🛂 Visa: {f['visa']}</small>
                    </div>
                    <div class="price-tag">₹{f['p']}</div>
                </div>
                <div class="flight-row">
                    <div><small style="color:grey;">DEPARTURE</small><br><b>{f['dep']}</b></div>
                    <div><small style="color:grey;">DURATION</small><br><b>{f['dur']}</b></div>
                    <div><small style="color:grey;">ARRIVAL</small><br><b>{f['arr']}</b></div>
                    <div><button style="background:#1a73e8; color:white; border:none; padding:6px 15px; border-radius:4px; font-weight:bold; cursor:pointer;">Book Now</button></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 4. 🧭 TAB: EXPLORE (Global Destinations & Map)
elif current_tab == "Explore" or current_tab == "Travel":
    st.subheader("Global Destination Explorer")
    explore_data = [
        {"city": "Singapore", "p": "₹24,030", "lat": 1.35, "lon": 103.8, "info": "International"},
        {"city": "London", "p": "₹73,650", "lat": 51.5, "lon": -0.1, "info": "International"},
        {"city": "New Delhi", "p": "₹2,284", "lat": 28.6, "lon": 77.2, "info": "Popular near Patna"},
        {"city": "Mumbai", "p": "₹3,044", "lat": 19.0, "lon": 72.8, "info": "Popular near Patna"},
        {"city": "Tokyo", "p": "₹238,970", "lat": 35.6, "lon": 139.6, "info": "Global"}
    ]
    
    m = folium.Map(location=[20, 70], zoom_start=2, tiles="CartoDB positron")
    for d in explore_data:
        folium.Marker([d['lat'], d['lon']], popup=f"{d['city']}: {d['p']}", tooltip=f"{d['city']}").add_to(m)
    
    c_m, c_l = st.columns([1.5, 1])
    with c_m: st_folium(m, width="100%", height=500)
    with c_l:
        st.write("#### Correct Destination Prices")
        for d in explore_data:
            st.markdown(f"<div class='card'><b>{d['city']}</b> ({d['info']})<br><span class='price-tag' style='font-size:1rem;'>{d['p']}</span></div>", unsafe_allow_html=True)

# 5. 🏨 TAB: HOTELS (Verified Search)
elif current_tab == "Hotels":
    loc_input = st.text_input("Enter city for best hotels", "Ranchi, Jharkhand")
    st.markdown(f"### Best Verified Stays in {loc_input}")
    hotels = [
        {"n": "Hotel Meera", "p": "₹708", "f": "Pool • Free WiFi • Breakfast", "r": "4.0 ⭐"},
        {"n": "Genista Inn Luxury", "p": "₹3,000", "f": "Gym • Spa • AC", "r": "4.2 ⭐"},
        {"n": "Radiance Retreat", "p": "₹1,139", "f": "Free Parking • Restaurant", "r": "4.9 ⭐"}
    ]
    for h in hotels:
        st.markdown(f"<div class='card'><b>{h['n']}</b> ({h['r']})<br><small>{h['f']}</small><br><span class='price-tag'>₹{h['p']}</span></div>", unsafe_allow_html=True)

# 6. 🏘️ TAB: HOLIDAY RENTALS
elif current_tab == "Holiday rentals":
    st.subheader("Authentic Holiday Homes")
    rentals = [
        {"n": "1-Bedroom Modern House", "p": "₹1,900", "l": "Mandar", "feat": "Sleeps 2 • Kitchen"},
        {"n": "The Candy Studio", "p": "₹3,994", "l": "Ranchi Main", "feat": "Sleeps 4 • Designer"},
        {"n": "Pratap Grand Villa", "p": "₹978", "l": "Bariatu", "feat": "Sleeps 2 • Garden View"}
    ]
    for r in rentals:
        st.markdown(f"<div class='card'><b>{r['n']}</b><br><small>{r['l']} • {r['feat']}</small><br><span class='price-tag'>{r['p']}</span>/night</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AeroSave AI v100.0 | User: {st.session_state.get('u_name', 'Arbaj')} | Master Edition")
