# ha_solis_modbus

<H2>Home Assistant YAML for Solis Hybrid Inverter using MODBUS</H2>

This is a Home Assistant YAML file for communicating with a Solis Hybrid inverter using a Data Logging Stick which uses pure Modbus over TCP. It has been tested using a Solis 5-eh1p(3-6)k inverter and:

- DLS-LAN stick: Serial number 1920xxxxxx [as shown here](https://tenergise.co.uk/product/solis-data-logging-stick/)
- S2-WL-ST 4-pin dual WiFi/LAN stick: Serial number 7Axxxxxxxxxxxxxx [as shown here](https://www.ginlong.com/accessories9/S2_WL_ST_us.html)

<b><u>The [S3-WIFI-ST](https://www.ginlong.com/accessories5/WiFi_Data_Logging_Stick_11231607.html) stick will NOT work.</b></u>

v1.1.0 now also supports writing to the inverter using a number of Automations. Scripts and Inputs.

<h3>Reading from the Inverter</h3>

The YAML file which can be included in the `configuration.yaml` file in the Home Assitant `config` folder. All that should need changing is the `solis_ip` secret which is included from `secrets.yaml`. Alternatively just overwrite with the IP address.

Scan intervals are set as follows:

- Instantaneous readings: 1 minute
- Daily totals: 5 minutes
- Monthly, Yearly and Lifetime totals: 1 hour

Include this file in your `configuation.yaml` file with:

    modbus: !include solis.yaml

Within this file you need to set the TCP port that MODBUS uss depending on the model of Data Logging Stick:

`port: 8899` for the older DLS-LAN stick or `port: 502` for the newer S2-WL-ST stick.

A fairly comprehensive set of both the <b>input</b> registers (33xxx) and <b>holding</b> registers (43xxx) is read. Other registers can be imported using the same format. A full list can be found [here](https://www.scss.tcd.ie/Brian.Coghlan/Elios4you/RS485_MODBUS-Hybrid-BACoghlan-201811228-1854.pdf) courtesy of Dr. Brian Coghlan. Note that some parameters are 32 bit and span two registers. Also note that 16 bit parameters can be signed (int16) or unsigned (uint16). More information on the Home Asistant Modbus integration can be found [here](https://www.home-assistant.io/integrations/modbus/).

<h3>Writing to the Inverter</h3>
This is done with a service call to the modbus integration. For example, to set the Timed Discharge Current Limit (register) to 50A:

    service: modbus.write_register
    data:
      address: 43141
      slave: 1
      value: 500
      hub: solis

The following scripts are included in `scripts.yaml` to assit with this:

- Solis Write Holding Register: writes `value` to `address`
- Solis Set Charge Current: sets the <b>Timed Charge Current</b> (Register 43131) to `current`
- Solis Set Eco7 Times: sets the 1st set of <b>Timed Charging Times</b> (Registers 43143 - 6) to the times specified by the `input_datetime` enties: `economy_7_start` and `economy_7_start`
- Solis Set Energy Storage Mode: sets the <b>Energy Storage Control Switch</b>(Register 43110) to that specified by the six `input_boolean` entites `solis_storage_mode_*`
- Set Solis Storage Toggles: sets the six `input_boolean` entites `solis_storage_mode_*` to match the values read from the inverter if they change (e.g. they are set manually on the inverter itself)

<h3>Template Sensors</h3>

There are also a number of template sensors some of which are just helpers but others are needed for some of the scripting below and rely on certain input entities (see below). These are included in a separate file `solis-templates.yaml` these can be included into your `configuation.yaml` file with the below. Alternatively you may wish to merge them into the file directly:

    template:
      !include solis-templates.yaml

<h3>Inputs</h3>

A number of helpers are needed for the scripts and automations included below. These are included in `inputs.yaml`. As with the other `.yaml` files they need to be either merged or included into your `configuation.yaml`. The inputs are as follows:

- Economy 7 Start Time: `input_boolean.economy_7_start`
- Economy 7 End Time: `input_boolean.economy_7_end`
- Solis Storage Mode toggles which set the following bits of the Energy Storage Control Switch:

       Bit 0 (1)  - Spontaneous Mode      input_boolean.solis_storage_mode_spontaneous
       Bit 1 (2)  - Timed Mode            input_boolean.solis_storage_mode_timed
       Bit 2 (4)  - Off-Grid Mode         input_boolean.solis_storage_mode_off_grid
       Bit 3 (8)  - Battery Wake-Up Mode  input_boolean.solis_storage_mode_wake_up
       Bit 4 (16) - Backup Mode           input_boolean.solis_storage_mode_backup
       Bit 5 (32) - Grid Charge Mode      input_boolean.solis_storage_mode_grid_charge

<h3>Utilities</h3>

Also included is a small Python script `modbus_test.py` 2hich will check modbus communications and, if all is well, will report back Inverter Temperature, Grid Voltage and Battery SOC:

    Inverter Temperature:     30.3 C
    Grid Voltage:            243.3 V
    Battery SOC:              15.0 %

The following YAML files are also included:

    octopus-intelligent.yaml - scripts and automations by @robjwalker to assist with Octopus Intelligent tariffs
    ng_eso_dfs.yaml          - sensors to detect the most recent National Grid ESO Demand Flexibility Service slot start and end times
