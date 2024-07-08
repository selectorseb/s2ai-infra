import json
import requests
from time import strftime, localtime


def get_interfaces(circuit_id: str = '', circuit_provider: str = '', site: list = [], device: str = '', interface: str = '', kpi: list = [], metric_state: str = '', time: str = "last 30 min") -> str:
    """
    Function to get status of interfaces, ports

    Parameters:
    - circuit_id (str): an alphanumeric number that uniquely identifies a circuit
    - circuit_provider (str): the organization that provides circuit services, e.g 'att', 'lumen', 'zayo', 'aws', 'gcp'
    - time (str): The time range, e.g., 'last 1 day', 'last 30 minutes' or 'last 2 days'. Default is 'last 30 min'.
    - site: A datacenter site with all devices. e.g - dnvr1, ari1, bpwifi, seattle
    - device: A network router. e.g - tr01.dnvr1, rs10101.sea1
    - interface: A port on a device e.g et-0/0/1, Eth0/0/1, Eth0/0/2, Ethernet0/10/1
    - metric_state: the failure threshold of the metric. e.g - warning, failed, errors, critical
    - kpi: the key performance indicator for the health of the interface. e.g - utilization, errors, bandwidth, transmit, receive, discards, status, optical light levels, optics, dom power, voltage

    Returns:
    - str: Returns the state of network topology. How devices are connected to each other
    """

    selector_url = "https://s2m.selector.ai/api/collab2-slack/rules/command"
    api_key = "70fN07ny3x3sENNwEO2o8cJr"
    query_to_run = '#select layer2_topology as topology '
    query_to_run = query_to_run + ' s2_inst=.*, '
    query_to_run = query_to_run + 'role=.*, '
    query_to_run = query_to_run + 's2ap_infra_health>=1, '

    query_to_run = query_to_run + ' for ' + time

    print(query_to_run)
    headers = dict()
    headers["Authorization"] = "Bearer " + api_key
    headers["Content-Type"] = "application/json"
    json_data = {
        'command': query_to_run,
        'utc_offset_sec': -25200,
    }
    return "No result returned."
    #response = requests.post(selector_url, headers=headers, json=json_data)
    #Decode json response
    result = json.loads(response.text)

    if len(result['data']) == 0:
        return "No result returned."
    output = "Following s2ap infra health status reported: \n"
    for item in (result['data']):
        if s2_inst != 'all' and item['s2_inst'] != s2_inst:
            continue

        if role != 'all' and item['role'] != role:
            continue

        entry = " - instance:" + item['s2_inst']
        entry = entry + " role:" + item['role']
        # if item['s2ap_infra_health'] is 1 then return healthy else return unhealthy
        if item['s2ap_infra_health'] == 1:
            entry = entry + " health:good"
        else:
            entry = entry + " health:violating"
        entry = entry + " \n"
        output = output + entry
    return output

# Test function
# print(get_s2ap_infra_health_status())
