# Troubleshooting Guide

This document provides solutions to common issues that may arise when using the Sufuss - Sophos License Server Simulator.

## SSL Certificate Issues

### Problem: Sophos device doesn't trust the simulator's SSL certificate

**Symptoms:**
- Sophos device fails to connect to the simulator
- Error messages about invalid certificate
- TLS handshake failures in logs

**Solutions:**

1. **Import CA Certificate to Sophos device:**
   - Copy the generated CA certificate (`app/certificates/ca.crt`) to the Sophos device
   - In the Sophos web interface, go to:
     - Certificates > Certificate Authorities > Add
     - Upload the CA certificate

2. **Check Certificate Domain Names:**
   - Ensure that the SSL certificate has the correct Subject Alternative Names (SANs) for all Sophos domains:
     - api.sophos.com
     - license.sophos.com
     - update.sophos.com
     - *.sophos.com
   - If necessary, regenerate the certificate:
     ```
     ./scripts/generate_certs.sh
     ```

3. **Check Certificate Dates:**
   - Verify that the certificate has not expired:
     ```
     openssl x509 -in app/certificates/server.crt -text -noout | grep "Not After"
     ```

## DNS Redirection Issues

### Problem: Sophos device is still connecting to the real Sophos servers

**Symptoms:**
- No connection attempts visible in the simulator logs
- Device continues to show real license status

**Solutions:**

1. **Verify DNS Configuration:**
   - Check if dnsmasq is running:
     ```
     systemctl status dnsmasq
     ```
   - Check dnsmasq configuration:
     ```
     cat /etc/dnsmasq.conf | grep sophos
     ```
   - Verify that the Sophos device is using the DNS server:
     ```
     nslookup api.sophos.com
     ```

2. **Configure Device to Use Your DNS Server:**
   - In the Sophos web interface, go to:
     - Network > DNS
     - Set the primary DNS server to your simulator server's IP address

3. **Use Hosts File Instead:**
   - If DNS redirection is not working, edit the hosts file on the Sophos device (if accessible):
     ```
     YOUR_SERVER_IP    api.sophos.com
     YOUR_SERVER_IP    license.sophos.com
     YOUR_SERVER_IP    update.sophos.com
     ```

4. **Use HTTP Proxy:**
   - Configure the Sophos device to use your server as an HTTP proxy:
     ```
     set advanced-firewall http-proxy YOUR_SERVER_IP:8000
     ```

## Database Issues

### Problem: Database connection errors

**Symptoms:**
- Application fails to start with database errors
- API calls return 500 errors

**Solutions:**

1. **Check PostgreSQL Service:**
   - Verify PostgreSQL is running:
     ```
     systemctl status postgresql
     ```
   - For Docker deployments:
     ```
     docker-compose ps
     ```

2. **Check Database Connection String:**
   - Verify that the `DATABASE_URL` environment variable is correctly set in `.env` file or environment
   - Default: `postgresql://postgres:postgres@localhost/sufuss`

3. **Create Database Manually:**
   ```
   sudo -u postgres psql
   CREATE DATABASE sufuss;
   ```

4. **Reset Database:**
   ```
   sudo -u postgres psql
   DROP DATABASE sufuss;
   CREATE DATABASE sufuss;
   ```
   Then re-initialize the database:
   ```
   python -m app.db.init_db
   ```

## License Activation Issues

### Problem: License activation fails

**Symptoms:**
- API calls to `/license/activate` return errors
- Device shows license as invalid

**Solutions:**

1. **Check License Existence:**
   - Verify the license exists in the database using the admin interface
   - If not, create a new license through the admin interface

2. **Check License Status:**
   - Ensure the license status is "registered" and not expired
   - Verify that `is_active` is set to `true`

3. **Check Device Association:**
   - A device must be associated with a valid license
   - Try registering the device first with `/device/register`

## Performance Issues

### Problem: Slow response times or high CPU usage

**Symptoms:**
- API responses are slow
- Server CPU usage is high

**Solutions:**

1. **Use Production ASGI Server:**
   - Replace uvicorn with gunicorn for production:
     ```
     pip install gunicorn
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
     ```

2. **Optimize Database Queries:**
   - Add indexes to frequently queried columns:
     ```sql
     CREATE INDEX idx_license_key ON licenses (license_key);
     CREATE INDEX idx_device_id ON devices (device_id);
     ```

3. **Increase Resources:**
   - Allocate more memory and CPU to the server
   - For Docker, update the resource limits in `docker-compose.yml`

## Common Error Messages

### "License key not found"

- Ensure you're using the correct license key format
- Check if the license exists in the database
- Create a new license through the admin interface

### "Device not found"

- Register the device first with `/device/register`
- Check device_id format and consistency

### "Database connection failed"

- Verify PostgreSQL is running
- Check connection string in `.env` file
- Confirm database name, username, and password are correct

### "SSL certificate validation failed"

- Import CA certificate to Sophos device
- Check certificate domains and dates
- Regenerate certificates if necessary

## Getting Help

If you encounter issues not covered in this guide:

1. Check the application logs:
   ```
   docker-compose logs app
   ```

2. Enable debug logging by setting environment variable:
   ```
   export LOG_LEVEL=DEBUG
   ```

3. Consult the [API Documentation](api.md) for correct request formats

4. Check the [README.md](../README.md) for setup instructions 