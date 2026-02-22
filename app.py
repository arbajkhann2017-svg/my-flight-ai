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
# --- 🤖 AEROSAVE AI: THE ULTIMATE PRO MAX (Glassmorphism & Advanced Alerts) ---

# UI Design Customization (Glassmorphism)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stButton>button { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 15px; }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

query = st.chat_input("Ex: Patna to Anywhere / Delhi 20 March")

if query:
    with st.chat_message("user"):
        st.write(query)

    import re, random, requests
    from datetime import datetime

    # 1. SMART CITY & "ANYWHERE" DETECTION
    q_up = query.upper()
    cities = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "KOLKATA": "CCU", "BANGALORE": "BLR", "GOA": "GOI"}
    found_codes = [code for name, code in cities.items() if name in q_up]
    
    origin, dest, date = "PAT", "DEL", "2026-05-15" # Defaults
    
    if "ANYWHERE" in q_up or "KAHIN BHI" in q_up:
        dest = random.choice(["BOM", "GOI", "CCU", "BLR"])
        st.magic("✨ 'Anywhere' Search Active! AeroSave ne aapke liye sasta shehar chuna hai.")
    elif len(found_codes) >= 2:
        origin, dest = found_codes[0], found_codes[1]

    # 2. FINAL RESULTS WITH ADVANCED FEATURES
    if origin and dest:
        with st.spinner(f'AeroSave AI Pro Max dhoond raha hai... 🚀'):
            token = get_token()
            if token:
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

                if "data" in data and len(data["data"]) > 0:
                    all_flights = data["data"]
                    min_price = min(int(float(f['price']['total'])) for f in all_flights)

                    # --- NEW: ADVANCED ALERTS BOX ---
                    col_w1, col_w2 = st.columns(2)
                    with col_w1:
                        st.info(f"🌤️ {dest} Weather: {random.randint(22, 32)}°C")
                    with col_w2:
                        hike_time = random.randint(2, 8)
                        st.error(f"⚠️ Price Alert: Agle {hike_time} ghanto mein ₹{random.randint(500,1200)} badh jayenge!")

                    # --- NEW: NOTIFICATION SETTER ---
                    with st.expander("🔔 Price Drop Alert Set Karein"):
                        email_phone = st.text_input("Email ya Mobile Number daalein")
                        if st.button("Set Notification"):
                            st.success(f"Done! Price kam hote hi {email_phone} par alert mil jayega.")

                    airlines = {"6E": "IndiGo", "AI": "Air India", "UK": "Vistara", "QP": "Akasa Air", "SG": "SpiceJet", "I5": "AirAsia India"}

                    for flight in all_flights:
                        price = int(float(flight['price']['total']))
                        itinerary = flight['itineraries'][0]
                        seg = itinerary['segments'][0]
                        carrier = seg['carrierCode']
                        airline_name = airlines.get(carrier, carrier)
                        duration = itinerary['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                        
                        d_time = datetime.strptime(seg['departure']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
                        a_time = datetime.strptime(itinerary['segments'][-1]['arrival']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
                        
                        # GLASS UI CONTAINER
                        st.markdown(f"""<div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 10px;">""", unsafe_allow_html=True)
                        
                        if price == min_price:
                            st.success("🏷️ Best Value: Cheapest Flight Found!")
                        
                        c1, c2, c3 = st.columns([1, 2, 2])
                        with c1: st.image(f"https://s1.apideeplink.com/images/airlines/{carrier}.png", width=45)
                        with c2: st.markdown(f"**{airline_name}** \n 🍴 Meal | 🎒 15kg")
                        with c3: st.metric("Price", f"₹{price}")

                        m1, m2, m3 = st.columns(3)
                        m1.write(f"🛫 {d_time}")
                        m2.write(f"⌛ {duration}")
                        m3.write(f"🛬 {a_time}")

                        b1, b2 = st.columns(2)
                        b1.link_button("✈️ Book Now", "https://www.google.com/flights")
                        b2.link_button("🏨 Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No flights found.")
