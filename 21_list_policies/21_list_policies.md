# SD-WAN List Policies Playbook Documentation

## Overview

The **list_policies.yml** playbook is an Ansible automation script designed to retrieve and catalog all policy configurations from Cisco SD-WAN environments. This playbook leverages the vManage REST API to extract comprehensive policy information and produces organized policy inventories for analysis, documentation, and compliance purposes.

## Use Case

**Use Case 21: List policies - Get all policies**

This playbook addresses the need to:

- Retrieve complete policy inventories from the SD-WAN environment
- Document all policy types including centralized, localized, and security policies
- Create baseline policy reports for change management and compliance
- Export policy data for offline analysis and review
- Provide automated policy discovery for regular audits and documentation updates
- Support policy migration and backup operations

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | `sandbox-sdwan-2.cisco.com` |
| **VMANAGE_USERNAME** | Username for vManage authentication | `devnetuser` |
| **VMANAGE_PASSWORD** | Password for vManage authentication | `RG!_Yw919_83` |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  policies_dir: "{{ generated_dir }}/policies"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── list_policies.yml
└── generated/
    ├── policy_inventory_summary.txt
    └── policies/
        ├── centralized_policies.json
        ├── localized_policies.json
        ├── policy_definitions.json
        └── security_policies.json
```

## Task Analysis

#### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, **VMANAGE_PASSWORD**, and **VMANAGE_PORT** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

#### Task 2: Directory Structure Creation

**Purpose:** Creates organized output directories for policy data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **policies** subdirectory to organize multiple policy files
- Sets appropriate permissions (755) for file access
- Ensures output locations exist before API calls
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting policy retrieval

**What it does:**
- Makes a REST API call to **/dataservice/system/device/controllers**
- Uses basic authentication with provided credentials
- Sets **60-second timeout** to handle slow connections
- Ignores SSL certificate validation for sandbox/self-signed certificates
- Stores connectivity results for validation

#### Task 4: Connectivity Validation

**Purpose:** Stops execution if connectivity test fails

**What it does:**
- Checks if the connectivity test returned **HTTP 200** status
- Fails the playbook with descriptive error if vManage is unreachable
- Prevents unnecessary API calls when connectivity issues exist
- Provides clear failure messaging for troubleshooting

#### Task 5: Get All Centralized Policies

**Purpose:** Retrieves vSmart centralized policies

**API Endpoint:** `/dataservice/template/policy/vsmart`

**What it does:**
- Queries vManage for all centralized (vSmart) policy configurations
- Uses GET method with basic authentication
- Handles 403 Forbidden responses (common in sandbox environments)
- Stores policy data for file output
- Includes error handling to continue execution if access is restricted

#### Task 6: Get All Localized Policies

**Purpose:** Retrieves vEdge localized policies

**API Endpoint:** `/dataservice/template/policy/vedge`

**What it does:**
- Queries vManage for all localized (vEdge) policy configurations
- Retrieves site-specific and device-specific policies
- Uses GET method with basic authentication
- Stores policy data for file output
- Continues execution even if some policies are inaccessible

#### Task 7: Get All Policy Definitions

**Purpose:** Retrieves detailed policy definitions

**API Endpoint:** `/dataservice/template/policy/definition`

**What it does:**
- Queries vManage for all policy definition objects
- Retrieves detailed configuration parameters for each policy type
- Includes QoS, security, and routing policy definitions
- Handles authentication and timeout settings
- Stores comprehensive policy definition data

#### Task 8: Get All Security Policies

**Purpose:** Retrieves security-specific policies

**API Endpoint:** `/dataservice/template/policy/security`

**What it does:**
- Queries vManage for all security policy configurations
- Retrieves firewall, IPS, and security template policies
- Uses consistent authentication and error handling
- Stores security policy data separately for organized output
- Continues execution if some security policies are restricted

#### Task 9: Save Centralized Policies to File

**Purpose:** Writes centralized policy data to JSON file

**Generated file:** **centralized_policies.json**

**What it does:**
- Converts API response to formatted JSON
- Saves data to organized policies subdirectory
- Uses conditional logic to only save when data exists
- Formats JSON with proper indentation for readability
- Skips file creation if API call failed or returned no data

#### Task 10: Save Localized Policies to File

**Purpose:** Writes localized policy data to JSON file

**Generated file:** **localized_policies.json**

**What it does:**
- Converts vEdge policy data to formatted JSON
- Saves to the policies subdirectory for organization
- Includes proper JSON formatting with 2-space indentation
- Only creates file when valid data exists
- Preserves complete policy configuration details

#### Task 11: Save Policy Definitions to File

**Purpose:** Writes policy definition data to JSON file

**Generated file:** **policy_definitions.json**

**What it does:**
- Converts policy definition API response to JSON format
- Saves detailed policy configuration parameters
- Includes QoS, security, and routing policy definitions
- Uses consistent formatting and error handling
- Creates comprehensive policy definition reference

#### Task 12: Save Security Policies to File

**Purpose:** Writes security policy data to JSON file

**Generated file:** **security_policies.json**

**What it does:**
- Converts security policy data to formatted JSON
- Saves firewall and security template configurations
- Maintains proper JSON structure and indentation
- Only creates file when API call succeeded
- Provides separate security policy documentation

#### Task 13: Create Consolidated Policy Summary

**Purpose:** Generates comprehensive policy inventory report

**Generated file:** **policy_inventory_summary.txt**

**What it does:**
- Creates human-readable summary of policy retrieval results
- Documents connection details and API call outcomes
- Reports count of policies retrieved for each category
- Lists all generated files with full paths
- Provides success/failure status for each policy type
- Creates centralized report for quick policy inventory overview

## Report Contents

The generated policy inventory typically includes:

- **Policy Counts:** Number of policies retrieved for each category
- **API Status:** Success/failure status for each policy type
- **File Locations:** Complete paths to all generated JSON files
- **Connection Details:** vManage host and authentication information
- **Execution Summary:** Overall success status and any limitations encountered