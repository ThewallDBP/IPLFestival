import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- Configuration ---
LOCK_TIME = 19 
ADMIN_PASSWORD = "admin_ipl_2026" # Only for you to clear data

st.set_page_config(page_title="IPL Private Login", page_icon="🔐")

# --- Connect to Google Sheets ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data (ttl=0 to get real-time updates)
try:
    df = conn.read(ttl=0)
    # Ensure columns exist
    if df.empty:
        df = pd.DataFrame(columns=["User", "Password", "Team"])
except:
    df = pd.DataFrame(columns=["User", "Password", "Team"])

st.title("🏏 IPL Match: Private Selection")

# --- Step 1: Secure Login/Registration ---
st.header("Login & Select Team")

user_name = st.text_input("Username (Apna Naam Likhein):", key="u_name").strip()
user_pass = st.text_input("Password (Secret Code):", type="password", key="u_pass").strip()
selected_team = st.radio("Choose Side:", ["Team A", "Team B"], key="u_team")

if st.button("Submit / Update"):
    if user_name and user_pass:
        # Check if user already exists in the sheet
        user_exists = user_name in df['User'].values
        
        if user_exists:
            # Check if password matches
            correct_pass = str(df.loc[df['User'] == user_name, 'Password'].values[0])
            if str(user_pass) == correct_pass:
                df.loc[df['User'] == user_name, 'Team'] = selected_team
                conn.update(data=df)
                st.success(f"Updated! {user_name}, aapka team change ho gaya hai.")
            else:
                st.error("❌ Galat Password! Aap is user ki team nahi badal sakte.")
        else:
            # New User Registration
            new_user = pd.DataFrame({"User": [user_name], "Password": [user_pass], "Team": [selected_team]})
            df = pd.concat([df, new_user], ignore_index=True)
            conn.update(data=df)
            st.success(f"✅ Registered! {user_name}, aapka selection save ho gaya.")
    else:
        st.warning("Naam aur Password dono zaruri hain!")

st.divider()

# --- Step 2: The Reveal Logic ---
current_hour = datetime.now().hour

if current_hour >= LOCK_TIME:
    st.subheader("📢 Final Teams (7 PM Reveal)")
    col1, col2 = st.columns(2)
    
    # Show only User and Team (Hide Passwords from everyone!)
    with col1:
        st.info("### Team A")
        team_a = df[df['Team'] == "Team A"]['User'].tolist()
        for u in team_a: st.write(f"👤 {u}")
            
    with col2:
        st.success("### Team B")
        team_b = df[df['Team'] == "Team B"]['User'].tolist()
        for u in team_b: st.write(f"👤 {u}")
else:
    st.info(f"🔒 Sabki choices 7:00 PM ko dikhengi. Abhi tak {len(df)} users ne join kiya hai.")

# --- Step 3: Admin Section ---
st.sidebar.title("Admin Only")
admin_in = st.sidebar.text_input("Admin Key", type="password")
if admin_in == ADMIN_PASSWORD:
    if st.sidebar.button("Reset Everything"):
        empty_df = pd.DataFrame(columns=["User", "Password", "Team"])
        conn.update(data=empty_df)
        st.sidebar.success("Sheet empty ho gayi!")
        st.rerun()
