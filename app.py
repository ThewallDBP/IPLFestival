import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# --- Configuration ---
DB_FILE = "ipl_data.db"
ADMIN_PASSWORD = "admin_ipl_2026"

st.set_page_config(page_title="IPL Match Selector", page_icon="🏏")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS matches 
                 (date TEXT, user TEXT, password TEXT, match_name TEXT, team TEXT)''')
    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    conn.close()
    return df

def save_data(date, user, password, match, team):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Check if user already exists for today's match
    c.execute("SELECT * FROM matches WHERE date=? AND user=? AND match_name=?", (date, user, match))
    row = c.fetchone()
    
    if row:
        if str(row[2]) == str(password):
            c.execute("UPDATE matches SET team=? WHERE date=? AND user=? AND match_name=?", (team, date, user, match))
            msg = "Updated!"
            status = "success"
        else:
            msg = "Wrong Password!"
            status = "error"
    else:
        c.execute("INSERT INTO matches VALUES (?,?,?,?,?)", (date, user, password, match, team))
        msg = "Registered!"
        status = "success"
    
    conn.commit()
    conn.close()
    return msg, status

init_db()
today_date = datetime.now().strftime("%d-%m-%Y")

st.title(f"🏏 IPL Selector - {today_date}")

# --- Step 1: User Input ---
st.header("Login & Selection")
match_choice = st.selectbox("Select Match:", ["Match 1 (3 PM)", "Match 2 (7 PM)"])
lock_time = 15 if "Match 1" in match_choice else 19

user_name = st.text_input("Username:", key="u_name").strip()
user_pass = st.text_input("Password:", type="password", key="u_pass").strip()
selected_team = st.radio("Choose Side:", ["Team A", "Team B"], key="u_team")

if st.button("Submit Selection"):
    if user_name and user_pass:
        msg, status = save_data(today_date, user_name, user_pass, match_choice, selected_team)
        if status == "success": st.success(msg)
        else: st.error(msg)
    else:
        st.warning("Please fill all details.")

st.divider()

# --- Step 2: Display Results ---
st.header(f"📊 Results for {match_choice}")
current_hour = datetime.now().hour
df = get_data()
today_data = df[(df['date'] == today_date) & (df['match_name'] == match_choice)]

if current_hour >= lock_time:
    c1, c2 = st.columns(2)
    with c1:
        st.info("### Team A")
        for u in today_data[today_data['team'] == "Team A"]['user'].tolist():
            st.write(f"👤 {u}")
    with c2:
        st.success("### Team B")
        for u in today_data[today_data['team'] == "Team B"]['user'].tolist():
            st.write(f"👤 {u}")
else:
    st.info(f"🔒 {match_choice} ki teams {lock_time}:00 baje khulengi.")
    st.metric("Users Registered", len(today_data))

# --- Admin Section ---
st.sidebar.title("Admin")
if st.sidebar.text_input("Admin Key", type="password") == ADMIN_PASSWORD:
    if st.sidebar.button("Clear Database"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            init_db()
            st.sidebar.success("Database Cleared!")
            st.rerun()
