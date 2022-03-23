#!/usr/bin/env python3
import logging

import click
from boto3 import client


logger = logging.getLogger()

def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state not in ['running', 'pending']:
        return instance['StateReason']['Message']

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
pass_client = click.make_pass_decorator(client)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--debug', is_flag=True, help="Print logging info.")
@click.pass_context
def kancli(ctx, debug):
    """
    Welcome to Kandula CLI!
    
    The tool provides command line interface
    to operate Kandula application servers.
    """

    ctx.ensure_object(dict)
    ctx.obj["client"] = client('ec2')
    ctx.obj["debug"] = debug

@kancli.command()
@click.pass_context
def get_instances(ctx):
    """
    Shows all AWS instances having
    tag 'Project' equal to 'kandula'.

    Items are sorted by instance names.
    """

    client = ctx["client"]
    debug = ctx["debug"]

    try:
        response = client.describe_instances()
    except Exception as e:
        logger.exception(e)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.exception("Bad request.")

    instances = []
    instances_data = [i for res in response['Reservations'] for i in res['Instances']]
    for i in instances_data:
        new_i = {}

        # Keys similar for all instances.
        new_i['Cloud'] = 'aws'
        new_i['Region'] = client.meta.region_name

        # Keys being present regardless of instance state.
        new_i['Id'] = i['InstanceId']
        new_i['Type'] = i['InstanceType']
        new_i['ImageId'] = i['ImageId']
        new_i['LaunchTime'] = i['LaunchTime']
        new_i['State'] = i['State']['Name']
        new_i['StateReason'] = get_state_reason(i)
        new_i['PrivateDnsName'] = i['PrivateDnsName']
        new_i['PublicDnsName'] = i['PublicDnsName']
        new_i['RootDeviceName'] = i['RootDeviceName']
        new_i['RootDeviceType'] = i['RootDeviceType']
        new_i['SecurityGroups'] = i['SecurityGroups']
        new_i['Tags'] = i['Tags']

        if 'kandula' not in map(lambda x: x['Value'], i['Tags']):
            continue

        for k, v in i["Tags"]:
            if k == "Name":
                new_i[k] = v
                break
        else:
            new_i["Name"] = "None"

        # Keys dependent on instance state.
        new_i['SubnetId'] = i.get('SubnetId')
        new_i['VpcId'] = i.get('VpcId')
        new_i['PrivateIpAddress'] = i.get('PrivateIpAddress')
        new_i['PublicIpAddress'] = i.get('PublicIpAddress')

        if len(i['NetworkInterfaces']) > 0:
            new_i['MacAddress'] = i['NetworkInterfaces'][0]['MacAddress']
            new_i['NetworkInterfaceId'] = i['NetworkInterfaces'][0]['NetworkInterfaceId']
        else:
            new_i['MacAddress'] = None
            new_i['NetworkInterfaceId'] = None

        instances.append(new_i)
    
    instances = sorted(instances, key=lambda x: x["Name"])
    return instances


@kancli.command()
@click.pass_context
def start_instances(ctx):



@kancli.command()
@click.pass_context
def stop_instances(ctx):



@kancli.command()
@click.pass_context
def terminate_instances(ctx):



if __name__ == '__main__':
    kancli()
