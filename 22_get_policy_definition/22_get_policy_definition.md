# SD-WAN Get Policy Definition Playbook Documentation

## Overview

The **get_policy_definition.yml** playbook is an Ansible automation script designed to retrieve detailed policy definition configurations from Cisco SD-WAN environments. This playbook leverages the vManage REST API to extract comprehensive policy definition information across multiple categories and produces organized documentation for analysis, configuration management, and compliance purposes.

## Use Case

**Use Case 22: Get policy definition - Retrieve policy definition details**

This playbook addresses the need to:

- Retrieve detailed policy definition configurations from the SD-WAN environment
- Document all policy definition types including QoS, data, control, and security definitions
- Create comprehensive policy definition inventories for change management and compliance
- Export policy definition data for offline analysis and configuration review
- Provide automated policy definition discovery for regular audits and documentation updates
- Support policy template analysis and configuration standardization

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | `vmanage-amfament-prod.sdwan.cisco.com` |
| **VMANAGE_USERNAME** | Username for vManage authentication | `automation` |
| **VMANAGE_PASSWORD** | Password for vManage authentication | `''` |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  policy_definitions_dir: "{{ generated_dir }}/policy_definitions"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_policy_definition.yml
└── generated/
    ├── policy_definitions_summary.txt
    └── policy_definitions/
        ├── policy_definitions_overview.json
        ├── qos_policy_definitions.json
        ├── data_policy_definitions.json
        ├── control_policy_definitions.json
        ├── approute_policy_definitions.json
        ├── acl_policy_definitions.json
        └── vpn_membership_definitions.json
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

**Purpose:** Creates organized output directories for policy definition data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **policy_definitions** subdirectory to organize multiple definition files
- Sets appropriate permissions (755) for file access
- Ensures output locations exist before API calls
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting policy definition retrieval

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

#### Task 5: Get All Policy Definitions Overview

**Purpose:** Retrieves general policy definitions summary

**API Endpoint:** `/dataservice/template/policy/definition`

**What it does:**
- Queries vManage for all policy definition objects overview
- Uses GET method with basic authentication
- Handles 403 Forbidden responses (common in sandbox environments)
- Stores policy definition overview data for file output
- Includes error handling to continue execution if access is restricted

#### Task 6: Get QoS Policy Definitions

**Purpose:** Retrieves Quality of Service policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/qosmap`

**What it does:**
- Queries vManage for all QoS mapping policy definitions
- Retrieves traffic classification and marking configurations
- Uses GET method with basic authentication
- Stores QoS policy definition data for file output
- Continues execution even if QoS definitions are inaccessible

#### Task 7: Get Data Policy Definitions

**Purpose:** Retrieves data plane policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/data`

**What it does:**
- Queries vManage for all data policy definition objects
- Retrieves traffic filtering and forwarding rule definitions
- Includes firewall and access control policy definitions
- Handles authentication and timeout settings
- Stores comprehensive data policy definition data

#### Task 8: Get Control Policy Definitions

**Purpose:** Retrieves control plane policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/control`

**What it does:**
- Queries vManage for all control policy definition objects
- Retrieves routing and control plane policy configurations
- Includes route redistribution and policy definitions
- Uses consistent authentication and error handling
- Stores control policy definition data separately for organized output

#### Task 9: Get Application-Aware Routing Policy Definitions

**Purpose:** Retrieves application-aware routing policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/approute`

**What it does:**
- Queries vManage for application-aware routing policy definitions
- Retrieves application-based path selection configurations
- Includes SLA and performance-based routing policies
- Handles authentication and error responses
- Stores application routing policy definition data

#### Task 10: Get Access Control List Definitions

