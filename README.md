# wiz-lab-devops

## Overview
A comprehensive DevOps security laboratory demonstrating vulnerability detection, secret scanning, and security best practices on AWS App Runner. This repo is designed for security training and demonstrates:
- Intentionally vulnerable container images for security scanning
- Secret detection and sensitive data exposure
- Multi-service architecture (NGINX + Flask)
- AWS App Runner deployment with CI/CD
- Infrastructure as Code (CloudFormation)

⚠️ **WARNING**: This repository contains intentionally vulnerable code and exposed secrets for educational purposes. DO NOT use this code in production environments.

## Architecture
This project deploys a multi-tier application to AWS App Runner, combining NGINX as a reverse proxy with a Python Flask backend:

1. **NGINX Frontend**:
   - Serves static HTML content
   - Acts as reverse proxy to Flask backend
   - **Vulnerable version**: nginx:1.18.0-alpine (contains known CVEs)
   - **Secure alternative**: nginx:alpine (latest)

2. **Flask Backend (Python 3.8)**:
   - REST API with multiple endpoints
   - **Intentionally vulnerable packages**:
     - Flask 1.1.1 (CVE-2023-30861)
     - Werkzeug 0.16.0 (CVE-2023-25577 - High Severity)
     - Jinja2 2.10.1 (CVE-2020-28493)
     - requests 2.20.0 (CVE-2018-18074)
     - urllib3 1.24.1 (Multiple CVEs)
   - Demonstrates common web vulnerabilities (SSTI, insecure deserialization)

3. **Security Issues Demonstrated**:
   - **Container Vulnerabilities**: Outdated base images and packages
   - **Secret Exposure**: Fake API keys and tokens in `website/keys.txt`
   - **Sensitive Data**: Sample PII data in `website/sample_data.txt`
   - **Vulnerable Dependencies**: Outdated jQuery (1.8.3) loaded from CDN
   - **Code Vulnerabilities**: SSTI, pickle deserialization, debug mode enabled

4. **AWS Infrastructure**:
   - **ECR**: Stores the Docker container images
   - **App Runner**: Runs the containerized application
   - **Route53**: Manages DNS for custom domain

5. **CI/CD**:
   - GitHub Actions workflows for automated deployment
   - Separate workflows for deploy, update, and delete operations

## Security Demonstrations

### Vulnerability Scanning
This repository is designed to trigger alerts in security scanning tools:

#### Container Vulnerabilities
- **NGINX**: Using version 1.18.0-alpine with known security issues
- **Python packages**: Multiple outdated dependencies with documented CVEs
- **Alpine Linux**: Older base image version

#### Secret Scanning
The `website/keys.txt` file contains fake credentials that should be detected by secret scanning tools:
- GitHub tokens
- Okta API tokens
- Square payment tokens

**Note**: All secrets in this repo are fake and for demonstration purposes only.

#### Sensitive Data Exposure
The `website/sample_data.txt` file contains sample PII (personally identifiable information):
- Social Security Numbers
- Credit card numbers
- Email addresses
- Physical addresses

This data is synthetic and demonstrates data exposure risks.

#### Application Vulnerabilities
The Flask application includes vulnerable code patterns:
- **Server-Side Template Injection (SSTI)**: `/api/greet` endpoint
- **Insecure Deserialization**: `/api/deserialize` endpoint using pickle
- **Debug Mode**: Flask running with debug=True
- **No Authentication**: API endpoints exposed without auth

### Flask API Endpoints

The application exposes several API endpoints for testing:

- `GET /api/info` - Returns version information for Flask, Werkzeug, and Jinja2
- `GET /api/health` - Health check endpoint
- `GET /api/vulnerable-data` - Returns information about known vulnerabilities
- `GET /api/greet?name=<name>` - Demonstrates SSTI vulnerability
- `POST /api/deserialize` - Demonstrates insecure pickle deserialization

## GitHub Actions Workflows
The repository includes three main workflows:
- `aws-apprunner-site-deploy.yml`: Initial deployment
- `aws-apprunner-site-updates.yml`: Update existing deployment
- `aws-apprunner-site-delete.yml`: Remove all resources

