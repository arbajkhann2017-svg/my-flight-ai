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
# --- 🤖 ULTRA SMART HYBRID SEARCH (Timing + NLP) ---
query = st.chat_input("Ex: Patna to Delhi 20 March")

if query:
    with st.chat_message("user"):
        st.write(query)

    # 1. SMART BACKUP: Bina AI ke shehar aur date pehchanna
    import re
    q_up = query.upper()
    
    # Common cities map
    city_map = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "BANGALORE": "BLR", "KOLKATA": "CCU"}
    found_cities = [code for city, code in city_map.items() if city in q_up]
    
    # 2. AI SE POOCHNA (Agar backup kaam na kare)
    prompt = f"Provide ONLY: Origin_IATA Dest_IATA YYYY-MM-DD for '{query}'. Use 2026. Ex: PAT DEL 2026-03-20"
    
    try:
        with st.spinner('Duniya bhar ki flights dhoond raha hoon... ✈️'):
            response = model.generate_content(prompt)
            ai_data = response.text.strip().split()
            
            if len(ai_data) >= 3:
                origin, dest, date = ai_data[0].upper(), ai_data[1].upper(), ai_data[2]
                
                token = get_token()
                if token:
                    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                    res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                    data = res.json()

                    with st.chat_message("assistant"):
                        if "data" in data and len(data["data"]) > 0:
                            st.success(f"✅ {origin} ➔ {dest} Flights on {date}")
                            for flight in data["data"]:
                                price = int(float(flight['price']['total']))
                                # TIMING EXTRACTION
                                seg = flight['itineraries'][0]['segments'][0]
                                d_time = seg['departure']['at'].split('T')[1][:5]
                                a_time = seg['arrival']['at'].split('T')[1][:5]
                                
                                with st.container():
                                    t1, t2, t3 = st.columns([1, 1, 1])
                                    t1.metric("🛫 Dep", d_time)
                                    t2.metric("🛬 Arr", a_time)
                                    t3.metric("💰 Price", f"₹{price}")
                                    
                                    col_b1, col_b2 = st.columns(2)
                                    col_b1.link_button("✈️ Book Flight", "https://www.google.com/flights")
                                    col_b2.link_button("🏨 View Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                                    st.markdown("---")
                        else:
                            st.warning(f"No flights found for {origin} to {dest} on {date}.")
            else:
                st.error("Kripya saaf likhein: 'Patna to Delhi 20 March'")
    except Exception as e:
        st.error("Kripya is tarah likhein: PAT DEL 2026-03-20")
