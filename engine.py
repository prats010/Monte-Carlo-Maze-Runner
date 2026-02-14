import numpy as np
from scipy.stats import norm
from dataclasses import dataclass
from typing import Tuple

@dataclass
class OptionParams:
    S0: float    # Initial Stock Price
    K: float     # Strike Price
    T: float     # Time to Maturity (years)
    r: float     # Risk-free rate
    sigma: float # Volatility
    paths: int   # Number of simulations

class MonteCarloEngine:
    def __init__(self, seed: int = None):
        # Initialize high-quality generator (PCG64) [cite: 317]
        self.rng = np.random.default_rng(seed)

    def black_scholes_price(self, params: OptionParams) -> float:
        """Calculate analytical solution for validation [cite: 607-609]"""
        d1 = (np.log(params.S0 / params.K) + (params.r + 0.5 * params.sigma**2) * params.T) / (params.sigma * np.sqrt(params.T))
        d2 = d1 - params.sigma * np.sqrt(params.T)
        price = params.S0 * norm.cdf(d1) - params.K * np.exp(-params.r * params.T) * norm.cdf(d2)
        return price

    def simulate_standard(self, params: OptionParams) -> Tuple[float, float, np.ndarray]:
        """
        Standard Monte Carlo Simulation for European Call Option.
        Returns: (Price Estimate, Standard Error, Path History)
        """
        # 1. Generate random samples Z ~ N(0,1)
        Z = self.rng.normal(0, 1, params.paths)
        
        # 2. Simulate terminal prices using Geometric Brownian Motion [cite: 613]
        drift = (params.r - 0.5 * params.sigma**2) * params.T
        diffusion = params.sigma * np.sqrt(params.T)
        ST = params.S0 * np.exp(drift + diffusion * Z)
        
        # 3. Calculate Payoff: max(ST - K, 0) [cite: 617]
        payoffs = np.maximum(ST - params.K, 0)
        
        # 4. Discount to present value [cite: 620]
        discount_factor = np.exp(-params.r * params.T)
        price_estimate = np.mean(payoffs) * discount_factor
        
        # 5. Calculate Standard Error [cite: 229]
        std_error = (np.std(payoffs) / np.sqrt(params.paths)) * discount_factor
        
        return price_estimate, std_error, ST

    def simulate_antithetic(self, params: OptionParams) -> Tuple[float, float]:
        """
        Variance Reduction: Antithetic Variates [cite: 417-427]
        Uses pairs (Z, -Z) to reduce variance.
        """
        n_pairs = params.paths // 2
        Z = self.rng.normal(0, 1, n_pairs)
        
        drift = (params.r - 0.5 * params.sigma**2) * params.T
        diffusion = params.sigma * np.sqrt(params.T)
        
        # Path 1 (using Z)
        ST1 = params.S0 * np.exp(drift + diffusion * Z)
        payoff1 = np.maximum(ST1 - params.K, 0)
        
        # Path 2 (using -Z) - The antithetic pair [cite: 454]
        ST2 = params.S0 * np.exp(drift + diffusion * (-Z))
        payoff2 = np.maximum(ST2 - params.K, 0)
        
        # Average the pair [cite: 454]
        payoff_pairs = 0.5 * (payoff1 + payoff2)
        
        discount_factor = np.exp(-params.r * params.T)
        price_estimate = np.mean(payoff_pairs) * discount_factor
        std_error = (np.std(payoff_pairs) / np.sqrt(n_pairs)) * discount_factor
        
        return price_estimate, std_error