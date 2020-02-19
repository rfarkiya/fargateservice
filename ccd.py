#!/usr/bin/python3

import boto3
import argparse
import sys

cd_client = boto3.client('codedeploy')
cf_client = boto3.client('cloudformation')

parser = argparse.ArgumentParser(description='Create Complete CodeDeploy Infrastrcuture for service')

parser.add_argument('--stackname', type=str, help='Service Stack Name', required=True)
parser.add_argument('--servicename', type=str, help='Micro Service Name', required=True)
parser.add_argument('--servicerolearn', type=str, help='ECS Service Role for CodeDeploy Service', required=True)
parser.add_argument('--clustername', type=str, help='ECS Cluster Name', required=True)

args = parser.parse_args()

stacks = cf_client.describe_stacks(StackName=args.stackname)
outputs = stacks["Stacks"][0]["Outputs"]

# Blue green Target groups
targetgroup1=""
targetgroup2=""

# Blue green Listeners
prodListenerArn=""
testListenerArn=""

# Get TargetGroupInfo
for output in outputs:
	keyName = output["OutputKey"]
	if keyName == "LoadBalancerTargetGroupBG1":
		targetgroup1 = output["OutputValue"]
	elif keyName == "LoadBalancerTargetGroupBG2":
		targetgroup2 = output["OutputValue"]
	elif keyName == "LoadBalancerListener":
		prodListenerArn = output["OutputValue"]
	elif keyName == "TESTLoadBalancerListener":
		testListenerArn = output["OutputValue"]

response = cd_client.create_application(
    applicationName=args.servicename + '-app',
        computePlatform='ECS'
        )

response = cd_client.create_deployment_group(
	applicationName=args.servicename + '-app',
	deploymentGroupName=args.servicename + '-app-dg',
	deploymentConfigName='CodeDeployDefault.ECSAllAtOnce',
	serviceRoleArn=args.servicerolearn,
	autoRollbackConfiguration={
		'enabled': True,
		'events': [
		'DEPLOYMENT_FAILURE', 'DEPLOYMENT_STOP_ON_ALARM', 
		'DEPLOYMENT_STOP_ON_REQUEST',
		]
	},
	deploymentStyle={
		'deploymentType': 'BLUE_GREEN',
		'deploymentOption': 'WITH_TRAFFIC_CONTROL'
	},
	blueGreenDeploymentConfiguration={
		'terminateBlueInstancesOnDeploymentSuccess': {
		'action': 'TERMINATE',
		'terminationWaitTimeInMinutes': 30
		},
    		'deploymentReadyOption': {
       			'actionOnTimeout': 'CONTINUE_DEPLOYMENT'
    		}
	},
	loadBalancerInfo={
		'targetGroupPairInfoList': [
		{
			'targetGroups': [
				{
					'name': targetgroup1
				},
				{
					'name': targetgroup2
				}
				],
			'prodTrafficRoute': {
				'listenerArns': [ prodListenerArn ]
			},
			'testTrafficRoute': {
          			'listenerArns': [ testListenerArn ]
			}
		}]
	},
	ecsServices=[
		{
			'serviceName': args.servicename,
			'clusterName': args.clustername
		}
	    ]
	)
