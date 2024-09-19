import numpy as np
import pandas as pd


class Backtest:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.realized_returns = self.calculate_realized_returns()

    def calculate_realized_returns(self):
        # Calculate daily percentage change for realized returns
        realized_returns = self.historical_data.pct_change().dropna()
        print("Realized Returns:")
        print(realized_returns)
        return realized_returns

    def backtest(self, model_expected_returns):
        realized_cumulative_returns = (1 + self.realized_returns).cumprod() - 1
        print("Realized Cumulative Returns:")
        print(realized_cumulative_returns)

        # Convert to Series if it's a DataFrame
        if isinstance(realized_cumulative_returns, pd.DataFrame):
            realized_cumulative_returns = realized_cumulative_returns.mean(axis=1)

        # Ensure realized_cumulative_returns is a Series with the correct index
        realized_cumulative_returns = realized_cumulative_returns.squeeze()

        # Initialize results DataFrame
        backtest_results = pd.DataFrame(index=model_expected_returns.index)
        backtest_results['Realized'] = realized_cumulative_returns

        # Ensure model_expected_returns has the same index as backtest_results
        model_expected_returns = model_expected_returns.reindex(backtest_results.index)
        print("Model Expected Returns (Reindex):")
        print(model_expected_returns)

        # For each model's expected returns
        for model_name in model_expected_returns.columns:
            # Add model returns to results
            backtest_results[f'{model_name}_Expected'] = model_expected_returns[model_name]

            # Calculate MAE and RMSE for each model
            backtest_results[f'{model_name}_MAE'] = np.abs(
                backtest_results[f'{model_name}_Expected'] - backtest_results['Realized'])
            backtest_results[f'{model_name}_RMSE'] = np.sqrt(
                (backtest_results[f'{model_name}_Expected'] - backtest_results['Realized']) ** 2)

        # Summarize MAE and RMSE for each model
        mae_summary = backtest_results.filter(like='_MAE').mean()
        rmse_summary = backtest_results.filter(like='_RMSE').mean()
        summary = pd.concat([mae_summary, rmse_summary], axis=1)
        summary.columns = ['MAE_Summary', 'RMSE_Summary']

        print("Backtest Results:")
        print(backtest_results)
        print("\nSummary:")
        print(summary)

        return backtest_results, summary
