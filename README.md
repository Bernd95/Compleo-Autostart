# Compleo Autostart
## The Problem
I use the wallbox Compleo ebox Professional with firmware v2.5.1. Depending on which of my RFID cards I show when connecting a car, the charging session is considered as private or business. But I want to avoid showing an RFID card each time I connect a car. Instead, the connected car should be detected automatically and the charging session should be considered accordingly.
## The Solution
Inspired by the solution [here](https://github.com/cs33lm/node-red-innogy-http-request) and with a lot of help from AI chatbots, I came up with a solution using [evcc](https://evcc.io/), [Home Assistant](https://www.home-assistant.io/) and the [Home Assistant Integration: evcc - Solar Charging (unofficial)](https://github.com/marq24/ha-evcc). The basic idea is as follows:
1. When the car is connected to my wallbox, evcc detects the car (in my case using the BMW Cardata backend).
1. An automation in HA detects that evcc switches to a known car.
1. It is checked that the car is not yet charging. See "open points" for a sensible extra check.
1. A python script is started with a parameter for either a private or business session.
1. The python scripts calls the web interface of the wallbox and initiates a session with the correct RFID.
1. The car starts charging.
1. A message is sent to my cell phone.
## The Documentation
Download the files compleo_start.py and automation.yaml. First, you have to replace some placeholders by your passwords and IDs. Let's start with compleo_start.py:
- `xxx_YOUR_PRIVATE_RFID` has to be replaced by the internal ID of your private RFID card. To find this ID, start a private charging session. Then open the web interface of the wallbox, go to LDP1 ➔ Session and search for `Contract ID`. This combination of letters and numbers is what you are looking for.
- `xxx_YOUR_BUSINESS_RFID` has to be replaced by the internal ID of your business RFID card.
- `xxx_YOUR_ADMIN_PASSWORD` has to be replaced by the password to access the wallbox. It is usually the PUK written on the back of the manual.

And in automation.yaml:
- `xxx_FAHRZEUGKENNUNG_PRIVAT` has to be replaced by the internal evcc ID of your private car. It should be something like `db:`and a number, so e. g. `db:3`.
- `xxx_FAHRZEUGKENNUNG_BUSINESS` has to be replaced by the internal evcc ID of your business car.
- `notify.xxx_mobile_app_ON_YOUR_PHONE` has to be replaced by the correct HA entity for your cell phone. This might be something like `notify.mobile_app_Toms_iPhone`.

Now you have to copy the file `compleo_start.py` to the directory config ➔ scripts on your HA server (so the scripts directory is in the same directory as the configuration.yaml). In the file configuration.yaml, add the following lines:
```
shell_command:
  compleo_start_private: "python3 /config/scripts/compleo_start.py private >> /config/compleo.log 2>&1"
  compleo_start_business: "python3 /config/scripts/compleo_start.py business >> /config/compleo.log 2>&1"
```
Don't forget to restart HA now. Then create an automation using the code in automation.yaml. That's it: Connect your car and have fun...
## The Open Point
As an extra messure, it would be good to check whether the connected car is really at home and connected. This would avoid errors if evcc detects the wrong car (which happened once to me so far). Since there is currently no stable BMW integration in Home Assistant, I have not yet implemented this.

