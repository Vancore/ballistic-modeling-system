# 🚀 Ballistic Modeling System

https://ballistic-modeling-system.streamlit.app/

**An interactive software suite for high-precision ballistic trajectory modeling in diverse environments.**

This project is a digital laboratory designed to calculate and visualize the motion of objects, accounting for both classical mechanics and complex aerodynamic factors.

---

## 🌟 Key Features

* **Dual Modeling:** Compare ideal parabolic motion (vacuum) and real-world ballistic curves (atmosphere) on a single interactive plot.
* **Physics Customization:** Fine-tune mass, cross-sectional area, air density, and drag coefficient ($C_w$).
* **High Precision:** Implements the **Euler-Cromer** semi-implicit numerical integration method for superior calculation stability.
* **Interactive Visualization:** Dynamic, zoomable plots powered by `Plotly`.
* **Telemetry System:** Automatic generation of detailed data tables for every time step (ideal for CSV export and machine learning datasets).

## 🛠 Tech Stack

* **Language:** Python 3.x
* **UI/Frontend:** [Streamlit](https://streamlit.io/)
* **Data Handling:** Pandas
* **Visualization:** Plotly
* **Imaging:** Pillow (PIL)

## 🔬 Mathematical Foundation

The system utilizes the **Euler-Cromer algorithm** to solve the equations of motion. Unlike the standard Euler method, it recalculates velocity *before* updating coordinates:

1.  **Acceleration** is calculated based on gravity and atmospheric drag.
2.  **New Velocity** is updated using the current acceleration.
3.  **New Coordinates** are calculated using the *updated* velocity.

This approach prevents "energy gain" errors, resulting in trajectories that mirror real-world physics.

## 📈 Research Insights

Key findings obtained through the simulation:
1.  **Optimal Angle Shift:** In atmospheric conditions, the optimal angle for maximum range is consistently below $45^\circ$.
2.  **Inertia vs. Drag:** Increased mass or decreased fluid density moves the "ballistic limit" closer to the ideal mathematical parabola.
