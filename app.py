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
# --- 🤖 ULTRA SMART AI SEARCH (Timing + NLP) ---
query = st.chat_input("Kahan jana hai? (Ex: Patna se Delhi 20 March ko)")

if query:
    with st.chat_message("user"):
        st.write(query)

    # Gemini ko aur zyada sakht instructions dena
    prompt = f"""
    You are a professional travel agent. Extract details from: '{query}'.
    Return ONLY 3 words separated by space:
    1. Origin IATA Code (e.g., Patna -> PAT)
    2. Destination IATA Code (e.g., Delhi -> DEL)
    3. Departure Date (YYYY-MM-DD). 
    Note: If year is missing, use 2026. If date is '20 March', use 2026-03-20.
    Example Output: PAT DEL 2026-03-20
    """
    
    try:
        with st.spinner('Aapki bhasha samajh raha hoon... ✨'):
            ai_response = model.generate_content(prompt).text.strip().split()
            
            if len(ai_response) >= 3:
                origin, dest, date = ai_response[0].upper(), ai_response[1].upper(), ai_response[2]
                
                token = get_token()
                if token:
                    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                    res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                    data = res.json()

                    with st.chat_message("assistant"):
                        if "data" in data and len(data["data"]) > 0:
                            st.success(f"✅ {origin} ➔ {dest} ki best flights ({date}):")
                            for flight in data["data"]:
                                price = flight['price']['total']
                                # TIMING NIKALNA
                                iten = flight['itineraries'][0]['segments'][0]
                                dep_time = iten['departure']['at'].split('T')[1][:5] # 14:30
                                arr_time = iten['arrival']['at'].split('T')[1][:5]   # 16:45
                                
                                with st.container():
                                    c1, c2, c3 = st.columns([2, 2, 1])
                                    with c1:
                                        st.markdown(f"**🛫 {dep_time}**")
                                        st.caption(origin)
                                    with c2:
                                        st.markdown(f"**🛬 {arr_time}**")
                                        st.caption(dest)
                                    with c3:
                                        st.subheader(f"₹{int(float(price))}")

                                    b1, b2 = st.columns(2)
                                    with b1:
                                        st.link_button("✈️ Book Now", f"https://www.google.com/flights")
                                    with b2:
                                        st.link_button(f"🏨 Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                                    st.markdown("---")
                        else:
                            st.warning(f"Maaf kijiye, {origin} se {dest} ke liye results nahi mile.")
            else:
                st.error("Kripya shehar aur date saaf likhein (Ex: Patna to Delhi 20 May)")
    except Exception as e:
        st.error("AI Busy hai, kripya codes use karein: PAT DEL 2026-03-20")
