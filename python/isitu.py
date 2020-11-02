import boto3
from typing import List, Union
import json


def all_public_amis_by_path_from_ssm():
    """
    The AWS CLI equivalent of:
    aws ssm get-parameters-by-path
    --path "/aws/service/ami-amazon-linux-latest"
    --region us-east-1
    """
    ssm = boto3.client('ssm')
    response = ssm.get_parameters_by_path()
    return response

def get_ami_data(names: Union[str, List[str]]=None) -> List[dict]:
    if names is None:
        names = [
            '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
        ]
    elif isinstance(names, str):
        names = [names]
    ssm = boto3.client('ssm')
    response = ssm.get_parameters(Names=names)
    metadata: dict = response['ResponseMetadata']
    if metadata['HTTPStatusCode'] == 200:
        params: List[dict] = response['Parameters']
        amis_data: List[dict] = [json.loads(p['Value']) for p in params]
        return amis_data
    return

def get_ami_id(names: Union[str, List[str]]=None) -> List[str]:
    amis_data = get_ami_data(names)
    ids = [value.get('image_id') for value in amis_data]
    return ids

def get_all_region_names() -> List[str]:
    client = boto3.client('ec2')
    response = client.describe_regions()
    regions: List[dict] = response.get('Regions')
    names: List[str] = [r['RegionName'] for r in regions]
    return names

def create_key_pair(key_name: str) -> dict:
    """
    Creates a 2048-bit RSA key pair with the specified name.
    Returns an unencryptem PEM RSA private key.
    """
    client = boto3.client('ec2')
    response = client.create_key_pair(KeyName=key_name)
    pem: str = response['KeyMaterial']
    return pem

ssm_ami = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended"
print(get_ami_id([ssm_ami]))