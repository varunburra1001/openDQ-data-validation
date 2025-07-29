import json
from datetime import datetime

def generate_html_report():
    # Load validation results
    with open('validation_results.json', 'r') as f:
        results = json.load(f)
    
    # Extract data
    validation = results["validation_results"]
    total_expectations = validation["statistics"]["evaluated_expectations"]
    successful_expectations = validation["statistics"]["successful_expectations"]
    failed_expectations = total_expectations - successful_expectations
    success_rate = (successful_expectations / total_expectations) * 100 if total_expectations > 0 else 0
    
    # Current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Quality Validation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .header {{
            background-color: #4a6fa5;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .expectation {{
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        .expectation-header {{
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }}
        .passed {{
            background-color: #d4edda;
            border-left: 5px solid #28a745;
        }}
        .failed {{
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
        }}
        .expectation-details {{
            padding: 15px;
            background-color: white;
            border-top: 1px solid #ddd;
        }}
        .status-badge {{
            padding: 3px 8px;
            border-radius: 12px;
            color: white;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .passed-badge {{
            background-color: #28a745;
        }}
        .failed-badge {{
            background-color: #dc3545;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Data Quality Validation Report</h1>
            <p>Generated on: {current_time}</p>
        </div>
        
        <div class="summary">
            <h2>Summary</h2>
            <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold;">{total_expectations}</div>
                    <div>Total Expectations</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #28a745;">{successful_expectations}</div>
                    <div>Passed</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #dc3545;">{failed_expectations}</div>
                    <div>Failed</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold;">{success_rate:.1f}%</div>
                    <div>Success Rate</div>
                </div>
            </div>
        </div>
        
        <h2>Detailed Results</h2>
        """
    
    # Add each expectation to the HTML
    for exp in validation["expectations"]:
        status = "passed" if exp["success"] else "failed"
        status_badge = "Passed" if exp["success"] else "Failed"
        badge_class = "passed-badge" if exp["success"] else "failed-badge"
        
        html += f"""
        <div class="expectation {status}">
            <div class="expectation-header">
                <h3>{exp['meta']['description']}</h3>
                <span class="status-badge {badge_class}">{status_badge}</span>
            </div>
            <div class="expectation-details">
                <table>
                    <tr>
                        <th>Expectation Type</th>
                        <td>{exp['expectation_type']}</td>
                    </tr>
                    <tr>
                        <th>Column</th>
                        <td>{exp['meta']['column']}</td>
                    </tr>
                    <tr>
                        <th>Elements Checked</th>
                        <td>{exp['result']['element_count']}</td>
                    </tr>
                    <tr>
                        <th>Unexpected Count</th>
                        <td>{exp['result']['unexpected_count']}</td>
                    </tr>
                    <tr>
                        <th>Unexpected %</th>
                        <td>{exp['result']['unexpected_percent']:.2f}%</td>
                    </tr>"""
        
        if not exp["success"] and exp["result"]["partial_unexpected_list"]:
            html += """
                    <tr>
                        <th>Unexpected Values</th>
                        <td>"""
            
            # Add unexpected values as a list
            html += "<ul>"
            for val in exp["result"]["partial_unexpected_list"]:
                html += f"<li>{val}</li>"
            html += "</ul>"
            
            html += """
                        </td>
                    </tr>"""
        
        html += """
                </table>
            </div>
        </div>"""
    
    # Add footer
    html += f"""
        <div class="footer">
            <p>Validation completed on {current_time}</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save the HTML report
    with open('validation_report.html', 'w') as f:
        f.write(html)
    
    print(f"HTML report generated: validation_report.html")

if __name__ == "__main__":
    generate_html_report()
