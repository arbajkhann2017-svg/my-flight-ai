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

query = st.chat_input("Kahan jana hai? (Example: Delhi to Patna on 15 May)")
# Simple extraction (Direct Search)
    import re
    words = query.upper().replace("TO", " ").split()
    codes = [w for w in words if len(w) == 3]
    
    if len(codes) >= 2:
        origin, dest = codes[0], codes[1]
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
        date = date_match.group(0) if date_match else "2026-05-15"
        
        with st.spinner('Searching flights...'):
            token = get_token()

    # AI Instruction for all routes
    prompt = f"Extract 'Origin City Code', 'Dest City Code', and 'Date' in YYYY-MM-DD format from: '{query}'. Return only 3 words separated by space, example: DEL PAT 2026-05-15"
    
    try:
        ai_resp = model.generate_content(prompt).text.strip().split()
        
        if len(ai_resp) >= 3:
            origin, dest, date = ai_resp[0], ai_resp[1], ai_resp[2]
            
            with st.spinner('Sabse sasti flights dhund raha hoon...'):
                token = get_token()
                if token:
                    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                    data = response.json()

                    with st.chat_message("assistant"):
                        if "data" in data and len(data["data"]) > 0:
                            st.subheader(f"📍 {origin} se {dest} ki jankari:")
                            for flight in data["data"]:
                                price = flight['price']['total']
                                currency = flight['price']['currency']
                                st.info(f"💰 Price: {price} {currency}")
                                st.write(f"📅 Date: {date}")
                                st.link_button("✈️ Book This Flight", f"https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}")
                                st.markdown("---")
                        else:
                            st.warning("Maaf kijiye, is route par abhi koi flights nahi mili. Kripya date check karein.")
                else:
                    st.error("API Connection Error! Please check your Amadeus Keys.")
        else:
            st.warning("Kripya shehar ka naam aur sahi date batayein.")
    except Exception as e:
        st.error("AI is busy, please try again.")
