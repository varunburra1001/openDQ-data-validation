import os
import subprocess
import pandas as pd

def setup_ge_project():
    # Create a sample dataset
    data = {
        'email': ['test@example.com', 'user@domain.com', 'invalid-email'],
        'age': [25, 30, 17],
        'country': ['India', 'USA', 'UK'],
        'name': ['John', 'Jane', 'Bob']
    }
    df = pd.DataFrame(data)
    
    # Save sample data
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/customers.csv', index=False)
    
    # Initialize Great Expectations project
    if not os.path.exists('great_expectations'):
        subprocess.run(["great_expectations", "init"], check=True, input=b"y\n")
    
    # Create expectation suite
    subprocess.run([
        "great_expectations", "suite", "new", 
        "--suite", "customers_suite",
        "--no-jupyter"
    ], check=True, input=b"y\n")
    
    # Create checkpoint
    checkpoint_config = """
    name: customers_checkpoint
    config_version: 1.0
    class_name: SimpleCheckpoint
    validations:
      - batch_request:
          datasource_name: pandas_datasource
          data_connector_name: default_inferred_data_connector_name
          data_asset_name: customers.csv
        expectation_suite_name: customers_suite
    """
    
    with open('great_expectations/checkpoints/customers_checkpoint.yml', 'w') as f:
        f.write(checkpoint_config)
    
    print("Great Expectations project setup complete!")
    print("Run 'python validate_data.py' to execute the validation.")

if __name__ == "__main__":
    setup_ge_project()
