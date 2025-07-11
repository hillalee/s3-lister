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
- Node.js and npm installed (for AWS CDK)
- Python 3.8+ installed
- AWS CDK installed:
  ```bash
  npm install -g aws-cdk
  ```

## Setup and Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/hillalee/serverless-s3-lister.git
cd serverless-s3-lister
```

### 2. Install Python and CDK dependencies

```bash
# Python requirements
pip install -r requirements.txt

# CDK dependencies
npm install
```

### 3. Bootstrap CDK (first time only)

```bash
cdk bootstrap
```

### 4. Deploy the stack

```bash
cdk deploy -c email=your@email.com
```

> ⚠️ The email must be confirmed manually after the first deployment. Check your inbox and confirm the SNS subscription to receive notifications.

## Project Structure

```
serverless-s3-lister/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── lambda/
│   ├── s3_lister.py            # Lambda function
│   └── requirements.txt
├── sample_files/               # Sample files uploaded during deployment
│   ├── document1.txt
│   └── image1.jpg
├── scripts/
│   ├── test_lambda.py          # Manual Lambda trigger script
│   └── upload_files.py         # Optional S3 upload script
├── serverless_stack.py         # CDK Stack definition
├── app.py                      # CDK entry point
├── requirements.txt            # Python dependencies
├── cdk.json                    # CDK config file
└── README.md
```

## Manual Lambda Testing

### Method 1: Using AWS CLI

```bash
aws lambda invoke \
  --function-name <your-lambda-name> \
  --payload '{}' \
  response.json

cat response.json
```

### Method 2: Using Python Test Script

```bash
python scripts/test_lambda.py
```

### Method 3: Using AWS Console

1. Go to AWS Lambda in the console
2. Select the deployed Lambda function
3. Click **Test**, choose or create a new test event with `{}` as the payload
4. Run the test

## Lambda Function Logic

1. Reads object list from the S3 bucket (set by environment variable)
2. Calculates a summary of object names and sizes
3. Sends an SNS email with the execution report
4. Returns a success message and file count

## GitHub Actions

The workflow in `.github/workflows/deploy.yml` uses `workflow_dispatch` to allow manual deployment from the GitHub UI. It installs dependencies, bootstraps CDK, and deploys the stack using the email context parameter.

## Troubleshooting

1. **Email not received**: Make sure to confirm the SNS subscription manually.
2. **Bucket name already taken**: Modify the CDK bucket name to be unique (e.g., append your username or use a hash).
3. **Lambda timeout**: You can increase the timeout in `serverless_stack.py`.
4. **Deployment failed**: CDK automatically rolls back changes on failure. Make sure all parameters are valid.

## Resources and Documentation

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---
