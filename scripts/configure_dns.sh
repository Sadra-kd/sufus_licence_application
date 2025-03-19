#!/bin/bash

# Directory for DNS configuration
DNS_DIR="/etc/dnsmasq.d"
CONFIG_FILE="$DNS_DIR/sophos-redirect.conf"

# Check if script is running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Ensure dnsmasq is installed
if ! command -v dnsmasq &> /dev/null; then
  echo "dnsmasq is not installed. Installing..."
  apt-get update && apt-get install -y dnsmasq
  if [ $? -ne 0 ]; then
    echo "Failed to install dnsmasq. Exiting."
    exit 1
  fi
fi

# Create directory if it doesn't exist
mkdir -p $DNS_DIR

# Get the server IP address or use provided IP
if [ -z "$1" ]; then
  # Try to get the primary IP address
  SERVER_IP=$(hostname -I | awk '{print $1}')
  if [ -z "$SERVER_IP" ]; then
    echo "Could not determine server IP. Please provide IP as argument."
    echo "Usage: $0 [server_ip]"
    exit 1
  fi
else
  SERVER_IP=$1
fi

# Create or overwrite the configuration file
cat > $CONFIG_FILE << EOF
# Sophos License Server DNS Redirection
# Generated on $(date)

# Main Sophos domains
address=/api.sophos.com/$SERVER_IP
address=/license.sophos.com/$SERVER_IP
address=/update.sophos.com/$SERVER_IP
address=/skuld.sophos.com/$SERVER_IP
address=/central.sophos.com/$SERVER_IP
address=/est.sophos.com/$SERVER_IP
address=/downloads.sophos.com/$SERVER_IP
address=/auth-info.sophos.com/$SERVER_IP
address=/cloud.sophos.com/$SERVER_IP
address=/id.sophos.com/$SERVER_IP

# Additional domains for SFOS 18.5.0
address=/licensing.sophos.com/$SERVER_IP
address=/firmware.sophos.com/$SERVER_IP
address=/origin-firmware.sophos.com/$SERVER_IP
address=/sav.sophos.com/$SERVER_IP
address=/sophosupd.com/$SERVER_IP
EOF

# Restart dnsmasq
systemctl restart dnsmasq

# Check if dnsmasq is running
if systemctl is-active --quiet dnsmasq; then
  echo "DNS configuration successful. All Sophos domains now redirect to $SERVER_IP"
  echo "Configuration file: $CONFIG_FILE"
else
  echo "Error: dnsmasq failed to start. Check logs with 'journalctl -u dnsmasq'"
  exit 1
fi

# Configure firewall to allow DNS queries (if UFW is installed)
if command -v ufw &> /dev/null; then
  echo "Configuring firewall to allow DNS queries..."
  ufw allow 53/udp
  ufw allow 53/tcp
  echo "Firewall configured."
fi

# Display testing instructions
echo ""
echo "Testing instructions:"
echo "---------------------"
echo "1. Configure your Sophos device to use this server ($SERVER_IP) as its DNS server"
echo "2. On any machine, test the DNS redirection with:"
echo "   dig @$SERVER_IP api.sophos.com"
echo "   dig @$SERVER_IP license.sophos.com"
echo "   The A record in the answer section should show $SERVER_IP"
echo ""
echo "3. Make sure to install the CA certificate on your Sophos device."
echo "   The CA certificate is available at: http://$SERVER_IP:8000/certificates/ca" 