import time
import pandas as pd
import logging

from tabulate import tabulate

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize a global DataFrame to store results
results_df = pd.DataFrame(columns=['Function', 'Module', 'Execution Time'])


class ExecutionTimeRecorder:
    def __init__(self, module_name):
        self.module_name = module_name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            exec_time = end_time - start_time

            # Log the execution time
            logger.info(f"{self.module_name}: {func.__name__} took {exec_time:.4f} seconds")

            # Append results to DataFrame using pd.concat()
            global results_df

            # Create a new DataFrame for the new row
            new_row_df = pd.DataFrame([{
                'Function': func.__name__,
                'Module': self.module_name,
                'Execution Time': exec_time
            }])

            # Filter out all-NA columns from new_row_df before concatenation
            new_row_df_cleaned = new_row_df.dropna(axis=1, how='all')

            # Concatenate the cleaned DataFrame
            results_df = pd.concat([results_df, new_row_df_cleaned], ignore_index=True)
            return result

        return wrapper

    @staticmethod
    def print_results():
        global results_df
        if not results_df.empty:
            print(tabulate(results_df, headers='keys', tablefmt='pretty'))
        else:
            print("No execution time data available.")

    @staticmethod
    def get_performance_dataframe():
        return results_df
#
# # Example usage of the decorator
# execution_logger = ExecutionTimeLogger(module_name='example_module')
#
#
# @execution_logger
# def example_function_1():
#     time.sleep(1)  # Simulating a delay
#
#
# @execution_logger
# def example_function_2():
#     time.sleep(2)  # Simulating a longer delay
#
#
# # Execute the functions
# example_function_1()
# example_function_2()
#
# # Print the results
# ExecutionTimeLogger.print_results()
