Below is an example of how you might document this issue:

---

**Title:**  
Publicly Accessible PDF Containing Sensitive Training Material

**Description:**  
A PDF file containing Persona training material is accessible without any form of authentication. This exposes sensitive internal content to anyone who knows or discovers the URL, leading to potential unauthorized access and information disclosure.

**Steps to Reproduce:**  
1. Open a web browser.  
2. Paste the direct URL of the PDF into the address bar.  
3. Access the document without being prompted for credentials.  

**Remediation:**  
- Implement proper authentication and authorization controls to restrict access to the PDF.  
- Store sensitive documents in a secure location and enforce access controls via the server or application layer.  
- Audit existing endpoints to ensure no other sensitive files are publicly accessible.

---  

This format clearly communicates the issue, impact, reproduction steps, and provides actionable remediation steps.
