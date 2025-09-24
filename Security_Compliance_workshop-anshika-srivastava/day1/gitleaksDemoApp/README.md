### How gitleaks was configured and run?

- Installed the correct release binary of gitleaks, extracted it and placed it in **/usr/local/bin**, Ran following commands.
> curl -LO https://github.com/gitleaks/gitleaks/releases/download/v8.28.0/gitleaks_8.28.0_linux_x64.tar.gz

> tar -xzvf gitleaks_8.28.0_linux_x64.tar.gz

> chmod +x gitleaks

> sudo mv gitleaks /usr/local/bin/gitleaks

- Verified with:
> gitleaks version

- Commited the changes, and then ran the following command:
> gitleaks detect

It detects for any secret leaks in staged files and commit history.

- Generated the report using the following command.
> gitleaks detect --report-path=gitleaks-report.json --report-format=json

### Steps to remove secrets
- Install git-filter-repo using following command:
> sudo apt install git-filter-repo

- Replace the secret text in the commit history using this command:
> git filter-repo --replace-text <(echo "oldSecret==>REDACTED")

- force push after cleaning

### Shift left Security and it's importance

The practice of integrating security measure earlier in the **SDLC** rather than waiting until
end.

- Fixing security issues early is cheaper and faster than fixing them post-release.
- Prevents serious security incidents by integrating protection from the beginning.
- fixing a vulnerability in production can be more expensive than fixing it during development.
- By embedding security in the process, releases can happen faster without last-minute security emergencies.
- Developers become more security-conscious, leading to better coding practices overall.

### How does detecting secrets early in the CI/CD pipeline prevent production vulnerabilities?

- Prevents sensitive credentials from reaching production or public repositories.
- Attackers cannot exploit hard-coded secrets.
- Encourages use of environment variables, secret managers, or vaults.

### What strategies can be used to store secrets securely instead of hardcoding them?

- Store secrets in environment variables injected at runtime.
- Use secret managers or vaults (e.g., Azure Key Vault, AWS Secrets Manager, HashiCorp Vault).
- Use encrypted configuration files and decrypt them at runtime.

### Describe a situation where a secret could still be exposed even after scanning, and how to prevent it.

- Define custom patterns in a .toml configuration file for Gitleaks to detect project-specific secrets.
- Rotate any exposed secrets immediately after detection.
- Combine scanning with proper secret management practices to reduce risks.


 