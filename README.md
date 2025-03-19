# Sufuss - Sophos License Server Simulator

Sufuss is a simulator for the Sophos license server, designed to work with Sophos XGS firewalls, especially SFOS 18.5.0. It provides a simulated environment for testing license validation and activation without connecting to the actual Sophos license servers.

## Features

- Simulates Sophos license validation and activation endpoints
- Works with Sophos XGS87 running SFOS 18.5.0
- Provides DNS redirection for Sophos domains
- Generates SSL certificates for secure connections
- Includes a dashboard for managing simulated licenses
- Logs all license validation and activation requests

## Requirements

- Ubuntu 20.04 or newer, or any Debian-based Linux distribution
- Python 3.8 or newer
- PostgreSQL 12 or newer
- DNSMasq for DNS redirection
- Network access from Sophos devices to the Sufuss server

## Quick Start Guide

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sufuss.git
   cd sufuss
   ```

2. Set up the Python environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   sudo -u postgres psql -c "CREATE USER sufuss WITH PASSWORD 'sufuss';"
   sudo -u postgres psql -c "CREATE DATABASE sufuss OWNER sufuss;"
   alembic upgrade head
   ```

4. Generate SSL certificates:
   ```
   bash scripts/generate_certs.sh
   ```

5. Configure DNS redirection:
   ```
   sudo bash scripts/configure_dns.sh
   ```

6. Start the Sufuss server:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile ./app/certificates/server.key --ssl-certfile ./app/certificates/server.crt
   ```

### Running as a Service

To run Sufuss as a system service:

1. Create a service file:
   ```
   sudo nano /etc/systemd/system/sufuss-api.service
   ```

2. Add the following configuration:
   ```
   [Unit]
   Description=Sufuss API Server
   After=network.target postgresql.service

   [Service]
   User=your_username
   Group=your_usergroup
   WorkingDirectory=/path/to/sufuss
   Environment="PATH=/path/to/sufuss/venv/bin"
   ExecStart=/path/to/sufuss/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile ./app/certificates/server.crt --ssl-certfile ./app/certificates/server.key

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable sufuss-api
   sudo systemctl start sufuss-api
   ```

## Configuring Sophos XGS87 with SFOS 18.5.0

### Step 1: Configure DNS Settings

1. Access your Sophos XGS87 admin interface
2. Navigate to Network → DNS
3. Set your Sufuss server IP as the primary DNS server
4. Save and apply changes

### Step 2: Import the CA Certificate

1. Download the Sufuss CA certificate from `http://YOUR_SUFUSS_SERVER:8000/certificates/ca`
2. In the Sophos admin interface, go to System → Certificates
3. Select "Certificate Authorities" tab
4. Click "Add" and upload the Sufuss CA certificate
5. Configure the following settings:
   - Name: Sufuss CA
   - Description: Sufuss License Server Simulator
   - Certificate Purpose: Select all options
6. Save the certificate

### Step 3: Test License Validation

1. Go to System → Licensing
2. Click "Synchronize" to test the connection to the simulated license server
3. If everything is configured correctly, you should see a successful synchronization message

## Troubleshooting

### DNS Issues

If the Sophos device is not resolving Sophos domains to your Sufuss server:

1. Verify dnsmasq is running: `systemctl status dnsmasq`
2. Test DNS resolution: `dig @YOUR_SUFUSS_SERVER api.sophos.com`
3. Check dnsmasq configuration: `cat /etc/dnsmasq.d/sophos-redirect.conf`

### Certificate Issues

If the Sophos device shows SSL certificate errors:

1. Verify the CA certificate is imported correctly
2. Regenerate certificates: `bash scripts/generate_certs.sh`
3. Ensure all Sophos domains are included in the certificate's SAN

### Connection Issues

If the Sophos device cannot connect to the Sufuss server:

1. Check firewall rules to ensure ports 443 and 53 are open
2. Verify the Sufuss server is reachable from the Sophos device
3. Check the Sufuss logs: `journalctl -u sufuss-api -f`

## Specific for SFOS 18.5.0

SFOS 18.5.0 requires additional domains to be redirected and has different API endpoints. The scripts and configuration have been updated to support this version specifically, including:

- Additional Sophos domains in DNS redirection
- More SAN entries in SSL certificates
- SFOS 18.5.0 specific API endpoints
- Better error handling and logging

### SFOS 18.5.0 Specific Domains

The following domains are critical for SFOS 18.5.0:
- skuld.sophos.com
- central.sophos.com
- est.sophos.com
- downloads.sophos.com
- auth-info.sophos.com
- cloud.sophos.com
- id.sophos.com
- licensing.sophos.com
- firmware.sophos.com
- origin-firmware.sophos.com
- sav.sophos.com
- sophosupd.com

All these domains are automatically redirected to your Sufuss server.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is provided as-is and is intended for testing purposes only. It is not affiliated with or endorsed by Sophos. Use at your own risk. 