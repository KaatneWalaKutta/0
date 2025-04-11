pandas
pdfplumber
python-docx
openpyxl


Unauthorized User Deprovisioning via Insecure API Endpoint


An API endpoint (/kioskmode/sessions/${n.kiosk_mode_session_id}/users/deprovision) was discovered in a JavaScript file, which allows an authenticated user to deprovision other users by substituting a valid kiosk_mode_session_id (GUID) obtained from another endpoint (/kioskmode/sessions). The JSON response from /kioskmode/sessions initially shows "is_deprovisioned_successfully": false, but after sending a deprovision request to the endpoint, it updates to "is_deprovisioned_successfully": true. This suggests that the endpoint lacks proper authorization checks, potentially allowing an authenticated user to deprovision users or sessions they should not have access to, leading to privilege escalation or unauthorized account manipulation.

Steps to Reproduce:

Log in to the application to establish an authenticated session.
Locate the JavaScript file containing the API endpoint path: /kioskmode/sessions/${n.kiosk_mode_session_id}/users/deprovision.
Send a GET request to /kioskmode/sessions (e.g., using a browser or a tool like curl or Postman) to retrieve a JSON response containing a list of sessions.
Identify a valid kiosk_mode_session_id (a GUID) from the response body (e.g., "kiosk_mode_session_id": "123e4567-e89b-12d3-a456-426614174000").
Check the initial state by inspecting the JSON response from /kioskmode/sessions, noting that "is_deprovisioned_successfully": false for the targeted session.
Send a request (e.g., POST or DELETE) to the deprovision endpoint with the substituted GUID:
Example: POST /kioskmode/sessions/123e4567-e89b-12d3-a456-426614174000/users/deprovision.
Re-check the /kioskmode/sessions endpoint and observe that "is_deprovisioned_successfully": true for the targeted session, confirming the deprovisioning occurred.

Enforce Proper Authorization Checks: Ensure the deprovision endpoint (/kioskmode/sessions/{session_id}/users/deprovision) validates that the authenticated user has explicit permission to deprovision the specified session or user. For example, tie the action to a role-based access control (RBAC) system where only administrators or authorized personnel can perform this operation.
