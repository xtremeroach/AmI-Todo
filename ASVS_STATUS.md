# ASVS Compliance Status: ImA TODO

This document tracks the application's compliance with OWASP ASVS 5.0.0 Level 1 and Level 2 requirements.

## Summary
- **Current Goal**: Reach ASVS Level 1 (Baseline) and implement initial Level 2 controls.
- **Last Review**: 2026-03-10
- **Overall Status**: `[IN PROGRESS]` - Most Level 1 requirements pass, but some are pending/failing. Level 2 has partial coverage.

| Level | Total Req | [PASS] | [FAIL] | [PENDING] | [N/A] |
|-------|-----------|--------|--------|-----------|-------|
| L1    | ~70       | 7      | 1      | 62        | 0     |
| L2    | ~200+     | 1      | 2      | 197+      | 0     |

---

## Level 1 Compliance Details

### V1: Encoding and Sanitization
- [PASS] **V1.2.1**: Output encoding (HTML/CSS/JS) is securely handled by Django's template auto-escaping.
- [PASS] **V1.2.4**: Parameterized queries / ORM usage is strictly enforced by the Django ORM.

### V3: Web Frontend Security
- [PASS] **V3.3.1**: Secure Cookie setup implemented (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` are configured).
- [PASS] **V3.4.1**: HSTS header implemented (`SECURE_HSTS_SECONDS` configured).

### V6: Authentication
- [PASS] **V6.2.1**: Minimum password length (8 characters) enforced via Django `MinimumLengthValidator`.
- [PASS] **V6.2.4**: Common passwords blocked via Django `CommonPasswordValidator`.
- [FAIL] **V6.3.2**: Disable default accounts. The system currently provisions a default `admin` superuser unconditionally during DB setup.

### V7: Session Management
- [PASS] **V7.2.4**: Session regeneration on login is natively handled by Django Auth.

---

## Level 2 Compliance Details (Incremental)

### V3: Web Frontend Security
- [FAIL] **V3.4.3**: Content-Security-Policy (CSP) headers are missing.

### V6: Authentication
- [FAIL] **V6.3.3**: Multi-Factor Authentication (MFA) is not implemented for local users.

### V16: Security Logging and Error Handling
- [PASS] **V16.3.1**: Detailed security logging implemented via the `AuthLog` model to track authentication success/failures.

> [!TIP]
> Run the ASVS review agent periodically to update this document.
