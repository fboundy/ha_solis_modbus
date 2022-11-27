#%%
# This script will test umodbus comms to a Solis Hybrid Inverter with a DLS-L LAN Data Logger
#
# It requires the umodbus module
#
# It will report the inverter temperaturem, the grid voltage and the battery state of charge

import socket
from umodbus import conf
from umodbus.client import tcp
from time import sleep

# configuration
CFG_IP = "192.168.4.79"  # Update with your inverter IP
CFG_PORT = 8899


# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((CFG_IP, CFG_PORT))

for addrs in range(33215, 33300):
    message = tcp.read_input_registers(slave_id=1, starting_address=addrs, quantity=1)
    response = tcp.send_message(message, sock)
    print(f"{addrs:8d}: {response}")
    # sleep(1)

sock.close()
# %%
