# Manual Setup Guide for Great Expectations

This guide will help you set up a Great Expectations project manually since we encountered some issues with the automated setup.

## Step 1: Create Sample Data

1. Create a `data` directory in your project folder.
2. Create a file named `customers.csv` in the `data` directory with the following content:

```csv
email,age,country,name
test@example.com,25,India,John
user@domain.com,30,USA,Jane
invalid-email,17,UK,Bob
```

## Step 2: Initialize Great Expectations

Open a command prompt and run:

```bash
pip install great_expectations
cd path\to\your\project\directory
great_expectations init
```

When prompted, type `y` and press Enter to confirm the initialization.

## Step 3: Create an Expectation Suite

Run the following command to create a new expectation suite:

```bash
great_expectations suite new
```

1. Choose option 1: "Create a new Expectation Suite"
2. Enter a name for your suite, e.g., `customers_suite`
3. Choose option 1: "Pandas"
4. Enter the path to your data file: `data/customers.csv`
5. Choose option 1: "Y" when asked if you want to proceed

This will open a Jupyter notebook. In the notebook:

1. Run all cells (Kernel > Restart & Run All)
2. Follow the instructions to add expectations
3. Save the notebook when done

## Step 4: Create a Checkpoint

1. Create a file named `customers_checkpoint.yml` in the `great_expectations/checkpoints/` directory with the following content:

```yaml
name: customers_checkpoint
config_version: 1.0
class_name: SimpleCheckpoint
validations:
  - batch_request:
      datasource_name: default
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: customers.csv
      batch_spec_passthrough:
        reader_method: read_csv
        reader_options: {}
    expectation_suite_name: customers_suite
```

## Step 5: Run the Validation

Run the validation using:

```bash
great_expectations checkpoint run customers_checkpoint
```

## Step 6: View the Results

You can view the validation results in the terminal output or find detailed results in the `great_expectations/uncommitted/validations/` directory.

## Step 7: (Optional) Generate Documentation

To generate data documentation:

```bash
great_expectations docs build
```

This will create documentation that you can view in your browser.
