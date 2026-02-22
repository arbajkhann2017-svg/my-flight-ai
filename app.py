import streamlit as st
import requests
import google.generativeai as genai

# API Configuration
AMADEUS_KEY = "iAo2G7nXdvKgiZzp011sEHZc6HAmPQ8C"
AMADEUS_SECRET = "yxG7clA4v002gkZG"
GEMINI_KEY = "AIzaSyCc9mYj-xpwK9nexV-GX4SQoxA-TqwbfKY"

# Gemini AI Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {"grant_type": "client_credentials", "client_id": AMADEUS_KEY, "client_secret": AMADEUS_SECRET}
    response = requests.post(url, data=data)
    return response.json().get('access_token')

st.set_page_config(page_title="AI Flight Bot", layout="centered")
st.title("✈️ Smart AI Flight Assistant")
st.write("AeroSave AI")

query = st.chat_input("Ex: Delhi to Patna on 25 March")

if query:
    with st.chat_message("user"):
        st.write(query)
    
    # AI extracts travel info from chat
        prompt = f"Extract only 'Origin Code', 'Dest Code', 'Date (YYYY-MM-DD)' from: '{query}'. Return format: DEL BOM 2026-05-20. Only return the codes, no extra text."
        try:
            model_response = model.generate_content(prompt)
            res_text = model_response.text.strip()
            res = res_text.split()
            
            # Agar AI ne sahi se 3 cheezein di hain
            if len(res) >= 3:
                token = get_token()
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={res[0]}&destinationLocationCode={res[1]}&departureDate={res[2]}&adults=1&max=5"
        
        token = get_token()
        url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={res[0]}&destinationLocationCode={res[1]}&departureDate={res[2]}&adults=1&max=3"
        flights = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()
        
        with st.chat_message("assistant"):
            if not flights.get('data'):
                st.write("Maaf kijiye, koi flight nahi mili.")
            else:
                for f in flights['data']:
                    price = f['price']['total']
                    st.success(f"✈️ Flight Found - Price: {price} INR")
                    st.link_button("Book Now", "https://your-affiliate-link.com") # Link baad mein badal lena
    except Exception as e:
        st.error("Please provide city names and date clearly.")
