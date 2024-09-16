import base64

# Base64 encoded string from your input
base64_str = "j3=3DEOowFcEwFHl6EOAyFcoUFV=TVEchwFHlUFOo6lVTTDcATE7oUE7AUET=3D=3D"

# Clean Base64 string
base64_str = base64_str.replace("=", "")  # Remove unnecessary '='
base64_str = base64_str.replace("3D", "=")  # Convert '3D' to '='

# Add padding if necessary
padding_needed = len(base64_str) % 4
if padding_needed:
    base64_str += '=' * (4 - padding_needed)

try:
    # Decode the Base64 data
    decoded_data = base64.b64decode(base64_str)
    print("Decoded Data (Binary):", decoded_data)
except Exception as e:
    print("An error occurred:", e)
