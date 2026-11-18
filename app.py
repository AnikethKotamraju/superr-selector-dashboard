import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG (Dark Mode by Default) ---
st.set_page_config(page_title="SupeRR Selector | Pressure Analytics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Cricket Theme
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
# Using the exact outputs from our Pandas Colab pipeline
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
    return batters, bowlers

bat_df, bowl_df = load_data()

# --- DASHBOARD TABS ---
tab1, tab2 = st.tabs(["🔥 Batters: Controlled Aggression", "🎯 Bowlers: Execution Stability"])

with tab1:
    st.header("Batting Strike Rate: Baseline vs Pressure")
    st.write("Players above the diagonal line elevate their game in high-leverage situations.")
    
    # Scatter Plot
    fig_bat = px.scatter(bat_df, x='Baseline_SR', y='Pressure_SR', text='Player', size='SR_Delta', 
                         color='SR_Delta', color_continuous_scale='Reds',
                         labels={'Baseline_SR': 'Baseline Strike Rate', 'Pressure_SR': 'Pressure Strike Rate'})
    
    # Add Parity Line
    fig_bat.add_shape(type="line", x0=70, y0=70, x1=250, y1=250, line=dict(color="white", dash="dash"))
    fig_bat.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig_bat.update_layout(template="plotly_dark", height=600)
    
    st.plotly_chart(fig_bat, use_container_width=True)
    st.dataframe(bat_df.style.background_gradient(cmap='Reds', subset=['SR_Delta']))

with tab2:
    st.header("Bowling Economy: Baseline vs Pressure")
    st.write("Positive Delta indicates fewer runs conceded per over under pressure.")
    
    # Bar Chart for ER Delta
    fig_bowl = px.bar(bowl_df.sort_values('ER_Delta', ascending=True), 
                      x='ER_Delta', y='Player', orientation='h',
                      color='ER_Delta', color_continuous_scale='Blues',
                      labels={'ER_Delta': 'Economy Improvement (Runs/Over)'})
    
    fig_bowl.update_layout(template="plotly_dark", height=500)
    
    st.plotly_chart(fig_bowl, use_container_width=True)
    st.dataframe(bowl_df.style.background_gradient(cmap='Blues', subset=['ER_Delta']))