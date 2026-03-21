import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# Конфиг страницы
st.set_page_config(
    page_title="Ballistic Modeling System v2.0",
    page_icon=Image.open("logo.png"),
    layout="wide"
)

# кастомный стиль
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono&display=swap');
    .main { background: radial-gradient(circle at top right, #1a1c2c, #0a0a0e); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 25, 0.95); border-right: 2px solid #3e3e4e; }
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        padding: 20px !important;
        border-radius: 15px;
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
    }
    p, label { font-family: 'Roboto Mono', monospace; color: #a0a0c0 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Ballistic Modeling System")

# Ввод параметров
sim_mode = st.sidebar.radio("Simulation Type:", ("Vacuum", "Atmosphere"))
v0 = st.sidebar.number_input("Velocity (m/s):", value=60.0, format="%.6f", step=0.1)
angle_deg = st.sidebar.number_input("Angle (deg):", value=45.0, format="%.4f", step=0.1)
g_val = st.sidebar.number_input("Gravity (m/s²):", value=9.80665, format="%.6f", step=0.0001)

rad = math.radians(angle_deg)
res_x, res_y, res_t = [], [], []
d_final, h_max, flight_time = 0.0, 0.0, 0.0

# Математическая модель
if sim_mode == "Atmosphere":
    m = st.sidebar.number_input("Mass (kg):", value=1.0, format="%.4f", step=0.01)
    cw = st.sidebar.number_input("Drag Coeff (Cw):", value=0.47, format="%.4f", step=0.0001)
    rho = st.sidebar.number_input("Air Density (kg/m³):", value=1.225, format="%.4f", step=0.001)
    area = st.sidebar.number_input("Cross-section Area (m²):", value=0.01, format="%.6f", step=0.000001)

    t, x, y = 0.0, 0.0, 0.0
    vx, vy = v0 * math.cos(rad), v0 * math.sin(rad)
    dt = 0.005 # Уменьшил шаг для большей точности

    while y >= 0:
        res_x.append(x)
        res_y.append(y)
        res_t.append(t)
        
        v_abs = math.sqrt(vx**2 + vy**2)
        # Сила сопротивления: F = 0.5 * Cw * rho * S * v^2
        f_drag = 0.5 * cw * rho * area * v_abs**2
        
        ax = -(f_drag * vx / v_abs) / m if v_abs > 0 else 0
        ay = -g_val - (f_drag * vy / v_abs) / m if v_abs > 0 else -g_val
        
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
        if y > h_max: h_max = y
    
    d_final, flight_time = x, t
else:
    d_final = (v0**2 * math.sin(2 * rad)) / g_val
    h_max = (v0**2 * (math.sin(rad)**2)) / (2 * g_val)
    flight_time = (2 * v0 * math.sin(rad)) / g_val
    
    points = 200
    for i in range(points + 1):
        curr_t = (flight_time / points) * i
        curr_x = v0 * math.cos(rad) * curr_t
        curr_y = v0 * math.sin(rad) * curr_t - 0.5 * g_val * curr_t**2
        res_x.append(curr_x)
        res_y.append(max(0.0, curr_y))
        res_t.append(curr_t)

# Вывод результатов
m1, m2, m3 = st.columns(3)
m1.metric("RANGE", f"{d_final:.6f} m")
m2.metric("APOGEE", f"{h_max:.6f} m")
m3.metric("FLIGHT TIME", f"{flight_time:.6f} s")

# График
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=res_x, y=res_y,
    mode='lines',
    line=dict(color='#00f2ff', width=3),
    fill='tozeroy',
    fillcolor='rgba(0, 242, 255, 0.07)',
    name='Trajectory Data'
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(10,10,15,0.5)',
    xaxis=dict(gridcolor='#333344', title="Horizontal Distance (m)", zerolinecolor='#444455'),
    yaxis=dict(gridcolor='#333344', title="Vertical Altitude (m)", scaleanchor="x", scaleratio=1),
    margin=dict(l=40, r=40, t=40, b=40),
    font=dict(family="Roboto Mono")
)

st.plotly_chart(fig, use_container_width=True)

# Лог данных
with st.expander("DETAILED ANALYTICS"):
    df_log = pd.DataFrame({"Time (s)": res_t, "X (m)": res_x, "Y (m)": res_y})
    st.dataframe(df_log, use_container_width=True)
