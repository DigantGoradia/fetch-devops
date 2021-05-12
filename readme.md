# Fetch Rewards DevOps
> A fetch rewards Devops script that spin up EC2 instance reading configuration from yaml file.
## Prerequisites
Before running the scripts, aws credentials are necessary to setup in the system.
This can be achieve through 2 different ways.
Reference: [configure aws in your system](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
1. install ```aws cli``` and configure the credentials
2. create .aws directory in user home directory and initialize necessary parameters in the files 
## Usage
1. Install required packages
```
pip3 install -r requirements.txt
```
2. Run launch_ec2.py script to spin up EC2 instance. this script will generate key-pair for all users in the format ```<username>.pem```. 
```
python launch_ec2.py
```
3. Running above python script will show the public IPv4 address of initiated EC2 instance, using that ip address ssh into instance.
```
ssh -i <username>.pem <usaername>@<public ip address>
```
