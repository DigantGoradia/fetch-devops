# Fetch Rewards DevOps
> A fetch rewards Devops script that spin up EC2 instance reading configuration from yaml file.
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
