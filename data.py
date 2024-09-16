import base64

# Binary data you obtained
decoded_data = b'\x8fq\x0e\xa3\x01\\\x13\x01G\x97\xa1\x0e\x03!\\\xa1AUMQ\x1c\x87\x01G\x95AN\xa3\xa9UM0\xdc\x011;\xa1A;\x01A\x13'

# Save the binary data to a file
with open('output.bin', 'wb') as f:
    f.write(decoded_data)
