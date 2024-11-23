## Portfolio Optimization Pipeline( PyPortOptimizationPipeline)

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

#### arguments:

* years (list): List of years to process.
* frequency (str): Frequency of data ("yearly" or "monthly"). Default is "yearly".
* data_directory (Path): Directory where the data and results will be stored. Default is project_directory / "data".
* months (list): List of months to process (optional). If not provided, all months of the specified years are processed.
* expected_return_methods (list): List of methods for calculating expected returns (optional).
* risk_return_methods (list): List of methods for calculating the risk-return matrix (optional).
* optimization_methods (list): List of optimization methods (optional).
* post_processing_methods (list): List of post-processing methods for optimization weights (optional).

#### Usage

```
# Run the pipeline for multiple years with yearly frequency
run_optimization_pipeline(
    years=[2023, 2024], 
    frequency="yearly", 
    expected_return_methods=['mean', 'geometric'], 
    risk_return_methods=['covariance'], 
    optimization_methods=['max_sharpe'], 
    post_processing_methods=['equal_weight', 'volatility_adjusted']
)
```

#### Configuration and Default Values

* Default Frequency: "yearly"
* Default Months: If not provided, the function will run for all months in the given years.
* Default Methods: If no methods are provided, the function will use default configurations for expected returns,
  risk-return matrix, optimization, and post-processing.

#### Performance Metrics

The following performance metrics are calculated for the optimized portfolio:

* Return: Total return over the given period.
* Risk: Total risk (e.g., standard deviation of returns).
* Sharpe Ratio: Risk-adjusted return.
  These metrics are based on the results of post-processing steps and optimizations.