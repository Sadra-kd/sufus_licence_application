#!/bin/bash

# Script to restart Sufuss services after configuration changes
# This script must be run with root privileges

# Check if script is running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo)"
  exit 1
fi

echo "====== Sufuss Service Restart Tool ======"
echo "This script will restart all Sufuss services and regenerate SSL certificates"
echo

# Stop services
echo "Stopping Sufuss services..."
systemctl stop sufuss-api.service
systemctl stop dnsmasq.service

# Regenerate certificates
echo "Regenerating SSL certificates..."
cd /home/sufus_licence_application
bash scripts/generate_certs.sh

# Update DNS configuration
echo "Updating DNS configuration..."
bash scripts/configure_dns.sh

# Restart services
echo "Starting Sufuss services..."
systemctl start dnsmasq.service
systemctl start sufuss-api.service

# Check service status
echo
echo "Service status:"
echo "---------------"
echo "DNS service:"
systemctl status dnsmasq.service --no-pager | grep Active
echo
echo "Sufuss API service:"
systemctl status sufuss-api.service --no-pager | grep Active
echo

# Display connection information
echo "Testing information:"
echo "-------------------"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Your Sufuss server IP is: $IP_ADDRESS"
echo
echo "1. Make sure your Sophos XGS87 is using $IP_ADDRESS as its DNS server"
echo "2. Import the CA certificate into your Sophos XGS87 from:"
echo "   http://$IP_ADDRESS:8000/certificates/ca"
echo "3. Test DNS redirection with:"
echo "   dig @$IP_ADDRESS api.sophos.com"
echo "   The answer should point to $IP_ADDRESS"
echo
echo "For Sophos XGS87 SFOS 18.5.0, the following domains are redirected:"
echo "- api.sophos.com"
echo "- license.sophos.com"
echo "- update.sophos.com"
echo "- skuld.sophos.com"
echo "- central.sophos.com"
echo "- est.sophos.com"
echo "- downloads.sophos.com"
echo "- auth-info.sophos.com"
echo "- cloud.sophos.com"
echo "- id.sophos.com"
echo "- licensing.sophos.com"
echo "- firmware.sophos.com"
echo "- origin-firmware.sophos.com"
echo "- sav.sophos.com"
echo "- sophosupd.com"
echo
echo "Restart complete!" 