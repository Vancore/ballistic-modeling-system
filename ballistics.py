import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ballistic Modeling System",
    page_icon="📐",
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

tp = st.sidebar.radio("Simulation Type:", ("Vacuum", "Atmosphere"))

v0 = st.sidebar.number_input("Velocity (m/s):", value=60.0, format="%.4f", step=0.1)
ang = st.sidebar.number_input("Angle (deg):", value=45.0, format="%.2f", step=0.1)
g = st.sidebar.number_input("Gravity (m/s²):", value=9.80665, format="%.5f", step=0.0001)

rd = math.radians(ang)
lx, ly, lt = [], [], []
d, h, t_end = 0, 0, 0

if tp == "Atmosphere":
    m = st.sidebar.number_input("Mass (kg):", value=1.0, format="%.4f", step=0.01)
    cw = st.sidebar.number_input("Drag Coeff:", value=0.47, format="%.4f", step=0.0001)
    rho = st.sidebar.number_input("Air Density:", value=1.225, format="%.4f", step=0.001)
    s = st.sidebar.number_input("Area (m2):", value=0.01, format="%.6f", step=0.000001)

    t, x, y = 0.0, 0.0, 0.0
    vx = v0 * math.cos(rd)
    vy = v0 * math.sin(rd)
    dt = 0.01

    while y >= 0:
        lx.append(x)
        ly.append(y)
        lt.append(t)
        
        vv = math.sqrt(vx**2 + vy**2)
        f = 0.5 * cw * rho * s * vv**2
        
        ax = -(f * vx / vv) / m if vv > 0 else 0
        ay = -g - (f * vy / vv) / m if vv > 0 else -g
        
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
        
        if y > h: h = y
    
    d = x
    t_end = t
else:
    d = (v0**2 * math.sin(2 * rd)) / g
    h = (v0**2 * (math.sin(rd)**2)) / (2 * g)
    t_end = (2 * v0 * math.sin(rd)) / g
    
    n = 100
    for i in range(n + 1):
        curr_x = (d / n) * i
        curr_y = curr_x * math.tan(rd) - (g * curr_x**2) / (2 * v0**2 * math.cos(rd)**2)
        curr_t = curr_x / (v0 * math.cos(rd)) if math.cos(rd) != 0 else 0
        lx.append(curr_x)
        ly.append(max(0.0, curr_y))
        lt.append(curr_t)

c1, c2, c3 = st.columns(3)
c1.metric("RANGE", f"{d:.4f} m")
c2.metric("APOGEE", f"{h:.4f} m")
c3.metric("TIME", f"{t_end:.4f} s")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=lx, y=ly,
    mode='lines',
    line=dict(color='#00f2ff', width=4, shape='spline'),
    fill='tozeroy',
    fillcolor='rgba(0, 242, 255, 0.05)',
    name='Trajectory'
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='#2e2e3e', title="Distance (m)"),
    yaxis=dict(gridcolor='#2e2e3e', title="Altitude (m)", scaleanchor="x", scaleratio=1),
    margin=dict(l=0, r=0, t=20, b=0),
    font=dict(family="Roboto Mono")
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("TELEMETRY LOG"):
    st.dataframe(
        pd.DataFrame({"Time": lt, "X": lx, "Y": ly}),
        use_container_width=True
    )
