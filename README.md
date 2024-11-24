## Portfolio Optimization Pipeline( PyPortOptimization)

This library is designed to automate the portfolio optimization process, including the calculation of expected returns,
risk-return matrix, optimizations, Monte Carlo simulations, post-processing of weights, and performance evaluation. The
user can customize the pipeline by providing their own methods for each step in the process.

### Features

* #### Customizable Pipeline:

Users can provide their own functions to calculate expected returns, risk-return matrices, optimization methods,
post-processing weights, and performance.

* #### Supports Different Frequencies:

Supports processing of data on both yearly and monthly frequencies.

* #### Flexible Date Ranges:

Users can specify the years and months they wish to process, allowing for highly customizable date ranges.

* #### Monte Carlo Simulation:

Built-in integration with Monte Carlo simulations to enhance the optimization process and help assess the robustness of
the optimized portfolio.

* #### Save Results:

Optimized portfolio results are saved as pickle files for easy retrieval and further analysis.

* #### Risk-Return Matrix Types:

The library supports multiple risk-return matrix types like covariance matrix, correlation matrix, and other
user-defined risk-return metrics. Users can choose the method they prefer or add new ones.

* #### Multiple Optimization Methods:

Several optimization methods are available, including mean-variance optimization, risk-parity, minimum volatility, and
other methods. Custom optimization strategies can also be implemented easily.

* #### SOLID Pricing:

The library uses SOLID principles to ensure scalability, maintainability, and flexibility of the code, making it easy to
extend and modify for specific user needs.

* #### Logging:

Detailed logging is integrated into the pipeline, allowing users to track the process and identify any potential issues
with the execution.

* #### Configuration Management:

Config files are used to easily manage settings like date ranges, frequency, and methods for each step in the process.
The library also supports reading configurations from a central configuration manager.

* #### ExecutionTimeRecorder

It s designed to track and store the execution time of all functions. It records the time each function takes to
execute and maintains a log for reference. This allows you to monitor the performance and efficiency of various
functions in your system.

### Requirements

To use this library, make sure you have the following Python packages installed:

* pandas
* numpy
* scipy
* matplotlib
* tabulate
  Additionally, you'll need the following custom modules (located in the src directory):

* execution_time_recorder: For logging execution times.
* dataDownloader: For downloading financial data.
* date_generation: For generating date ranges.
* expected_return: For calculating expected returns.
* monte_carlo_simulation: For running Monte Carlo simulations.
* optimization: For portfolio optimization methods.
* performance_metrics: For calculating portfolio performance.
* processing_weight: For post-processing optimization weights.
* risk_returns: For calculating risk-return matrices.

### Library Structure

* execution_time_recorder.py: Records the execution time of functions in the pipeline.
* dataDownloader/main.py: Contains logic for downloading or fetching data.
* date_generation/generate_date_ranges.py: Generates date ranges based on user input (years, months, frequency).
* expected_return/main.py: Contains functions for calculating expected returns.
* monte_carlo_simulation.py: Runs Monte Carlo simulations for portfolio analysis.
* optimization/main.py: Contains the optimization logic (e.g., using Markowitz optimization).
* performance_metrics/main.py: Calculates the performance metrics based on portfolio weights.
* processing_weight/main.py: Post-processes optimization weights after the optimization phase.
* risk_returns/main.py: Calculates risk-return matrices (e.g., covariance matrix).

### Function

#### run_optimization_pipeline

#### arguments

1. Years (Mandatory):
    * This parameter accepts a list of years. It is mandatory and should be provided for running the optimization
      pipeline.
      For example, years=[2023, 2024].

2. Months (Optional):
    * If not provided, the function will consider all months in the given years for the analysis.
    * If frequency="monthly", you can specify the months in a list, e.g., months=[1, 2] for January and February.
    * If months is not specified for frequency="monthly", it will run for all months within the provided years.

3. Tickers: List of tickers(optional)

4. Frequency:
    * monthly: The pipeline will generate portfolios on a monthly basis. You can provide specific months to analyze, or
      it
      will use all months for each year if not specified.
    * yearly: This option generates portfolios for each year. The start date will be the 1st day of the year, and the
      end
      date will be the last day of the year.
    * multiyear: The pipeline will consider portfolios consolidated across multiple years. The start date will be the
      1st
      day of the first year, and the end date will be the last day of the last year in the list of years.

