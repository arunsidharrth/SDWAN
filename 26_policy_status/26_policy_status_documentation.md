# SD-WAN Get Policy Status Playbook Documentation

## Overview

The **get_policy_status.yml** playbook is an Ansible automation script designed to retrieve comprehensive policy status and deployment information from Cisco SD-WAN environments. This playbook uses session-based authentication to connect to the vManage controller and extracts detailed policy status data, activation history, deployment information, and error reports for analysis, monitoring, and troubleshooting purposes.

## Use Case

**Use Case 26: Get policy status - Get policy status**

This playbook addresses the need to:

- Retrieve comprehensive policy status information from the SD-WAN environment
- Monitor policy activation and deployment status across devices
- Extract policy deployment history and activation records
- Identify policy errors, warnings, and deployment issues
- Create organized status reports for policy compliance monitoring
- Provide automated policy status documentation for operational oversight

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage.sdwan.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | admin |
| **VMANAGE_PASSWORD** | Password for vManage authentication | (required) |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('admin') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  policy_output_dir: "{{ generated_dir }}/policy_status"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_policy_status.yml
└── generated/
    └── policy_status/
        ├── policy_status.json
        ├── policy_status_summary.json
        ├── device_policy_status.json
        ├── policy_activation_history.json
        ├── policy_deployment_status.json
        ├── policy_errors_warnings.json
        └── execution_summary.txt
