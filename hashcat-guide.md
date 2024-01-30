# Use Hashcat to crack password
Hashcat supports GPU, so the speed will be faster than CPU, this is a guide to use MacBook to run hashcat

## Install tools
1. Install hcxtools and hashcat
```bash
brew install hcxtools hashcat
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
cap_name=$(basename ${caps} .cap)
hcxpcapngtool ${caps} -o ${cap_name}_hash.txt
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
# Windows
hashcat.exe -m 22000 -w 3 .\toCrack\wifiHashes.txt .\passwordLists\hashkiller-dict.txt

# Mac
hash_file=${cap_name}_hash.txt
hashcat -D 2 -d 3 -m 22000 -w 3 ${hash_file} ${dict} -o ${cap_name}_key.txt --potfile-path ${cap_name}.potfile
```
Parameter explain:
`-D 2` will force the hashcat to only look for GPUs. (-D is for specifying device type)
`-d 3` will force it to use the Radeon Pro 560X Compute Engine. (-d is for specifying the backend device number)

## Test
1. Say `cap_name=test`
2. Test hasfile, save it as `${cap_name}_hash.txt`
```bash
WPA*02*49526c027401f63edc80c85aa442d750*9c7f81f75873*902bd2173a69*373032*e68ae1f2d3035d0331929680c7b37a34cbb5a6a49818508d8aa0ce1fc15731ea*0103007502010a00000000000000000001cee19b37dacef48e3fef8da8e293941ee5982787b9a3d8f60fc8d5e1e80f14b4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001630140100000fac040100000fac040100000fac020000*82
``` 
3. Test key `13981897424`, save it as dictionary


## Reference
[Cracking WPA2-PSK with Hashcat](https://node-security.com/posts/cracking-wpa2-with-hashcat/)
[hashcat](https://hashcat.net/hashcat/)