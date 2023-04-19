#!/usr/bin/env python

import requests
import os
import json
import yaml
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class sonic_client:
  def __init__(
      self, 
      switch_address,
      username,
      password,
      proto="https",
      insecure=True,
  ):
    self.switch_address = switch_address
    self.username = username,
    self.password = password,
    self.proto = proto
    self.insecure = insecure
    self.token = self.authenticate()
    self.auth_header = {"Authorization": "Bearer {}".format(self.token)}
  
  def authenticate(self):
    url = "{}://{}/authenticate".format(self.proto, self.switch_address)
    data = {
      "username": username, 
      "password": password
    }
    
    resp = requests.post(
      url,
      verify=not self.insecure,
      auth=requests.auth.HTTPBasicAuth(self.username, self.password),
      json=data
    )

    return resp.json()["access_token"]

  def list_vlans(self):
    url = "{}://{}/restconf/data/sonic-vlan:sonic-vlan".format(self.proto, self.switch_address)
    headers=self.auth_header
    
    resp = requests.get(
      url,
      verify=not self.insecure,
      headers=headers,
    )

    return resp.json()

  def create_vlan(self, vlan):
    url = "{}://{}/restconf/data/openconfig-interfaces:interfaces".format(self.proto, self.switch_address)
    headers = {
      **self.auth_header,
      **{
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
      },
    }
    data = {
      "openconfig-interfaces:interface": [
        {
          "name": vlan,
          "config": {
            "name": vlan,
          }
        }
      ]
    }
    
    requests.post(
      url,
      verify=not self.insecure,
      headers=headers,
      json=data,
    )

  def get_vlan(self, vlan):
    url = "{}://{}/restconf/data/openconfig-interfaces:interfaces/interface={}".format(self.proto, self.switch_address)
    headers = {
      **self.auth_header,
      **{
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
      },
    }
    data = {
      "openconfig-interfaces:interface": [
        {
          "name": vlan,
          "config": {
            "name": vlan,
          }
        }
      ]
    }
    
    requests.post(
      url,
      verify=not self.insecure,
      headers=headers,
      json=data,
    )

  def delete_vlan(self, vlan):
    url = "{}://{}/restconf/data/openconfig-interfaces:interfaces/interface={}".format(self.proto, self.switch_address, vlan)
    headers = {
      **self.auth_header,
      **{
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
      },
    }
    
    requests.delete(
      url,
      verify=not self.insecure,
      headers=headers,
    )

if __name__ == "__main__":
  switch_address = os.getenv("SONIC_ADDRESS")
  username = os.getenv("SONIC_USERNAME")
  password = os.getenv("SONIC_PASSWORD")

  client = sonic_client(switch_address, username, password)

  if len(sys.argv) != 2:
    print("please provide a path to a config file to read.")
  
  config = sys.argv[1]

  switch_config = {}
  if os.path.exists(config):
    if os.path.isfile(config):
      with open(config, "r") as cfg_file:
        switch_config = yaml.safe_load(cfg_file)
  else: 
    print("config file does not exists: ", config)
  
  for vlan in switch_config["config"]["vlans"]:
    if vlan["state"] == "present":
      print("creating vlan", vlan["name"])
      client.create_vlan(vlan["name"])
      print(json.dumps(client.list_vlans(), indent=4))

    if vlan["state"] == "absent":
      print(client.list_vlans())
      print("deleting vlan", vlan["name"])
      client.delete_vlan(vlan["name"])

      vlans_deleted = False
      while not vlans_deleted:
        vlans = client.list_vlans()

        if not vlans:
          vlans_deleted = True
        
        if vlan["name"] not in [ vlan["name"] for vlan in vlans["sonic-vlan:sonic-vlan"]["VLAN"]["VLAN_LIST"] ]:
          vlans_deleted = True

        time.sleep(2)

      print("vlans after delete: ", client.list_vlans())
