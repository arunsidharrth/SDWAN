# SD-WAN List Device Templates Playbook Documentation

## Overview

The **list_device_templates.yml** playbook is an Ansible automation script designed to retrieve all device template configurations from Cisco SD-WAN environments. This playbook uses REST API calls to extract comprehensive device template information from the vManage controller and produces organized output files for analysis, documentation, and template management purposes.

## Use Case

**Use Case 17: List device templates - Get all device templates**

This playbook addresses the need to:

- Retrieve complete inventory of all device templates from the SD-WAN environment
- Document device template configurations for analysis and review
- Export template data for backup, migration, or configuration comparison
- Create baseline documentation for change management and compliance
- Provide automated template inventory for configuration management workflows

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage-amfament-prod.sdwan.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | automation |
| **VMANAGE_PASSWORD** | Password for vManage authentication | |
| **VMANAGE_PORT** | HTTPS port for vManage connection | 443 |

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
├── list_device_templates.yml
└── generated/
    ├── device_templates.json
    └── device_templates_summary.csv
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

**Purpose:** Creates the output directory for generated template files

**What it does:**

- Creates the **generated** directory relative to the playbook location
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before template retrieval
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting template retrieval

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

#### Task 5: Get Device Templates List

**Purpose:** Retrieves complete inventory of all device templates from vManage

**API endpoint called:**
```
GET /dataservice/template/device
```

**What it does:**

- Makes REST API call to retrieve all device templates
- Uses basic authentication with provided credentials
- Sets **60-second timeout** for API response
- Retrieves comprehensive template data including metadata and configuration details
- Stores complete response in **device_templates_response** variable

#### Task 6: Save Device Templates to JSON File

**Purpose:** Creates comprehensive JSON file with all device template data

**Generated file:** **device_templates.json**

**What it does:**

- Converts complete API response to formatted JSON
- Includes all template metadata, configurations, and relationships
- Creates structured data file for programmatic access
- Preserves all original data structure and formatting
- Enables detailed analysis and processing of template data

#### Task 7: Create Device Templates Summary CSV

**Purpose:** Generates human-readable summary of all device templates

**Generated file:** **device_templates_summary.csv**

**What it does:**

- Extracts key template information into CSV format
- Creates structured tabular data for spreadsheet analysis
- Includes essential template metadata and status information
- Handles missing fields with default values to prevent errors
- Joins multiple device types with semicolon separator for readability

**CSV columns created:**
- Template ID - Unique template identifier
- Template Name - Human-readable template name
- Device Type - Supported device types (semicolon-separated)
- Factory Default - Whether template is factory-provided
- Last Updated - Last modification timestamp
- Created By - User who created the template
- Attached Devices - Number of devices using this template
- Template Description - Template description text

#### Task 8: Display Device Templates Count

**Purpose:** Provides execution status and template inventory summary

**What it displays:**

- Success confirmation message
- Total count of device templates retrieved
- Confirms successful completion of template inventory process

## Generated Files

The playbook produces two output files:

- **device_templates.json:** Complete device template inventory with all metadata and configuration details
- **device_templates_summary.csv:** Human-readable summary with key template information in tabular format

## Report Contents

The generated files typically include:

### JSON File Contents:
- **Template Metadata:** Complete template identification and properties
- **Configuration Details:** Full device template configuration parameters
- **Device Compatibility:** Supported device types and platform information
- **Attachment Information:** Details of devices currently using each template
- **Audit Information:** Creation/modification timestamps and user details
- **Feature Template References:** Associated feature templates within device templates

### CSV File Contents:
- **Template Inventory:** Complete list of all device templates
- **Template Properties:** Key identifying information for each template
- **Usage Statistics:** Number of devices attached to each template
- **Audit Trail:** Creation and modification tracking information
- **Template Descriptions:** Human-readable descriptions of template purposes
- **Device Type Support:** Compatible device platforms for each template

## Template Information Captured

The retrieved device template data includes:

- **Template Identification:** Unique IDs, names, and descriptions
- **Device Compatibility:** Supported device types and model information
- **Template Configuration:** Complete device template definitions
- **Feature Template Relationships:** Associated feature templates and their configurations
- **Usage Analytics:** Current device attachments and deployment statistics
- **Factory vs Custom:** Distinction between factory-default and custom templates
- **Audit Information:** Complete creation and modification history
- **Template Status:** Current state and deployment readiness