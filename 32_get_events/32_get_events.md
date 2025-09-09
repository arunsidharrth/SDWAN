# Use Case 32: Get Events - Retrieve System Events

## Overview

The **get_events.yml** playbook is an Ansible automation script designed to retrieve system events from Cisco SD-WAN vManage controllers. This playbook connects to the vManage API, authenticates using session-based authentication, and extracts comprehensive event information for monitoring, troubleshooting, and auditing purposes.

## Use Case

**Use Case 32: Get events - Retrieve system events**

This playbook addresses the need to:

- Retrieve real-time system events from the SD-WAN environment
- Monitor network events, alarms, and system status
- Extract event data for analysis and troubleshooting
- Create automated event collection for compliance and auditing
- Provide structured event data for integration with monitoring systems

## Prerequisites

### Environment Setup

The playbook uses hard-coded values optimized for Cisco DevNet sandbox environment:

| Variable | Value | Description |
|----------|-------|-------------|
| **vmanage_host** | sandbox-sdwan-2.cisco.com | vManage controller hostname |
| **vmanage_username** | devnetuser | Username for vManage authentication |
| **vmanage_password** | RG!_Yw919_83 | Password for vManage authentication |
| **vmanage_port** | 443 | HTTPS port for vManage access |

### vManage Version Compatibility

- **Supported Version**: vManage 20.15
- **API Endpoints**: Uses standard dataservice REST APIs
- **Authentication**: Session-based with CSRF token protection

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "sandbox-sdwan-2.cisco.com"
  vmanage_username: "devnetuser"
  vmanage_password: "RG!_Yw919_83"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  request_timeout: 30
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_events.yml
└── ../generated/
    ├── events.json
    └── events_summary.txt
```

## Task Analysis

### Task 1: Create Generated Directory

**Purpose:** Creates the output directory for event data files

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before data extraction
- Creates parent directories if they don't exist

### Task 2: Debug Variables

**Purpose:** Displays connection parameters for verification

**What it does:**
- Shows the vManage host, port, and constructed URL
- Provides visibility into connection parameters
- Helps troubleshoot connectivity issues
- Confirms proper variable assignment

### Task 3: Set Full URL

**Purpose:** Constructs the complete vManage API URL

**What it does:**
- Combines host and port into a complete HTTPS URL
- Creates the **vmanage_url** variable for consistent API calls
- Ensures proper URL formatting for all subsequent requests
- Provides a single point of URL management

### Task 4: Debug Final URL

**Purpose:** Confirms the constructed URL is correct

**What it does:**
- Displays the final URL that will be used for API calls
- Validates URL construction before making requests
- Helps identify URL formatting issues
- Provides debugging information for troubleshooting

### Task 5: Test vManage Connectivity

**Purpose:** Verifies the vManage controller is accessible

**What it does:**
- Makes an HTTP GET request to the vManage base URL
- Tests network connectivity and SSL/TLS functionality
- Accepts multiple status codes (200, 302, 401, 403) as valid responses
- Sets **30-second timeout** to handle network delays
- Ignores SSL certificate validation for lab environments

### Task 6: Authenticate and Get Session Token

**Purpose:** Establishes authenticated session with vManage

**Authentication method:** POST to `/j_security_check`

**What it does:**
- Sends username and password via form-encoded POST request
- Establishes session-based authentication with vManage
- Receives session cookies for subsequent API calls
- Uses the standard vManage authentication endpoint
- Handles authentication redirects (status codes 200, 302)

### Task 7: Extract Session Cookies

**Purpose:** Captures session cookies from authentication response

**What it does:**
- Extracts **cookies_string** from the login response
- Stores session cookies in the **session_cookies** variable
- Prepares authentication cookies for subsequent API calls
- Enables session persistence across multiple requests

### Task 8: Debug Session Cookies

**Purpose:** Displays session cookie information for verification

**What it does:**
- Shows the first 100 characters of the session cookie string
- Verifies that authentication was successful
- Provides debugging information for session issues
- Confirms JSESSIONID was properly obtained

### Task 9: Get CSRF Token

**Purpose:** Retrieves Cross-Site Request Forgery protection token

**API endpoint:** `/dataservice/client/token`

**What it does:**
- Makes authenticated GET request to the CSRF token endpoint
- Uses session cookies for authentication
- Retrieves the CSRF token required for data modification operations
- Sets **return_content: yes** to capture the token value
- Handles the token as plain text content

### Task 10: Debug CSRF Response

**Purpose:** Displays detailed CSRF token response information

**What it does:**
- Shows the HTTP status code from the token request
- Displays the actual CSRF token content
- Checks for JSON response format (typically not used)
- Provides comprehensive debugging information
- Helps troubleshoot CSRF token retrieval issues

### Task 11: Set CSRF Token

**Purpose:** Stores the CSRF token for API requests

**What it does:**
- Extracts the token from the response content
- Stores the token in the **csrf_token** variable
- Provides fallback logic for different response formats
- Prepares the token for use in subsequent API calls

### Task 12: Debug CSRF Token

**Purpose:** Confirms the CSRF token was properly extracted

**What it does:**
- Displays the complete CSRF token value
- Verifies token extraction was successful
- Provides the token value for debugging purposes
- Confirms token availability for API requests

### Task 13: Get System Events

**Purpose:** Retrieves system events from vManage

**API endpoint:** `/dataservice/event`

**What it does:**
- Makes authenticated GET request to the events API endpoint
- Uses session cookies and CSRF token for authentication
- Sets proper HTTP headers (Content-Type, Accept, X-XSRF-TOKEN)
- Retrieves comprehensive system event data
- Returns JSON-formatted event information
- Captures the response for file generation

### Task 14: Save Events to JSON File

**Purpose:** Creates structured JSON file with event data

**Generated file:** **events.json**

**What it does:**
- Converts the API response to formatted JSON
- Saves complete event data to the generated directory
- Creates human-readable JSON with proper indentation
- Preserves all event details and metadata
- Sets appropriate file permissions (644)

### Task 15: Create Events Summary

**Purpose:** Generates human-readable event summary

**Generated file:** **events_summary.txt**

**What it does:**
- Creates a structured text summary of retrieved events
- Displays total event count and source information
- Shows details for the first 10 events including:
  - Event ID and event name/type
  - Device system IP address
  - Event severity level
  - Event timestamp
- Indicates if additional events are available
- Provides overview information for quick assessment

## Generated Files

### events.json
Contains the complete JSON response from the vManage events API, including:
- **Event metadata**: Event IDs, types, timestamps
- **Device information**: System IPs, hostnames, device types
- **Event details**: Severity levels, descriptions, categories
- **System data**: Complete API response structure

### events_summary.txt
Contains a human-readable summary including:
- **Event count**: Total number of events retrieved
- **Source information**: vManage controller URL
- **Event preview**: First 10 events with key details
- **Overview data**: Quick assessment information

## Report Contents

The retrieved event data typically includes:

- **System Events**: Device status changes, connectivity events
- **Alarm Information**: Critical system alarms and notifications
- **Network Events**: Interface status, routing changes, connectivity issues
- **Security Events**: Authentication events, policy violations
- **Performance Events**: Bandwidth utilization, latency issues
- **Configuration Events**: Template changes, policy updates
- **Device Events**: Device registration, deregistration, status changes