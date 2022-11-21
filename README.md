# ha_solis_modbus
<H3>Home Assistant YAML for Solis Hybrid Inverter using MODBUS</H3>

This is a Home Assistant YAML file for communicating with a Solis Hybrid inverter using a DLS-L LAN Data Logging Stick which uses pure Modbus over TCP. It has been tested using a stick with Serial number 1920xxxxxx and a Solis 5-eh1p(3-6)k inverter.

The YAML file which can be included in the <i>configuration.yaml</i> file in the Home Assitant <i>config</i> folder. All that should need changing is the <i>solis_ip</i> secret which is inlcluded from <i>secrets.yaml</i>. 

Scan intervals are set as follows:

 - Instantaneous readings: 1 minute
 - Daily totals: 5 minutes
 - Monthly, Yearly and Lifetime totals: 1 hour


There is also a single template sensor which negates the grid power so that export is negative and import is positive - mainly for presentation purposes.

    modbus: !include solis.yaml
    
    template:
      sensor:
        name: "Solis Grid Active Power (Negative)"
        unique_id: "Solis Grid Active Power (Negative)"
        unit_of_measurement: W
        device_class: power
        state_class: measurement
        state: >-
          {{ -1 * states('sensor.solis_grid_active_power') | float }}

Other registers can be imported using the same format. A full list can be found [here](https://www.scss.tcd.ie/Brian.Coghlan/Elios4you/RS485_MODBUS-Hybrid-BACoghlan-201811228-1854.pdf) courtesy of Dr. Brian Coghlan.
