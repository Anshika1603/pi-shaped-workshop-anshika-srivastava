# Day 3 — Secure Coding Practices & Code Scanning

## CI/CD-Based Secure Coding & Code Scanning with Bandit, Semgrep, Gitleaks & OWASP ZAP

## Objective

To integrate Bandit, Semgrep, Gitleaks, and OWASP ZAP into a GitHub Actions CI/CD pipeline for detecting insecure coding practices, hardcoded secrets, and runtime vulnerabilities. To demonstrate remediation by fixing at least one vulnerability and validating the improvement through re-scanning.

---

## GitHub Actions CI/CD Integration

* A workflow `.github/workflows/security-scan-day3.yml` was created to run on every push to the `master` branch.
* Stages:

  * **Bandit scan** → generates `bandit-report.html`.
  * **Semgrep scan** → generates `semgrep-report.json`.
  * **Gitleaks scan** → detects hardcoded secrets.
  * **OWASP ZAP scan (DAST)** → runs against the Flask app on `http://localhost:5000` and generates `zap-report.html`.
* All reports are saved as CI/CD artifacts for review.

---

## Screenshots / Artifacts

* **Bandit Report:** ![bandir report Summary](screenshots/banditReport.png)
* **Semgrep Report:** ![Semgrep report Summary](screenshots/semgrepReport.png)

---

## Vulnerabilities Found

### 1. Hardcoded Secret Key

* **Impact:**
  A hardcoded secret (`SECRET_KEY`) was found in `app.py`. Attackers gaining access to code can hijack Flask sessions because the key is predictable.
* **Recommended Fix:**
  Remove hardcoded values from code. Instead, load secrets from **environment variables** or a **secrets manager**.

  ```python
  import os
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
  ```

---

### 2. Use of `eval()`

* **Impact:**
  The application uses Python’s `eval()` on user input in `app.py`. This is highly dangerous because an attacker can execute **arbitrary Python code**, potentially leading to **remote code execution (RCE)**.
* **Recommended Fix:**
  Avoid `eval()`. If you only need to safely evaluate literals (e.g., numbers, lists, dicts), use `ast.literal_eval()`.

  ```python
  import ast
  cmd = request.args.get('cmd', '')
  try:
      result = ast.literal_eval(cmd)
  except Exception:
      result = "Invalid input"
  ```

---

## Evidence of Fixing One Issue

* **Before:** `app.config['SECRET_KEY'] = 'hardcoded_secret_12345'` flagged by Bandit and Gitleaks.
* **After Fix:**

  ```python
  import os
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-default-secret')
  ```
* **Result:** Re-running Bandit, Semgrep, and Gitleaks locally and in CI/CD showed the hardcoded secret issue was no longer flagged.

* **Bandit Report:** ![bandir report Summary](screenshots/banditReportAfterFix.png)
* **Semgrep Report:** ![Semgrep report Summary](screenshots/semgrepReportAfterFix.png)

---

## Core Concept Questions

### 1. What is the difference between SAST, DAST, and secrets scanning, and why should all be part of a CI/CD pipeline?

* **SAST (Static Application Security Testing):** Scans source code before execution (e.g., Bandit, Semgrep).
* **DAST (Dynamic Application Security Testing):** Tests the running app for real attack vectors (e.g., ZAP).
* **Secrets Scanning:** Detects exposed credentials in repositories (e.g., Gitleaks).
* **Why all three:** They complement each other to provide complete security coverage.

### 2. Why is storing secrets in code dangerous? What’s a secure alternative?

* **Danger:** Secrets committed to code may leak via Git history, forks, or logs.
* **Alternatives:** Environment variables, GitHub Secrets, or enterprise secrets managers (AWS Secrets Manager, Vault, etc.).

### 3. How does adding these scans to a pipeline help enforce Shift-Left Security?

* Runs security checks early in the SDLC.
* Provides developers immediate feedback on vulnerabilities.
* Reduces remediation costs by catching issues before deployment.

### 4. If a scan fails in your pipeline, what is the next step for a developer or DevOps engineer?

* Review the report.
* Validate whether the issue is a **true positive** or **false positive**.
* If valid: create a bug/issue, fix in code, rotate any exposed secrets.
* Push changes → pipeline re-runs and verifies the fix.

---