import os
import sys
import subprocess

def main():
    print("Initializing Great Expectations project...")
    
    # Create the great_expectations directory if it doesn't exist
    ge_dir = os.path.join(os.getcwd(), "great_expectations")
    if not os.path.exists(ge_dir):
        os.makedirs(ge_dir)
    
    # Create a minimal great_expectations.yml
    ge_yml = os.path.join(ge_dir, "great_expectations.yml")
    if not os.path.exists(ge_yml):
        with open(ge_yml, 'w') as f:
            f.write("""# Great Expectations configuration file
datasources: {}
stores:
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: expectations/
  validations_store:
    class_name: ValidationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/validations/
  evaluation_parameter_store:
    class_name: EvaluationParameterStore

anonymous_usage_statistics:
  enabled: False

data_docs_sites:
  local_site:
    class_name: SiteBuilder
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/data_docs/
""")
    
    # Create necessary directories
    for subdir in ["expectations", "checkpoints", "plugins", "uncommited/validations", "uncommitted/data_docs"]:
        os.makedirs(os.path.join(ge_dir, subdir), exist_ok=True)
    
    print("Great Expectations project initialized successfully!")
    print("Next steps:")
    print("1. Create an expectation suite using 'python -m great_expectations suite new'")
    print("2. Create a checkpoint to validate your data")

if __name__ == "__main__":
    main()
