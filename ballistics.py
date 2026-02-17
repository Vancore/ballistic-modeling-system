import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ballistic Modeling System",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1 {font-family: 'Helvetica', sans-serif; color: #e6e6e6;}
    .stMetric {background-color: #262730; padding: 10px; border-radius: 5px; border-left: 3px solid #4CAF50;}
    </style>
    """, unsafe_allow_html=True)

c1, c2 = st.columns([1, 10])
with c1:
    st.markdown("# 📐")
with c2:
    st.title("Ballistic Modeling System")

st.sidebar.markdown("### ⚙️ Simulation Config")

mode = st.sidebar.radio(
    "Physical Model:",
    ("Vacuum Model", "Atmospheric Model")
)

st.sidebar.markdown("---")

v0 = st.sidebar.number_input(
    r"Initial Velocity ($v_0$), m/s", 
    value=50.0, 
    format="%.4f", 
    step=0.1
)
deg = st.sidebar.number_input(
    r"Elevation Angle ($\alpha$), deg", 
    value=45.0, 
    format="%.4f", 
    step=0.1
)
g = st.sidebar.number_input(
    r"Gravitational Acceleration ($g$), m/s²", 
    value=9.80665, 
    format="%.5f", 
    step=0.00001
)

rad = math.radians(deg)

xs, ys, ts = [], [], []
dist, h_max, t_max = 0, 0, 0

if mode == "Atmospheric Model":
    st.sidebar.markdown("#### Environment & Object")
    m = st.sidebar.number_input(
        r"Projectile Mass ($m$), kg", 
        value=1.0, 
        min_value=1e-9,
        format="%.6f",
        step=0.000001
    )
    cw = st.sidebar.number_input(
        r"Drag Coefficient ($C_x$)", 
        value=0.47, 
        format="%.4f", 
        step=0.0001
    )
    rho = st.sidebar.number_input(
        r"Air Density ($\rho$), kg/m³", 
        value=1.225, 
        format="%.4f", 
        step=0.001
    )
    s = st.sidebar.number_input(
        r"Cross-sectional Area ($S$), m²", 
        value=0.01, 
        format="%.6f",
        step=0.000001
    )

    t, x, y = 0.0, 0.0, 0.0
    vx = v0 * math.cos(rad)
    vy = v0 * math.sin(rad)
    dt = 0.001
    max_steps = 100000 
    steps_count = 0

    while y >= 0.0 and steps_count < max_steps:
        xs.append(x)
        ys.append(y)
        ts.append(t)

        v = math.sqrt(vx**2 + vy**2)
        f = 0.5 * cw * rho * s * v * v
        mass = m if m > 0 else 1e-9

        ax = -f * vx / (mass * v) if v > 0 else 0
        ay = -g - f * vy / (mass * v) if v > 0 else -g

        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
        
        steps_count += 1

        if y > h_max: h_max = y
    
    dist = x
    t_max = t

else:
    safe_v0 = v0 if v0 > 0 else 1e-5
    
    L = (safe_v0**2 * math.sin(2 * rad)) / g
    H = (safe_v0**2 * (math.sin(rad)**2)) / (2 * g)
    T = (2 * safe_v0 * math.sin(rad)) / g

    dist, h_max, t_max = L, H, T

    steps = 500
    dx = L / steps if steps > 0 else 1e-9
    
    curr_x = 0.0
    while curr_x <= L:
        cos_rad = math.cos(rad)
        if abs(cos_rad) < 1e-9:
             curr_y = 0
             curr_t = 0
        else:
            curr_y = curr_x * math.tan(rad) - (g * curr_x**2) / (2 * safe_v0**2 * cos_rad**2)
            curr_t = curr_x / (safe_v0 * cos_rad)

        if curr_y < 0: curr_y = 0

        xs.append(curr_x)
        ys.append(curr_y)
        ts.append(curr_t)
        curr_x += dx

    xs.append(L)
    ys.append(0)
    ts.append(T)

st.markdown("### 📊 Performance Metrics")
k1, k2, k3 = st.columns(3)

with k1:
    st.metric(label="Maximum Range", value=f"{dist:.4f} m", delta="Horizontal")
with k2:
    st.metric(label="Peak Altitude (Apogee)", value=f"{h_max:.4f} m", delta="Vertical")
with k3:
    st.metric(label="Total Flight Time", value=f"{t_max:.4f} s", delta="Temporal")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=xs, y=ys,
    mode='lines',
    name='Trajectory Vector',
    line=dict(color='#00cc96', width=4),
    hovertemplate='<b>Distance</b>: %{x:.4f} m<br><b>Altitude</b>: %{y:.4f} m<extra></extra>'
))

apogee_x = dist/2
if mode == "Atmospheric Model" and ys:
    try:
        max_idx = ys.index(max(ys))
        apogee_x = xs[max_idx]
    except ValueError:
        apogee_x = 0

fig.add_trace(go.Scatter(
    x=[apogee_x], 
    y=[h_max],
    mode='markers',
    name='Apogee',
    marker=dict(size=12, color='white', symbol='diamond')
))

fig.update_layout(
    template="plotly_dark",
    xaxis_title='Horizontal Distance (m)',
    yaxis_title='Vertical Altitude (m)',
    height=600,
    margin=dict(l=40, r=40, t=40, b=40),
    hovermode="x unified",
    font=dict(family="Courier New, monospace", size=12)
)

fig.update_yaxes(scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📄 Detailed Telemetry Data"):
    telemetry_df = pd.DataFrame({
        "Time (s)": ts,
        "X-Coordinate (m)": xs,
        "Y-Coordinate (m)": ys
    })
    st.dataframe(telemetry_df, use_container_width=True)
