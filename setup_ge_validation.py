import os
import pandas as pd
import great_expectations as ge
from great_expectations.datasource import PandasDatasource

def setup_ge_project():
    # Create a new Great Expectations project
    os.makedirs('great_expectations', exist_ok=True)
    
    # Set up the data context
    context = ge.get_context(project_root_dir=os.getcwd())
    
    # Create a sample dataset (you can replace this with your actual data)
    data = {
        'email': ['test@example.com', 'user@domain.com', 'invalid-email'],
        'age': [25, 30, 17],
        'country': ['India', 'USA', 'UK'],
        'name': ['John', 'Jane', 'Bob']
    }
    df = pd.DataFrame(data)
    
    # Save sample data
    os.makedirs('data', exist_ok=True)
    csv_path = os.path.join('data', 'customers.csv')
    df.to_csv(csv_path, index=False)
    
    # Add a pandas datasource
    datasource = PandasDatasource(name="pandas_datasource")
    context.add_datasource(datasource)
    
    # Create expectation suite
    suite_name = "customers_suite"
    context.create_expectation_suite(
        expectation_suite_name=suite_name,
        overwrite_existing=True
    )
    
    # Create batch request
    batch = datasource.get_batch(
        batch_kwargs={"dataset": df},
        expectation_suite_name=suite_name,
    )
    
    # Add expectations
    batch.expect_column_values_to_not_be_null(column="email")
    batch.expect_column_values_to_match_regex(
        column="email", 
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    batch.expect_column_values_to_be_between(
        column="age", 
        min_value=18, 
        max_value=60
    )
    batch.expect_column_values_to_be_in_set(
        column="country", 
        value_set=["India", "USA", "UK"]
    )
    
    # Save expectations
    batch.save_expectation_suite(discard_failed_expectations=False)
    
    # Create checkpoint configuration
    checkpoint_config = {
        "name": "customers_checkpoint",
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "validations": [
            {
                "batch_kwargs": {"dataset": df},
                "expectation_suite_name": suite_name
            }
        ]
    }
    
    # Add checkpoint
    context.add_checkpoint(**checkpoint_config)
    
    print("Great Expectations project setup complete!")
    print("Run 'python validate_data.py' to execute the validation.")

if __name__ == "__main__":
    setup_ge_project()