**Purpose:** Retrieves ACL policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/acl`

**What it does:**
- Queries vManage for all access control list definitions
- Retrieves network access control and filtering rules
- Includes permit/deny rules and traffic matching criteria
- Uses consistent error handling for restricted access
- Stores ACL definition data for comprehensive documentation

#### Task 11: Get VPN Membership Policy Definitions

**Purpose:** Retrieves VPN membership policy definitions

**API Endpoint:** `/dataservice/template/policy/definition/vpnmembershipgroup`

**What it does:**
- Queries vManage for VPN membership group definitions
- Retrieves VPN segmentation and grouping configurations
- Includes site-to-VPN mapping and membership rules
- Handles authentication and timeout settings
- Stores VPN membership definition data

#### Task 12: Save Policy Definitions Overview to File

**Purpose:** Writes policy definitions overview data to JSON file

**Generated file:** **policy_definitions_overview.json**

**What it does:**
- Converts API response to formatted JSON
- Saves data to organized policy_definitions subdirectory
- Uses conditional logic to only save when data exists
- Formats JSON with proper indentation for readability
- Skips file creation if API call failed or returned no data

#### Task 13: Save QoS Policy Definitions to File

**Purpose:** Writes QoS policy definition data to JSON file

**Generated file:** **qos_policy_definitions.json**

**What it does:**
- Converts QoS policy definition data to formatted JSON
- Saves to the policy_definitions subdirectory for organization
- Includes proper JSON formatting with 2-space indentation
- Only creates file when valid data exists
- Preserves complete QoS policy configuration details

#### Task 14: Save Data Policy Definitions to File

**Purpose:** Writes data policy definition data to JSON file

**Generated file:** **data_policy_definitions.json**

**What it does:**
- Converts data policy definition API response to JSON format
- Saves detailed traffic filtering and forwarding rule definitions
- Includes firewall and access control policy configurations
- Uses consistent formatting and error handling
- Creates comprehensive data policy definition reference

#### Task 15: Save Control Policy Definitions to File

**Purpose:** Writes control policy definition data to JSON file

**Generated file:** **control_policy_definitions.json**

**What it does:**
- Converts control policy definition data to formatted JSON
- Saves routing and control plane policy configurations
- Maintains proper JSON structure and indentation
- Only creates file when API call succeeded
- Provides separate control policy definition documentation

#### Task 16: Save Application-Aware Routing Policy Definitions to File

**Purpose:** Writes application routing policy definition data to JSON file

**Generated file:** **approute_policy_definitions.json**

**What it does:**
- Converts application-aware routing policy data to formatted JSON
- Saves application-based path selection configurations
- Includes SLA and performance-based routing policy definitions
- Uses consistent formatting and conditional file creation
- Documents application routing policy templates

#### Task 17: Save ACL Policy Definitions to File

**Purpose:** Writes ACL policy definition data to JSON file

**Generated file:** **acl_policy_definitions.json**

**What it does:**
- Converts access control list definition data to formatted JSON
- Saves network access control and filtering rule definitions
- Maintains proper JSON structure with detailed rule information
- Only creates file when valid ACL data exists
- Provides comprehensive ACL definition documentation

#### Task 18: Save VPN Membership Policy Definitions to File

**Purpose:** Writes VPN membership policy definition data to JSON file

**Generated file:** **vpn_membership_definitions.json**

**What it does:**
- Converts VPN membership definition data to formatted JSON
- Saves VPN segmentation and grouping configurations
- Includes site-to-VPN mapping and membership rule details
- Uses consistent formatting and error handling
- Documents VPN membership policy templates

#### Task 19: Create Consolidated Policy Definitions Summary

**Purpose:** Generates comprehensive policy definitions inventory report

**Generated file:** **policy_definitions_summary.txt**

**What it does:**
- Creates human-readable summary of policy definition retrieval results
- Documents connection details and API call outcomes
- Reports count of policy definitions retrieved for each category
- Lists all generated files with full paths
- Provides success/failure status for each policy definition type
- Describes each policy definition category and its purpose
- Creates centralized report for quick policy definition inventory overview

## Report Contents

The generated policy definitions inventory typically includes:

- **Policy Definition Counts:** Number of definitions retrieved for each category
- **API Status:** Success/failure status for each policy definition type
- **File Locations:** Complete paths to all generated JSON files
- **Connection Details:** vManage host and authentication information
- **Category Descriptions:** Explanation of each policy definition type retrieved
- **Execution Summary:** Overall success status and any access limitations encountered