# ETS VPN Autologin
This project automates the extraction of authentication cookies (specifically the `webvpn` cookie) from the Office365 ETS login flow that uses TOTP (Time-based One-Time Password) and then uses the cookie to connect to a VPN service. It also includes a Node.js utility for extracting OTP codes from Google Authenticator migration QR codes.

## Features

- **Python Automation**: Uses Playwright to automate login and extract cookies from a web service (e.g., https://accesvpn.etsmtl.ca).
- **TOTP Support**: Generates TOTP codes for 2FA using a shared secret.
- **Shell Script**: Runs the Python automation and uses the extracted cookie to connect to the VPN with `openconnect`.
- **Node.js Utility**: Extracts OTP codes from Google Authenticator migration QR codes using a provided script.

## Structure

```
config.json                # Credentials and secrets (not tracked in git)
main.py                    # Main Python script for cookie extraction
script.sh                  # Shell script to automate the process

totp.py                    # TOTP code generator

google_qr-code_extractor/  # Node.js utility for QR code extraction
  ├── index.js
  ├── migration-payload.proto
  ├── otp-codes.sh
  └── package.json
```

## Setup

### Python Environment
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

### Node.js Environment (for QR code extraction)
1. Install dependencies:
   ```bash
   cd google_qr-code_extractor
   npm install
   ```

## Usage

### 1. Configure Credentials
Create a `config.json` file in the root directory with the following structure:
```json
{
  "username": "your_username",
  "password": "your_password",
  "totp_secret": "YOUR_TOTP_SECRET"
}
```

### 2. Extract Cookie and Connect to VPN
Run the shell script:
```bash
./script.sh
```
This will:
- Activate the Python environment
- Run the Python script to extract the `webvpn` cookie
- Use `openconnect` to connect to the VPN using the cookie

### 3. Extract OTP Codes from Google Authenticator QR (only need to be done once)
To extract OTP codes from a Google Authenticator migration QR code:
```bash
cd google_qr-code_extractor
node index.js "YOUR_QR_CODE_STRING"
```

## Notes
- The `config.json` file should **not** be committed to version control as it contains sensitive information.
- The Python script requires Playwright and a supported browser (installed via `playwright install`).
- The Node.js utility requires Node.js and npm.

## License
MIT