```

## Task Analysis

#### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, and **VMANAGE_PASSWORD** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

#### Task 2: Directory Structure Creation

**Purpose:** Creates organized output directories for policy status data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **policy_status** subdirectory for organized output
- Sets appropriate permissions (755) for file access
- Ensures output locations exist before data collection

#### Task 3: vManage Authentication

**Purpose:** Establishes authenticated session with vManage controller

**Authentication method:** `/j_security_check` endpoint

**What it does:**
- Sends POST request with username/password credentials
- Uses form-encoded authentication data
- Disables SSL certificate validation for development environments
- Captures session cookie for subsequent API calls

#### Task 4: Session Cookie Extraction

**Purpose:** Extracts session information for API authentication

**What it does:**
- Retrieves session cookie from authentication response
- Stores cookie data for use in subsequent API requests
- Enables session-based authentication for all API calls

#### Task 5: CSRF Token Retrieval

**Purpose:** Obtains CSRF token for API security requirements

**Endpoint:** `/dataservice/client/token`

**What it does:**
- Makes authenticated request to retrieve CSRF token
- Implements retry logic (3 attempts with 5-second delays)
- Handles cases where CSRF tokens are not required
- Stores token for inclusion in API headers

#### Task 6: CSRF Token Configuration

**Purpose:** Configures CSRF token handling based on availability

**What it does:**
- Sets CSRF token variable from API response
- Provides fallback to empty string if token unavailable
- Prepares authentication headers for API calls

#### Task 7: CSRF Requirement Testing

**Purpose:** Determines if CSRF tokens are required for policy status API access

**Test endpoint:** `/dataservice/template/policy/status`

**What it does:**
- Tests API access with CSRF token included
- Determines authentication requirements for policy status endpoints
- Stores result for conditional API call handling
- May encounter permission restrictions (403 Forbidden)

#### Task 8: Primary Policy Status Retrieval (with CSRF)

**Purpose:** Retrieves main policy status information using CSRF authentication

**Endpoint:** `/dataservice/template/policy/status`

**What it does:**
- Makes authenticated GET request for overall policy status
- Includes session cookie and CSRF token in headers
- Sets 60-second timeout for API response
- Executed when CSRF token test succeeds
- May encounter permission restrictions in sandbox environments

#### Task 9: Primary Policy Status Retrieval (without CSRF)

**Purpose:** Retrieves policy status information without CSRF token

**Endpoint:** `/dataservice/template/policy/status`

**What it does:**
- Makes authenticated GET request using only session cookie
- Fallback method when CSRF tokens are not required
- Executed when CSRF token test fails
- Handles permission-restricted environments gracefully

#### Task 10: Alternative Policy Summary Endpoint (with CSRF)

**Purpose:** Attempts alternative endpoint for policy status summary

**Endpoint:** `/dataservice/template/policy/status/summary`

**What it does:**
- Tries policy status summary endpoint when main endpoint fails
- Uses CSRF token authentication
- Provides alternative source for policy status information
- May encounter service availability issues (503 errors)

#### Task 11: Alternative Policy Summary Endpoint (without CSRF)

**Purpose:** Attempts summary endpoint without CSRF token

**Endpoint:** `/dataservice/template/policy/status/summary`

**What it does:**
- Fallback to policy summary endpoint without CSRF authentication
- Executed when main endpoints fail
- Ensures maximum compatibility across environments
- Alternative approach for policy status data

#### Task 12: Device Policy Status Retrieval (with CSRF)

**Purpose:** Retrieves per-device policy status information

**Endpoint:** `/dataservice/device/policy/status`

**What it does:**
- Gets device-specific policy deployment status
- Shows policy status on individual network devices
- Uses CSRF authentication when required
- May encounter service availability limitations

#### Task 13: Device Policy Status Retrieval (without CSRF)

**Purpose:** Retrieves device policy status without CSRF token

**Endpoint:** `/dataservice/device/policy/status`

**What it does:**
- Alternative method for device policy status data
- Maintains functionality without CSRF requirements
- Ensures comprehensive device status collection

#### Task 14: Policy Status Processing

**Purpose:** Consolidates successful API responses for data processing

**What it does:**
- Evaluates all policy status API endpoint responses
- Selects successful responses (HTTP 200) from available sources
- Determines which authentication method worked
- Sets working datasets for file storage operations
- Handles scenarios where all endpoints fail

#### Task 15: API Status Display

**Purpose:** Provides detailed status information for troubleshooting

**What it displays:**
- Status codes for all attempted policy status API endpoints
- Authentication method used (with/without CSRF)
- Success/failure details for each endpoint
- Record counts for retrieved policy status data
- Comprehensive troubleshooting information

#### Task 16: Main Policy Status File Storage

**Purpose:** Saves primary policy status information

**Generated file:** `policy_status.json`

**What it does:**
- Stores overall policy status and activation information
- Converts policy status data to formatted JSON
- Only creates file when successful API response received
- Provides baseline policy status inventory

#### Task 17: Policy Summary File Storage

**Purpose:** Saves policy status summary information

**Generated file:** `policy_status_summary.json`

**What it does:**
- Stores condensed policy status summary data
- Provides high-level policy status overview
- Creates summary view of policy deployment status

#### Task 18: Device Policy Status File Storage

**Purpose:** Saves per-device policy status information

**Generated file:** `device_policy_status.json`

**What it does:**
- Stores device-specific policy deployment status
- Shows policy status on individual network devices
- Provides device-level policy compliance information

#### Task 19: Policy Activation History Retrieval (with CSRF)

**Purpose:** Retrieves historical policy activation information

**Endpoint:** `/dataservice/template/policy/history`

**What it does:**
- Gets chronological record of policy activations and changes
- Shows policy deployment timeline and modifications
- Uses CSRF authentication when required
- Provides audit trail for policy management activities

#### Task 20: Policy Activation History Retrieval (without CSRF)

**Purpose:** Retrieves policy history without CSRF token

**Endpoint:** `/dataservice/template/policy/history`

**What it does:**
- Alternative method for policy activation history
- Maintains audit trail functionality without CSRF requirements
- Ensures comprehensive historical data collection

#### Task 21: Policy History File Storage

**Purpose:** Saves policy activation history information

**Generated file:** `policy_activation_history.json`

**What it does:**
- Stores chronological policy activation and modification records
- Provides audit trail for compliance and troubleshooting
- Documents policy change management activities

#### Task 22: Policy Deployment Status Retrieval (with CSRF)

**Purpose:** Retrieves detailed deployment status per device

**Endpoint:** `/dataservice/device/policy/deployment`

**What it does:**
- Gets device-specific policy deployment details
- Shows deployment success/failure status per device
- Uses CSRF authentication when required
- Provides granular deployment monitoring information

#### Task 23: Policy Deployment Status Retrieval (without CSRF)

**Purpose:** Retrieves deployment status without CSRF token

**Endpoint:** `/dataservice/device/policy/deployment`

**What it does:**
- Alternative method for deployment status data
- Maintains deployment monitoring without CSRF requirements
- Ensures comprehensive deployment status collection

#### Task 24: Policy Deployment File Storage

**Purpose:** Saves detailed deployment status information

**Generated file:** `policy_deployment_status.json`

**What it does:**
- Stores per-device policy deployment status and results
- Provides deployment success/failure tracking
- Documents deployment issues and resolution status

#### Task 25: Policy Errors and Warnings Retrieval (with CSRF)

**Purpose:** Retrieves policy error and warning information

**Endpoint:** `/dataservice/template/policy/errors`

**What it does:**
- Gets policy validation errors and configuration warnings
- Shows policy syntax issues and deployment problems
- Uses CSRF authentication when required
- Provides troubleshooting information for policy issues

#### Task 26: Policy Errors and Warnings Retrieval (without CSRF)

**Purpose:** Retrieves policy errors without CSRF token

**Endpoint:** `/dataservice/template/policy/errors`

**What it does:**
- Alternative method for policy error and warning data
- Maintains error reporting without CSRF requirements
- Ensures comprehensive issue identification

#### Task 27: Policy Errors File Storage

**Purpose:** Saves policy error and warning information

**Generated file:** `policy_errors_warnings.json`

**What it does:**
- Stores policy validation errors and configuration warnings
- Provides troubleshooting data for policy deployment issues
- Documents policy syntax and configuration problems

#### Task 28: Execution Summary Creation

**Purpose:** Creates comprehensive execution report

**Generated file:** `execution_summary.txt`

**What it does:**
- Documents complete execution results with detailed status information
- Lists all policy status API endpoint status codes with error analysis
- Shows authentication method used and success/failure details
- Counts retrieved policy records, summaries, and deployment data
- Provides troubleshooting information for permission failures (403 errors)
- Documents service availability issues (503 errors) with resolution guidance
- Lists all created output files or explains why no data was retrieved
- Includes specific guidance for sandbox limitations and production requirements

## Report Contents

The generated reports include the following policy status information:

### Policy Status (`policy_status.json`)
- Overall policy activation status and deployment state
- Global policy configuration status across the SD-WAN environment
- Policy synchronization status between controllers and devices
- System-wide policy health and operational status

### Policy Status Summary (`policy_status_summary.json`)
- Condensed policy status overview with key metrics
- High-level policy deployment statistics
- Summary of active, inactive, and pending policies
- Policy compliance summary across the network

### Device Policy Status (`device_policy_status.json`)
- Per-device policy deployment status and compliance
- Individual device policy synchronization state
- Device-specific policy errors and warnings
- Policy version information deployed on each device

### Policy Activation History (`policy_activation_history.json`)
- Chronological record of policy activations and deactivations
- Policy change management audit trail
- Historical policy deployment timeline
- Policy modification and rollback history

### Policy Deployment Status (`policy_deployment_status.json`)
- Detailed deployment status for each policy on each device
- Deployment success/failure tracking with timestamps
- Policy push status and synchronization results
- Device-specific deployment error details

### Policy Errors and Warnings (`policy_errors_warnings.json`)
- Policy validation errors and configuration issues
- Syntax errors and policy rule conflicts
- Deployment warnings and recommendation alerts
- Troubleshooting information for policy problems

### Execution Summary (`execution_summary.txt`)
- Complete execution log with timestamps and detailed status analysis
- Policy status API endpoint results with comprehensive error documentation
- Authentication method documentation and troubleshooting guidance
- File creation summary with detailed explanation of failures
- Performance metrics and execution details with error resolution strategies
- Specific documentation of 403 Forbidden and 503 Service Unavailable errors
- Sandbox environment limitations and production deployment requirements
- Comprehensive troubleshooting guide for policy status access issues