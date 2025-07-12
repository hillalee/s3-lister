# Serverless S3 Object Lister with Email Notifications (CDK Version)

A fully automated serverless application built with **AWS CDK** that lists objects from an S3 bucket and sends email notifications via SNS upon execution. This project demonstrates Infrastructure as Code (IaC) best practices, CI/CD automation, and AWS-managed services.

## Architecture Overview

This application consists of:
- **AWS Lambda Function**: Lists S3 objects and publishes messages to SNS
- **S3 Bucket**: Stores sample files uploaded during deployment
- **SNS Topic**: Sends email notifications when Lambda executes
- **IAM Role**: Provides least-privilege permissions for Lambda
- **GitHub Actions**: Automates CDK deployment

## Features

- Fully serverless design using AWS Lambda, S3, and SNS
- Infrastructure defined and deployed using AWS CDK
- Email notifications sent on each Lambda invocation
- Automatic file upload to S3 during deployment
- Manual Lambda invocation for testing
- CI/CD pipeline via GitHub Actions
- Runtime parameters passed using CDK context (`cdk deploy -c email=you@example.com`)
- Safeguards for email confirmation and resource reuse

## Prerequisites

- AWS CLI configured (`aws configure`)
- Python 3.11+ installed
- AWS CDK installed:
  ```bash
  npm install -g aws-cdk
  ```

## Setup and Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/hillalee/s3-lister.git
cd s3-lister
```


### 2. Manage Github Secrets

In order to login to AWS services, you need to insert your credentials as secrets. You can read about github secrets [here](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions). 
You can view your credentials running ```cat ~/.aws/credentials``` (on a linux machine).
You can either update them in the github website, or through using the GitHub CLI tool (`gh`):
#### Steps:

1. **Install GitHub CLI** (if you haven't yet):
   ```bash
   # Windows (winget)
   winget install --id GitHub.cli

   # macOS (Homebrew)
   brew install gh

   # Linux (apt)
   sudo apt install gh
   ```

2. **Authenticate to GitHub:**
   ```bash
   gh auth login
   ```

3. **Set or update your AWS credentials:**

   ```bash
   gh secret set AWS_ACCESS_KEY_ID --body "AKIA123EXAMPLE" --repo hilalee/s3-lister
   gh secret set AWS_SECRET_ACCESS_KEY --body "mySecretKeyHere" --repo hilalee/s3-lister
   ```

This securely updates your secrets, which are used by the GitHub Actions workflow.


### 3. Deploy Github Actions Workflow
In order to deploy the workflow, we have two options:

---

#### Option 1: Via Web Browser (GitHub UI)

1. Open your GitHub repository in a web browser.
2. Click the **Actions** tab.
3. Select the **CDK Deploy** workflow from the list.
4. Click the **Run workflow** button (top right).
5. Enter your email address for SNS notifications in the input field.
6. Click **Run workflow** to start the deployment.

The workflow will handle the full deployment and upload sample files automatically.

---

#### Option 2: Via GitHub CLI (`gh`)

Make sure you have the GitHub CLI installed and authenticated.

Run this command in your terminal inside the repo folder:

```bash
gh workflow run deploy.yml --ref main --field email=your@email.com
```

> ⚠️ The email must be confirmed manually after the first deployment. Check your inbox and confirm the SNS subscription to receive notifications. Notice email may get to spam folder.


## Project Structure

```
s3-lister/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── lambda/
│   ├── lambda_handler.py       # Lambda function
│   └── requirements.txt
├── sample_files/               # Sample files uploaded during deployment
│   ├── doc1.txt
│   ├── doc2.txt
│   └── belle.jpg
├── scripts/
│   ├── test_event.json          # Manual Lambda trigger script
│   ├── test_lambda.py          # Manual Lambda trigger script
│   └── upload_files.py         # Optional S3 upload script
├── stacks/
│   ├── __init__.py           
│   └── serverless_stack.py
├── app.py                      # CDK entry point
├── requirements.txt            # Python dependencies
├── cdk.json                    # CDK config file
├── package.json                # node dependencies
└── README.md
```

## Manual Lambda Testing

### Method 1: Using Python Test Script

```bash
python scripts/test_lambda.py <your-lambda-name>
```

### Method 2: Using AWS CLI

```bash
aws lambda invoke \
  --function-name <your-lambda-name> \
  --payload '{}' \
  response.json

more response.json
```
> On PowerShell, use backticks (`) instead of \.




## Lambda Function Logic

1. Reads object list from the S3 bucket (set by environment variable)
2. Calculates a summary of object names 
3. Sends an SNS email with the execution report
4. Returns a success message 

## GitHub Actions

The workflow in `.github/workflows/deploy.yml` uses `workflow_dispatch` to allow manual deployment from the GitHub UI. It installs dependencies, bootstraps CDK, and deploys the stack using the email context parameter.The workflow automates the complete deployment process through the following steps:

1. Manual Trigger - Workflow can be triggered manually with an email parameter for notifications
2. Environment Setup - Configures Python 3.11 environment and installs project dependencies
3. AWS Configuration - Sets up AWS credentials and bootstraps CDK environment
4. Infrastructure Deployment - Deploys the complete CDK stack (Lambda, S3, IAM roles) to AWS
5. Sample Data Upload - Automatically uploads sample files to the newly created S3 bucket
6. Event-Driven Processing - Lambda function is pre-configured to trigger on any new file uploads

## Troubleshooting

1. **Email not received**: Make sure to confirm the SNS subscription manually.
2. **Lambda timeout**: You can increase the timeout in `serverless_stack.py`.
3. **Deployment failed**: CDK automatically rolls back changes on failure. Make sure all parameters are valid.

## Resources and Documentation I've Used

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

**Resources I particularly enjoyed:**
- [AWS CDK security best practices](https://docs.aws.amazon.com/cdk/v2/guide/best-practices-security.html#:~:text=Considerations%20for%20granting%20least%20privilege,impact%20developer%20productivity%20and%20deployments.)
- [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples/tree/main)

## Extra Features
I added some extra features to this project:
- Lambda function is invoked each time files are uploaded to S3 bucket.

Features or I would add or change in the future:
1. Cleaner bootstrap first run, maybe just using default email instead of a flag.
2. When uploading multiple files, lambda is sending an email after each time. I would limit it to each group upload.
3. Lambda is using its env vars when invoked - for scalability, use event and context instead.

## About
This project was made with ♥ by Hilalee. AWS is super cool! 

---
