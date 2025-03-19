# Changelog

## Version 0.2.0 (Latest)

### Added
- Enhanced support for Sophos XGS87 running SFOS 18.5.0
- Added additional Sophos domains to DNS redirection
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
- Extended SSL certificate Subject Alternative Names (SAN) to cover all required domains
- Added new API endpoint handlers:
  - Central management endpoints
  - API endpoints
  - Services endpoints
  - Download/update endpoints
  - Authentication endpoints
- Created static file serving for additional resources
- Added restart_services.sh script to easily restart all services after configuration changes
- Improved detailed logging with prefixes for better troubleshooting
- Added Content-Disposition header for certificate downloads to improve browser handling

### Changed
- Enhanced existing API endpoint handlers with better logging and response structures
- Improved error handling in catch-all routes
- Updated main.py to handle a wider variety of SFOS 18.5.0 requests
- Modified exception handler to provide more detailed logging
- Updated configure_dns.sh script to support more domains and provide better feedback
- Updated generate_certs.sh to include all necessary domains and improve certificate generation
- Expanded README with specific instructions for SFOS 18.5.0

### Fixed
- DNS configuration now properly redirects all required domains for SFOS 18.5.0
- Certificate generation now includes all required SANs for proper validation
- Improved error recovery to provide valid license responses even when exceptions occur

## Version 0.1.0

### Initial Release
- Basic Sophos license server simulation
- License validation and activation endpoints
- DNS redirection for core Sophos domains
- SSL certificate generation and handling
- PostgreSQL database integration for license storage
- Basic web interface for license management 