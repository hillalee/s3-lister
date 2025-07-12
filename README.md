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

> ⚠️ The email must be confirmed manually after the first deployment. Check your inbox and confirm the SNS subscription to receive notifications. Notice email may get to spam folder.

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

more response.json
```

### Method 2: Using Python Test Script

```bash
python scripts/test_lambda.py <your-lambda-name>
```

### Method 3: Using JSON Event File
This method has 2 options: via AWS console, and via AWS CLI.
Option 1:
1. Go to AWS Lambda in the console
2. Select the deployed Lambda function
3. Click **Test**, choose or create a new test event with `{}` as the payload
4. Run the test

Option 2:

```bash
aws lambda invoke \
  --function-name <your-lambda-name> \
  --payload file://test_event.json \
  response.json

more response.json
```

## Lambda Function Logic

1. Reads object list from the S3 bucket (set by environment variable)
2. Calculates a summary of object names and sizes
3. Sends an SNS email with the execution report
4. Returns a success message and file count

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

**Resources I particulary enjoyed:**
- [AWS CDK security best practices] [https://docs.aws.amazon.com/cdk/v2/guide/best-practices-security.html#:~:text=Considerations%20for%20granting%20least%20privilege,impact%20developer%20productivity%20and%20deployments.]
- [Security best practices in IAM] [https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html]


---
