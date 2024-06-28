import json
from openai import OpenAI

import s2_llm
        
def test_pingmesh():
    with open('./data/questions_pingmesh.json', 'r') as file:
        pingmesh = json.load(file)
    s2_llm.execute_questions(pingmesh)

def test_circuits():
    with open('./data/questions_circuits.json', 'r') as file:
        circuits = json.load(file)
    s2_llm.execute_questions(circuits)

def test_topology():
    with open('./data/questions_topology.json', 'r') as file:
        topology = json.load(file)
    s2_llm.execute_questions(topology)

def test_interfaces():
    with open('./data/questions_interfaces.json', 'r') as file:
        interfaces = json.load(file)
    s2_llm.execute_questions(interfaces)