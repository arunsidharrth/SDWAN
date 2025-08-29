# SD-WAN Get vSmart Policy Playbook Documentation

## Overview

The **get_vsmart_policy.yml** playbook is an Ansible automation script designed to retrieve comprehensive vSmart centralized policy information from Cisco SD-WAN environments. This playbook uses session-based authentication to connect to the vManage controller and extracts detailed centralized policy configurations, device assignments, and activation status for analysis, documentation, and auditing purposes.

## Use Case

**Use Case 25: Get vSmart policy - Get vSmart policy**

This playbook addresses the need to:

- Retrieve all centralized vSmart policies configured in the SD-WAN environment
- Extract detailed centralized policy definitions and configurations
- Document policy device assignments and deployment status
- Gather policy activation and status information
- Create organized output for centralized policy analysis and compliance reporting
- Provide automated centralized policy documentation for regular audits

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
  policy_output_dir: "{{ generated_dir }}/vsmart_policies"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_vsmart_policy.yml
└── generated/
    └── vsmart_policies/
        ├── vsmart_policies_list.json
        ├── vsmart_policy_<id>_<n>.json
        ├── vsmart_policy_preview_<id>_<n>.json
        ├── vsmart_policy_devices_<id>_<n>.json
        ├── vsmart_policy_activation_status.json
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

**Purpose:** Creates organized output directories for vSmart policy data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **vsmart_policies** subdirectory for organized output
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

**Purpose:** Determines if CSRF tokens are required for vSmart policy API access

**Test endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Tests API access with CSRF token included
- Determines authentication requirements for centralized policies
- Stores result for conditional API call handling
- May receive 403 Forbidden in restricted environments

#### Task 8: Primary vSmart Policy List Retrieval (with CSRF)

**Purpose:** Retrieves centralized vSmart policies using CSRF authentication

**Endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Makes authenticated GET request for vSmart centralized policies
- Includes session cookie and CSRF token in headers
- Sets 60-second timeout for API response
- Executed when CSRF token test succeeds
- May encounter permission restrictions (403 errors)

#### Task 9: Primary vSmart Policy List Retrieval (without CSRF)

**Purpose:** Retrieves centralized vSmart policies without CSRF token

**Endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Makes authenticated GET request using only session cookie
- Fallback method when CSRF tokens are not required
- Executed when CSRF token test fails
- Handles permission-restricted environments

#### Task 10: Alternative Central Policy Endpoint (with CSRF)

**Purpose:** Attempts alternative API endpoint for centralized policy data

**Endpoint:** `/dataservice/template/policy/central`

**What it does:**
- Tries centralized policy endpoint when vSmart endpoint fails
- Uses CSRF token authentication
- Provides fallback for different API configurations
- Alternative approach for centralized policy access

#### Task 11: Alternative Central Policy Endpoint (without CSRF)

**Purpose:** Attempts alternative endpoint without CSRF token

**Endpoint:** `/dataservice/template/policy/central`

**What it does:**
- Fallback to centralized policy endpoint without CSRF authentication
- Executed when primary endpoints fail
- Ensures maximum compatibility across environments
- Last attempt for centralized policy data

#### Task 12: Policy List Processing

**Purpose:** Selects successful API response for further processing

**What it does:**
- Evaluates all centralized policy API endpoint responses
- Selects the first successful response (HTTP 200)
- Determines which authentication method worked
- Sets working dataset for subsequent operations
- Identifies successful API endpoint for documentation
- Handles scenarios where all endpoints fail

#### Task 13: API Status Display

**Purpose:** Provides detailed status information for troubleshooting

**What it displays:**
- Status codes for all attempted vSmart policy API endpoints
- Authentication method used (with/without CSRF)
- Successful endpoint identification
- Number of centralized policies discovered
- Troubleshooting information for permission failures

#### Task 14: vSmart Policy List Storage

**Purpose:** Saves retrieved centralized policy list to file system

**Generated file:** `vsmart_policies_list.json`

**What it does:**
- Converts centralized policy list to formatted JSON
- Saves data to organized output directory
- Only executes when successful API response received
- Creates baseline centralized policy inventory

#### Task 15: Individual vSmart Policy Details Retrieval (with CSRF)

**Purpose:** Retrieves detailed configuration for each centralized policy

**Endpoint pattern:** `/dataservice/template/policy/{endpoint}/definition/{policyId}`

**What it does:**
- Iterates through each discovered centralized policy
- Retrieves complete policy definition and configuration
- Uses CSRF authentication when required
- Handles API timeouts and permission errors gracefully

#### Task 16: Individual vSmart Policy Details Retrieval (without CSRF)

**Purpose:** Retrieves centralized policy details without CSRF authentication

**What it does:**
- Fallback method for environments not requiring CSRF tokens
- Same functionality as CSRF version but simplified headers
- Ensures compatibility across different vManage configurations
- Handles permission restrictions appropriately

#### Task 17: Policy Details Processing

**Purpose:** Selects appropriate centralized policy details response

**What it does:**
- Chooses response based on authentication method used
- Prepares detailed centralized policy data for file storage
- Maintains consistency with authentication approach

#### Task 18: Individual vSmart Policy File Creation

**Purpose:** Saves detailed centralized policy information to separate files

**File pattern:** `vsmart_policy_{policyId}_{policyName}.json`

