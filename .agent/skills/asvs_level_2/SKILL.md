---
name: Implement ASVS Level 2
description: Guidelines and instructions for implementing OWASP Application Security Verification Standard (ASVS) Level 2 requirements (incremental to Level 1) based on the project's official CSV.
---

# ASVS Level 2 Implementation Guide (Incremental)

This skill provides instructions for ensuring a web application meets the OWASP ASVS Level 2 requirements, as defined in `OWASP_Application_Security_Verification_Standard_5.0.0_en.csv`.

> [!NOTE]
> Level 2 is cumulative. You **must** satisfy all Level 1 requirements first (see ASVS Level 1 skill). This guide only lists the **new** requirements introduced at Level 2.

## Instructions
1. **Verify Level 1:** Ensure all Level 1 controls are in place.
2. **Review CSV:** This checklist is derived from the `req_id` and `req_description` fields where `L` is 2.
3. **Analyze & Implement:** Check the codebase for these specific Standard Assurance controls.
4. **Report Status:** Update the `ASVS_STATUS.md` file in the project root to reflect the current compliance state for Level 2 items.

## Reporting Compliance
Maintain the `ASVS_STATUS.md` file in the project root. Ensure Level 2 items are clearly marked as such and their status is tracked alongside Level 1 items to provide a holistic overview.

## Level 2 Incremental Checklist

### V1: Encoding and Sanitization
- [ ] **V1.1.1**: Verify that input is decoded or unescaped into a canonical form only once before processing.
- [ ] **V1.1.2**: Verify that the application performs output encoding and escaping either as a final step or by the interpreter itself.
- [ ] **V1.2.6**: Verify protection against LDAP injection vulnerabilities.
- [ ] **V1.2.7**: Verify protection against XPath injection attacks (parameterization/precompiled queries).
- [ ] **V1.2.9**: Verify that special characters in regular expressions are escaped.
- [ ] **V1.3.3**: Verify that data passed to potentially dangerous contexts is sanitized (safe characters, length trimming).
- [ ] **V1.3.6**: Verify protection against SSRF (allowlist of protocols, domains, paths, ports).
- [ ] **V1.5.2**: Verify deserialization of untrusted data enforces safe handling (allowlist of object types).

### V2: Validation and Business Logic
- [ ] **V2.1.2**: Verify documentation defines how to validate logical/contextual consistency of combined data (e.g., suburb/ZIP match).
- [ ] **V2.3.2**: Verify business logic limits are implemented as documented.
- [ ] **V2.3.3**: Verify transactions are used (all-or-nothing logic).
- [ ] **V2.4.1**: Verify anti-automation controls protect against excessive calls (exfiltration, DoS, quota exhaustion).

### V3: Web Frontend Security
- [ ] **V3.3.2**: Verify 'SameSite' attribute on cookies is set according to purpose (CSRF/UI redress protection).
- [ ] **V3.3.4**: Verify 'HttpOnly' for non-script-accessible cookies (session tokens).
- [ ] **V3.4.3**: Verify **Content-Security-Policy (CSP)** header is included to limit malicious JS.
- [ ] **V3.4.4**: Verify 'X-Content-Type-Options: nosniff' header is present.
- [ ] **V3.4.6**: Verify 'frame-ancestors' directive in CSP to prevent clickjacking.

### V6: Authentication
- [ ] **V6.2.11**: Verify a documented list of context-specific words is used to prevent easy-to-guess passwords.
- [ ] **V6.3.3**: Verify **Multi-Factor Authentication (MFA)** or combination of factors is used.
- [ ] **V6.4.3**: Verify secure password reset process does not bypass MFA.
- [ ] **V6.8.2**: Verify digital signatures on authentication assertions (JWT/SAML) are always validated.

### V7: Session Management
- [ ] **V7.1.1**: Verify session inactivity timeout and absolute maximum lifetime are documented.
- [ ] **V7.3.1**: Verify presence of an **inactivity timeout**.

### V11: Cryptography
- [ ] **V11.1.1**: Verify documented policy for management of cryptographic keys/lifecycle.
- [ ] **V11.4.2**: Verify passwords are stored using approved, computationally intensive KDFs (password hashing).
- [ ] **V11.5.1**: Verify random numbers/strings are generated using a **CSPRNG** with 128 bits of entropy.

### V13: Configuration
- [ ] **V13.2.1**: Verify backend components (APIs, middleware) use individual service accounts or short-term tokens for authentication.
- [ ] **V13.3.1**: Verify use of a **secrets management solution** (key vault).
- [ ] **V13.4.2**: Verify debug modes are disabled in production.

### V16: Security Logging and Error Handling
- [ ] **V16.3.1**: Verify all authentication operations (success/fail) are logged with metadata.
- [ ] **V16.5.1**: Verify generic error messages are returned (no stack traces/secret keys).
