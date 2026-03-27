import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DATA_FILE = "predictions.csv"
LOCK_TIME = 19  # 7:00 PM (24-hour format)
ADMIN_PASSWORD = "ipl2026"  # Change this to your preferred password

st.set_page_config(page_title="IPL Team Selector", page_icon="🏏")

# --- Initialize Data File ---
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["User", "Team"])
    df.to_csv(DATA_FILE, index=False)

st.title("🏏 IPL Match: Team Selection")
st.write("Pick your side before 7:00 PM!")

# --- Step 1: User Login & Selection ---
st.header("Make Your Choice")

# Added a unique 'key' to prevent DuplicateElementId error
user_name = st.text_input("Enter your name:", key="main_user_input").strip()

selected_team = st.radio(
    "Which side are you on?", 
    ["Team A", "Team B"], 
    key="team_radio"
)

if st.button("Submit Selection", key="submit_btn"):
    if user_name:
        df = pd.read_csv(DATA_FILE)
        # If user exists, update their choice; otherwise, add them
        if user_name in df['User'].values:
            df.loc[df['User'] == user_name, 'Team'] = selected_team
            st.info(f"Updated: {user_name} is now on {selected_team}")
        else:
            new_row = pd.DataFrame({"User": [user_name], "Team": [selected_team]})
            df = pd.concat([df, new_row], ignore_index=True)
            st.success(f"Welcome to the game, {user_name}!")
        
        df.to_csv(DATA_FILE, index=False)
    else:
        st.error("Please enter your name before submitting.")

st.divider()

# --- Step 2: The Reveal Logic ---
st.header("Match Lineups")

current_hour = datetime.now().hour
df_results = pd.read_csv(DATA_FILE)

if current_hour >= LOCK_TIME:
    st.subheader("📢 The Reveal is LIVE!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚩 Team A")
        team_a_list = df_results[df_results['Team'] == "Team A"]['User'].tolist()
        if team_a_list:
            for user in team_a_list:
                st.write(f"• {user}")
        else:
            st.write("_No players yet_")
            
    with col2:
        st.markdown("### 🚩 Team B")
        team_b_list = df_results[df_results['Team'] == "Team B"]['User'].tolist()
        if team_b_list:
            for user in team_b_list:
                st.write(f"• {user}")
        else:
            st.write("_No players yet_")
else:
    time_left = LOCK_TIME - current_hour
    st.info(f"🔒 Selections are hidden until 7:00 PM. Check back in about {time_left} hour(s)!")
    st.metric("Total Participants", len(df_results))

# --- Step 3: Admin Section (Sidebar) ---
st.sidebar.title("Admin Panel")
# Added unique 'key' and 'type=password' for security
admin_input = st.sidebar.text_input("Enter Admin Password", type="password", key="admin_pass_input")

if admin_input == ADMIN_PASSWORD:
    st.sidebar.warning("Authenticated")
    if st.sidebar.button("Clear All Data for New Match", key="clear_data_btn"):
        df_empty = pd.DataFrame(columns=["User", "Team"])
        df_empty.to_csv(DATA_FILE, index=False)
        st.sidebar.success("All selections have been cleared!")
        st.rerun()
