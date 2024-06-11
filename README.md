This Repository includes Python scripts that enables operation of the In-Situ imaging system.
Run the script GUI_Control.py on Raspberry Pi to operate the system through an interface. Some packages require Linux operating system and will NOT run on Windows or Mac OS

For data processing of images please go to: https://github.com/MartinReinhard10/In-Situ_Soil_Optode_Data_Processing

Please refer to the paper ... for further information regarding the in-situ imaging system for planar optodes in soils.
For additional questions please contact: martinreinhard@bio.au.dk

---
**Setup of Raspberry Pi**
Download Raspberry Pi Imager v1.7.3 to PC or MAC
Write Raspberry Pi OS (Debian Bookworm 64-bit) with Desktop to MicroSD card.
Boot Raspberry Pi and create user.
Connect to WiFi mobile hotspot and edit the wpa_supplicant.conf file
- In Terminal open with: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
  
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=<YOUR TWO LETTER COUNTRY CODE>

  network={
      ssid="<YOUR NETWORK NAME>"
      psk="<YOUR NETWORK PASSWORD>"
      key_mgmt=WPA-PSK
  }