**What it does:**
- Creates individual JSON file for each centralized policy
- Sanitizes policy names for filesystem compatibility
- Includes complete centralized policy definition and metadata
- Skips failed API calls to prevent empty files

#### Task 19: vSmart Policy Preview Retrieval (with CSRF)

**Purpose:** Retrieves configuration preview for each centralized policy

**Endpoint pattern:** `/dataservice/template/policy/{endpoint}/preview/{policyId}`

**What it does:**
- Gets configuration preview for each centralized policy
- Shows generated policy configuration
- Uses CSRF authentication when required
- Provides policy validation and preview information

#### Task 20: vSmart Policy Preview Retrieval (without CSRF)

**Purpose:** Retrieves policy previews without CSRF token

**What it does:**
- Alternative method for policy preview data
- Maintains functionality without CSRF requirements
- Ensures comprehensive policy documentation

#### Task 21: vSmart Policy Preview File Storage

**Purpose:** Saves policy configuration previews

**File pattern:** `vsmart_policy_preview_{policyId}_{policyName}.json`

**What it does:**
- Stores policy configuration preview data
- Shows generated configuration for each centralized policy
- Provides policy validation information

#### Task 22: vSmart Policy Device Assignment Retrieval (with CSRF)

**Purpose:** Retrieves device assignment information for centralized policies

**Endpoint pattern:** `/dataservice/template/policy/{endpoint}/devices/{policyId}`

**What it does:**
- Gets list of devices assigned to each centralized policy
- Shows policy deployment status and scope
- Uses CSRF authentication when required
- Provides centralized policy utilization information

#### Task 23: vSmart Policy Device Assignment Retrieval (without CSRF)

**Purpose:** Retrieves device assignments without CSRF token

**What it does:**
- Alternative method for device assignment data
- Maintains functionality without CSRF requirements
- Ensures comprehensive deployment information

#### Task 24: vSmart Policy Device Assignment File Storage

**Purpose:** Saves device assignment information

**File pattern:** `vsmart_policy_devices_{policyId}_{policyName}.json`

**What it does:**
- Stores policy-to-device assignment information
- Shows which devices use each centralized policy
- Provides deployment scope documentation

#### Task 25: Overall Policy Activation Status Retrieval (with CSRF)

**Purpose:** Retrieves global centralized policy activation status

**Endpoint:** `/dataservice/template/policy/status`

**What it does:**
- Gets system-wide policy activation information
- Shows overall deployment and activation status
- May encounter service availability issues (503 errors)
- Uses CSRF authentication when required

#### Task 26: Overall Policy Activation Status Retrieval (without CSRF)

**Purpose:** Alternative method for activation status retrieval

**What it does:**
- Attempts status retrieval without CSRF authentication
- Provides fallback for different authentication requirements
- Handles service availability limitations

#### Task 27: Policy Activation Status File Storage

**Purpose:** Saves overall policy activation status

**Generated file:** `vsmart_policy_activation_status.json`

**What it does:**
- Stores system-wide centralized policy activation status
- Only creates file when API call succeeds
- Provides global policy deployment overview

#### Task 28: Execution Summary Creation

**Purpose:** Creates comprehensive execution report

**Generated file:** `execution_summary.txt`

**What it does:**
- Documents complete execution results with detailed status information
- Lists all centralized policy API endpoint status codes
- Shows authentication method used and success/failure details
- Counts retrieved policies, previews, and device assignments
- Provides troubleshooting information for permission failures (403 errors)
- Documents service availability issues (503 errors)
- Lists all created output files or explains why no files were created

## Report Contents

The generated reports include the following centralized policy information:

### vSmart Policies List (`vsmart_policies_list.json`)
- Complete inventory of all centralized vSmart policies
- Centralized policy metadata including names, IDs, and types
- Creation and modification timestamps for centralized policies
- Policy descriptions and centralized policy categories

### Individual vSmart Policy Files (`vsmart_policy_<id>_<n>.json`)
- Detailed centralized policy definitions and configurations
- Policy assembly and centralized rule structures
- Centralized policy settings and parameters
- Policy type classifications for centralized policies

### vSmart Policy Previews (`vsmart_policy_preview_<id>_<n>.json`)
- Generated configuration preview for centralized policies
- Policy validation and configuration verification
- Preview of deployed centralized policy configurations
- Configuration syntax and structure validation

### vSmart Policy Device Assignments (`vsmart_policy_devices_<id>_<n>.json`)
- Device-to-centralized-policy mapping information
- Deployment status for each centralized policy
- Device assignment counts for centralized policies
- Centralized policy utilization and scope metrics

### Policy Activation Status (`vsmart_policy_activation_status.json`)
- Global centralized policy activation status
- System-wide deployment state information
- Overall centralized policy activation overview
- Administrative status details for centralized policies

### Execution Summary (`execution_summary.txt`)
- Complete execution log with timestamps and detailed status information
- Centralized policy API endpoint status and results with error analysis
- Authentication method documentation and troubleshooting guidance
- File creation summary or detailed explanation of permission/access failures
- Performance metrics and execution details with error resolution guidance
- Specific documentation of 403 Forbidden errors indicating insufficient permissions for centralized policy access
- Guidance on sandbox limitations and production environment requirements