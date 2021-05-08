from os import read
import yaml
import boto3

CONFIG_FILE_PATH = './config.yaml'

with open(CONFIG_FILE_PATH, 'r') as config_file:
    data = config_file.read()

#Try laoding the config file
try:
    config = yaml.safe_load(data)
except Exception as e:
    print('An Error occurred: ', e)

#Read necessary configurations for creating ec2
instanceType = config['server']['instance_type']
imageId = config['server']['ami_type']
minCount = config['server']['min_count']
maxCount = config['server']['max_count']
vol1_device = config['server']['volumes'][0]['device']
vol1_size = int(config['server']['volumes'][0]['size_gb'])
vol2_device = config['server']['volumes'][1]['device']
vol2_size = int(config['server']['volumes'][1]['size_gb'])

#Create ec2 instance
try:
    ec2 = boto3.client('ec2')

    print('Creating EC2 instance...')
    ec2.run_instances(
        ImageId = imageId,
        InstanceType = instanceType,
        MinCount = minCount,
        MaxCount = maxCount 
    )
except Exception as e:
    print('An Error occurred: ', e)

