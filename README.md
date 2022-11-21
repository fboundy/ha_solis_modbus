# ha_solis_modbus
<H3>Home Assistant YAML for Solis Hybrid Inverter using MODBUS</H3>

This is a Home Assistant YAML file for communicating with a Solis Hybrid inverter using a DLS-L LAN Data Logging Stick which uses pure Modbus over TCP. It has been tested using a stick with Serial number 1920xxxxxx and a Solis 5-eh1p(3-6)k inverter.

The YAML file which can be included in the <i>configuration.yaml</i> file in the Home Assitant <i>config</i> folder. All that should need changing is the <i>solis_ip</i> secret which is inlcluded from <i>secrets.yaml</i>. Scan interval is set to 60s for all sensors which you may wish to reduce:

    modbus: !include solis.yaml    

Other registers can be imported using the same format. A full list can be found [here](https://www.scss.tcd.ie/Brian.Coghlan/Elios4you/RS485_MODBUS-Hybrid-BACoghlan-201811228-1854.pdf) courtesy of Dr. Brian Coghlan.
