# ASVS Compliance Status: ImA TODO

This document tracks the application's compliance with OWASP ASVS 5.0.0 Level 1 and Level 2 requirements.

## Summary
- **Current Goal**: Reach ASVS Level 1 (Baseline) and implement initial Level 2 controls.
- **Last Review**: 2026-03-10
- **Overall Status**: `[IN PROGRESS]`

| Level | Total Req | [PASS] | [FAIL] | [PENDING] | [N/A] |
|-------|-----------|--------|--------|-----------|-------|
| L1    | ~70       | 0      | 0      | 70        | 0     |
| L2    | ~200+     | 0      | 0      | 200+      | 0     |

---

## Level 1 Compliance Details

### V1: Encoding and Sanitization
- [PENDING] **V1.2.1**: Output encoding (HTML/CSS/JS).
- [PENDING] **V1.2.4**: Parameterized queries / ORM usage (Django ORM generally handles this).

### V6: Authentication
- [PENDING] **V6.2.1**: Minimum password length (8 characters).
- [PENDING] **V6.3.2**: Disable default accounts.

### V7: Session Management
- [PENDING] **V7.2.4**: Session regeneration on login.

---

## Level 2 Compliance Details (Incremental)

### V3: Web Frontend Security
- [PENDING] **V3.4.3**: Content-Security-Policy (CSP) headers.

### V6: Authentication
- [PENDING] **V6.3.3**: Multi-Factor Authentication (MFA).

### V18: Logging and Reporting
- [PENDING] **V18.1.1**: Detailed security logging.

> [!TIP]
> Run the ASVS review agent periodically to update this document.
