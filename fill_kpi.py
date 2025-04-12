import pdfplumber
import re

def extract_from_pdf(pdf_path):
    extracted = {
        "reviewer_name": None,
        "tools_used": [],
        "links_tested": None,
        "vulnerable_links": None,
        "false_positives": None,
        "total_vulnerabilities": None,
        "test_url": None,
        "testing_environment": None,
        "access_levels": None,
        "user_roles": [],
        "scope_of_test": None,
        "application_owner": None,
    }

    full_text = ""
    table_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        cleaned_row = [cell.strip() if cell else "" for cell in row]
                        table_data.append(cleaned_row)

    # --- Extract from table: reviewer name ---
    for row in table_data:
        if len(row) >= 4 and "reviewer" in row[-1].lower():
            extracted["reviewer_name"] = row[0]
            break

    # --- Extract from paragraph text ---
    tools = re.findall(r'\b(AppScan|Burp Suite)\b', full_text, re.IGNORECASE)
    if tools:
        extracted["tools_used"] = list(set([tool.strip() for tool in tools]))

    links_match = re.search(r'identified.*?(\d+)\s+links', full_text, re.IGNORECASE)
    if links_match:
        extracted["links_tested"] = int(links_match.group(1))

    vuln_match = re.search(r'found\s+(\d+)\s+vulnerabilities', full_text, re.IGNORECASE)
    if vuln_match:
        extracted["vulnerable_links"] = int(vuln_match.group(1))

    fp_match = re.search(r'(\d+)\s+vulnerabilities.*?false positives', full_text, re.IGNORECASE)
    if fp_match:
        extracted["false_positives"] = int(fp_match.group(1))

    total_match = re.search(r'total of\s+(\d+)\s+vulnerabilities', full_text, re.IGNORECASE)
    if total_match:
        extracted["total_vulnerabilities"] = int(total_match.group(1))

    # --- Extract from key-value structure at end of document ---
    for row in table_data:
        if len(row) >= 2:
            key = row[0].lower()
            val = row[1].strip()
            if "test url" in key:
                extracted["test_url"] = val
            elif "testing environment" in key:
                extracted["testing_environment"] = val
            elif "access levels" in key:
                extracted["access_levels"] = val
            elif "scope of test" in key:
                extracted["scope_of_test"] = val
            elif "point of contact" in key:
                extracted["application_owner"] = val
            elif "user roles" in key:
                # Collect multiple lines if necessary
                extracted["user_roles"].append(val)

    return extracted


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_from_pdf.py <file.pdf>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = extract_from_pdf(file_path)

    print("\n🟢 Extracted Fields:")
    for key, val in result.items():
        print(f"{key:25}: {val}")
