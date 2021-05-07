import yaml
import boto3

CONFIG_FILE = './config.yaml'

#Try laoding the config file
try:
    config = yaml.safe_load(CONFIG_FILE)
except Exception as e:
    print('An Error occurred: ', e)
