# Ballistic Modeling System (BMS)

**High-fidelity trajectory simulation engine for vacuum and atmospheric physics.**

## 📌 Project Overview
BMS is a specialized computational tool for simulating projectile motion with extreme precision. It bridges the gap between simple school physics and real-world ballistics by implementing complex atmospheric drag calculations.

## 🚀 Key Capabilities
* **Dual-Core Simulation**: Switch instantly between an ideal vacuum environment and a realistic atmospheric model.
* **Drag Equation Integration**: Uses the Euler method for numerical integration, factoring in air density ($\rho$), drag coefficient ($C_x$), and cross-sectional area.
* **Real-Time Computation**: Adaptive calculation engine that updates telemetry and visuals the moment a parameter is changed.
* **Telemetry Dashboard**: Comprehensive data logging of time-stamped coordinates and velocity vectors for deep-dive analysis.

## 🧮 Physical Logic
The system handles the complex interaction of forces:
1. **Gravity**: Constant downward acceleration ($g$).
2. **Aerodynamic Drag**: A velocity-dependent force $F = \frac{1}{2} C_w \rho S v^2$ that acts opposite to the motion vector, creating realistic "curved" trajectories.

## 🛠 Tech Stack
* **Core Logic**: Python 3 (Math & Physics)
* **Interface**: Streamlit Framework
* **Data Handling**: Pandas
* **Visualization**: Plotly Engine
