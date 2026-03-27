import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DATA_FILE = "predictions.csv"
LOCK_TIME = 19  # 7:00 PM in 24-hour format

st.set_page_config(page_title="IPL Team Selector", page_icon="🏏")
st.title("🏏 IPL Match: Team Selection")

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["User", "Team"])
    df.to_csv(DATA_FILE, index=False)

# --- Step 1: Login & Selection ---
st.header("Make Your Choice")
user_name = st.text_input("Enter your name:").strip()
selected_team = st.radio("Which side are you on?", ["Team A", "Team B"])

if st.button("Submit Selection"):
    if user_name:
        # Save to CSV
        df = pd.read_csv(DATA_FILE)
        # Update if user exists, else add new
        if user_name in df['User'].values:
            df.loc[df['User'] == user_name, 'Team'] = selected_team
        else:
            new_row = pd.DataFrame({"User": [user_name], "Team": [selected_team]})
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Got it, {user_name}! You are on {selected_team}.")
    else:
        st.error("Please enter a name first.")

st.divider()

# --- Step 2: The Reveal Logic ---
st.header("Who is on which side?")

current_hour = datetime.now().hour
df_results = pd.read_csv(DATA_FILE)

if current_hour >= LOCK_TIME:
    st.subheader("📢 The Reveal!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🚩 Team A")
        team_a_list = df_results[df_results['Team'] == "Team A"]['User'].tolist()
        for user in team_a_list:
            st.write(f"• {user}")
            
    with col2:
        st.write("### 🚩 Team B")
        team_b_list = df_results[df_results['Team'] == "Team B"]['User'].tolist()
        for user in team_b_list:
            st.write(f"• {user}")
else:
    time_left = LOCK_TIME - current_hour
    st.info(f"🔒 Selections are hidden until 7:00 PM. Check back in about {time_left} hour(s)!")
    st.write(f"Current participants: {len(df_results)}")
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DATA_FILE = "predictions.csv"
LOCK_TIME = 19  # 7:00 PM in 24-hour format

st.set_page_config(page_title="IPL Team Selector", page_icon="🏏")
st.title("🏏 IPL Match: Team Selection")

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["User", "Team"])
    df.to_csv(DATA_FILE, index=False)

# --- Step 1: Login & Selection ---
st.header("Make Your Choice")
user_name = st.text_input("Enter your name:").strip()
selected_team = st.radio("Which side are you on?", ["Team A", "Team B"])

if st.button("Submit Selection"):
    if user_name:
        # Save to CSV
        df = pd.read_csv(DATA_FILE)
        # Update if user exists, else add new
        if user_name in df['User'].values:
            df.loc[df['User'] == user_name, 'Team'] = selected_team
        else:
            new_row = pd.DataFrame({"User": [user_name], "Team": [selected_team]})
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Got it, {user_name}! You are on {selected_team}.")
    else:
        st.error("Please enter a name first.")

st.divider()

# --- Step 2: The Reveal Logic ---
st.header("Who is on which side?")

current_hour = datetime.now().hour
df_results = pd.read_csv(DATA_FILE)

if current_hour >= LOCK_TIME:
    st.subheader("📢 The Reveal!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🚩 Team A")
        team_a_list = df_results[df_results['Team'] == "Team A"]['User'].tolist()
        for user in team_a_list:
            st.write(f"• {user}")
            
    with col2:
        st.write("### 🚩 Team B")
        team_b_list = df_results[df_results['Team'] == "Team B"]['User'].tolist()
        for user in team_b_list:
            st.write(f"• {user}")
else:
    time_left = LOCK_TIME - current_hour
    st.info(f"🔒 Selections are hidden until 7:00 PM. Check back in about {time_left} hour(s)!")
    st.write(f"Current participants: {len(df_results)}")
