# dumbir: HomeAssistant Custom Component 
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Thunderbird2086/ha-custom-component-dumbir)](https://github.com/Thunderbird2086/ha-custom-component-dumbir/releases/latest)<br>

* Supported Home Assistant version
  * 0.1.3 or below: 0.92 or above as of April 24th 2019
  * 0.1.4 or above: 0.115 or above as of September 19th 2020

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
    remote: rm3_01
    ir_codes: 'ir_codes/climate/daikin_arc478a19.yaml'
    # if you have external temperature sensor
    temperature_sensor: sensor.aqara_01_temperature
    # if you have external power sensor
    power_sensor: sensor.ac_power

  - platform: dumbir
    name: Mitsubishi
    remote: rm3_03
    ir_codes: 'ir_codes/climate/mitsubishi_msz_j229_w.yaml'
    # it's better to use openweathermap if you don't have external temperature sensor
    temperature_sensor: sensor.openweathermap_temperature


light:
  - platform: dumbir
    name: 'Light 01'
    remote: rm3_02
    ir_codes: 'ir_codes/lights/national-hhfz5160.yaml'


media_player:
  - platform: dumbir
    name: TV
    remote: rm4_01
    ir_codes: 'ir_codes/media_players/sharp.yaml'
    # if you have external power sensor
    power_sensor: sensor.tv_power
```

For the details, refer to [wiki](https://github.com/Thunderbird2086/ha-custom-component-dumbir/wiki).
