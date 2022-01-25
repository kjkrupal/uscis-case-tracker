# Serverless USCIS Case Tracker 

A simple serverless app that runs on a schedule and sends USCIS case status updates. To configure your schedule,
USCIS case number and recipient email, edit the `environment.ini` file.

This project uses aws cdk to deploy stack. See the following steps to set up your project and deploy your app.

## Setup

### Install aws cli
Refer the AWS documentation to install aws cli. [Click here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

### Install aws cdk
Refer the AWS documentation to install aws cdk. [Click here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html).

### Create and activate virtualenv
```
$ python3 -m venv .venv
$ source .venv/bin/activate -- For mac/linux users
$ .venv\Scripts\activate.bat -- For windows users
```

### Install the required dependencies
```
$ pip install -r requirements.txt
```

### Synthesize and deploy your cdk app
```
$ cdk synth
$ cdk bootstrap --profile <<< YOUR_AWS_PROFILE >>>
$ cdk deploy --profile <<< YOUR_AWS_PROFILE >>>
```
