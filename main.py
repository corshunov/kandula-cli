#!/usr/bin/env python3
import logging
import json

import click
from boto3 import client


logger = logging.getLogger()

def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state not in ['running', 'pending']:
        return instance['StateReason']['Message']

def apply_style(state, string):
    fg = None
    blink = False

    if state == "pending":
        fg = 'green'
        blink = True
    elif state == "running":
        fg = 'green'
        blink = False
    elif state == "shutting-down":
        fg = 'red'
        blink = True
    elif state == "terminated":
        fg = 'red'
        blink = False
    elif state == "stopping":
        fg = None
        blink = True
    elif state == "stopped":
        fg = None
        blink = False
    return click.style(string, fg=fg, blink=blink)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.version_option("1.0.0", '-v', '--version', prog_name='Kandula CLI')
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


def get_full_text(instances):
    text = click.style("Kandula instances:", bold=True)

    for i in instances:
        string = apply_style(i["State"], i.pop('Name'))
        text += click.style(f"\n\n- {string}", bold=True)

        for k,v in i.items():
            if k == "State":
                v = apply_style(i["State"], v)
            elif k == "SecurityGroups":
                v = ', '.join( map(lambda x: f"{x['GroupName']} ({x['GroupId']})", v) )
            elif k == "Tags":
                v = ', '.join( map(lambda x: f"{x['Key']}={x['Value']}", v) )
            text += f"\n     {k}: {v}"
    return text

def get_short_text(instances):
    text = click.style("Kandula instances:", bold=True)
    for i in instances:
        string = apply_style(i["State"], i['Name'])
        text += f"\n- {string}"
    return text

@kancli.command('get-instances', short_help='Return AWS Kandula instances.')
@click.option('-s', '--state', type=click.Choice(['all', 'pending', 'running',
                                                  'shutting-down', 'terminated',
                                                  'stopping', 'stopped']),
              multiple=True, default=['all'], help="Filters instances according to state (deafult is 'all').")
@click.option('-f', '--full', is_flag=True, default=False,
              help="Returns all data about instances.")
@click.option('-o', '--output', type=click.Choice(['text', 'json']),
              default='text', help="Output format (default is 'text').")
@click.pass_context
def get_instances(ctx, state, full, output):
    """
    Returns AWS instances having tag 'Project' with value 'kandula'.

    Items are sorted by instance names.
    """

    state = sorted(set(state))

    client = ctx.obj["client"]
    debug = ctx.obj["debug"]

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

        name = "no name"
        flag = False
        for tag_data in i["Tags"]:
            if tag_data["Key"] == "Name":
                name = tag_data["Value"]

            if tag_data["Key"] == "Project" and tag_data["Value"] == "kandula":
                flag = True
        
        if flag == False:
            continue

        i_state = i['State']['Name']
        if 'all' not in state and i_state not in state:
            continue

        # Keys similar for all instances.
        new_i['Cloud'] = 'aws'
        new_i['Region'] = client.meta.region_name

        # Keys being present regardless of instance state.
        new_i["Name"] = name
        new_i['Id'] = i['InstanceId']
        new_i['Type'] = i['InstanceType']
        new_i['ImageId'] = i['ImageId']
        new_i['LaunchTime'] = i['LaunchTime']
        new_i['State'] = i_state
        new_i['StateReason'] = get_state_reason(i)
        new_i['PrivateDnsName'] = i['PrivateDnsName']
        new_i['PublicDnsName'] = i['PublicDnsName']
        new_i['RootDeviceName'] = i['RootDeviceName']
        new_i['RootDeviceType'] = i['RootDeviceType']
        new_i['SecurityGroups'] = i['SecurityGroups']
        new_i['Tags'] = i['Tags']

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

    if len(instances) == 0:
        click.secho(f'No Kandula instances with {"state" if len(state) == 1 else "states"} {", ".join(state)}.', bold=True)
        return

    if full:
        if output == "text":
            click.echo_via_pager(get_full_text(instances))
        elif output == "json":
            click.echo(json.dumps(instances, indent=4, default=str))
    else:
        if output == "text":
            click.echo_via_pager(get_short_text(instances))
        elif output == "json":
            instances = list(map(lambda x: x["Name"], instances))
            click.echo(json.dumps(instances, indent=4, default=str))

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@kancli.command('start-instances', short_help="Start instances.")
@click.option('-y', is_flag=True, callback=abort_if_false,
              expose_value=False, prompt='Are you sure you want to start the instances?')
@click.pass_context
def start_instances(ctx):
    ...


@kancli.command('stop-instances', short_help="Stop instances.")
@click.option('-y', is_flag=True, callback=abort_if_false,
              expose_value=False, prompt='Are you sure you want to stop the instances?')
@click.pass_context
def stop_instances(ctx):
    ...


@kancli.command('terminate-instances', short_help="Terminate instances.")
@click.option('-y', is_flag=True, callback=abort_if_false,
              expose_value=False, prompt='Are you sure you want to terminate the instances?')
@click.pass_context
def terminate_instances(ctx):
    ...


if __name__ == '__main__':
    kancli()
