"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

from ucsmsdk.ucshandle import UcsHandle

# TODO: This should be set as env variables
USERNAME = "username"
PASSWORD = "password"
IP = "UCSM IP"


class UCSMController:
    def __init__(self):
        self.handle = UcsHandle(ip=IP, username=USERNAME, password=PASSWORD)
        if not self.handle.login():
            raise Exception("No valid UCS Manager credentials")

    def GetHandle(self):
        return self.handle

    def GetInterfaceProfiles(self):
        handle = self.GetHandle()
        return handle.query_classid("vnicLanConnTempl")

    def GetBIOSProfiles(self):
        handle = self.GetHandle()
        return handle.query_classid("biosVProfile")

    def GetSvcProfiles(self):
        handle = self.GetHandle()
        return handle.query_classid("lsServer")

    def GetByDN(self, dn, hierarchy=True):
        handle = self.GetHandle()
        return handle.query_dn(dn, hierarchy=hierarchy)

    def Logout(self):
        self.handle.logout()