5. Expected Return Methods:   The pipeline supports various methods to estimate expected returns:
    * ARIMA: Uses statistical modeling for forecasting returns based on historical patterns.
    * Arithmetic Mean Historical Return: Calculates the average historical return.
    * Black-Litterman Model: Combines historical data with subjective views.
    * Capital Asset Pricing Model (CAPM): Estimates returns based on market beta and risk-free rate.
    * CAGR: Calculates the Compound Annual Growth Rate based on historical returns.
    * Exponential Moving Average: A weighted average of past returns, more sensitive to recent returns.
    * Fama-French Model: Uses market, size, and value factors to estimate expected returns.
    * Gordon Growth Model: Estimates expected equity returns based on dividend yield and growth rate.
    * Holt-Winters: A combination of exponential smoothing and seasonality forecasting.
    * Linear Regression: Estimates expected returns based on a linear relationship with independent variables.
    * Risk Parity: Allocates risk evenly among assets to achieve the desired risk profile.
    * TWRR: Time-weighted return to account for cash flows.

6. Risk-Return Methods: The pipeline supports multiple risk-return modeling techniques:
    * AutoencoderRiskModel
    * CopulaRiskModel
    * ExponentialCovariance
    * GaussianProcessRiskModel
    * KMeansClustering
    * LedoitWolfShrinkage, etc.
      These models help estimate the risk-return matrix that is essential for portfolio optimization.

7. Optimization Methods: The pipeline supports a variety of portfolio optimization methods:
    * PyPortfolioOptFrontier
    * MVRiskFolioOptimizer
    * MADRiskFolioOptimizer
    * CVaRRiskFolioOptimizer, etc.
      These methods help optimize the portfolio based on various risk-return trade-offs and constraints.

8. Post-Processing Methods:The pipeline includes custom algorithms for portfolio weight allocation:

    * CustomClusteredAllocator
    * CustomDiversityAllocator
    * CustomProportionalRoundingAllocator
    * CustomTransactionCostAllocator
    * CustomWeightedFloorAllocator
    * GreedyPortfolio
    * LpPortfolio
      These methods help adjust and allocate weights to the portfolio in a manner that aligns with specific strategies
      or risk profiles.

#### Usage

1. Run the pipeline for multiple years with yearly frequency:

```
run_optimization_pipeline(
    years=[2023, 2024],
    months=[1, 2],
    tickers=["AAPL", "GOOGL"],
    frequency="yearly",
    expected_return_methods=['mean', 'geometric'],
    risk_return_methods=['covariance'],
    optimization_methods=['max_sharpe'],
    post_processing_methods=['equal_weight', 'volatility_adjusted']
)
```

2. Run the pipeline for multiple years with monthly frequency and specific months:

```run_optimization_pipeline(
    years=[2023, 2024],
    months=[1, 2, 3],
    tickers=None,  # If no specific tickers are needed
    frequency="monthly",
    expected_return_methods=['CAGR', 'EMA'],
    risk_return_methods=['GaussianProcessRiskModel'],
    optimization_methods=['MVRiskFolioOptimizer'],
    post_processing_methods=['GreedyPortfolio']
) 
```

3. Run the pipeline for multiple years with multiyear frequency:

```
run_optimization_pipeline(
    years=[2021, 2022, 2023],
    months=None,  # Will use all months
    tickers=["HDFCBANK.NS", "RELIANCE.NS"],
    frequency="multiyear",
    expected_return_methods=['CAPM', 'ARIMA'],
    risk_return_methods=['AutoencoderRiskModel'],
    optimization_methods=['MADRiskFolioOptimizer'],
    post_processing_methods=['CustomTransactionCostAllocator']
)


```

#### Performance Metrics

The following performance metrics are calculated for the optimized portfolio:

* Return: Total return over the given period.
* Risk: Total risk (e.g., standard deviation of returns).
* Sharpe Ratio: Risk-adjusted return.
  These metrics are based on the results of post-processing steps and optimizations.