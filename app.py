import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from engine import MonteCarloEngine, OptionParams
from database import save_result

# Page Configuration
st.set_page_config(page_title="Monte Carlo Maze Runner", layout="wide", page_icon="🎲")

# [cite_start]Custom CSS for "Maze" Aesthetic [cite: 1257, 1266]
st.markdown("""
<style>
    .stApp { background-color: #0A0E27; color: #F0F0F0; }
    div[data-testid="stMetricValue"] { color: #00D9FF; }
</style>
""", unsafe_allow_html=True)

st.title("🎲 Monte Carlo Maze Runner")
st.markdown("Navigate the maze of probability. Use random sampling to converge on the truth.")

# --- Sidebar: Mission Control ---
st.sidebar.header("⚙️ Simulation Parameters")
scenario = st.sidebar.selectbox("Select Challenge", ["European Call Option", "Pi Estimation"])

if scenario == "European Call Option":
    S0 = st.sidebar.number_input("Initial Price ($)", 100.0)
    K = st.sidebar.number_input("Strike Price ($)", 100.0)
    T = st.sidebar.number_input("Time (Years)", 1.0)
    r = st.sidebar.number_input("Risk-free Rate", 0.05)
    sigma = st.sidebar.number_input("Volatility", 0.2)
    
n_samples = st.sidebar.slider("Sample Budget (N)", 100, 50000, 5000, step=100)
method = st.sidebar.radio("Technique", ["Standard Monte Carlo", "Antithetic Variates"])

# --- Main Display ---
col1, col2 = st.columns([2, 1])

if st.button("🚀 Run Simulation"):
    engine = MonteCarloEngine()
    
    # 1. Setup
    params = OptionParams(S0, K, T, r, sigma, n_samples)
    true_price = engine.black_scholes_price(params)
    
    start_time = time.time()
    
    # 2. Run Progressive Simulation (to visualize convergence)
    # We break N into chunks to animate the chart
    chunks = 20
    chunk_size = n_samples // chunks
    
    convergence_history = []
    progress_bar = st.progress(0)
    chart_placeholder = st.empty()
    
    current_estimate = 0
    
    for i in range(1, chunks + 1):
        current_n = i * chunk_size
        temp_params = OptionParams(S0, K, T, r, sigma, current_n)
        
        if method == "Antithetic Variates":
            est, err = engine.simulate_antithetic(temp_params)
        else:
            est, err, _ = engine.simulate_standard(temp_params)
            
        convergence_history.append({
            "Samples": current_n,
            "Estimate": est,
            "True Value": true_price,
            "Error Band Upper": est + 1.96*err,  # 95% Confidence Interval
            "Error Band Lower": est - 1.96*err
        })
        
        # Real-time Chart Update
        df = pd.DataFrame(convergence_history)
        fig = go.Figure()
        
        # Plot Estimate Line
        fig.add_trace(go.Scatter(x=df["Samples"], y=df["Estimate"], mode='lines', name='Estimate', line=dict(color='#00D9FF')))
        
        # Plot True Value Line
        fig.add_trace(go.Scatter(x=df["Samples"], y=df["True Value"], mode='lines', name='True Value (Black-Scholes)', line=dict(color='#FF006E', dash='dash')))
        
        # Plot Confidence Interval
        fig.add_trace(go.Scatter(x=df["Samples"], y=df["Error Band Upper"], mode='lines', line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=df["Samples"], y=df["Error Band Lower"], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0, 217, 255, 0.2)', name='95% CI'))

        fig.update_layout(
            title="Convergence: Law of Large Numbers",
            xaxis_title="Number of Samples",
            yaxis_title="Option Price",
            template="plotly_dark",
            height=400
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(i / chunks)
        time.sleep(0.05) # Animation delay
        
        current_estimate = est

    end_time = time.time()
    elapsed = end_time - start_time
    
    # 3. Save to Database
    save_result(scenario, n_samples, true_price, current_estimate, method, elapsed)

    # 4. Results Dashboard
    with col2:
        st.success("Simulation Complete!")
        st.metric("Final Estimate", f"${current_estimate:.4f}")
        st.metric("True Value", f"${true_price:.4f}")
        
        error = abs(current_estimate - true_price)
        st.metric("Absolute Error", f"{error:.4f}", delta_color="inverse")
        
        st.info(f"⏱️ Time: {elapsed:.4f}s")
        if method == "Antithetic Variates":
            st.caption("Variance Reduction Active: ~50% efficiency gain expected.")

# --- Leaderboard Section ---
st.markdown("---")
st.subheader("🏆 Leaderboard (Recent Runs)")

# Fetch recent runs from DB
from database import SessionLocal, SimulationResult
session = SessionLocal()
results = session.query(SimulationResult).order_by(SimulationResult.timestamp.desc()).limit(5).all()
session.close()

if results:
    data = [{
        "Method": r.method, 
        "Samples": r.n_samples, 
        "Error": f"{r.error:.5f}", 
        "Time (s)": f"{r.computation_time:.4f}"
    } for r in results]
    st.table(pd.DataFrame(data))