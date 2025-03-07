import streamlit as st
import re
import random
import string
import pandas as pd

# Initialize password history if not set
if 'passwords' not in st.session_state:
    st.session_state.passwords = []

# Function to evaluate password strength
def evaluate_password(password):
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("🔴 Password should be at least 12 characters long.")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🟠 Use a mix of uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🟡 Include at least one number.")
    
    if re.search(r"[!@#$%^&*()_+{}|:<>?~]", password):
        score += 1
    else:
        feedback.append("🔵 Add a special character (!@#$%^&*()_+{}|:<>?~).")
    
    return score, feedback

# Function to generate a secure password
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:<>?~"
    return ''.join(random.choice(chars) for _ in range(length))

# Streamlit UI
st.set_page_config(page_title="🔑 Password Guardian", layout="wide")
st.markdown(
    """
    <style>
        body { background-color: #121212; color: #E0E0E0; }
        .stTextInput, .stButton>button, .stSlider { border-radius: 8px; font-size: 16px; }
        .stButton>button { background: linear-gradient(90deg, #00b4d8, #0077b6); color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔑 Password Guardian")
st.write("A modern tool to check and generate secure passwords!")

menu = st.sidebar.radio("🔍 Menu", ["Check Password", "Generate Password", "Saved Passwords", "Security Tips"])

if menu == "Check Password":
    password = st.text_input("🔑 Enter your password", type="password")
    account = st.text_input("📌 Account name (optional)")
    
    if st.button("🔍 Check Strength"):
        if password:
            score, feedback = evaluate_password(password)
            st.progress(score / 4)
            if score == 4:
                st.success("✅ Excellent Password!")
            elif score == 3:
                st.warning("⚠️ Good Password, but could be stronger.")
            else:
                st.error("❌ Weak Password. Improve using suggestions below.")
            for tip in feedback:
                st.write(tip)
        else:
            st.warning("⚠️ Please enter a password.")
    
    if st.button("💾 Save Password") and password and account:
        if any(p['password'] == password for p in st.session_state.passwords):
            st.error("🚫 This password is already saved. Choose a different one!")
        else:
            st.session_state.passwords.append({"account": account, "password": password})
            st.success("✅ Password saved!")

elif menu == "Generate Password":
    length = st.slider("🔢 Select password length", 12, 24, 16)
    if st.button("🔄 Generate Password"):
        new_password = generate_password(length)
        st.text_area("🔑 Your Secure Password", new_password)

elif menu == "Saved Passwords":
    st.subheader("🔒 Your Saved Passwords")
    if st.session_state.passwords:
        df = pd.DataFrame(st.session_state.passwords)
        st.dataframe(df)
    else:
        st.info("ℹ️ No passwords saved yet.")

elif menu == "Security Tips":
    st.subheader("🛡️ Password Security Tips")
    tips = [
        "✅ Use a unique password for each account.",
        "✅ Avoid using personal information (e.g., birthdates, names).",
        "✅ Use a password manager for convenience and security.",
        "✅ Enable two-factor authentication (2FA) wherever possible.",
        "✅ Regularly update passwords and avoid reusing old ones."
    ]
    for tip in tips:
        st.write(tip)

st.markdown("<hr><p style='text-align: center;'>🔐 Stay Safe Online! 🔐</p>", unsafe_allow_html=True)
