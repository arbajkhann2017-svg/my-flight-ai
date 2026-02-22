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
# --- 🤖 SMART AI DIMAAG (Gemini NLP) ---
    prompt = f"""
    You are a flight assistant. Analyze this user query: '{query}'.
    Extract these 3 things and return ONLY them separated by a single space:
    1. Origin Airport IATA Code (3 letters)
    2. Destination Airport IATA Code (3 letters)
    3. Departure Date (format: YYYY-MM-DD)
    
    If no year is mentioned, use 2026. If no date is mentioned, use 2026-05-15.
    Output Example: DEL PAT 2026-05-25
    """
    
    try:
        with st.spinner('Aapki baat samajh raha hoon... ✨'):
            # AI extraction (English/Hindi/Hinglish sab samjhega)
            ai_response = model.generate_content(prompt).text.strip().split()
            
            if len(ai_response) >= 3:
                origin, dest, date = ai_response[0], ai_response[1], ai_response[2]
                
                token = get_token()
                if token:
                    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                    data = response.json()

                    with st.chat_message("assistant"):
                        if "data" in data and len(data["data"]) > 0:
                            st.success(f"✅ Hame {origin} se {dest} ki best deals mili hain!")
                            for flight in data["data"]:
                                price = flight['price']['total']
                                
                                # --- PREMIUM INTERFACE CARDS ---
                                with st.container():
                                    c1, c2 = st.columns([3, 1])
                                    with c1:
                                        st.markdown(f"#### ✈️ {origin} ➔ {dest}")
                                        st.caption(f"📅 Date: {date} | Economy Class")
                                    with c2:
                                        st.subheader(f"₹{price}")
                                    
                                    btn_col1, btn_col2 = st.columns(2)
                                    with btn_col1:
                                        st.link_button("✈️ Book Flight", f"https://www.google.com/flights?q=flights+from+{origin}+to+{dest}+on+{date}")
                                    with btn_col2:
                                        st.link_button(f"🏨 Hotels in {dest}", f"https://www.booking.com/searchresults.html?ss={dest}")
                                    st.markdown("---")
                        else:
                            st.warning(f"Maaf kijiye, {origin} se {dest} ke liye flights nahi mili.")
                else:
                    st.error("API Key issue! Keys check karein.")
            else:
                st.error("Kripya shehar aur date sahi se likhein.")
    except Exception as e:
        st.error("AI is busy, please try again in a moment.")
