import re
from docx import Document

def extract_text_and_tables_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []

    # Extract paragraph text
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())

    # Extract tables as key-value if 2-column or special case for reviewer table
    table_data = []
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) >= 2:
                table_data.append(cells)

    return "\n".join(full_text), table_data


def extract_fields(text, table_data):
    fields = {}

    # Reviewer name
    for row in table_data:
        if len(row) >= 2 and "reviewer" in row[-1].lower():
            fields["reviewer_name"] = row[0]
            break

    # Tools used
    tools_match = re.search(r"(?:used|leveraged).*?(AppScan.*?Burp Suite.*?)\.", text, re.IGNORECASE)
    if tools_match:
        tools_text = tools_match.group(1)
        tools = re.findall(r'[A-Za-z0-9\-\s]*?(AppScan|Burp Suite|ZAP|Nessus|Nmap|[^,\.]+)', tools_text)
        fields["tools_used"] = list(set([t.strip() for t in tools if t.strip()]))

    # Links tested
    links_match = re.search(r'identified\s+(\d+)\s+links', text, re.IGNORECASE)
    if links_match:
        fields["links_tested"] = int(links_match.group(1))

    # Vulnerable links
    vuln_links = re.search(r'found\s+(\d+)\s+vulnerabilities', text, re.IGNORECASE)
    if vuln_links:
        fields["vulnerable_links"] = int(vuln_links.group(1))

    # False positives
    fp_match = re.search(r'(\d+)\s+vulnerabilities.*?false positives', text, re.IGNORECASE)
    if fp_match:
        fields["false_positives"] = int(fp_match.group(1))

    # Total vulnerabilities
    total_vuln = re.search(r'identified a total of\s+(\d+)\s+vulnerabilities', text, re.IGNORECASE)
    if total_vuln:
        fields["total_vulnerabilities"] = int(total_vuln.group(1))

    # Table-driven config values
    lookup_keys = {
        "Testing environment": "testing_environment",
        "No of access levels": "access_levels",
        "Point of Contact(App team)": "application_owner",
        "Test URL": "test_url",
        "User Roles": "user_roles",
        "Scope of test": "scope_of_test",
        "Testing Window": "testing_window",
    }

    for row in table_data:
        if len(row) >= 2:
            key, val = row[0], row[1]
            for k in lookup_keys:
                if key.strip().lower() == k.lower():
                    fields[lookup_keys[k]] = val.strip()

    return fields


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_fields.py <file.docx>")
        sys.exit(1)

    file_path = sys.argv[1]
    text, table_data = extract_text_and_tables_from_docx(file_path)
    extracted = extract_fields(text, table_data)

    print("\n🟢 Extracted Fields:")
    for k, v in extracted.items():
        print(f"{k:25}: {v}")
