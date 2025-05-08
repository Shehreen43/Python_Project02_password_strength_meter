# Password Strength Meter with Streamlit
import streamlit as st
import re
import random

# ----- 💎 Custom CSS for styling -----
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1E90FF, #ADD8E6); /* Gradient background */
    }

    /* Typing animation styles */
    .typing-text {
        overflow: hidden;
        border-right: .15em solid white; /* Bright blue for the caret */
        white-space: nowrap;
        animation: typing 4s steps(40, end) infinite, blink-caret .75s step-end infinite;
        font-size: 2em;
        font-weight: bold;
        color: white; /* White color for text */
    }

    /* Keyframes for typing effect */
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #1E90FF; }
    }
    </style>
""", unsafe_allow_html=True)

# ----- ⚙️ Password evaluation logic -----
BLACKLIST = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password1', 'password123']

def check_password_strength(password):
    score, feedback = 0, []

    if password.lower() in BLACKLIST:
        feedback.append("❌ Common password. Please choose something unique.")
        return 0, feedback

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Minimum 8 characters required.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Include at least one number.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    return score, feedback

def generate_strong_password(length=12):
    chars = {
        'upper': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        'lower': "abcdefghijklmnopqrstuvwxyz",
        'digits': "0123456789",
        'specials': "!@#$%^&*"
    }
    all_chars = ''.join(chars.values())

    # Ensure at least one of each type
    password = [
        random.choice(chars['upper']),
        random.choice(chars['lower']),
        random.choice(chars['digits']),
        random.choice(chars['specials'])
    ] + random.choices(all_chars, k=length - 4)

    random.shuffle(password)
    return ''.join(password)

# ----- 🌟 Streamlit App UI -----
st.title("🔐 Password Strength Checker")

# Applying both typing and color change animations
st.markdown('<div class="typing-text">Enter your password below to check its strength:</div>', unsafe_allow_html=True)

password = st.text_input("Enter your password", type="password")

# ----- 🔍 Password Check Button -----
if st.button("Check Password"):
    if password:
        score, feedback = check_password_strength(password)
        percent = int((score / 4) * 100)
        colors = {4: "green", 3: "yellow", 2: "orange", 1: "red", 0: "red"}
        messages = {
            4: "✅ Strong Password!",
            3: "⚠️ Moderate - consider improvements.",
            2: "❌ Weak - improve using suggestions.",
            1: "❌ Very Weak - improve using suggestions.",
            0: "❌ Common or empty password!"
        }

        st.markdown(
            f"""
            <div style="background-color: lightgray; border-radius: 5px; height: 30px;">
                <div class="progress-bar" style="
                    width: {percent}%;
                    background-color: {colors.get(score)};
                    height: 30px;
                    border-radius: 5px;
                    text-align: center;
                    line-height: 30px;
                    color: white;
                    font-weight: bold;">
                    {percent}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write(f"### {messages.get(score)}")

        if feedback:
            st.write("### Feedback:")
            for tip in feedback:
                st.write(tip)
    else:
        st.warning("⚠️ Please enter a password.")

# ----- 💡 Suggest Password Button -----
if st.button("Suggest Strong Password "):
    st.info(f"💡 Suggested Strong Password: `{generate_strong_password()}`")

