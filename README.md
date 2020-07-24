# dumbir: HomeAssistant Custom Component 
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Thunderbird2086/ha-custom-component-dumbir)](https://github.com/Thunderbird2086/ha-custom-component-dumbir/releases/latest)<br>

* Supported Home Assistant version : 0.92 or above as of April 24th 2019

dumbIR is using Broadlink Universal Remote, and supports climate, media\_player and light currently.

## How to install
1. copy the directory `custom_components/dumbir` to `.homeassistant/custom_compoents/dumbir`.
1. copy IR yaml file to `.homeassistant/ir_codes/<entity>/`.
1. Add configuration to `.homessistant/configuration.yaml`.

## Sample configuration 

```
climate:
  - platform: dumbir
    name: Daikin
    host: 192.168.0.128
    ir_codes: 'ir_codes/climate/daikin_arc478a19.yaml'
    # if you have external temperature sensor
    temperature_sensor: sensor.aqara_01_temperature
    # if you have external power sensor
    power_sensor: sensor.ac_power

  - platform: dumbir
    name: Mitsubishi
    host: 192.168.0.128
    ir_codes: 'ir_codes/climate/mitsubishi_msz_j229_w.yaml'
    # it's better to use owm if you don't have external temperature sensor
    temperature_sensor: sensor.owm_temperature


light:
  - platform: dumbir
    name: 'Light 01'
    host: 192.168.0.128
    ir_codes: 'ir_codes/lights/national-hhfz5160.yaml'


media_player:
  - platform: dumbir
    name: TV
    host: 192.168.0.128
    ir_codes: 'ir_codes/media_players/sharp.yaml'
    # if you have external power sensor
    power_sensor: sensor.tv_power


switch:
  # dumbir needs broadlink switch
  - platform: broadlink 
    host: 192.168.0.128
    mac: aa:bb:cc:dd:ee:ff
```

For the details, refer to [wiki](https://github.com/Thunderbird2086/ha-custom-component-dumbir/wiki).
