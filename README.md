# 🎲 Monte Carlo Maze Runner

**Monte Carlo Maze Runner** is a gamified simulation platform that transforms abstract numerical methods into visual, interactive challenges. It allows users to run real-time Monte Carlo simulations to solve complex financial problems (like Option Pricing) and mathematical estimations (like Pi), visualizing the "Law of Large Numbers" as a maze of converging paths.

![Monte Carlo Simulation](https://upload.wikimedia.org/wikipedia/commons/8/84/Pi_30K.gif)
*(Example: Visualizing random sampling)*

## 🚀 Features

* **Real-Time Simulation Engine:** High-performance Python backend using `numpy` for vectorized calculations.
* **Interactive Frontend:** Built with **Streamlit** for instant parameter tuning and visualization.
* **Financial Models:**
    * [cite_start]**European Call Options:** Price options using Geometric Brownian Motion (Black-Scholes framework) [cite: 602-604].
    * [cite_start]**Pi Estimation:** Classic Monte Carlo experiment to estimate $\pi$ using random sampling [cite: 196-207].
* **Variance Reduction:**
    * [cite_start]**Antithetic Variates:** Implements variance reduction to improve convergence speed by ~50% using negatively correlated paths $(Z, -Z)$ [cite: 409-417].
* **Live Analytics:**
    * Real-time convergence charts (Estimate vs. Sample Size).
    * Confidence Interval bands (95%).
    * Leaderboard system to track computational efficiency.
* **Database Integration:** Persists all simulation runs using **SQLite/SQLAlchemy** for historical analysis.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Frontend:** Streamlit
* **Computation:** NumPy, SciPy
* **Visualization:** Plotly (Interactive Charts)
* **Database:** SQLite + SQLAlchemy

---

## 📦 Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/prats010/Monte-Carlo-Maze-Runner.git](https://github.com/prats010/Monte-Carlo-Maze-Runner.git)
cd Monte-Carlo-Maze-Runner
2. Install DependenciesEnsure you have Python installed, then run:Bashpip install numpy scipy sqlalchemy streamlit plotly pandas
3. Initialize the DatabaseRun the database script once to create the maze_runner.db file and the necessary tables.Bashpython database.py
4. Launch the AppStart the Streamlit server:Bashstreamlit run app.py
The application should automatically open in your default web browser at http://localhost:8501.🎮 How to PlaySelect a Challenge: Choose "European Call Option" from the sidebar.Configure Parameters:Adjust Volatility ($\sigma$), Risk-free Rate ($r$), and Time to Maturity ($T$).Set your Sample Budget ($N$): Higher samples = higher accuracy but slower speed.Choose Your Technique:Standard Monte Carlo: The baseline random sampling method.Antithetic Variates: A smarter sampling technique that reduces error variance.Run Simulation: Click the rocket button 🚀. Watch the convergence chart update in real-time as the simulation "finds" the true value.Check the Leaderboard: See how your run compares in terms of speed and accuracy.📂 Project Structuremonte-carlo-maze-runner/
│
├── app.py              # Main frontend application (Streamlit)
├── engine.py           # Computational core (Monte Carlo logic)
├── database.py         # Database models and connection logic
├── maze_runner.db      # SQLite database (created after running setup)
└── README.md           # Project documentation
📚 Theory ReferenceThis project implements core concepts from quantitative finance:Geometric Brownian Motion: $dS_t = \mu S_t dt + \sigma S_t dW_t$ Standard Error: Error decreases by $1/\sqrt{N}$.Antithetic Variates: Using pairs of $(U, 1-U)$ to reduce variance .📄 LicenseStrictly Private and Confidential - Internal Training Version.Based on the ZeTheta Algorithms Training Curriculum.
