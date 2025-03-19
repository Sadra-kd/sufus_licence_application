#!/bin/bash

# Create certificates directory if it doesn't exist
CERT_DIR="./app/certificates"
mkdir -p $CERT_DIR

# Generate CA key and certificate
openssl genrsa -out $CERT_DIR/ca.key 4096
openssl req -x509 -new -nodes -key $CERT_DIR/ca.key -sha256 -days 3650 -out $CERT_DIR/ca.crt \
    -subj "/C=US/ST=State/L=City/O=Sufuss Simulator/OU=Sufuss CA/CN=Sufuss Root CA"

# Generate server key and CSR
openssl genrsa -out $CERT_DIR/server.key 2048
openssl req -new -key $CERT_DIR/server.key -out $CERT_DIR/server.csr \
    -subj "/C=US/ST=State/L=City/O=Sufuss Simulator/OU=Sufuss Server/CN=api.sophos.com"

# Create config file for SAN (Subject Alternative Names)
cat > $CERT_DIR/server.ext << EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = api.sophos.com
DNS.2 = license.sophos.com
DNS.3 = update.sophos.com
DNS.4 = *.sophos.com
DNS.5 = localhost
DNS.6 = skuld.sophos.com
DNS.7 = central.sophos.com
DNS.8 = est.sophos.com
DNS.9 = downloads.sophos.com
DNS.10 = auth-info.sophos.com
DNS.11 = cloud.sophos.com
DNS.12 = id.sophos.com
DNS.13 = sophosupd.com
DNS.14 = *.sophosupd.com
DNS.15 = licensing.sophos.com
DNS.16 = firmware.sophos.com
DNS.17 = origin-firmware.sophos.com
DNS.18 = sav.sophos.com
EOF

# Sign the CSR with our CA
openssl x509 -req -in $CERT_DIR/server.csr -CA $CERT_DIR/ca.crt -CAkey $CERT_DIR/ca.key \
    -CAcreateserial -out $CERT_DIR/server.crt -days 3650 -sha256 -extfile $CERT_DIR/server.ext

# Verify the certificate
openssl verify -CAfile $CERT_DIR/ca.crt $CERT_DIR/server.crt

# Display certificate details
echo "Certificate details:"
openssl x509 -in $CERT_DIR/server.crt -text -noout | grep -E "Subject:|DNS:"

# Clean up intermediate files
rm $CERT_DIR/server.csr $CERT_DIR/server.ext

echo "SSL certificates generated in $CERT_DIR directory."
echo "Install $CERT_DIR/ca.crt as a trusted CA on Sophos devices."
echo "The CA certificate is also available at: http://YOUR_SERVER_IP:8000/certificates/ca" 