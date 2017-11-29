# PoC environment

Simple CloudFormation stack which creates development environment which is automatically provisioned using [CloudConfig](https://coreos.com/os/docs/latest/cloud-config.html) and installs [CoreOS](https://coreos.com) as operating system.

Components:
- VPC + public Subnet connected to InternetGateway
- ECR
- EC2 with AutoScaling group and LunchConfiguration 
- S3 bucket
- Security Groups
- IAM role for above AWS resources

## Environment bootstrap

This section consists of step by step guide how bootstrap PoC development environment.

### Render CloudFormation stack

Run:

    cd scripts/
    pip install -r requirements.txt
    python render.py --user-data ../poc-user-data.yaml --template ../poc.stack.yaml.tmpl --output ../poc.stack.yaml

### Generate SSH access key
  
Go to the AWS Management Console -> EC2 -> Key Pairs.    
    
For more information take a look at [Amazon EC2 Key Pairs](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
    
### Apply CloudFormation stack    
    
Go to the AWS Management Console -> CloudFormation -> Create Stack.

## SSH access

In order to connect over ssh to one of the EC2 instance you have to open AWS SecurityGroup on port 22.
Then:

    ssh -i ssh_key.pem core@IP

## Running application

In terms of CoreOS everything is based on docker containers or systemd services. 
You can run standalone docker container using `docker run .. ` or take a look at `pos-user-data.yaml` and
uncomment systemd service:

    - name: app.service
      command: "start"
      content: |
        [Unit]
        Description=Start
        Wants=docker.service ecr-login.service
    
        [Service]
        Restart=always
        RestartSec=5
        TimeoutSec=60
        ExecStartPre=-/usr/bin/docker rm -f app
        ExecStart=/usr/bin/docker run --rm --name app 003048186787.dkr.ecr.eu-west-1a.amazonaws.com/poc:latest
        ExecStop=/usr/bin/docker rm -f app

For more information take a look at [Getting started with systemd](https://coreos.com/os/docs/latest/getting-started-with-systemd.html).



    
