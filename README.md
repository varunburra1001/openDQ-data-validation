# Data Validation with Great Expectations

This project sets up a data validation framework using Great Expectations, similar to OpenDQ's `.pwd` validation operations.

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the Great Expectations project and create sample data:
   ```bash
   python setup_ge_validation.py
   ```
   This will:
   - Create a sample dataset in `data/customers.csv`
   - Set up the Great Expectations project structure
   - Define validation rules (expectations)
   - Create a validation checkpoint

## Running Validations

To run the validations:
```bash
python validate_data.py
```

This will:
1. Load the validation rules from the expectation suite
2. Validate the data against these rules
3. Save detailed results to `validation_results.json`

## Project Structure

- `great_expectations/`: Configuration and expectations
  - `expectations/`: Contains expectation suites (like `.pwd` files)
  - `checkpoints/`: Validation configurations
  - `uncommitted/`: Validation results and data docs
- `data/`: Sample data files
- `setup_ge_validation.py`: Script to set up the project
- `validate_data.py`: Script to run validations
- `requirements.txt`: Python dependencies

## Customizing Validations

Edit the expectations in `setup_ge_validation.py` to match your validation requirements. The current validations include:
- Email format validation
- Age range check (18-60)
- Country whitelist (India, USA, UK)
- Required field checks

## Viewing Results

After running validations, you can view the results in:
- `validation_results.json`: Detailed validation results
- `great_expectations/uncommitted/`: Additional validation artifacts

To generate and view data documentation:
```bash
great_expectations docs build
```
