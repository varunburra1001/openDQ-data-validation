import pandas as pd
import re
import json

def validate_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_data():
    # Read the data
    df = pd.read_csv("data/customers.csv")
    
    # Initialize results
    results = {
        "validation_results": {
            "expectations": [],
            "statistics": {"evaluated_expectations": 0, "successful_expectations": 0}
        }
    }
    
    # Check 1: Email format validation
    invalid_emails = df[~df['email'].apply(validate_email)]['email'].tolist()
    email_success = len(invalid_emails) == 0
    results["validation_results"]["expectations"].append({
        "expectation_type": "email_format_validation",
        "success": email_success,
        "result": {
            "element_count": len(df),
            "unexpected_count": len(invalid_emails),
            "unexpected_percent": (len(invalid_emails) / len(df)) * 100 if len(df) > 0 else 0,
            "partial_unexpected_list": invalid_emails[:10]  # Show up to 10 examples
        },
        "meta": {"column": "email", "description": "Check if email format is valid"}
    })
    
    # Check 2: Age range validation
    invalid_ages = df[(df['age'] < 18) | (df['age'] > 60)]['age'].tolist()
    age_success = len(invalid_ages) == 0
    results["validation_results"]["expectations"].append({
        "expectation_type": "age_range_validation",
        "success": age_success,
        "result": {
            "element_count": len(df),
            "unexpected_count": len(invalid_ages),
            "unexpected_percent": (len(invalid_ages) / len(df)) * 100 if len(df) > 0 else 0,
            "partial_unexpected_list": invalid_ages[:10]  # Show up to 10 examples
        },
        "meta": {"column": "age", "description": "Check if age is between 18 and 60"}
    })
    
    # Check 3: Country validation
    valid_countries = ["India", "USA", "UK"]
    invalid_countries = df[~df['country'].isin(valid_countries)]['country'].tolist()
    country_success = len(invalid_countries) == 0
    results["validation_results"]["expectations"].append({
        "expectation_type": "country_validation",
        "success": country_success,
        "result": {
            "element_count": len(df),
            "unexpected_count": len(invalid_countries),
            "unexpected_percent": (len(invalid_countries) / len(df)) * 100 if len(df) > 0 else 0,
            "partial_unexpected_list": list(set(invalid_countries))[:10]  # Show up to 10 unique examples
        },
        "meta": {"column": "country", "description": "Check if country is in the allowed list"}
    })
    
    # Update statistics
    results["validation_results"]["statistics"]["evaluated_expectations"] = len(results["validation_results"]["expectations"])
    results["validation_results"]["statistics"]["successful_expectations"] = sum(
        [exp["success"] for exp in results["validation_results"]["expectations"]]
    )
    
    # Save results to a file
    with open("validation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"Validation completed. Results saved to validation_results.json")
    print(f"Total expectations: {results['validation_results']['statistics']['evaluated_expectations']}")
    print(f"Successful expectations: {results['validation_results']['statistics']['successful_expectations']}")
    
    # Print detailed results
    print("\nDetailed Results:")
    for exp in results["validation_results"]["expectations"]:
        status = "PASSED" if exp["success"] else "FAILED"
        print(f"- {exp['meta']['description']}: {status}")
        if not exp["success"]:
            print(f"  - {exp['result']['unexpected_count']} unexpected values found")
            if exp["result"]["partial_unexpected_list"]:
                print(f"  - Examples: {', '.join(map(str, exp['result']['partial_unexpected_list'][:3]))}...")

if __name__ == "__main__":
    validate_data()
