import pdfplumber
import pandas as pd
import re

#######
  #  Requirements to install
  #  pip install pdfplumber pandas
#######

# Define the PDF file path
pdf_path = 'Report.pdf'

# Function to extract the Reviewer value from the table
def extract_reviewer(pdf):
    # Extract the first page's table
    table = pdf.pages[0].extract_table()
    # Loop through the table and find the row with 'Reviewer' in the Description column (index 3)
    for row in table:
        if row and len(row) > 3 and row[3] == 'Reviewer':  # Adjust row[3] for Description column
            return row[0]  # Assuming the Name column is at index 0
    return None

# Function to extract the required numeric values from the text
def extract_numbers(text, pattern):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

# Function to extract text from PDF
def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Initialize the result dictionary
        result = {
            "Reviewer": None,
            "Tools Utilized": None,
            "Identified Links": None,
            "No of Vulnerabilities": None,
            "False Positives": None,
            "Test URL": None,
            "Testing Environment": None,
            "Access Levels": None,
            "User Roles": None,
            "Scope of Test": None
        }
        
        # Extract text from the entire PDF
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # 1. Extract Reviewer value
        result['Reviewer'] = extract_reviewer(pdf)

        # 2. Extract Tools Utilized by scanning for known tools
        known_tools = [
            "Burp Suite", "Nmap", "Wireshark", "OWASP ZAP", "Metasploit",
            "HCL AppScan", "Nessus", "Nikto", "SQLmap", "Hydra", "Acunetix",
            "OpenVAS", "Dirb", "Dirbuster", "Fiddler"
        ]

        found_tools = [tool for tool in known_tools if tool.lower() in text.lower()]
        if found_tools:
            result['Tools Utilized'] = ', '.join(found_tools)

        # 3. Extract Identified Links
        result['Identified Links'] = extract_numbers(text, r'has identified (\d+) links')

        # 4. Extract No of Vulnerabilities
        result['No of Vulnerabilities'] = extract_numbers(text, r'a total of (\d+) vulnerabilities')

        # 5. Extract False Positives
        result['False Positives'] = extract_numbers(text, r'(\d+) vulnerabilities have been confirmed as false positives')

        # 6. Extract information from the table for Test URL, Testing Environment, etc.
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row[0] == 'Test URL':
                        result['Test URL'] = row[1]
                    elif row[0] == 'Testing Environment':
                        result['Testing Environment'] = row[1]
                    elif row[0] == 'Number of access levels in scope':
                        result['Access Levels'] = row[1]
                    elif row[0] == 'User Roles':
                        result['User Roles'] = row[1]
                    elif row[0] and 'scope of test' in row[0].strip().lower():
                        result['Scope of Test'] = row[1]

        return result

# Function to convert the extracted data into a DataFrame and save it as CSV
def convert_to_csv(extracted_data, output_csv='report.csv'):
    # Convert dictionary to DataFrame
    df = pd.DataFrame([extracted_data])
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Data has been written to {output_csv}")

# Extract the data
extracted_data = extract_pdf_data(pdf_path)

# Convert to CSV
convert_to_csv(extracted_data)