## Usage

### Deploying the Application
1. Configure AWS credentials in GitHub Secrets
2. Use the provided GitHub Actions workflow or manually trigger the deployment
3. The workflow will:
   - Create an ECR repository
   - Build and push the Docker image
   - Deploy to App Runner
   - Configure DNS for custom domain

### Security Testing Workflow
1. **Deploy vulnerable version** (default):
   - Uses outdated NGINX and Python packages
   - Exposes secrets and PII
   - Includes vulnerable code patterns

2. **Run security scans**:
   - Container image scanning (Wiz, Snyk, Trivy, etc.)
   - Secret scanning (GitGuardian, TruffleHog, etc.)
   - SAST/DAST tools

3. **Remediate** (optional):
   - Uncomment secure versions in Dockerfile
   - Update Flask dependencies in `requirements.txt`
   - Remove sensitive data files
   - Fix vulnerable code patterns

### Switching Between Vulnerable and Secure Versions

#### NGINX Version
In `Dockerfile`, switch between:
```dockerfile
# Vulnerable (default)
FROM nginx:1.18.0-alpine

# Secure
# FROM nginx:alpine
```

#### Python Packages
In `website/flask-app/requirements.txt`, replace vulnerable packages with secure versions:
```python
# Vulnerable (default)
Flask==1.1.1
Werkzeug==0.16.0
Jinja2==2.10.1

# Secure (commented out)
# Flask==3.0.0
# Werkzeug==3.0.1
# Jinja2==3.1.3
```

## Development

### Project Structure
```
wiz-lab-devops/
├── Dockerfile                    # Multi-stage build with NGINX + Flask
├── website/
│   ├── index.html               # Frontend with API integration
│   ├── keys.txt                 # Fake secrets for scanning demos
│   ├── sample_data.txt          # Sample PII data
│   ├── nginx.conf               # NGINX reverse proxy config
│   ├── supervisord.conf         # Process manager config
│   └── flask-app/
│       ├── app.py               # Flask API with vulnerabilities
│       └── requirements.txt     # Vulnerable Python packages
├── aws/
│   ├── ecr-create.yaml          # ECR CloudFormation template
│   ├── apprunner-create.yaml    # App Runner CloudFormation template
│   └── route53-records.yaml     # DNS CloudFormation template
└── .github/workflows/           # CI/CD workflows
```

### Modifying the Website
1. Edit files in the `website/` directory
2. Changes will trigger the update workflow automatically (if configured)

### Local Testing
To run the container locally:

```bash
# Build the image
docker build -t nginx-flask-demo .

# Run the container
docker run -d -p 8080:80 -p 5000:5000 nginx-flask-demo

# Test the application
curl http://localhost:8080                    # NGINX static content
curl http://localhost:8080/api/info           # Flask API via NGINX proxy
```

Then visit http://localhost:8080 in your browser.

### Testing Individual Services
```bash
# Test Flask API directly
curl http://localhost:5000/api/health

# Test vulnerable endpoint
curl http://localhost:5000/api/greet?name=test

# Check versions
curl http://localhost:5000/api/info
```

## Security Remediation

To convert this from a vulnerable demo to a secure deployment:

1. **Update Dockerfile**:
   - Use `nginx:alpine` instead of `nginx:1.18.0-alpine`
   - Update Python packages to latest versions

2. **Remove sensitive files**:
   ```bash
   rm website/keys.txt
   rm website/sample_data.txt
   ```

3. **Fix Flask vulnerabilities**:
   - Update `requirements.txt` to latest package versions
   - Remove vulnerable endpoints (`/api/greet`, `/api/deserialize`)
   - Disable debug mode
   - Add authentication

4. **Update frontend**:
   - Update jQuery to latest version
   - Remove references to vulnerable endpoints

## Learning Objectives

This lab teaches:
- How to identify container vulnerabilities
- Secret detection in source code
- PII and sensitive data exposure risks
- Common web application vulnerabilities
- Security scanning tool integration
- Remediation strategies
- Secure CI/CD practices

## License

This project is for educational purposes only. The intentionally vulnerable code should never be used in production environments.
