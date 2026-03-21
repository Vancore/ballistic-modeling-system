import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(
    page_title="Ballistic Modeling System",
    page_icon=Image.open("logo.png"),
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono&display=swap');

    .main {
        background: radial-gradient(circle at top right, #1a1c2c, #0a0a0e);
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.95);
        border-right: 2px solid #3e3e4e;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        padding: 20px !important;
        border-radius: 15px;
        transition: transform 0.3s;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        border-color: #00f2ff;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.3);
    }

    h1 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #00f2ff, #0062ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        margin-bottom: 50px;
    }

    .stDataFrame {
        border: 1px solid #3e3e4e;
        border-radius: 10px;
    }
    
    p, label {
        font-family: 'Roboto Mono', monospace;
        color: #a0a0c0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Ballistic Modeling System")

rezhim = st.sidebar.radio("Simulation Type:", ("Vacuum", "Atmosphere"))

v0 = st.sidebar.number_input("Velocity (m/s):", value=60.0, format="%.10f", step=0.1)
ugol = st.sidebar.number_input("Angle (deg):", value=45.0, format="%.10f", step=0.1)
g_const = st.sidebar.number_input("Gravity (m/s²):", value=9.80665, format="%.10f", step=0.0001)

rad = math.radians(ugol)
x_coords = []
y_coords = []
t_points = []
dist, vysota, t_total = 0.0, 0.0, 0.0

if rezhim == "Atmosphere":
    m = st.sidebar.number_input("Mass (kg):", value=1.0, format="%.10f", step=0.01)
    k_cw = st.sidebar.number_input("Drag Coeff:", value=0.47, format="%.10f", step=0.0001)
    rho_air = st.sidebar.number_input("Air Density:", value=1.225, format="%.10f", step=0.001)
    surf_s = st.sidebar.number_input("Area (m2):", value=0.01, format="%.10f", step=0.000001)

    t, x, y = 0.0, 0.0, 0.0
    vx = v0 * math.cos(rad)
    vy = v0 * math.sin(rad)
    step = 0.01

    while y >= 0:
        x_coords.append(x)
        y_coords.append(y)
        t_points.append(t)
        
        v_tek = math.sqrt(vx**2 + vy**2)
        f_resist = 0.5 * k_cw * rho_air * surf_s * v_tek**2
        
        ax = -(f_resist * vx / v_tek) / m if v_tek > 0 else 0
        ay = -g_const - (f_resist * vy / v_tek) / m if v_tek > 0 else -g_const
        
        vx += ax * step
        vy += ay * step
        x += vx * step
        y += vy * step
        t += step
        
        if y > vysota: 
            vysota = y
    
    dist = x
    t_total = t
else:
    dist = (v0**2 * math.sin(2 * rad)) / g_const
    vysota = (v0**2 * (math.sin(rad)**2)) / (2 * g_const)
    t_total = (2 * v0 * math.sin(rad)) / g_const
    
    n_steps = 100
    for i in range(n_steps + 1):
        curr_x = (dist / n_steps) * i
        curr_y = curr_x * math.tan(rad) - (g_const * curr_x**2) / (2 * v0**2 * math.cos(rad)**2)
        curr_t = curr_x / (v0 * math.cos(rad)) if math.cos(rad) != 0 else 0
        x_coords.append(curr_x)
        y_coords.append(max(0.0, curr_y))
        t_points.append(curr_t)

col1, col2, col3 = st.columns(3)
col1.metric("RANGE", f"{dist:.10f} m")
col2.metric("APOGEE", f"{vysota:.10f} m")
col3.metric("TIME", f"{t_total:.10f} s")

kartinka = go.Figure()
kartinka.add_trace(go.Scatter(
    x=x_coords, y=y_coords,
    mode='lines',
    line=dict(color='#00f2ff', width=4, shape='spline'),
    fill='tozeroy',
    fillcolor='rgba(0, 242, 255, 0.05)',
    name='Trajectory'
))

kartinka.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='#2e2e3e', title="Distance (m)"),
    yaxis=dict(gridcolor='#2e2e3e', title="Altitude (m)", scaleanchor="x", scaleratio=1),
    margin=dict(l=0, r=0, t=20, b=0),
    font=dict(family="Roboto Mono")
)

st.plotly_chart(kartinka, use_container_width=True)

with st.expander("TELEMETRY LOG"):
    st.dataframe(
        pd.DataFrame({"Time": t_points, "X": x_coords, "Y": y_coords}),
        use_container_width=True
    )
