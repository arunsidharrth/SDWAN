# SD-WAN List Policy Lists Playbook Documentation

## Overview

The **list_policy_list.yml** playbook is an Ansible automation script designed to retrieve and catalog all policy list configurations from Cisco SD-WAN environments. This playbook leverages the vManage REST API to extract comprehensive policy list information across multiple categories and produces organized inventories for analysis, configuration management, and policy development purposes.

## Use Case

**Use Case 23: List policy lists - Get all policy lists**

This playbook addresses the need to:

- Retrieve complete policy list inventories from the SD-WAN environment
- Document all policy list types including site, VPN, prefix, and application lists
- Create baseline policy list reports for configuration management and compliance
- Export policy list data for offline analysis and policy development
- Provide automated policy list discovery for regular audits and documentation updates
- Support policy creation and template development with existing list references

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
  policy_lists_dir: "{{ generated_dir }}/policy_lists"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── list_policy_list.yml
└── generated/
    ├── policy_lists_summary.txt
    └── policy_lists/
        ├── policy_lists_overview.json
        ├── site_lists.json
        ├── vpn_lists.json
        ├── prefix_lists.json
        ├── application_lists.json
        ├── data_prefix_lists.json
        ├── color_lists.json
        ├── sla_class_lists.json
        ├── policer_lists.json
        └── community_lists.json
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

**Purpose:** Creates organized output directories for policy list data

**What it does:**
- Creates the **generated** directory relative to the playbook location
- Creates the **policy_lists** subdirectory to organize multiple list files
- Sets appropriate permissions (755) for file access
- Ensures output locations exist before API calls
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting policy list retrieval

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

#### Task 5: Get All Policy Lists Overview

**Purpose:** Retrieves general policy lists summary

**API Endpoint:** `/dataservice/template/policy/list`

**What it does:**
- Queries vManage for all policy list objects overview
- Uses GET method with basic authentication
- Retrieves comprehensive summary of all policy list types
- Stores policy list overview data for file output
- Includes error handling to continue execution if access issues occur

#### Task 6: Get Site Lists

**Purpose:** Retrieves site grouping and location definitions

**API Endpoint:** `/dataservice/template/policy/list/site`

**What it does:**
- Queries vManage for all site list configurations
- Retrieves site groupings and geographical location definitions
- Used for location-based policy application and routing decisions
- Stores site list data for detailed analysis
- Continues execution regardless of individual API call results

#### Task 7: Get VPN Lists

**Purpose:** Retrieves VPN segment and service groupings

**API Endpoint:** `/dataservice/template/policy/list/vpn`

**What it does:**
- Queries vManage for all VPN list configurations
- Retrieves VPN segment definitions and service groupings
- Used for network segmentation and service chaining policies
- Handles authentication and timeout settings consistently
- Stores VPN list data for policy development reference

#### Task 8: Get Prefix Lists

**Purpose:** Retrieves IP address and subnet groupings

**API Endpoint:** `/dataservice/template/policy/list/prefix`

**What it does:**
- Queries vManage for all prefix list configurations
- Retrieves IP address ranges and subnet groupings
- Used for routing policies and traffic classification
- Includes error handling for API access restrictions
- Stores prefix list data for network topology analysis

#### Task 9: Get Application Lists

**Purpose:** Retrieves application and service groupings

**API Endpoint:** `/dataservice/template/policy/list/app`

**What it does:**
- Queries vManage for all application list configurations
- Retrieves application definitions and service groupings
- Used for application-aware routing and QoS policies
- Handles consistent authentication and error processing
- Stores application list data for traffic management analysis

#### Task 10: Get Data Prefix Lists

**Purpose:** Retrieves data plane IP prefix groupings

**API Endpoint:** `/dataservice/template/policy/list/dataprefix`

**What it does:**
- Queries vManage for data plane prefix list configurations
- Retrieves IP prefix definitions specific to data plane operations
- Used for data policy and traffic forwarding decisions
- Uses consistent error handling approach
- Stores data prefix list information separately for organized output

#### Task 11: Get Color Lists

**Purpose:** Retrieves WAN transport color definitions

**API Endpoint:** `/dataservice/template/policy/list/color`

**What it does:**
- Queries vManage for color list configurations
- Retrieves WAN transport color definitions and groupings
- Used for transport selection and path preference policies
- Handles authentication and timeout configurations
- Stores color list data for transport policy analysis

#### Task 12: Get SLA Class Lists

**Purpose:** Retrieves service level agreement classifications

**API Endpoint:** `/dataservice/template/policy/list/slaClass`

**What it does:**
- Queries vManage for SLA class list configurations
- Retrieves service level agreement classification definitions
- Used for application-aware routing and performance policies
- Handles 404 Not Found responses for version compatibility
- May not be available in all vManage software versions

#### Task 13: Get Policer Lists

**Purpose:** Retrieves traffic policing and rate limiting definitions

**API Endpoint:** `/dataservice/template/policy/list/policer`

**What it does:**
- Queries vManage for policer list configurations
- Retrieves traffic policing and rate limiting definitions
- Used for QoS policies and bandwidth management
- Stores policer list data for traffic control analysis
- Continues execution regardless of API call results

