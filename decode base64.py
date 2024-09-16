import base64

# Base64 encoded string
base64_str = "j3=DEOowFcEwFHl6EOAyFcoUFV=TVEchwFHlUFOo6lVTTDcATE7oUE7AUET=="

# Clean up the Base64 string
base64_str = base64_str.replace("=", "")

try:
    # Decode the Base64 data
    decoded_data = base64.b64decode(base64_str, validate=True)

    # Output the decoded data
    decoded_text = decoded_data.decode('utf-8', errors='ignore')
    print("Decoded Data:\n", decoded_text)
except Exception as e:
    print("An error occurred:", e)
