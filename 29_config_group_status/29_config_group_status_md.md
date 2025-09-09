# Configuration Group Status Playbook Documentation

## Overview

The **config_group_status.yml** playbook is an Ansible automation script designed to retrieve configuration group status from Cisco SD-WAN environments. This playbook handles API endpoint changes in vManage 20.15 by testing multiple potential endpoints and gracefully falling back to working alternatives when specific configuration group APIs are unavailable.

## Use Case

**Use Case 29: Get configuration group status - Retrieve configuration group status information**

This playbook addresses the need to:

- Retrieve configuration group status from the SD-WAN environment
- Handle API endpoint changes in vManage 20.15
- Test multiple endpoints to find working configuration APIs
- Export configuration group or related template data for analysis
- Provide automated status reporting with fallback mechanisms

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage-amfament-prod.sdwan.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | automation |
| **VMANAGE_PASSWORD** | Password for vManage authentication | |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── config_group_status.yml
└── generated/
    └── config_groups/
        ├── config_group_status.json
        └── endpoint_info.txt
```

## Task Analysis

#### Task 1: Gathering Facts

**Purpose:** Collects system facts including timestamp information for logging

**What it does:**
- Gathers Ansible facts from the localhost
- Provides timestamp data for endpoint information logging
- Enables access to `ansible_date_time` variables

#### Task 2: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, and **VMANAGE_PASSWORD** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

#### Task 3: Directory Creation

**Purpose:** Creates the output directory structure for generated reports

**What it does:**
- Creates the **generated/config_groups** directory relative to the playbook location
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before data retrieval
- Creates parent directories if they don't exist

#### Task 4: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting data retrieval

**What it does:**
- Makes a REST API call to **/dataservice/system/device/controllers**
- Uses basic authentication with provided credentials
- Sets **60-second timeout** to handle slow connections
- Ignores SSL certificate validation for internal/self-signed certificates
- Stores connectivity results for validation

#### Task 5: Connectivity Validation

**Purpose:** Stops execution if connectivity test fails

**What it does:**
- Checks if the connectivity test returned **HTTP 200** status
- Fails the playbook with descriptive error if vManage is unreachable
- Prevents unnecessary API operations when connectivity issues exist
- Provides clear failure messaging for troubleshooting

#### Task 6: Try Primary Configuration Group Endpoint

**Purpose:** Attempts to retrieve configuration group data from the primary modern API endpoint

**API endpoint tested:** `/dataservice/v1/config-group`

**What it does:**
- Connects to vManage using the v1 configuration group API
- Uses basic authentication with provided credentials
- Sets appropriate JSON headers for API communication
- Ignores errors to allow fallback to alternative endpoints
- Stores results for later evaluation

#### Task 7: Try Alternative Configuration Group Endpoint

**Purpose:** Tests an alternative configuration group endpoint if the primary fails

**API endpoint tested:** `/dataservice/configgroup`

**What it does:**
- Only executes if the primary endpoint returned non-200 status
- Tests alternative configuration group API format
- Uses same authentication and timeout settings
- Ignores errors to continue with additional fallbacks
- Stores results for comparison and selection

#### Task 8: Try Device Template Groups Endpoint

**Purpose:** Falls back to device template endpoint for configuration-related data

**API endpoint tested:** `/dataservice/template/device`

**What it does:**
- Only executes if both configuration group endpoints failed
- Retrieves device template information as a configuration proxy
- Provides related configuration data when specific group APIs are unavailable
- Uses same authentication and error handling approach
- Stores results as final fallback option

#### Task 9: Set Final Result

**Purpose:** Determines which endpoint was successful and selects the appropriate data

**What it does:**
- Evaluates the status codes from all attempted endpoints
- Selects the first successful response (HTTP 200) in priority order
- Sets the `final_result` variable with the working endpoint's data
- Enables conditional file saving based on successful data retrieval

#### Task 10: Save Configuration Data

**Purpose:** Saves the retrieved configuration data to a JSON file

**Generated file:** **config_group_status.json**

**What it does:**
- Saves the successful API response as formatted JSON
- Only executes if valid data was retrieved from any endpoint
- Creates standardized output file in the config_groups subdirectory
- Preserves original API response structure and content

#### Task 11: Save Endpoint Information

**Purpose:** Creates a detailed log of endpoint testing and results

**Generated file:** **endpoint_info.txt**

**What it does:**
- Documents which endpoint was successful
- Records the HTTP status code and timestamp
- Lists all endpoints that were tested
- Provides troubleshooting information for API changes
- Creates a reference for future playbook updates

#### Task 12: Completion Notification

**Purpose:** Provides execution status and file location information

**What it displays:**
- Full path to the generated configuration data file
- Successful endpoint URL that provided the data
- Completion confirmation message
- Error message if no data was retrieved

## Report Contents

The generated reports contain:

- **config_group_status.json:** Configuration group data or device template information, including:
  - Template configurations and metadata
  - Associated device information
  - Configuration status and deployment details
  - Template definitions and parameters

- **endpoint_info.txt:** Endpoint testing results, including:
  - Successful endpoint URL and status
  - List of all tested endpoints
  - Timestamp of data retrieval
  - Troubleshooting reference information