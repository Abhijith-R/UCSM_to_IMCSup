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
import requests
from jinja2 import Environment
from jinja2 import FileSystemLoader
import os

requests.packages.urllib3.disable_warnings()

# TODO: This should be set as env variables
API_KEY = "API KEY"
IMCSUP_URL = "YOUR IMC IP"

DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
IMCSUP_TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/imcSupTemplates'))


def makeCall(p_url, method, data=""):
    """
    Main method to make an API call to IMC Supervisor. Please use this one to all the calls that you want to make
    :param p_url: API URL
    :param method: POST/GET are supported at this moment
    :param data: Payload to send
    :return:
    """
    headers = {'X-Cloupia-Request-Key': API_KEY}
    if method == "POST":
        response = requests.post(IMCSUP_URL + p_url, data=data, headers=headers, verify=False)
    elif method == "GET":
        response = requests.get(IMCSUP_URL + p_url, headers=headers, verify=False)
    else:
        raise Exception(method + " not supported")
    if 199 < response.status_code < 300:
        return response
    else:
        raise Exception(response.text)


def getServers():
    """
    Get all servers managed by IMC Supervisor
    :return: XML (in plain text) with the list of servers
    """
    print("Getting all servers from IMC")
    p_url = "cloupia/api-v2/CIMCServerByMacAddress"
    return makeCall(p_url, "GET").text


def CreateVICAdapterPolicy(vicAdapterPolicy):
    """
    Creates an vic adapter policy in IMC.
    :param vicAdapterPolicy: Dictionary with a policy definition including VNICs and HBAs
    :return: None
    """
    print("Making sure VIC Policy " + vicAdapterPolicy["name"] + " exists")
    p_url = "cloupia/api-v2/CIMCHardwarePolicy"
    template = IMCSUP_TEMPLATES.get_template('VICPolicyDef.j2.xml')
    policyDef = template.render(vicAdapterPolicy=vicAdapterPolicy)
    template = IMCSUP_TEMPLATES.get_template('CreateHWPolicy.j2.xml')
    payload = template.render(name=vicAdapterPolicy["name"], type="VIC Adapter Policy",
                              policyDef=policyDef.replace('"', '&quot;').replace("<", "&lt;").replace(">", "&gt;"))
    makeCall(p_url, method="POST", data=payload)


def CreateBIOSPolicy(biosPolicy):
    """
    Creates a BIOS Policy in IMC Sup
    :param biosPolicy: Dictionary with name and POST-error-pause data
    :return:
    """
    print("Making sure BIOS Policy " + biosPolicy["name"] + " exists")
    p_url = "cloupia/api-v2/CIMCHardwarePolicy"
    template = IMCSUP_TEMPLATES.get_template('BIOSPolicyDef.j2.xml')
    policyDef = template.render(biosPolicy=biosPolicy)
    template = IMCSUP_TEMPLATES.get_template('CreateHWPolicy.j2.xml')
    payload = template.render(name=biosPolicy["name"], type="BIOS Policy",
                              policyDef=policyDef.replace('"', '&quot;').replace("<", "&lt;").replace(">", "&gt;"))
    makeCall(p_url, method="POST", data=payload)

def AddServerRackAccount(serverIP,username,password):
    """
    Adds a Server Rack Account
    :param serverIP: IP address of the server
    :param username: Server username
    :param password: Server password
    :return:
    """
    p_url = "cloupia/api-v2/CIMCInfraAccount"
    template = IMCSUP_TEMPLATES.get_template('AddServerRackAccount.j2.xml')
    payload = template.render(server=serverIP, username=username, password=password)
    makeCall(p_url, method="POST", data=payload)


