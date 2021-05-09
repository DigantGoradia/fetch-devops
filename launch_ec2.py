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

#AWS resources initialization
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

#Create key-pair
try:
    print('Creating key-pair...')
    keyName ='fetch-rewards-user'
    key_response = ec2_client.create_key_pair(KeyName = keyName)
    with open('private.pem', 'w') as key:
        key.write(str(key_response['KeyMaterial']))
except Exception as e:
    print(e)

# create VPC and other resources
try:
    vpc = ec2_resource.create_vpc(CidrBlock='10.10.0.0/16')
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "fetchReward_exe_vpc"}])
    vpc.wait_until_available()
    print(vpc.id)

    # create then attach internet gateway
    ig = ec2_resource.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    print(ig.id)

    # create a route table and a public route
    route_table = vpc.create_route_table()
    route = route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=ig.id
    )
    print(route_table.id)

    # create subnet
    subnet = ec2_resource.create_subnet(CidrBlock='10.10.1.0/24', VpcId=vpc.id)
    print(subnet.id)

    # associate the route table with the subnet
    route_table.associate_with_subnet(SubnetId=subnet.id)

    # Create sec group
    sec_group = ec2_resource.create_security_group(
        GroupName='sec_group_fetchRewards', Description='Fetch Rewards Security Group', VpcId=vpc.id)
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22
    )
    print(sec_group.id)
except Exception as e:
    print(e)

#Create ec2 instance
try:
    print('Creating EC2 instance...')
    ec2_client.run_instances(
        BlockDeviceMappings = blockDevices,
        ImageId = imageId,
        InstanceType = instanceType,
        MinCount = minCount,
        MaxCount = maxCount,
        NetworkInterfaces = [
            {
                'SubnetId': subnet.id,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [sec_group.group_id]
            }
        ],
        KeyName = keyName
    )

    ec2_client.instances[0].wait_until_running()
    print('EC2 instance created: ', ec2_client.instances[0].id)
except Exception as e:
    print(e)

