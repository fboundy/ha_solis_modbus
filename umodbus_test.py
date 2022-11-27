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
CFG_IP = "192.168.4.79"  # Update with your inverter IP
CFG_PORT = 8899

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
        "desc": "Battery Storage Mode (W)",
        "addrs": 43110,
        "len": 1,
        "scale": 1,
        "uom": "",
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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((CFG_IP, CFG_PORT))

for payload in payloads:
    message = tcp.read_input_registers(slave_id=1, starting_address=payload["addrs"], quantity=payload["len"])
    response = tcp.send_message(message, sock)
    val = float(response[0]) * payload["scale"]
    print(f"{(payload['desc']+':'):25s}{val:5.1f} {payload['uom']}")

sock.close()
# %%
