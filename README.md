# Introduction to feature management with Unleash.io

Welcome to this lab exercise where we will explore feature management using Unleash.

## Overview

In this lab, we will:

* Use the Unleash UI to create a feature toggle
* Utilize AWS Cloud 9, a web-based development environment, to build and run an AWS Lambda function
* Observe how we can switch the toggle on or off and observe the resulting responses
* Deploy the Lambda function and test the API endpoint in a browser

Observe the effects of setting the toggle on or off by viewing the results in our browser.


## Create a toggle in unleash io

* Log in to your Unleash dashboard at https://www.getunleash.io/
* Click on the "Feature Toggles" button on the top navigation menu.
* Click on the "New Feature Toggle" button.
* Enter a name for the feature toggle, including your name to avoid naming conflicts (e.g. glenn_toggle)
* Choose the "Release" toggle type.
* Leave the remaining values as their default.
* Click on the "Create Feature Toggle" button.

## Log in to your AWS Cloud9  environment 

Go to the AWS Management Console (https://244530008913.signin.aws.amazon.com/console) 

* Enter your username (the first part of your email address, before the @ symbol) and the password provided in class.
* Click on the "Sign In" button.
* Once you are logged in, you will be directed to the AWS Management Console home page.
* In the top left corner, you will see a navigation menu. Click on the "Services" button.
* In the services menu, look for the "Cloud9" service.
* Click on the Cloud9 service to open the Cloud9 dashboard.
* You will now be able to see the list of environments that you have access to.
* Select your environment 
* Familiarize yourself with Cloud9 by exploring and experimenting with the platform.

## No auto save! 

The number #1 problem for most students using Cloud9 is that they forget to explicitly save files  - as there is no auto save!

## Clone this repo

Clone this repository into your cloud 9 environment. Use the Terminal on the bottom of the screen in your cloud 9 environment 

```text
git clone https://github.com/glennbechdevops/unleash-feature-management
```

## Add an Unleash token to your template.yml file 

The token will be given in class

````text
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.9
      Environment:
        Variables:
          UNLEASH_API_TOKEN: <insert token here>
      Architectures:
````

Also, in ```app.py``` you need to change the following line to use your feature toggle  

```shell
    if client.is_enabled('glenn_toggle'):
```

## Build and run the Lambda function locally 

```shell
cd unleash-feature-management/
sam build --use-container
sam local invoke
```

The output is not very human readable, but you can see a status code and a text in there ... this will be better after we deploy it and access via browser. 
Typical output for a 200 OK.

```text
Invoking app.lambda_handler (python3.9)
Skip pulling image and use local one: public.ecr.aws/sam/emulation-python3.9:rapid-1.57.0-x86_64.

Mounting /home/ec2-user/environment/unleash-feature-management/.aws-sam/build/HelloWorldFunction as /var/task:ro,delegated inside runtime container
start
[WARNING]       2023-01-25T23:45:17.604Z        15b7c626-1327-47ee-b86c-40d0e9ffdaa4    scheduler_executor should only be used with a custom scheduler.
END RequestId: 15b7c626-1327-47ee-b86c-40d0e9ffdaa4
REPORT RequestId: 15b7c626-1327-47ee-b86c-40d0e9ffdaa4  Init Duration: 0.27 ms  Duration: 713.09 ms     Billed Duration: 714 ms Memory Size: 512 MB     Max Memory Used: 512 MB
{"statusCode": 200, "body": "{\"message\": \"hello world\"}"}test.user:~/environment/unleash-feature-management (main) $ sam local invoke```
```

Try to toggle your feature on and off. When the toggle is off, the lambda should return a HTTP 501 / Not implemented
When enabled, it should return 200 ok


## Deploy the lambda to AWS
```shell
sam deploy --guided
```

Please note that you do not need to provide the "guided" flag after the first deployment has been done. During the deployment process, provide the following input, but use your own name in the stack name.

```
Setting default arguments for 'sam deploy'
=========================================
Stack Name [sam-app]: glenn-app
AWS Region [eu-west-1]:
#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
Confirm changes before deploy [y/N]: N
#SAM needs permission to be able to create roles to connect to the resources in your template
Allow SAM CLI IAM role creation [Y/n]: Y
#Preserves the state of previously provisioned resources when an operation fails
Disable rollback [y/N]: N
HelloWorldFunction may not have authorization defined, Is this okay? [y/N]: Y
Save arguments to configuration file [Y/n]: Y
SAM configuration file [samconfig.toml]:
SAM configuration environment [default]:
```

This will take some time, and when it is done - the Endpoint given to your lambda will be displayed - something like this 
```shell
Key                 HelloWorldApi                                                                                                                                                                                                         
Description         API Gateway endpoint URL for Prod stage for Hello World function                                                                                                                                                      
Value               https://6ztkdjfii8.execute-api.eu-west-1.amazonaws.com/Prod/hello/    
```

You can now test your endpoint in your browser, and change the toggle on- and off at unleash.io and see that the browser either returns 
501 Not implemented- or 200 OK. 

# Bonus challenge; 

Explore the Unleash IO and see if you can create a gradual roll out strategy for your toggle! 
