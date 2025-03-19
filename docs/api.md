# Sufuss API Documentation

This document provides details on the available API endpoints for the Sufuss - Sophos License Server Simulator.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

The API endpoints do not require authentication as they are designed to simulate the Sophos license server API which doesn't use authentication for license validation.

## Endpoints

### License Management

#### Validate License

```
POST /api/v1/license/validate
```

Validates a license key for a specific device.

**Request Body:**

```json
{
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "device_id": "DEVICE-12345"
}
```

**Response:**

```json
{
  "valid": true,
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "status": "registered",
  "expiry_date": "2023-12-31T23:59:59.999Z",
  "services": [
    {
      "name": "Firewall",
      "feature_code": "FW",
      "status": "running",
      "description": "Sophos Firewall Service"
    },
    {
      "name": "IPS",
      "feature_code": "IPS",
      "status": "running",
      "description": "Intrusion Prevention System"
    }
  ],
  "message": "License is valid"
}
```

#### Activate License

```
POST /api/v1/license/activate
```

Activates a license for a specific device.

**Request Body:**

```json
{
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "device_id": "DEVICE-12345",
  "device_name": "My Sophos Firewall",
  "device_type": "physical",
  "model": "XG 135",
  "firmware_version": "18.5.0",
  "ip_address": "192.168.1.1"
}
```

**Response:**

```json
{
  "success": true,
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "status": "registered",
  "expiry_date": "2023-12-31T23:59:59.999Z",
  "services": [
    {
      "name": "Firewall",
      "feature_code": "FW",
      "status": "running",
      "description": "Sophos Firewall Service"
    },
    {
      "name": "IPS",
      "feature_code": "IPS",
      "status": "running",
      "description": "Intrusion Prevention System"
    }
  ],
  "message": "License activated successfully"
}
```

#### Get License Status

```
POST /api/v1/license/status
```

Gets the status of a license for a specific device.

**Request Body:**

```json
{
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "device_id": "DEVICE-12345"
}
```

**Response:**

```json
{
  "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
  "status": "registered",
  "expiry_date": "2023-12-31T23:59:59.999Z",
  "is_active": true,
  "services": [
    {
      "name": "Firewall",
      "feature_code": "FW",
      "status": "running",
      "description": "Sophos Firewall Service"
    },
    {
      "name": "IPS",
      "feature_code": "IPS",
      "status": "running",
      "description": "Intrusion Prevention System"
    }
  ]
}
```

### Device Management

#### Register Device

```
POST /api/v1/device/register
```

Registers a device without associating it with a license yet.

**Request Body:**

```json
{
  "device_id": "DEVICE-12345",
  "name": "My Sophos Firewall",
  "device_type": "physical",
  "model": "XG 135",
  "firmware_version": "18.5.0",
  "ip_address": "192.168.1.1"
}
```

**Response:**

```json
{
  "success": true,
  "device_id": "DEVICE-12345",
  "message": "Device registered successfully"
}
```

#### Get Device Information

```
GET /api/v1/device/{device_id}
```

Gets information about a specific device.

**Response:**

```json
{
  "device_id": "DEVICE-12345",
  "name": "My Sophos Firewall",
  "device_type": "physical",
  "model": "XG 135",
  "firmware_version": "18.5.0",
  "ip_address": "192.168.1.1",
  "id": 1,
  "license_id": 1,
  "last_seen": "2023-05-31T12:34:56.789Z",
  "is_active": true,
  "created_at": "2023-05-31T12:00:00.000Z",
  "updated_at": "2023-05-31T12:34:56.789Z"
}
```

#### List Devices

```
GET /api/v1/device/
```

Lists all registered devices.

**Query Parameters:**

- `skip` (optional): Number of devices to skip (default: 0)
- `limit` (optional): Maximum number of devices to return (default: 100)

**Response:**

```json
[
  {
    "device_id": "DEVICE-12345",
    "name": "My Sophos Firewall",
    "device_type": "physical",
    "model": "XG 135",
    "firmware_version": "18.5.0",
    "ip_address": "192.168.1.1",
    "id": 1,
    "license_id": 1,
    "last_seen": "2023-05-31T12:34:56.789Z",
    "is_active": true,
    "created_at": "2023-05-31T12:00:00.000Z",
    "updated_at": "2023-05-31T12:34:56.789Z"
  }
]
```

## Error Responses

All API endpoints can return the following error responses:

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error. Please check the logs for more details."
}
``` 