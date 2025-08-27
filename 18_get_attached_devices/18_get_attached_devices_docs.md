# Get Attached Devices Playbook Documentation

## Overview

The **get_attached_devices.yml** playbook is an Ansible automation script designed to retrieve information about devices attached to templates in Cisco SD-WAN environments. This playbook uses REST API calls to the vManage controller to extract device attachment information and produces organized reports for analysis, documentation, and operational visibility.

## Use Case

**Use Case 18: Get attached devices - List devices using template**

This playbook addresses the need to:

- Retrieve devices attached to specific device templates
- Get comprehensive inventory of all template-attached devices
- Generate reports showing template-to-device relationships
- Export device attachment data for offline analysis and review
- Provide automated reporting for template usage and device management

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage-amfament-prod.sdwan.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | automation |
| **VMANAGE_PASSWORD** | Password for vManage authentication | (required) |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  template_id: ""
  template_name: ""
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_attached_devices.yml
└── generated/
    ├── device_templates.json
    ├── attached_devices_{template_id}.json
    ├── attached_devices_{template_id}.csv
    ├── all_attached_devices.json
    └── all_attached_devices.csv
```

## Task Analysis

#### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, **VMANAGE_PASSWORD**, and **VMANAGE_PORT** are set
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

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting data retrieval

**What it does:**
- Makes a REST API call to **/dataservice/system/device/controllers**
- Uses basic authentication with provided credentials
- Sets **60-second timeout** to handle slow connections
- Ignores SSL certificate validation for internal/self-signed certificates
- Stores connectivity results for validation

#### Task 4: Connectivity Validation

**Purpose:** Stops execution if connectivity test fails

**What it does:**
- Checks if the connectivity test returned **HTTP 200** status
- Fails the playbook with descriptive error if vManage is unreachable
- Prevents unnecessary API operations when connectivity issues exist
- Provides clear failure messaging for troubleshooting

#### Task 5: Get All Device Templates

**Purpose:** Retrieves complete list of device templates when no specific template is provided

**API Endpoint:** `/dataservice/template/device`

**What it does:**
- Connects to vManage using provided credentials
- Retrieves all available device templates
- Executes only when both template_id and template_name are empty
- Stores template data for subsequent processing
- Provides template inventory for selection purposes

#### Task 6: Find Template by Name

**Purpose:** Locates specific template ID when template name is provided

**What it does:**
- Searches through retrieved device templates
- Matches provided template_name with templateName field
- Sets template_id variable with corresponding templateId
- Enables template-specific queries using human-readable names
- Handles template name to ID resolution

#### Task 7: Get Attached Devices for Specific Template

**Purpose:** Retrieves devices attached to a specific template

**API Endpoint:** `/dataservice/template/device/config/attached/{template_id}`

**What it does:**
- Queries vManage for devices attached to specified template
- Executes only when template_id is provided
- Returns detailed information about each attached device
- Includes device configuration status and template relationship
- Provides template-specific device inventory

#### Task 8: Get All Devices with Templates

**Purpose:** Retrieves all devices and filters for those with template attachments

**API Endpoint:** `/dataservice/device`

**What it does:**
- Queries all devices in the SD-WAN fabric
- Executes when no specific template is requested
- Provides comprehensive device inventory
- Returns device operational status and configuration details

#### Task 9: Filter Devices with Attached Templates

**Purpose:** Processes device data to identify template-attached devices

**What it does:**
- Filters device list to include only devices with templates
- Selects devices where 'template' field is defined and not empty
- Creates structured data matching expected format
- Ensures consistent data structure for reporting

#### Task 10: Save Device Templates List

**Purpose:** Creates JSON file containing all device templates

**Generated file:** **device_templates.json**

**What it does:**
- Exports complete template inventory in JSON format
- Includes template IDs, names, and configuration details
- Provides reference data for template selection
- Enables offline analysis of template structure

#### Task 11: Save Attached Devices (Specific Template)

**Purpose:** Creates JSON file for devices attached to specific template

**Generated file:** **attached_devices_{template_id}.json**

**What it does:**
- Exports device data in structured JSON format
- Includes device UUIDs, names, configuration status
- Maintains template relationship information
- Enables programmatic processing of attachment data

#### Task 12: Save All Attached Devices

**Purpose:** Creates JSON file containing all template-attached devices

**Generated file:** **all_attached_devices.json**

**What it does:**
- Exports comprehensive device attachment data
- Includes devices from all templates
- Provides complete inventory in JSON format
- Supports bulk analysis and reporting operations

#### Task 13: Create CSV Report (Specific Template)

**Purpose:** Generates CSV report for devices attached to specific template

**Generated file:** **attached_devices_{template_id}.csv**

**What it does:**
- Creates human-readable CSV format report
- Includes key device attributes in tabular format
- Contains columns: Device UUID, Name, Type, Template Name, Site ID, etc.
- Enables spreadsheet analysis and reporting
- Provides template-specific device summary

#### Task 14: Create CSV Report (All Devices)

**Purpose:** Generates comprehensive CSV report for all attached devices

**Generated file:** **all_attached_devices.csv**

**What it does:**
- Creates complete inventory in CSV format
- Includes all template-attached devices across the environment
- Provides standardized reporting format
- Enables comprehensive analysis and audit reporting

## Usage Examples

### Get All Attached Devices
```bash
ansible-playbook get_attached_devices.yml
```

### Get Devices for Specific Template ID
```bash
ansible-playbook get_attached_devices.yml -e "template_id=12345678-1234-1234-1234-123456789012"
```

### Get Devices for Specific Template Name
```bash
ansible-playbook get_attached_devices.yml -e "template_name=Branch-Router-Template"
```

## Report Contents

The generated reports include:

- **Device Templates:** Complete template inventory with IDs and names
- **Device Information:** UUID, hostname, device type, and model information
- **Template Relationships:** Which templates are attached to which devices
- **Configuration Status:** Current operational mode and configuration state
- **Network Details:** Site ID, system IP, and version information
- **Status Information:** Device operational status and connectivity state

## Output Files

### JSON Files
- **device_templates.json:** Complete template inventory
- **attached_devices_{template_id}.json:** Template-specific device data
- **all_attached_devices.json:** Comprehensive device attachment data

### CSV Files
- **attached_devices_{template_id}.csv:** Template-specific device report
- **all_attached_devices.csv:** Complete device attachment report

All files are generated in the **generated** directory for easy access and further processing.