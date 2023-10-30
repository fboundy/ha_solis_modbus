# %%
from pymodbus.client import ModbusTcpClient
import yaml


# %%
# configuration
CFG = {
    "Waveshare": {
        "IP": "192.168.4.40",
        "PORT": 502,
    },
    "S2-WL": {
        "IP": "192.168.4.240",
        "PORT": 502,
    },
    "DLS-L": {
        "IP": "192.168.4.79",
        "PORT": 8899,
    },
}  # Update with your inverter IP

devices = [
    # 'S2-WL',
    "Waveshare",
]

input_registers = [
    {
        "desc": "Inverter Temperature",
        "addr": 33093,
        "len": 1,
        "scale": 0.1,
        "uom": "C",
    },
    {
        "desc": "Grid Voltage",
        "addr": 33251,
        "len": 1,
        "scale": 0.1,
        "uom": "V",
    },
    {
        "desc": "Battery SOC",
        "addr": 33139,
        "len": 1,
        "scale": 1,
        "uom": "%",
    },
    {
        "desc": "Battery Storage Mode (R)",
        "addr": 33132,
        "len": 1,
        "scale": 1,
        "uom": "",
    },
]


# %%
def secret_constructor(loader, node):
    # Process the node and return the corresponding Python object
    return None


yaml.add_constructor("!secret", secret_constructor)

with open("solis.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

sensors = data[0]["sensors"]
# %%

# Enable values to be signed (default is False).
sock = {}
for device in devices:
    client = ModbusTcpClient(host=CFG[device]["IP"], port=CFG[device]["PORT"])

    if client.connect():
        str = f"Device {device} connected at {CFG[device]['IP']}:{CFG[device]['PORT']}"
        print(str)
        print("-" * len(str) + "\n")
        for j, sensor in enumerate(sensors[:8]):
            # fmt=f"8.{max(int(-np.log10(sensor['scale'])),0)}f"
            if sensor["input_type"] == "input":
                result = client.read_input_registers(
                    sensor["address"], slave=sensor["slave"]
                )

            elif sensor["input_type"] == "holding":
                result = client.read_holding_registers(
                    sensor["address"], slave=sensor["slave"]
                )

            for i, register in enumerate(result.registers):
                print(
                    f"{j:>3d} {(sensor['name']+f' [Byte {i}]:'):60s}{register*sensor['scale']:6.1f} {sensor.get('unit_of_measurement')}"
                )
        print("\n\n")
    else:
        print(
            f"Failed to connect to Device {device} at {device['IP']}:{device['PORT']}"
        )

    client.close()

# %%
client = ModbusTcpClient(host=CFG[device]["IP"], port=CFG[device]["PORT"])
print(client.connect())
# %%
result = client.read_input_registers(33022, count=6, slave=sensor["slave"])
print(result.registers)
client = ModbusTcpClient(host=CFG[device]["IP"], port=CFG[device]["PORT"])
result = client.read_holding_registers(43000, count=6, slave=sensor["slave"])
print(result.registers)
# %%
