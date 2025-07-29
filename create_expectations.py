import os
import pandas as pd
import great_expectations as ge
from great_expectations.data_context import FileDataContext

def create_expectation_suite():
    # Set up the data context
    context = FileDataContext(project_root_dir=os.getcwd())
    
    # Create a new expectation suite
    suite_name = "customers_suite"
    
    # Create a validator using the CSV file directly
    validator = context.sources.pandas_default.read_csv(
        "data/customers.csv"
    )
    
    # Create a new expectation suite
    validator.save_expectation_suite(suite_name=suite_name)
    
    # Get the validator with the new suite
    validator = context.get_validator(
        datasource_name="pandas_default",
        data_connector_name="default_runtime_data_connector",
        data_asset_name="customers",
        runtime_parameters={"batch_data": validator._batch.data},
        batch_identifiers={"default_identifier_name": "default_identifier"},
        expectation_suite_name=suite_name
    )
    
    # Add expectations
    validator.expect_column_values_to_not_be_null(column="email")
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    validator.expect_column_values_to_be_between(
        column="age",
        min_value=18,
        max_value=60
    )
    validator.expect_column_values_to_be_in_set(
        column="country",
        value_set=["India", "USA", "UK"]
    )
    
    # Save the expectation suite
    validator.save_expectation_suite(discard_failed_expectations=False)
    
    print(f"Expectation suite '{suite_name}' created successfully!")

if __name__ == "__main__":
    create_expectation_suite()
