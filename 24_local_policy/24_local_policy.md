# SD-WAN Get Localized Policy Playbook Documentation

## Overview

The **complete_localized_policy.yml** playbook is an Ansible automation script designed to retrieve comprehensive localized policy information from Cisco SD-WAN environments. This playbook uses session-based authentication to connect to the vManage controller and extracts detailed policy configurations, attachments, and status information for analysis, documentation, and auditing purposes.

## Use Case

**Use Case 24: Get localized policy - Retrieve localized policy**

This playbook addresses the need to:

- Retrieve all localized policies configured in the SD-WAN environment
- Extract detailed policy definitions and configurations
- Document policy device attachments and assignments
- Gather policy status and activation information
- Create organized output for offline analysis and compliance reporting
- Provide automated policy documentation for regular audits

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
  policy_output_dir: "{{ generated_dir }}/localized_policies"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── complete_localized_policy.yml
└── generated/
    └── localized_policies/
        ├── localized_policies_list.json
        ├── policy_<id>_<name>.json
        ├── policy_device_attachments.json
        ├── policy_status.json
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

**Purpose:** Creates organized output directories for policy data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **localized_policies** subdirectory for organized output
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

**Purpose:** Determines if CSRF tokens are required for API access

**Test endpoint:** `/dataservice/template/policy/vedge`

**What it does:**
- Tests API access with CSRF token included
- Determines authentication requirements for the environment
- Stores result for conditional API call handling

#### Task 8: Primary Policy List Retrieval (with CSRF)

**Purpose:** Retrieves localized policies using CSRF authentication

**Endpoint:** `/dataservice/template/policy/vedge`

**What it does:**
- Makes authenticated GET request for vEdge policies
- Includes session cookie and CSRF token in headers
- Sets 60-second timeout for API response
- Executed when CSRF token test succeeds

#### Task 9: Primary Policy List Retrieval (without CSRF)

**Purpose:** Retrieves localized policies without CSRF token

**Endpoint:** `/dataservice/template/policy/vedge`

**What it does:**
- Makes authenticated GET request using only session cookie
- Fallback method when CSRF tokens are not required
- Executed when CSRF token test fails

#### Task 10: Alternative vSmart Policy Endpoint (with CSRF)

**Purpose:** Attempts alternative API endpoint for policy data

**Endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Tries vSmart policy endpoint when vEdge endpoint fails
- Uses CSRF token authentication
- Provides fallback for different API configurations

#### Task 11: Alternative vSmart Policy Endpoint (without CSRF)

**Purpose:** Attempts alternative endpoint without CSRF token

**Endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Fallback to vSmart endpoint without CSRF authentication
- Executed when primary endpoints fail
- Ensures maximum compatibility across environments

#### Task 12: Policy List Processing

**Purpose:** Selects successful API response for further processing

**What it does:**
- Evaluates all API endpoint responses
- Selects the first successful response (HTTP 200)
- Determines which authentication method worked
- Sets working dataset for subsequent operations
- Identifies successful API endpoint for documentation

#### Task 13: API Status Display

**Purpose:** Provides detailed status information for troubleshooting

**What it displays:**
- Status codes for all attempted API endpoints
- Authentication method used (with/without CSRF)
- Successful endpoint identification
- Number of policies discovered
- Troubleshooting information for failed attempts

#### Task 14: Policy List Storage

**Purpose:** Saves retrieved policy list to file system

**Generated file:** `localized_policies_list.json`

**What it does:**
- Converts policy list to formatted JSON
- Saves data to organized output directory
- Only executes when successful API response received
- Creates baseline policy inventory

#### Task 15: Individual Policy Details Retrieval (with CSRF)

**Purpose:** Retrieves detailed configuration for each policy

**Endpoint pattern:** `/dataservice/template/policy/{endpoint}/definition/{policyId}`

