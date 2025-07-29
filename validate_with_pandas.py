import pandas as pd
import re
import json

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))

def validate_data():
    # Read the data
    df = pd.read_csv("data/customers.csv")
    
    # Initialize results
    results = {
        "validation_results": {
            "expectations": [],
            "statistics": {
                "total_records": len(df),
                "evaluated_expectations": 0,
                "successful_expectations": 0
            }
        }
    }
    
    # Check 1: Email format validation
    email_validation = df['email'].apply(validate_email)
    email_failures = df[~email_validation]['email'].tolist()
    
    results["validation_results"]["expectations"].append({
        "expectation_type": "valid_email_format",
        "success": len(email_failures) == 0,
        "result": {
            "element_count": len(df),
            "unexpected_count": len(email_failures),
            "unexpected_percent": (len(email_failures) / len(df)) * 100,
            "partial_unexpected_list": email_failures[:10]  # Show first 10 failures
        },
        "meta": {"column": "email", "description": "Check if email format is valid"}
    })
    
    # Check 2: Age range validation (18-60)
    age_validation = (df['age'] >= 18) & (df['age'] <= 60)
    age_failures = df[~age_validation]['age'].tolist()
    
    results["validation_results"]["expectations"].append({
        "expectation_type": "valid_age_range",
        "success": len(age_failures) == 0,
        "result": {
            "element_count": len(df),
            "unexpected_count": len(age_failures),
            "unexpected_percent": (len(age_failures) / len(df)) * 100,
            "partial_unexpected_list": age_failures[:10]  # Show first 10 failures
        },
        "meta": {"column": "age", "description": "Check if age is between 18 and 60"}
    })
    
    # Check 3: Country validation
    valid_countries = ["India", "USA", "UK"]
    country_validation = df['country'].isin(valid_countries)
    country_failures = df[~country_validation]['country'].unique().tolist()
    
    results["validation_results"]["expectations"].append({
        "expectation_type": "valid_country",
        "success": len(country_failures) == 0,
        "result": {
            "element_count": len(df),
            "unexpected_count": (~country_validation).sum(),
            "unexpected_percent": ((~country_validation).sum() / len(df)) * 100,
            "partial_unexpected_list": country_failures
        },
        "meta": {"column": "country", "description": f"Check if country is in {valid_countries}"}
    })
    
    # Update statistics
    results["validation_results"]["statistics"]["evaluated_expectations"] = len(results["validation_results"]["expectations"])
    results["validation_results"]["statistics"]["successful_expectations"] = sum(
        1 for exp in results["validation_results"]["expectations"] if exp["success"]
    )
    
    # Calculate overall success
    results["validation_results"]["success"] = all(
        exp["success"] for exp in results["validation_results"]["expectations"]
    )
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        import numpy as np
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_numpy_types(item) for item in obj]
        return obj
    
    # Save results to a file
    with open("validation_results.json", "w") as f:
        json.dump(convert_numpy_types(results), f, indent=2)
    
    # Print summary
    print("\nValidation Results:")
    print("=" * 50)
    print(f"Total Records: {results['validation_results']['statistics']['total_records']}")
    print(f"Total Expectations: {results['validation_results']['statistics']['evaluated_expectations']}")
    print(f"Successful: {results['validation_results']['statistics']['successful_expectations']}")
    print(f"Failed: {results['validation_results']['statistics']['evaluated_expectations'] - results['validation_results']['statistics']['successful_expectations']}")
    
    print("\nDetailed Results:")
    print("-" * 50)
    for exp in results["validation_results"]["expectations"]:
        status = "PASS" if exp["success"] else "FAIL"
        print(f"[{status}] {exp['meta']['description']}")
        if not exp["success"]:
            print(f"   - Failed values: {exp['result']['partial_unexpected_list']}")
    
    print("\nResults saved to: validation_results.json")
    return results

if __name__ == "__main__":
    validate_data()
