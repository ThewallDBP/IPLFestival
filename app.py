import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- Configuration ---
ADMIN_PASSWORD = "admin_ipl_2026"

st.set_page_config(page_title="IPL Match Selector", page_icon="🏏")

# --- Connection ---
conn = st.connection("gsheets", type=GSheetsConnection)

today_date = datetime.now().strftime("%d-%m-%Y")

# Data Read karne ka asaan tareeka
try:
    df = conn.read(ttl=0)
    if df is None or len(df) == 0:
        df = pd.DataFrame(columns=["Date", "User", "Password", "Match", "Team"])
except Exception:
    df = pd.DataFrame(columns=["Date", "User", "Password", "Match", "Team"])

st.title(f"🏏 IPL Match Selector - {today_date}")

# --- Input Section ---
match_choice = st.selectbox("Select Match:", ["Match 1 (3 PM)", "Match 2 (7 PM)"])
lock_time = 15 if "Match 1" in match_choice else 19

user_name = st.text_input("Username:", key="u_name").strip()
user_pass = st.text_input("Password:", type="password", key="u_pass").strip()
selected_team = st.radio("Choose Side:", ["Team A", "Team B"], key="u_team")

if st.button("Submit / Update Selection"):
    if user_name and user_pass:
        # Check if user exists today for this match
        mask = (df['Date'] == today_date) & (df['User'] == user_name) & (df['Match'] == match_choice)
        
        if mask.any():
            idx = df[mask].index[0]
            if str(df.at[idx, 'Password']) == str(user_pass):
                df.at[idx, 'Team'] = selected_team
                # Yahan error aa raha tha, isliye hum clear_cache karke update karenge
                conn.update(data=df)
                st.success("Updated!")
            else:
                st.error("Wrong Password!")
        else:
            new_row = pd.DataFrame({
                "Date": [today_date], "User": [user_name], 
                "Password": [user_pass], "Match": [match_choice], "Team": [selected_team]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=df)
            st.success("Registered!")
    else:
        st.warning("Fill all details.")

# --- Display Section ---
# (Wahi purana logic display ke liye...)
st.divider()
current_hour = datetime.now().hour
today_data = df[(df['Date'] == today_date) & (df['Match'] == match_choice)]

if current_hour >= lock_time:
    c1, c2 = st.columns(2)
    with c1:
        st.info("Team A")
        st.write(today_data[today_data['Team'] == "Team A"]['User'].tolist())
    with c2:
        st.success("Team B")
        st.write(today_data[today_data['Team'] == "Team B"]['User'].tolist())
else:
    st.info(f"Locked until {lock_time}:00. Current: {len(today_data)} users.")
