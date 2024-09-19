import pandas as pd

from plugIn.expected_return.main import get_expected_return
from plugIn.get_stocks import get_stocks
from plugIn.risk_returns.main import calculate_all_risk_matrix
from pypfopt.efficient_frontier import EfficientFrontier

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Assuming results_df is already created from the previous code

def plot_performance_metrics(results_df):
    # Pivot the DataFrame for heatmap visualization
    performance_df = results_df.pivot_table(index='Risk Model', columns='Expected Return Type',
                                            values=['Expected Annual Return', 'Annual Volatility', 'Sharpe Ratio'])

    # Create a figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharex=True, sharey=True)
    metrics = ['Expected Annual Return', 'Annual Volatility', 'Sharpe Ratio']

    for i, metric in enumerate(metrics):
        sns.heatmap(performance_df[metric], annot=True, cmap='viridis', ax=axes[i])
        axes[i].set_title(metric)
        axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45)
        axes[i].set_yticklabels(axes[i].get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.show()


def plot_weights(results_df):
    # Extract and plot weights for each combination
    for idx, row in results_df.iterrows():
        expected_return_type = row['Expected Return Type']
        risk_model = row['Risk Model']
        weights = row['Weights']

        # Create a DataFrame for plotting
        weights_df = pd.DataFrame(list(weights.items()), columns=['Asset', 'Weight'])

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Asset', y='Weight', data=weights_df)
        plt.title(f'Weights for {expected_return_type} with {risk_model}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Assuming data is already obtained
    data = get_stocks()
    expected_return_df = get_expected_return(data)
    risk_return_dict = calculate_all_risk_matrix(data)

    print("Expected Return DataFrame:")
    # print(expected_return_df)

    results = []
    for return_type in expected_return_df.columns:
        mu = expected_return_df[return_type]  # Expected returns for this type

        # Iterate over each risk model in risk_return_dict
        for risk_model_name, cov_matrix in risk_return_dict.items():
            # Ensure the covariance matrix and expected returns are aligned
            if cov_matrix.shape[0] == mu.shape[0]:
                try:
                    # Initialize EfficientFrontier with the current mu and covariance matrix
                    ef = EfficientFrontier(mu, cov_matrix)

                    # Optimize the portfolio for the maximum Sharpe ratio
                    weights = ef.max_sharpe()

                    # Clean weights to remove small values
                    cleaned_weights = ef.clean_weights()

                    # Convert cleaned weights to a DataFrame for easier storage
                    weights_df = pd.DataFrame.from_dict(cleaned_weights, orient='index', columns=['Weight'])

                    # Get performance metrics
                    expectedAnnualReturn, annualVolatility, sharpeRatio = ef.portfolio_performance(verbose=False)

                    # Append results to the list
                    results.append({
                        'Expected Return Type': return_type,
                        'Risk Model': risk_model_name,
                        'Weights': weights_df.to_dict()['Weight'],
                        'Expected Annual Return': expectedAnnualReturn,
                        'Annual Volatility': annualVolatility,
                        'Sharpe Ratio': sharpeRatio,
                    })
                except Exception as e:
                    print(f"Error processing {return_type} with {risk_model_name}: {e}")
                    continue

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Print or save the results DataFrame
    print(results_df)
    plot_performance_metrics(results_df)
    # plot_weights(results_df)
