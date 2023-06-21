#%%
# This script will test umodbus comms to a Solis Hybrid Inverter with a DLS-L LAN Data Logger
#
# It requires the umodbus module
#
# It will report the inverter temperaturem, the grid voltage and the battery state of charge

import socket
from umodbus import conf
from umodbus.client import tcp

# configuration
CFG = {
    'Waveshare': {
        'IP': "192.168.4.40",
        'PORT': 502,
    },

    'S2-WL': {
        'IP': "192.168.4.237",
        'PORT': 502,
    }, 

    'DLS-L': {
        'IP': "192.168.4.79",
        'PORT': 8899,
    } 

}  # Update with your inverter IP

devices = ['S2-WL', 'Waveshare', ]

payloads = [
    {
        "desc": "Inverter Temperature",
        "addrs": 33093,
        "len": 1,
        "scale": 0.1,
        "uom": "C",
    },
    {
        "desc": "Grid Voltage",
        "addrs": 33251,
        "len": 1,
        "scale": 0.1,
        "uom": "V",
    },
    {
        "desc": "Battery SOC",
        "addrs": 33139,
        "len": 1,
        "scale": 1,
        "uom": "%",
    },
    {
        "desc": "Battery Storage Mode (R)",
        "addrs": 33132,
        "len": 1,
        "scale": 1,
        "uom": "",
    },
]

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True
sock = {}
for device in devices:
    sock[device] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock[device].connect((CFG[device]['IP'], CFG[device]['PORT']))
    print(f"Device: {device}")
    print('-' * 32 + '\n')
    for payload in payloads:
        message = tcp.read_input_registers(slave_id=1, starting_address=payload["addrs"], quantity=payload["len"])
        response = tcp.send_message(message, sock[device])
        val = float(response[0]) * payload["scale"]
        print(f"{(payload['desc']+':'):25s}{val:5.1f} {payload['uom']}")

    print("\n\n")
    sock[device].close()    
    
# %%
