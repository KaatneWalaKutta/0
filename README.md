Below is an example of how you might document this issue:

---

**Title:**  
Publicly Accessible PDF Containing Sensitive Training Material

**Description:**  
An endpoint hosting a PDF file containing persona training material is publicly accessible without any authentication. This exposes potentially sensitive or confidential information to anyone who has or discovers the URL, leading to an information disclosure vulnerability. Lack of access controls violates the principle of least privilege and could result in unauthorized individuals accessing proprietary or private data.

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
