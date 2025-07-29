import os
import json
import subprocess

def run_validation():
    try:
        # Run the checkpoint using CLI
        result = subprocess.run(
            ["great_expectations", "checkpoint", "run", "customers_checkpoint"],
            capture_output=True,
            text=True
        )
        
        # Print the output
        print("\n" + "="*50)
        print("VALIDATION OUTPUT")
        print("="*50)
        print(result.stdout)
        
        if result.stderr:
            print("\nERRORS:")
            print(result.stderr)
        
        # Find and display the validation results file
        results_dir = os.path.join("great_expectations", "uncommitted", "validations")
        if os.path.exists(results_dir):
            latest_run = sorted(os.listdir(results_dir))[-1]  # Get the latest run
            results_file = os.path.join(results_dir, latest_run, "validation.json")
            
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    result_data = json.load(f)
                
                # Print summary
                print("\n" + "="*50)
                print("VALIDATION SUMMARY")
                print("="*50)
                
                success = result_data["success"]
                status = "SUCCESS" if success else "FAILED"
                print(f"\nValidation Status: {status}")
                
                # Print statistics
                stats = result_data["statistics"]
                print("\nStatistics:")
                print(f"  - Evaluated Expectations: {stats['evaluated_expectations']}")
                print(f"  - Successful Expectations: {stats['successful_expectations']}")
                print(f"  - Unsuccessful Expectations: {stats['unsuccessful_expectations']}")
                print(f"  - Success Percent: {stats['success_percent']:.2f}%")
                
                # Save a copy of the results
                output_file = 'validation_results.json'
                with open(output_file, 'w') as f:
                    json.dump(result_data, f, indent=2)
                print(f"\nDetailed results saved to '{output_file}'")
        
        print("\nRun 'great_expectations docs build' to generate data documentation")
        
    except Exception as e:
        print(f"Error during validation: {str(e)}")
        raise

if __name__ == "__main__":
    import os
    if not os.path.exists('great_expectations'):
        print("Great Expectations project not found. Running setup first...")
        import setup_ge_validation
        setup_ge_validation.setup_ge_project()
    
    run_validation()
