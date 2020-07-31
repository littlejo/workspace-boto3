#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import botocore.waiter
import botocore.session
import json

session = boto3.session.Session()

with open('waiters-2.json') as json_file:
    data = json.load(json_file)
model = botocore.waiter.WaiterModel(data)

class workspaces:
    def __init__(self):
        self.wss = session.client('workspaces')

    def terminate(self, id_=''):
        if id_ == '':
            id_ = self.get_workspace()[0]
        try:
            return self.wss.terminate_workspaces(TerminateWorkspaceRequests=[{'WorkspaceId': id_}])
        except ClientError as e:
            print(e)

    def start(self, id_=''):
        if id_ == '':
            id_ = self.get_workspace()[0]
        try:
            return self.wss.start_workspaces(StartWorkspaceRequests=[{'WorkspaceId': id_}])
        except ClientError as e:
            print(e)

    def stop(self, id_=''):
        if id_ == '':
            id_ = self.get_workspace()[0]
        try:
            return self.wss.stop_workspaces(StopWorkspaceRequests=[{'WorkspaceId': id_}])
        except ClientError as e:
            print(e)

    def wait(self, id_='', status="WorkspaceRunning"):
        if id_ == '':
            id_ = self.get_workspace()[0]
        waiter = botocore.waiter.create_waiter_with_client(status, model, self.wss)
        waiter.wait(WorkspaceIds=[id_])

    def bundle_list(self):
        response = self.wss.describe_workspace_bundles(
                         Owner="AMAZON",
                   )
        bundle_list = [bundle_dict['BundleId'] for bundle_dict in response['Bundles']]
        return bundle_list

    def get_used_bundle_list(self):
        response = self.wss.describe_workspaces()
        bundle_list = [_dict['BundleId'] for _dict in response['Workspaces']]
        return bundle_list

    def describe(self):
        response = self.wss.describe_workspaces()
        return response

    def get_workspace(self):
        response = self.wss.describe_workspaces()
        workspaces_list = [_dict['WorkspaceId'] for _dict in response['Workspaces']]
        return workspaces_list

    def dir_list(self):
        response = self.wss.describe_workspace_directories()
        directory_list = [dir_dict['DirectoryId'] for dir_dict in response['Directories']]
        return directory_list

    def commission(self, dir_id='', user_name='littlejo', bundle_id='', volume_encryption_key='', user_volume_encryption_key=False, root_volume_encryption_key=False, running_mode='AUTO_STOP', running_mode_auto_stop_timeout=60, root_volume_size=80, user_volume_size=50, compute_type_name='STANDARD'):
        if dir_id == '':
            dir_id = self.dir_list()[0]
        if bundle_id == '':
            #bundle_id = self.get_used_bundle_list()[0]
            bundle_id = "wsb-clj85qzj1"
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_workspaces
        response = self.wss.create_workspaces(
                          Workspaces=[
                              {
                                  'DirectoryId': dir_id,
                                  'UserName': user_name,
                                  'BundleId': bundle_id,
                                  #'VolumeEncryptionKey': volume_encryption_key,
                                  'UserVolumeEncryptionEnabled': user_volume_encryption_key,
                                  'RootVolumeEncryptionEnabled': root_volume_encryption_key,
                                  'WorkspaceProperties': {
                                      'RunningMode': running_mode,
                                      'RunningModeAutoStopTimeoutInMinutes': running_mode_auto_stop_timeout,
                                      'RootVolumeSizeGib': root_volume_size,
                                      'UserVolumeSizeGib': user_volume_size,
                                  #    'ComputeTypeName': compute_type_name
                                  },
                                  'Tags': [
                                      {
                                          'Key': 'string',
                                          'Value': 'string'
                                      },
                                  ]
                              },
                          ]
                   )
        print(response)
    
    def commission_wait(self):
        self.commission()
        print("Commission in progress")
        self.wait()
        print("DONE")

    def stop_wait(self):
        self.stop()
        print("Stopping workspace...")
        self.wait(status="WorkspaceStopped")
        print("DONE")

    def start_wait(self):
        self.start()
        print("Starting workspace...")
        self.wait(status="WorkspaceRunning")
        print("DONE")

    def terminate_wait(self):
        self.terminate()
        print("Terminating workspace...")
        self.wait(status="WorkspaceTerminated")
        print("DONE")


workspace = workspaces()
#workspace.commission()
workspace.terminate_wait()
#print(workspace.terminate())
#print(workspace.get_used_bundle_list())
#print(workspace.get_workspace())
#workspace.terminate("ws-f9lqyj2lv")
#workspace.commission()
