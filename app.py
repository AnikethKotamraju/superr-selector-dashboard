import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG (Dark Mode) ---
st.set_page_config(page_title="SupeRR Selector | Pressure Analytics", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1, h2, h3 {color: #FF4B4B;}
    .stDataFrame {background-color: #262730;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏏 SupeRR Selector: Players Under Pressure")
st.markdown("Interactive Data Appendix for Round 1 Methodology Report")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    batters = pd.DataFrame({
        'Player': ['Corbin Bosch', 'Tristan Stubbs', 'Ruturaj Gaikwad', 'Harry Tector', 'Marcus Stoinis', 
                   'Suryakumar Yadav', 'Shamim Hossain', 'Shadab Khan', 'Rishabh Pant', 'Jaker Ali Anik'],
        'Baseline_SR': [71.08, 134.35, 130.96, 112.80, 139.56, 157.58, 110.82, 121.38, 130.95, 112.18],
        'Pressure_SR': [183.61, 230.77, 223.44, 193.33, 218.90, 235.07, 185.51, 195.77, 204.72, 183.51],
        'SR_Delta': [112.52, 96.42, 92.48, 80.54, 79.34, 77.49, 74.68, 74.40, 73.77, 71.32]
    })
    
    bowlers = pd.DataFrame({
        'Player': ['Adam Milne', 'Rasikh Salam', 'Kartik Tyagi', 'Haris Rauf', 'Shamar Joseph', 
                   'Shaheen Afridi', 'Naseem Shah', 'Mohammad Saifuddin', 'Vaibhav Arora', 'Lungi Ngidi'],
        'Baseline_ER': [8.59, 8.97, 9.69, 8.25, 8.89, 7.39, 7.94, 7.95, 8.61, 8.36],
        'Pressure_ER': [6.95, 7.46, 8.26, 6.83, 7.96, 6.64, 7.50, 7.54, 8.28, 8.15],
        'ER_Delta': [1.64, 1.51, 1.43, 1.42, 0.93, 0.75, 0.44, 0.40, 0.34, 0.21]
    })
    return batters.sort_values('SR_Delta', ascending=True), bowlers.sort_values('ER_Delta', ascending=True)

bat_df, bowl_df = load_data()

# --- DASHBOARD TABS ---
tab1, tab2 = st.tabs(["🔥 Batters: Radial Wagon Wheel", "🎯 Bowlers: Economy Squeeze"])

with tab1:
    st.header("Batting Intent: The Pressure Wagon Wheel")
    st.write("A 360-degree view of boundary intent. Slice length equals Strike Rate under pressure; color intensity indicates the Delta jump from their baseline.")
    
    # Polar Bar Chart (Replaces standard X/Y scatter)
    fig_bat = px.bar_polar(bat_df, r="Pressure_SR", theta="Player", 
                           color="SR_Delta", color_continuous_scale="Reds",
                           template="plotly_dark")
    
    fig_bat.update_layout(
        height=600,
        polar=dict(radialaxis=dict(showticklabels=True, ticks='', gridcolor='#333333')),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig_bat, use_container_width=True)
    st.dataframe(bat_df.sort_values('SR_Delta', ascending=False).style.background_gradient(cmap='Reds', subset=['SR_Delta']))

with tab2:
    st.header("Bowling Execution: The Economy Squeeze")
    st.write("Gray dot = Baseline Economy. Blue dot = Pressure Economy. The connecting line visually represents how much a bowler 'squeezes' the run flow under extreme pressure.")
    
    # Dumbbell Squeeze Plot (Replaces standard bar chart)
    fig_bowl = go.Figure()
    
    for i, row in bowl_df.iterrows():
        fig_bowl.add_trace(go.Scatter(
            x=[row['Baseline_ER'], row['Pressure_ER']], 
            y=[row['Player'], row['Player']],
            mode='lines+markers',
            marker=dict(color=['#555555', '#00b4d8'], size=14, line=dict(width=2, color='white')),
            line=dict(color='#333333', width=4),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"{row['Player']}<br>Baseline: {row['Baseline_ER']}<br>Pressure: {row['Pressure_ER']}"
        ))

    fig_bowl.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Economy Rate (Runs per Over)",
        yaxis_title="",
        xaxis=dict(gridcolor='#333333', zeroline=False),
        yaxis=dict(gridcolor='#333333')
    )
    
    st.plotly_chart(fig_bowl, use_container_width=True)
    st.dataframe(bowl_df.sort_values('ER_Delta', ascending=False).style.background_gradient(cmap='Blues', subset=['ER_Delta']))
