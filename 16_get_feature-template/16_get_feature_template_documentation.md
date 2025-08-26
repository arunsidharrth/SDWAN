# SD-WAN Get Feature Template Playbook Documentation

## Overview

The **get_feature_template.yml** playbook is an Ansible automation script designed to retrieve specific feature template configurations from Cisco SD-WAN environments. This playbook uses REST API calls to extract detailed feature template information from the vManage controller and produces organized output files for analysis, documentation, and configuration management purposes.

## Use Case

**Use Case 16: Get feature template - Retrieve specific feature template**

This playbook addresses the need to:

- Retrieve detailed configuration of a specific feature template from the SD-WAN environment
- Extract complete template definitions including all configuration parameters
- Document individual feature template settings for analysis and review
- Export template data for backup, migration, or configuration comparison
- Provide automated template retrieval for configuration management workflows

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage-amfament-prod.sdwan.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | automation |
| **VMANAGE_PASSWORD** | Password for vManage authentication | |
| **TEMPLATE_ID** | Feature template ID to retrieve (optional) | |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  template_id: "{{ lookup('env', 'TEMPLATE_ID') | default('') }}"
  use_first_template: "{{ lookup('env', 'USE_FIRST_TEMPLATE') | default('true') }}"
  generated_dir: "{{ playbook_dir }}/../generated"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_feature_template.yml
└── generated/
    ├── feature_template_{template_id}.json
    ├── feature_template_definition_{template_id}.json
    └── feature_template_summary_{template_id}.txt
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

#### Task 5: Debug Template Variables

**Purpose:** Displays template ID and configuration values for troubleshooting

**What it displays:**

- Current value of **template_id** variable
- Current value of **use_first_template** variable
- Boolean evaluation of empty template_id condition
- Boolean evaluation of use_first_template condition

#### Task 6: Get Feature Templates List (Auto-selection)

**Purpose:** Retrieves all available feature templates when no specific template ID is provided

**API endpoint called:**
```
GET /dataservice/template/feature
```

**What it does:**

- Makes REST API call to retrieve complete feature templates list
- Uses basic authentication with provided credentials
- Sets 60-second timeout for API response
- Only executes when template_id is empty (length = 0)
- Stores results in **feature_templates_list** variable

#### Task 7: Set Template ID to First Available Template

**Purpose:** Automatically selects the first available template when no ID is specified

**What it does:**

- Extracts the **templateId** from the first template in the list
- Sets the **template_id** variable to this value
- Only executes when original template_id was empty
- Ensures a valid template ID is available for subsequent operations
- Handles cases where template list is empty or undefined

#### Task 8: Display Selected Template Information

**Purpose:** Shows which template was automatically selected

**What it displays:**

- Selected template ID
- Template name from the templates list
- Template type from the templates list
- Only executes when auto-selection was performed

#### Task 9: Template ID Validation

**Purpose:** Ensures a valid template ID is available before proceeding

**What it does:**

- Checks if template_id has been set (length > 0)
- Fails execution with helpful error message if no template ID available
- Provides guidance for manual template ID specification
- Prevents API calls with empty template IDs

#### Task 10: Get Specific Feature Template

**Purpose:** Retrieves detailed configuration of the specified feature template

**API endpoint called:**
```
GET /dataservice/template/feature/object/{templateId}
```

**What it does:**

- Makes REST API call to retrieve complete template configuration
- Uses the determined template_id in the URL path
- Uses basic authentication with provided credentials
- Sets 60-second timeout for API response
- Stores complete template data in **feature_template_response** variable

#### Task 11: Save Complete Feature Template to JSON

**Purpose:** Creates comprehensive JSON file with all template data

**Generated file:** **feature_template_{template_id}.json**

**What it does:**

- Converts complete API response to formatted JSON
- Includes all template metadata and configuration
- Creates file with template ID in filename for easy identification
- Preserves all original data structure and formatting

#### Task 12: Extract Template Definition

**Purpose:** Creates separate file containing only the template configuration

**Generated file:** **feature_template_definition_{template_id}.json**

**What it does:**

- Extracts only the **templateDefinition** section from the response
- Creates separate JSON file for the configuration portion
- Only executes if templateDefinition exists in the response
- Provides clean configuration data without metadata

#### Task 13: Create Template Summary Report

**Purpose:** Generates human-readable summary of template information

**Generated file:** **feature_template_summary_{template_id}.txt**

**What it includes:**

- Template Name and Type
- Supported Device Types
- Factory Default status
- Template Description
- Creation and modification timestamps
- Creator and modifier information
- Configuration availability status
- File references for detailed data

#### Task 14: Display Template Information

**Purpose:** Provides execution status and template details

**What it displays:**

- Success confirmation message
- Retrieved template ID
- Template name from API response
- Template type from API response
- Supported device types list

## Generated Files

The playbook produces three output files:

- **feature_template_{template_id}.json:** Complete template object with all metadata and configuration
- **feature_template_definition_{template_id}.json:** Template configuration only (conditional - created only if templateDefinition exists)
- **feature_template_summary_{template_id}.txt:** Human-readable summary with key template information

## Template Information Captured

The retrieved template data typically includes:

- **Template Metadata:** Name, type, description, and identification
- **Device Compatibility:** Supported device types and platform information
- **Template Configuration:** Complete feature configuration parameters
- **Audit Information:** Creation/modification timestamps and user details
- **Factory Default Status:** Whether template is a factory-provided template
- **Template Definition:** Detailed configuration parameters and values