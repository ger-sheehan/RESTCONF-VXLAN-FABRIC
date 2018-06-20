
import requests
import base64
import yaml
from string import Template

auth = base64.b64encode('admin:password')
headers = {
    'authorization': 'Basic %s' % auth,
    'content-type': "application/yang.data+xml"
    }

def enable_features(device,role):
    payload = load_templates(device, 'templates/{0}/{1}'.format(role,'features.txt'))
    send_payload(device,payload)

def configure_ospf(device,role):
    payload = load_templates(device, 'templates/{0}/{1}'.format(role,'ospf.txt'))
    send_payload(device,payload)


def configure_bgp(device,role):
    payload = load_templates(device, 'templates/{0}/{1}'.format(role,'bgp.txt'))
    send_payload(device,payload)

def load_templates(device,path):
    with open('host_vars/{0}.yml'.format(device), 'r') as f:
        config = yaml.load(f)
    inputs = open( path )
    src = Template( inputs.read() )
    payload = src.substitute(config)
    return payload

def send_payload(device, payload):
    url = "http://{0}/restconf/data/Cisco-NX-OS-device:System".format(device)
    
    try:
        response = requests.request("PUT", url,data=payload,headers=headers)
    except requests.exceptions.RequestException as e:
        print e
        print payload
        sys.exit(1)
    print response.status_code

    if response.status_code/100 != 2:
        print payload
        print response.content

def main():

    spines = ['n9kv-spine-1', 'n9kv-spine-2']
    leaves = ['n9kv-leaf-1', 'n9kv-leaf-2']

    for spine in spines:
        enable_features(spine,'spine')
        configure_ospf(spine,'spine')
        configure_bgp(spine,'spine')

    for leaf in leaves:
        enable_features(leaf,'leaf')
        configure_ospf(leaf,'leaf')
        configure_bgp(leaf,'leaf')

if __name__ == '__main__':
  main()
