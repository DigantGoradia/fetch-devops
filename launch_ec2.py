import yaml
import boto3

CONFIG_FILE_PATH = './config.yaml'

with open(CONFIG_FILE_PATH, 'r') as config_file:
    data = config_file.read()

#Try laoding the config file
try:
    config = yaml.safe_load(data)
except Exception as e:
    print(e)

#Read necessary configurations for creating ec2
instanceType = config['server']['instance_type']
imageId = config['server']['ami_type']
minCount = config['server']['min_count']
maxCount = config['server']['max_count']
virtualizationType = config['server']['virtualization_type']

blockDevices = []
for volume in config['server']['volumes']:
    volumeConfig = {
        'DeviceName': volume['device'],
        'Ebs': {
            'VolumeSize': volume['size_gb'],
            #'VolumeType': volume['type']
        }
    }

    blockDevices.append(volumeConfig)

print(blockDevices)

#Create ec2 instance
try:
    ec2 = boto3.client('ec2')

    print('Creating EC2 instance...')
    ec2.run_instances(
        BlockDeviceMappings = blockDevices,
        ImageId = imageId,
        InstanceType = instanceType,
        MinCount = minCount,
        MaxCount = maxCount
    )
except Exception as e:
    print(e)

