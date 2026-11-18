import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="SupeRR Selector | Pressure Analytics", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1, h2, h3 {color: #FF4B4B;}
    .stDataFrame {background-color: #262730;}
    /* Force charts to use full width and reduce gaps */
    .css-18e3th9 {padding-top: 1rem; padding-bottom: 1rem;}
    .block-container {padding-top: 2rem;}
    /* Custom metric box styling */
    .metric-box {
        background-color: #1E212B; 
        border-left: 4px solid #FF4B4B; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 20px;
        color: #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏏 SupeRR Selector: Players Under Pressure")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    batters = pd.DataFrame({
        'Player': ['Corbin Bosch', 'Tristan Stubbs', 'Ruturaj Gaikwad', 'Harry Tector', 'Marcus Stoinis', 
                   'Suryakumar Yadav', 'Shamim Hossain', 'Shadab Khan', 'Rishabh Pant', 'Jaker Ali Anik'],
        'Baseline_SR': [71.08, 134.35, 130.96, 112.80, 139.56, 157.58, 110.82, 121.38, 130.95, 112.18],
        'Pressure_SR': [183.61, 230.77, 223.44, 193.33, 218.90, 235.07, 185.51, 195.77, 204.72, 183.51],
        'SR_Delta': [112.52, 96.42, 92.48, 80.54, 79.34, 77.49, 74.68, 74.40, 73.77, 71.32]
    }).sort_values('SR_Delta', ascending=True)
    
    bowlers = pd.DataFrame({
        'Player': ['Adam Milne', 'Rasikh Salam', 'Kartik Tyagi', 'Haris Rauf', 'Shamar Joseph', 
                   'Shaheen Afridi', 'Naseem Shah', 'Mohammad Saifuddin', 'Vaibhav Arora', 'Lungi Ngidi'],
        'Baseline_ER': [8.59, 8.97, 9.69, 8.25, 8.89, 7.39, 7.94, 7.95, 8.61, 8.36],
        'Pressure_ER': [6.95, 7.46, 8.26, 6.83, 7.96, 6.64, 7.50, 7.54, 8.28, 8.15],
        'ER_Delta': [1.64, 1.51, 1.43, 1.42, 0.93, 0.75, 0.44, 0.40, 0.34, 0.21]
    }).sort_values('ER_Delta', ascending=False).reset_index(drop=True)
    
    return batters, bowlers

bat_df, bowl_df = load_data()

# --- DASHBOARD TABS ---
tab1, tab2 = st.tabs(["🔥 Batters: Wagon Wheel", "🎯 Bowlers: Pitch Map Target"])

with tab1:
    st.subheader("Batting Intent: The Pressure Wagon Wheel")
    
    # Custom Glossary Box for Batters
    st.markdown("""
    <div class="metric-box">
        <b>📖 Metric Glossary:</b><br>
        • <b>Baseline SR:</b> The batter's standard Strike Rate in normal, low-pressure match phases.<br>
        • <b>Pressure SR:</b> The Strike Rate when the game is on the line (Required Run Rate > 10.5 or early collapse).<br>
        • <b>SR Delta:</b> <i>(Pressure SR - Baseline SR)</i>. A positive Delta proves the batter actively elevates their scoring rate in the clutch rather than going into a shell.
    </div>
    """, unsafe_allow_html=True)
    
    # Polar Bar Chart with Numbers and tighter margins
    fig_bat = px.bar_polar(bat_df, r="Pressure_SR", theta="Player", 
                           color="SR_Delta", color_continuous_scale="Reds",
                           text="Pressure_SR", template="plotly_dark")
    
    # Format numbers to be clean integers on the wheel
    fig_bat.update_traces(texttemplate='%{text:.0f}', textposition='middle')
    
    # Reduce margins massively to close the gap to the legend
    fig_bat.update_layout(
        height=650,
        margin=dict(t=20, b=20, l=0, r=0),
        polar=dict(radialaxis=dict(showticklabels=False, ticks='', gridcolor='#333333')),
        coloraxis_colorbar=dict(title="SR Delta", x=0.95, y=0.5)
    )
    
    st.plotly_chart(fig_bat, use_container_width=True)
    st.dataframe(bat_df.sort_values('SR_Delta', ascending=False).style.background_gradient(cmap='Reds', subset=['SR_Delta']), use_container_width=True)

with tab2:
    st.subheader("Bowling Execution: The Economy Pitch Map")
    
    # Custom Glossary Box for Bowlers
    st.markdown("""
    <div class="metric-box">
        <b>📖 Metric Glossary:</b><br>
        • <b>Baseline ER:</b> The bowler's standard Economy Rate (runs conceded per over) in normal phases.<br>
        • <b>Pressure ER:</b> Economy Rate during high-leverage death overs (17-20) when defending a tight total.<br>
        • <b>ER Delta:</b> <i>(Baseline ER - Pressure ER)</i>. A positive Delta means the bowler successfully 'squeezes' the run flow and concedes fewer relative runs under pressure.
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Pitch Map using Shapes
    fig_bowl = go.Figure()

    # Draw the green cricket pitch
    fig_bowl.add_shape(type="rect", x0=-0.5, x1=9.5, y0=6.0, y1=9.0, fillcolor="#4a7c59", line_color="#ffffff", line_width=2, layer="below")
    
    # Draw popping crease and bowling crease lines for aesthetics
    fig_bowl.add_shape(type="line", x0=-0.5, x1=9.5, y0=6.5, y1=6.5, line=dict(color="white", width=2, dash="dash"), layer="below")
    fig_bowl.add_shape(type="line", x0=-0.5, x1=9.5, y0=8.5, y1=8.5, line=dict(color="white", width=2, dash="dash"), layer="below")

    # Plot the bowlers as 'cricket balls' on the pitch
    fig_bowl.add_trace(go.Scatter(
        x=bowl_df.index, 
        y=bowl_df['Pressure_ER'],
        mode='markers+text',
        marker=dict(
            size=bowl_df['ER_Delta'] * 25,  
            color='#FF4B4B', 
            line=dict(width=2, color='white')
        ),
        text=bowl_df['Player'] + "<br>" + bowl_df['Pressure_ER'].astype(str),
        textposition="top center",
        textfont=dict(color="white", size=12),
        hoverinfo='text',
        hovertext=f"Baseline ER: " + bowl_df['Baseline_ER'].astype(str)
    ))

    fig_bowl.update_layout(
        template="plotly_dark",
        height=650,
        margin=dict(t=30, b=30, l=0, r=0),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False), 
        yaxis=dict(
            title="Pressure Economy Rate (Runs Conceded)", 
            showgrid=False, 
            zeroline=False, 
            range=[9.2, 5.8] 
        )
    )
    
    st.plotly_chart(fig_bowl, use_container_width=True)
    st.dataframe(bowl_df.style.background_gradient(cmap='Blues', subset=['ER_Delta']), use_container_width=True)
