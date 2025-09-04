# Use Case 27: List Configuration Groups - Get all configuration groups

## Overview

The **list_config.yml** playbook is an Ansible automation script designed to retrieve configuration groups from Cisco SD-WAN environments. This playbook leverages the vManage REST API to extract configuration group information and produces organized reports for analysis, documentation, and auditing purposes.

## Use Case

**Use Case: List Configuration Groups - Get all configuration groups**

This playbook addresses the need to:

- Retrieve all configuration groups from the SD-WAN environment
- Document configuration group details including names, descriptions, and associated templates
- Create baseline reports for change management and compliance
- Export configuration group data for offline analysis and review
- Provide automated reporting for regular audits and documentation updates

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | sandbox-sdwan-2.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | devnetuser |
| **VMANAGE_PASSWORD** | Password for vManage authentication | RG!_Yw919_83 |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('sandbox-sdwan-2.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('devnetuser') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('RG!_Yw919_83') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  config_groups_subdir: "{{ generated_dir }}/config_groups"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── list_config.yml
└── ../generated/
    └── config_groups/
        ├── config_groups_data.json
        ├── config_groups_data.txt
        ├── device_templates_data.json
        └── device_templates_data.txt
```

## Task Analysis

#### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, and **VMANAGE_PASSWORD** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

#### Task 2: Directory Creation

**Purpose:** Creates the output directory for generated reports

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before report generation
- Creates parent directories if they don't exist

#### Task 3: Config Groups Subdirectory Creation

**Purpose:** Creates organized subdirectory for configuration group reports

**What it does:**
- Creates the **config_groups** subdirectory within generated folder
- Maintains organized file structure for different use cases
- Sets appropriate permissions for file access
- Prevents file conflicts with other playbook outputs

#### Task 4: Login to vManage and Get Session

**Purpose:** Authenticates with vManage using form-based login

**What it does:**
- Makes a POST request to **/j_security_check** endpoint
- Uses form-encoded authentication with username and password
- Establishes session cookies for subsequent API calls
- Sets 60-second timeout for connection handling
- Ignores SSL certificate validation for sandbox environments

#### Task 5: Get CSRF Token

**Purpose:** Retrieves CSRF token required for API authentication

**What it does:**
- Makes a GET request to **/dataservice/client/token** endpoint
- Uses session cookies from the login step
- Retrieves CSRF token for secure API operations
- Handles token service unavailability gracefully
- Stores token for use in subsequent API calls

#### Task 6: Check Authentication Status

**Purpose:** Displays current authentication status for troubleshooting

**What it does:**
- Shows login and token retrieval status codes
- Provides informative messages about authentication state
- Indicates when proceeding with session-only authentication
- Helps users understand the authentication flow

#### Task 7: Validate Authentication - Fail Only on Login Failure

**Purpose:** Ensures successful login before proceeding with API calls

**What it does:**
- Checks if login returned **HTTP 200** or **302** status
- Allows continuation even if CSRF token service is unavailable
- Fails the playbook only if login authentication fails
- Provides clear failure messaging for troubleshooting

#### Task 8: Get All Configuration Groups

**Purpose:** Retrieves configuration groups from the primary endpoint

**API Endpoint:** `/dataservice/template/config-group`

**What it does:**
- Attempts to retrieve all configuration groups from vManage
- Uses session cookies and CSRF token (if available) for authentication
- Handles both successful responses and permission errors
- Sets ignore_errors to allow fallback strategies
- Stores response for processing and fallback decisions

#### Task 9: Check if Configuration Groups Access is Denied

**Purpose:** Provides user feedback when primary endpoint access is denied

**What it does:**
- Detects **HTTP 403 Forbidden** responses
- Displays informative message about permission issues
- Explains potential causes and next steps
- Prepares user for fallback data retrieval

#### Task 10: Try Alternative Endpoint - Device Templates

**Purpose:** Retrieves device templates as fallback when config groups are inaccessible

**API Endpoint:** `/dataservice/template/device`

**What it does:**
- Executes only when configuration groups return 403 error
- Uses same authentication method as primary endpoint
- Retrieves device template information as alternative data
- Provides useful SD-WAN configuration information when available

#### Task 11: Try Another Alternative - Feature Templates

**Purpose:** Retrieves feature templates as second fallback option

**API Endpoint:** `/dataservice/template/feature`

**What it does:**
- Executes only when both config groups and device templates fail
- Provides third-tier fallback for data retrieval
- Ensures users get some configuration data when possible
- Uses consistent authentication across all attempts

#### Task 12: Determine Which Data to Use

**Purpose:** Selects the best available data source for report generation

**What it does:**
- Evaluates success status of all API attempts
- Prioritizes configuration groups over alternatives
- Sets appropriate data type for report formatting
- Prepares variables for consistent report generation

#### Task 13: Save Configuration Data to JSON File

**Purpose:** Creates machine-readable JSON output for programmatic use

**Generated file:** `{data_type}_data.json`

**What it does:**
- Converts API response to formatted JSON
- Saves to organized subdirectory structure
- Preserves all API response details for analysis
- Enables integration with other automation tools

#### Task 14: Save Configuration Data to Text File

**Purpose:** Creates human-readable report for documentation and review

**Generated file:** `{data_type}_data.txt`

**What it does:**
- Formats API data into structured text report
- Includes comprehensive configuration details
- Shows authentication method used
- Provides different formats based on data type retrieved
- Creates detailed listings with all available attributes

#### Task 15: Handle API Access Errors

**Purpose:** Provides comprehensive error reporting when all endpoints fail

**What it does:**
- Displays detailed status information for all attempted endpoints
- Shows authentication method and status codes
- Provides troubleshooting guidance for common issues
- Suggests next steps for resolving access problems

#### Task 16: Display Completion Message

**Purpose:** Provides execution status and file location information

**What it displays:**
- Success confirmation with authentication method used
- Full paths to generated report files
- Data type retrieved (config groups, device templates, or feature templates)
- Notes about fallback data when applicable

## Report Contents

The generated report includes different content based on data availability:

### Configuration Groups (Primary Data)
- **Group Details:** Name, description, device type, solution
- **Timestamps:** Creation and last update dates
- **User Information:** Created by and last updated by users
- **Template Associations:** Linked templates and their types
- **System Information:** Group ID, factory default status, profile type

### Device Templates (Fallback Data)
- **Template Details:** Name, description, device type
- **Identification:** Template ID and type information
- **Timestamps:** Creation and modification dates
- **User Tracking:** Creator and modifier information
- **System Attributes:** Factory default status and template type

### Feature Templates (Secondary Fallback)
- **Template Information:** Name, description, template type
- **Device Compatibility:** Supported device types
- **Management Data:** Creation and update tracking
- **System Properties:** Template ID and factory default status