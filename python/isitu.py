from json.decoder import JSONDecodeError
import boto3
from typing import List, Union
import json


def all_public_amis_by_path_from_ssm(path: str=None):
    """
    The AWS CLI equivalent of:
    aws ssm get-parameters-by-path
    --path "/aws/service/ami-amazon-linux-latest"
    --region us-east-1
    """
    if path is None:
        path = "/aws/service/ami-amazon-linux-latest"
    ssm = boto3.client('ssm')
    response = ssm.get_parameters_by_path(Path=path)
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
        try:
            amis_data: List[dict] = [json.loads(p['Value']) for p in params]
        except JSONDecodeError:
            amis_data: List[dict] = [p['Value'] for p in params]
        return amis_data
    return

def get_ami_id(names: Union[str, List[str]]=None) -> List[str]:
    amis_data = get_ami_data(names)
    if isinstance(amis_data[0], dict):
        ids = [value.get('image_id') for value in amis_data]
    else:
        ids = amis_data
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

if  __name__ == '__main__':
    print('Examples:\n')
    ssm_ami = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended"
    print('ECS Optimized AMI id', get_ami_id([ssm_ami]), sep='\n')
    print('Linux 2 AMI ID', get_ami_id(), sep='\n')
    print('All region names:', get_all_region_names(), sep='\n')
    print('All public AMIS by path', all_public_amis_by_path_from_ssm(), sep='\n')