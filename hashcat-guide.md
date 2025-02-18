# Use Hashcat to crack password
Hashcat supports GPU, so the speed will be faster than CPU, this is a guide to use MacBook to run hashcat

## TL;DR Use script
1. Copy `crack_script/run_hashcat.sh` to your work path
2. Edit the path vars and change the cap name `cap=`
3. Ensure `dict` folder exists and `phone.dict` is ready
```
├── caps
│   ├── handshake_G_44-F7-70-16-1E-62_2024-11-30T16-32-44.cap
│   └── handshake_G_44-F7-70-16-1E-62_2024-11-30T16-32-44.hc22000
├── dict
│   └── 8_digits.dict
├── handshake_G_44-F7-70-16-1E-62_2024-11-30T16-32-44_key.txt
├── handshake_G_44-F7-70-16-1E-62_2024-11-30T16-32-44.potfile
├── log
│   ├── run_hashcat_20241116.log
│   └── run_hashcat_20241130.log
└── run_hashcat.sh
```
4. run `run_hashcat.sh`

## Install tools
1. Install hcxtools and hashcat
```bash
brew install hcxtools hashcat
sudo apt install -y hcxtools hashcat
```

## Collect host information
1. Use `hashcat -I` to collect host information, expect to see the GPU
   
## Prepare dictionary and cap file
1. The dictionary should be ready
```
# example
dict=/Users/chend/Desktop/phone_dict_gen/phone.dict
```

## Extract Hashes
Next we need to extract the required data and convert it to a format Hashcat can understand
```bash
cap=9C-7F-81-F7-58-73_handshake.cap
cap_name=$(basename ${cap} .cap)
hcxpcapngtool -o ${cap_name}.hc22000 ${cap_name}.cap 
```
Output should be like:
```
reading from 9C-7F-81-F7-58-73_handshake.cap...
failed to read packet 7216

summary capture file
--------------------
file name................................: 9C-7F-81-F7-58-73_handshake.cap
version (pcap/cap).......................: 2.4 (very basic format without any additional information)
timestamp minimum (GMT)..................: 17.01.2024 23:05:31
timestamp maximum (GMT)..................: 18.01.2024 00:18:18
used capture interfaces..................: 1
link layer header type...................: DLT_IEEE802_11 (105)
endianess (capture system)...............: little endian
...
EAPOL M1 messages........................: 3
EAPOL M2 messages........................: 1
EAPOL M3 messages........................: 2
EAPOL pairs (total)......................: 2
EAPOL pairs (best).......................: 1
EAPOL pairs written to combi hash file...: 1 (RC checked)
EAPOL M32E2..............................: 1
packet read error........................: 1

Warning: missing frames!
This dump file contains no undirected proberequest frames.
An undirected proberequest may contain information about the PSK.
That makes it hard to recover the PSK.
```

## Start Hashcat
```bash
# Windows in git cmd
work_path=/c/Users/duche/Desktop/project/phone_dict_gen
dict_path=${work_path}/phone.dict
cap_path=${dict_path}/caps
cap_name=24-69-8E-C1-82-37_handshake

ls -l ${dict_path}
ls -l ${cap_name}.hc22000

hashcat -m 22000 -w 3 --hwmon-disable \
--session ${cap_name} --status --status-timer 10 \
${cap_path}/${cap_name}.hc22000 \
${dict_path}/phone.dict \
-o ${cap_name}_key.txt --potfile-path ${cap_name}.potfile

# Restore session
hashcat --session ${cap_name} --restore

# Mac cannot work with GPU
hash_file=${cap_name}_hash.txt
hashcat -D 2 -d 3 -m 22000 -w 3 ${hash_file} ${dict} -o ${cap_name}_key.txt --potfile-path ${cap_name}.potfile
```
Parameter explain:
`-D 2` will force the hashcat to only look for GPUs. (-D is for specifying device type)
`-d 3` will force it to use the Radeon Pro 560X Compute Engine. (-d is for specifying the backend device number)

## Demo
1. Say `cap_name=test`
2. Test hasfile, save it as `${cap_name}_hash.txt`
```bash
WPA*02*78ec7edcd261cbd4ecfae7744fe4a3a7*24698ec18237*d8aa59584261*323032*dcab6957d64454a5759ab7a83e3bde73bd7bbcff777aeb91b1a02b24c2ff3416*0103007502010a000000000000000000012016734a4a7126b793325e7ecf138f17572a0262d1905bbb2dc5735582488201000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001630140100000fac040100000fac040100000fac020000*02
``` 
3. Test key `13981897424`, save it as dictionary
```
2131231231231212
wpakey.txt12312312312                 
1232132131231231
213123123123213
321123123123
3231231231231
32123321321321
3123123123123123
13981897424
444123123123
```
4. Run test

## Benchmark
Command: `hashcat -b -m 22000 -w 3`

| Chip          | Hash mode                      | Speed (-w 3) | Speed (-w 4) | Time to run 8digit + phone dict est. (min) |
| ------------- | ------------------------------ | ------------ | ------------ | ------------------------------------------ |
| 4070 Ti super | 22000 (WPA-PBKDF2-PMKID+EAPOL) | 1149.4 kH/s  | 1237.4 kH/s  | 65                                         |
| NVIDIA RTX 4000 Ada Generation | 22000 (WPA-PBKDF2-PMKID+EAPOL) | 785.9 kH/s  | 791.0 kH/s  | -                                         |
| Apple M3 | 22000 (WPA-PBKDF2-PMKID+EAPOL) | 98568 H/s  | 101.9 kH/s  | -                                         |


## Reference
[Cracking WPA2-PSK with Hashcat](https://node-security.com/posts/cracking-wpa2-with-hashcat/)
[hashcat](https://hashcat.net/hashcat/)