#### Task 14: Get Community Lists

**Purpose:** Retrieves BGP community value groupings

**API Endpoint:** `/dataservice/template/policy/list/community`

**What it does:**
- Queries vManage for BGP community list configurations
- Retrieves community value groupings for routing policies
- Used for advanced routing control and path manipulation
- Handles authentication and error responses consistently
- Stores community list data for routing policy development

#### Task 15: Save Policy Lists Overview to File

**Purpose:** Writes policy lists overview data to JSON file

**Generated file:** **policy_lists_overview.json**

**What it does:**
- Converts API response to formatted JSON
- Saves data to organized policy_lists subdirectory
- Uses conditional logic to only save when data exists
- Formats JSON with proper indentation for readability
- Skips file creation if API call failed or returned no data

#### Task 16: Save Site Lists to File

**Purpose:** Writes site list data to JSON file

**Generated file:** **site_lists.json**

**What it does:**
- Converts site list data to formatted JSON
- Saves to the policy_lists subdirectory for organization
- Includes proper JSON formatting with 2-space indentation
- Only creates file when valid data exists
- Preserves complete site grouping and location definitions

#### Task 17: Save VPN Lists to File

**Purpose:** Writes VPN list data to JSON file

**Generated file:** **vpn_lists.json**

**What it does:**
- Converts VPN list API response to JSON format
- Saves detailed VPN segment and service grouping definitions
- Includes network segmentation and service chaining configurations
- Uses consistent formatting and error handling
- Creates comprehensive VPN list reference documentation

#### Task 18: Save Prefix Lists to File

**Purpose:** Writes prefix list data to JSON file

**Generated file:** **prefix_lists.json**

**What it does:**
- Converts prefix list data to formatted JSON
- Saves IP address ranges and subnet grouping configurations
- Maintains proper JSON structure and indentation
- Only creates file when API call succeeded
- Provides detailed prefix list documentation for routing policies

#### Task 19: Save Application Lists to File

**Purpose:** Writes application list data to JSON file

**Generated file:** **application_lists.json**

**What it does:**
- Converts application list data to formatted JSON
- Saves application definitions and service grouping configurations
- Includes application-aware routing and QoS policy references
- Uses consistent formatting and conditional file creation
- Documents application classification and traffic management lists

#### Task 20: Save Data Prefix Lists to File

**Purpose:** Writes data prefix list data to JSON file

**Generated file:** **data_prefix_lists.json**

**What it does:**
- Converts data prefix list data to formatted JSON
- Saves data plane IP prefix grouping configurations
- Maintains proper JSON structure with detailed prefix information
- Only creates file when valid data exists
- Provides data plane prefix documentation for policy development

#### Task 21: Save Color Lists to File

**Purpose:** Writes color list data to JSON file

**Generated file:** **color_lists.json**

**What it does:**
- Converts color list data to formatted JSON
- Saves WAN transport color definitions and groupings
- Includes transport selection and path preference configurations
- Uses consistent formatting and error handling
- Documents transport policy color classifications

#### Task 22: Save SLA Class Lists to File

**Purpose:** Writes SLA class list data to JSON file

**Generated file:** **sla_class_lists.json**

**What it does:**
- Converts SLA class list data to formatted JSON
- Saves service level agreement classification definitions
- Only creates file when API endpoint exists and returns data
- Handles version compatibility issues gracefully
- May be skipped if endpoint is not available in vManage version

#### Task 23: Save Policer Lists to File

**Purpose:** Writes policer list data to JSON file

**Generated file:** **policer_lists.json**

**What it does:**
- Converts policer list data to formatted JSON
- Saves traffic policing and rate limiting definitions
- Includes QoS policy and bandwidth management configurations
- Uses consistent formatting and conditional processing
- Documents traffic control and policing policy references

#### Task 24: Save Community Lists to File

**Purpose:** Writes community list data to JSON file

**Generated file:** **community_lists.json**

**What it does:**
- Converts community list data to formatted JSON
- Saves BGP community value groupings for routing policies
- Maintains proper JSON structure with community value details
- Only creates file when valid community data exists
- Provides BGP routing policy community reference documentation

#### Task 25: Create Consolidated Policy Lists Summary

**Purpose:** Generates comprehensive policy lists inventory report

**Generated file:** **policy_lists_summary.txt**

**What it does:**
- Creates human-readable summary of policy list retrieval results
- Documents connection details and API call outcomes
- Reports count of policy lists retrieved for each category
- Lists all generated files with full paths
- Provides success/failure status for each policy list type
- Describes each policy list category and its purpose in SD-WAN operations
- Creates centralized report for quick policy list inventory overview
- Handles version compatibility issues and missing endpoints gracefully

## Report Contents

The generated policy lists inventory typically includes:

- **Policy List Counts:** Number of lists retrieved for each category
- **API Status:** Success/failure status for each policy list type
- **File Locations:** Complete paths to all generated JSON files
- **Connection Details:** vManage host and authentication information
- **Category Descriptions:** Explanation of each policy list type and its SD-WAN usage
- **Execution Summary:** Overall success status and any version compatibility limitations