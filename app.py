import streamlit as st
import cv2
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
import pandas as pd
from streamlit_option_menu import option_menu


# openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key if using GPT-based chatbot

# Load the sample drug database
def load_database():
    return pd.read_csv('drug_database.csv')

# Verify drug using the barcode
def verify_drug(barcode):
    db = load_database()
    return db[db['barcode'] == barcode].to_dict(orient='records')

# Load chatbot responses from the document
def load_responses():
    responses = {}
    with open('chatbot_responses.txt', 'r') as file:
        content = file.read()
        sections = content.split('\n\n')
        for section in sections:
            if section.strip():
                title, body = section.split('\n', 1)
                responses[title.strip()] = body.strip()
    return responses

# Get response from the document
def get_response(user_input, responses):
    for key in responses:
        if key.lower() in user_input.lower():
            return responses[key]
    return "I'm sorry, I don't have information on that topic."

# Chatbot function to handle user queries
def chatbot_response(user_input):
    responses = load_responses()
    return get_response(user_input, responses)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Barcode Scanning", "Chatbot"],
        icons=["house", "qr-code", "chat-dots"],
        menu_icon="cast",
        default_index=0,
    )

# Home Page
if selected == "Home":
    st.title("Unified AI-Driven Drug Authentication System")
    st.write("""
    **Welcome to the Unified AI-Driven Drug Authentication, Verification, and Public Education System.**
    
    This app helps users to authenticate drugs by scanning barcodes or QR codes. It also provides educational 
    information about drug safety, identifying counterfeit drugs, and general drug usage tips through an 
    interactive chatbot.
    
    **Features:**
    - **Barcode Scanning:** Scan drug barcodes to verify their authenticity.
    - **Interactive Chatbot:** Get educational information and safety warnings about drugs.
    - **Public Education:** Learn how to identify fake drugs and ensure your safety.
    """)

# Barcode Scanning Page
elif selected == "Barcode Scanning":
    st.title("Drug Authentication via Barcode Scanning")
    st.subheader("Scan Drug Barcode or QR Code")
    
    uploaded_file = st.file_uploader("Upload an image of the drug packaging", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Convert image to OpenCV format
        image = Image.open(uploaded_file).convert('RGB')
        opencv_image = np.array(image)
        
        # Scan barcode/QR code
        decoded_objects = decode(opencv_image)
        barcode_data = ""
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
        
        if barcode_data:
            st.write("Extracted Barcode Data: ", barcode_data)
            
            # Verify drug
            drug_info = verify_drug(barcode_data)
            if drug_info:
                st.success("The drug is genuine!")
                drug = drug_info[0]
                st.write("Drug Name:", drug["name"])
                st.write("Manufacturer:", drug["manufacturer"])
                st.write("Ingredients:", drug["ingredients"])
                st.write("Safety Warnings:", drug["warnings"])
                st.write("Usage Instructions:", drug["usage"])
            else:
                st.error("The drug is fake or not recognized.")
                st.write("Risk associated with fake drugs includes potential health hazards. Please report to authorities.")
        else:
            st.error("No barcode detected in the image.")

# Chatbot Page
elif selected == "Chatbot":
    st.title("Interactive Drug Safety Chatbot")
    st.subheader("Ask any question related to drug safety, counterfeit drugs, or general drug education.")
    
    user_input = st.text_input("Ask a question:")
    if user_input:
        response = chatbot_response(user_input)
        st.write("Chatbot:", response)
