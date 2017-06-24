# check_headers
Simple script to check for expected header values on multiple domains

## Usage
Adjust config settings and run with python
```
python check_headers.py
```


## Expected output
Something like this:
```
[URL] https://www.google.com
 [INFO] Following redirect to https://www.google.de/?gfe_rd=cr&ei=4JZOWdu6LrTb8Afp15-wAw
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] http://www.google.com
 [INFO] Following redirect to http://www.google.de/?gfe_rd=cr&ei=4JZOWdjZPK7b8Afht4-4DQ
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] https://www.google.de
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] http://www.google.de
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] https://www.google.fr
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] http://www.google.fr
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] https://www.google.it
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options

[URL] http://www.google.it
 [OK] x-frame-options: SAMEORIGIN
 [ERROR] Missing strict-transport-security
 [OK] x-xss-protection: 1; mode=block
 [ERROR] Missing x-content-type-options
```