**What it does:**
- Iterates through each discovered policy
- Retrieves complete policy definition and configuration
- Uses CSRF authentication when required
- Handles API timeouts and errors gracefully

#### Task 16: Individual Policy Details Retrieval (without CSRF)

**Purpose:** Retrieves policy details without CSRF authentication

**What it does:**
- Fallback method for environments not requiring CSRF tokens
- Same functionality as CSRF version but simplified headers
- Ensures compatibility across different vManage configurations

#### Task 17: Policy Details Processing

**Purpose:** Selects appropriate policy details response

**What it does:**
- Chooses response based on authentication method used
- Prepares detailed policy data for file storage
- Maintains consistency with authentication approach

#### Task 18: Individual Policy File Creation

**Purpose:** Saves detailed policy information to separate files

**File pattern:** `policy_{policyId}_{policyName}.json`

**What it does:**
- Creates individual JSON file for each policy
- Sanitizes policy names for filesystem compatibility
- Includes complete policy definition and metadata
- Skips failed API calls to prevent empty files

#### Task 19: Policy Attachment Information (with CSRF)

**Purpose:** Retrieves device attachment information for policies

**Endpoint:** `/dataservice/template/policy/{endpoint}/devices`

**What it does:**
- Gets list of devices using each policy
- Shows policy deployment status
- Uses CSRF authentication when required
- Provides policy utilization information

#### Task 20: Policy Attachment Information (without CSRF)

**Purpose:** Retrieves attachment info without CSRF token

**What it does:**
- Alternative method for device attachment data
- Maintains functionality without CSRF requirements
- Ensures comprehensive data collection

#### Task 21: Policy Attachment File Storage

**Purpose:** Saves device attachment information

**Generated file:** `policy_device_attachments.json`

**What it does:**
- Stores policy-to-device mapping information
- Shows which policies are actively deployed
- Provides deployment status overview

#### Task 22: Policy Status Information (with CSRF)

**Purpose:** Retrieves overall policy status from vManage

**Endpoint:** `/dataservice/template/policy/status`

**What it does:**
- Gets global policy status information
- Shows activation states and deployment status
- May fail with 403 in restricted environments (sandbox)

#### Task 23: Policy Status Information (without CSRF)

**Purpose:** Alternative method for policy status retrieval

**What it does:**
- Attempts status retrieval without CSRF authentication
- Provides fallback for different authentication requirements

#### Task 24: Policy Status File Storage

**Purpose:** Saves policy status information

**Generated file:** `policy_status.json`

**What it does:**
- Stores overall policy deployment status
- Only creates file when API call succeeds
- Provides system-wide policy overview

#### Task 25: Execution Summary Creation

**Purpose:** Creates comprehensive execution report

**Generated file:** `execution_summary.txt`

**What it does:**
- Documents complete execution results
- Lists all API endpoint status codes
- Shows authentication method used
- Counts retrieved policies and details
- Provides troubleshooting information for failures
- Lists all created output files

## Report Contents

The generated reports include the following information:

### Localized Policies List (`localized_policies_list.json`)
- Complete inventory of all localized policies
- Policy metadata including names, IDs, and types
- Creation and modification timestamps
- Policy descriptions and categories

### Individual Policy Files (`policy_<id>_<name>.json`)
- Detailed policy definitions and configurations
- Policy assembly and rule structures
- Feature settings and parameters
- Policy type classifications (feature, data, application firewall)

### Policy Device Attachments (`policy_device_attachments.json`)
- Device-to-policy mapping information
- Deployment status for each policy
- Device attachment counts
- Policy utilization metrics

### Policy Status Information (`policy_status.json`)
- Global policy activation status
- Deployment state information
- System-wide policy overview
- Administrative status details

### Execution Summary (`execution_summary.txt`)
- Complete execution log with timestamps
- API endpoint status and results
- Authentication method documentation
- File creation summary
- Troubleshooting information for any failures
- Performance metrics and execution details