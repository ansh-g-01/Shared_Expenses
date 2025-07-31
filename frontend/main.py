import streamlit as st
import requests

# === Streamlit UI ===
st.set_page_config(page_title="Register", layout="centered")
st.title("Register New User")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")

if st.button("Register"):
    # Input validation  
    if not name or not email or not phone:
        st.warning("Please fill all fields.")
    elif not phone.isdigit():
        st.warning("Phone number must be numeric.")
    else:
        payload = {
            "name": name,
            "email": email,
            "phone": int(phone)
        }

        try:
            response = requests.post("http://localhost:8000/register/", json=payload)

            if response.status_code == 200:
                st.success("User registered successfully!")
                st.json(response.json())
            else:
                st.error(f"Registration failed: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
