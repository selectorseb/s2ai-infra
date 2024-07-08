import json
import s2_llm
        
def test_status():
    data =  [
         {
            "phrase" : "status of ports",
            "function": "get_interfaces",
            "enabled": "1",
            "filters": {
                "time" : "last 30 min"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_site():
    data =  [
        {
            "phrase" : "status of ports in sea",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "seattle"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_site_1():
    data =  [
        {
            "phrase" : "status of ports in arizona",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_site_2():
    data =  [
        {
            "phrase" : "status of ports in denver and arizona",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "ari1,dnvr1"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_site_3():
    data =  [
        {
            "phrase" : "status of ports in denver, arizona and atlanta",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "ari1,dnvr1,atl1"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi():
    data =  [
        {
        "phrase" : "status of ports with high utilization in arizona",
        "function": "get_interfaces",
        "filters": {
            "time" : "last 30 min",
            "site" : "ari1",
            "kpi"  : "utilization"
        }
    }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi_1():
    data =  [
            {
            "phrase" : "status of ports with high utilization in arizona and denver",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : ["ari1","dnvr1"],
                "kpi"  : "utilization"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi_2():
    data =  [
            {
            "phrase" : "status of ports with high utilization in arizona on router RTR3.dnvr1",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona",
                "kpi"  : "utilization",
                "device": "RTR3.dnvr1"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi_3():
    data =  [
            {
            "phrase" : "status of Ethernet100* ports with high utilization in arizona on router RTR3.dnvr1",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona",
                "kpi"  : "utilization",
                "device": "RTR3.dnvr1",
                "interface": "Ethernet100*"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi_4():
    data =  [
            {
            "phrase" : "status of Ethernet100* ports with high errors in arizona on router RTR3.dnvr1",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona",
                "kpi"  : "errors",
                "device": "RTR3.dnvr1",
                "interface": "Ethernet100*"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True

def test_status_kpi_4_multiple():
    data =  [
            {
            "phrase" : "status of Ethernet100* ports with high errors,discards and drops in arizona on router RTR3.dnvr1",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona",
                "kpi"  : "errors,discards,drops",
                "device": "RTR3.dnvr1",
                "interface": "Ethernet100*"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True

def test_status_devices():
    data =  [
        {
            "phrase" : "status of Eth100* ports with high utilization in arizona on router rt43.1.1",
            "function": "get_interfaces",
            "filters": {
                "time" : "last 30 min",
                "site" : "arizona",
                "kpi"  : "utilization",
                "device": "rt43.1.1",
                "interface": "Eth100*"
            }
        }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_status_kpi_optics():
    data =  [
        {
        "phrase" : "status of ports with optics issues in arizona",
        "function": "get_interfaces",
        "filters": {
            "time" : "last 30 min",
            "site" : "ari1",
            "kpi"  : "optics"
        }
    }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_errors():
    data =  [
        {
        "phrase" : "Are there any interface errors at nyc1?",
        "function": "get_interfaces",
        "filters": {
            "time" : "last 30 min",
            "site" : "nyc1",
            "kpi"  : "errors"
        }
    }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 

def test_errors():
    data =  [
        {
        "phrase" : "Are there any interface errors at nyc1?",
        "function": "get_interfaces",
        "filters": {
            "time" : "last 30 min",
            "site" : "nyc1",
            "kpi"  : "errors"
        }
    }
    ]
    function, filter = s2_llm.execute_questions(data)   
    assert function == True
    assert filter == True 
