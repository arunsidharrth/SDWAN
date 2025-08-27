# Get Template Input Playbook Documentation

## Overview

The **get_template_input.yml** playbook is an Ansible automation script designed to retrieve template input parameters from Cisco SD-WAN environments. This playbook uses REST API calls to the vManage controller to extract template configuration requirements for both device templates and feature templates, producing organized reports for template analysis, configuration planning, and deployment preparation.

## Use Case

**Use Case 19: Get template input - Get template input parameters**

This playbook addresses the need to:

- Retrieve input parameters required for device and feature templates
- Understand template configuration requirements before deployment
- Generate reports showing template parameter specifications
- Export template input data for offline analysis and configuration planning
- Provide automated documentation for template parameter requirements

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
  template_type: "device"  # device or feature
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_template_input.yml
└── generated/
    ├── device_templates.json
    ├── feature_templates.json
    ├── device_template_input_{template_id}.json
    ├── feature_template_details_{template_id}.json
    ├── feature_types.json
    ├── device_template_input_{template_id}.csv
    └── feature_template_details_{template_id}.csv
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
- Executes only when template_id, template_name are empty and template_type is "device"
- Stores template data including template IDs, names, device types, and descriptions
- Provides device template inventory for selection and analysis

#### Task 6: Get All Feature Templates

**Purpose:** Retrieves complete list of feature templates when template_type is set to "feature"

**API Endpoint:** `/dataservice/template/feature`

**What it does:**
- Connects to vManage using provided credentials
- Retrieves all available feature templates
- Executes only when template_id, template_name are empty and template_type is "feature"
- Stores feature template data including template IDs, names, and configurations
- Provides feature template inventory for selection and analysis

#### Task 7: Find Device Template by Name

**Purpose:** Locates specific device template ID when template name is provided

**What it does:**
- Searches through retrieved device templates
- Matches provided template_name with templateName field
- Sets template_id variable with corresponding templateId
- Executes only when template_name is provided and template_type is "device"
- Enables template-specific queries using human-readable names

#### Task 8: Find Feature Template by Name

**Purpose:** Locates specific feature template ID when template name is provided

**What it does:**
- Searches through retrieved feature templates
- Matches provided template_name with templateName field
- Sets template_id variable with corresponding templateId
- Executes only when template_name is provided and template_type is "feature"
- Enables feature template queries using human-readable names

#### Task 9: Get Device Template Input

**Purpose:** Retrieves input parameters required for a specific device template

**API Endpoint:** `/dataservice/template/device/config/input/{template_id}`

**What it does:**
- Queries vManage for input parameters of specified device template
- Executes only when template_id is provided and template_type is "device"
- Returns detailed parameter specifications including data types, requirements, and defaults
- Includes column definitions, property names, and validation rules
- Provides essential information for template attachment and configuration

#### Task 10: Get Feature Template Input Types

**Purpose:** Retrieves available feature template types and their specifications

**API Endpoint:** `/dataservice/template/feature/types`

**What it does:**
- Queries vManage for available feature template types
- Executes only when template_id is provided and template_type is "feature"
- Returns feature template type definitions and supported parameters
- Provides reference data for feature template analysis
- Supports understanding of feature template categories

#### Task 11: Get Specific Feature Template Details

**Purpose:** Retrieves detailed configuration for a specific feature template

**API Endpoint:** `/dataservice/template/feature/object/{template_id}`

**What it does:**
- Queries vManage for specific feature template configuration
- Executes only when template_id is provided and template_type is "feature"
- Returns complete template definition including configuration objects
- Includes template structure, parameters, and default values
- Provides detailed template specification for analysis and deployment

#### Task 12: Save Device Templates List

**Purpose:** Creates JSON file containing all device templates

**Generated file:** **device_templates.json**

**What it does:**
- Exports complete device template inventory in JSON format
- Includes template IDs, names, device types, and configuration details
- Executes only when device templates were successfully retrieved
- Provides reference data for template selection and analysis
- Enables offline review of available device templates

#### Task 13: Save Feature Templates List

**Purpose:** Creates JSON file containing all feature templates

**Generated file:** **feature_templates.json**

**What it does:**
- Exports complete feature template inventory in JSON format
- Includes template IDs, names, types, and configuration details
- Executes only when feature templates were successfully retrieved
- Provides reference data for feature template selection
- Enables offline review of available feature templates

#### Task 14: Save Device Template Input

**Purpose:** Creates JSON file for device template input parameters

**Generated file:** **device_template_input_{template_id}.json**

**What it does:**
- Exports device template input parameters in structured JSON format
- Includes parameter specifications, data types, and requirements
- Executes only when device template input was successfully retrieved
- Maintains complete parameter definition for configuration planning
- Enables programmatic processing of template requirements

#### Task 15: Save Feature Template Details

**Purpose:** Creates JSON file for feature template configuration details

**Generated file:** **feature_template_details_{template_id}.json**

**What it does:**
- Exports feature template configuration in structured JSON format
- Includes complete template definition and parameter specifications
- Executes only when feature template details were successfully retrieved
- Provides detailed template structure for analysis
- Supports template configuration and deployment planning

#### Task 16: Save Feature Types

**Purpose:** Creates JSON file containing feature template types

**Generated file:** **feature_types.json**

**What it does:**
- Exports feature template type definitions in JSON format
- Includes available template types and their specifications
- Executes only when feature types were successfully retrieved
- Provides reference data for feature template categories
- Supports understanding of template type capabilities

#### Task 17: Create CSV Report for Device Template Input

**Purpose:** Generates CSV report for device template input parameters

**Generated file:** **device_template_input_{template_id}.csv**

**What it does:**
- Creates human-readable CSV format report of template parameters
- Includes columns: Template ID, Name, Parameter Name, Data Type, Requirements, Defaults
- Extracts parameter details from template input data structure
- Executes only when device template input data is available
- Enables spreadsheet analysis of template requirements

#### Task 18: Create CSV Report for Feature Template Details

**Purpose:** Generates CSV report for feature template configuration

**Generated file:** **feature_template_details_{template_id}.csv**

**What it does:**
- Creates summary CSV report of feature template information
- Includes template ID, name, type, device type, and configuration details
- Provides high-level template overview in tabular format
- Executes only when feature template details are available
- Enables quick review of template specifications

## Usage Examples

### Get All Device Template Parameters (Default)
```bash
ansible-playbook get_template_input.yml
```

### Get All Feature Template Parameters
```bash
ansible-playbook get_template_input.yml -e "template_type=feature"
```

### Get Input for Specific Device Template by ID
```bash
ansible-playbook get_template_input.yml -e "template_id=12345678-1234-1234-1234-123456789012 template_type=device"
```

### Get Input for Specific Template by Name
```bash
ansible-playbook get_template_input.yml -e "template_name=DC_cEdge_Template template_type=device"
```

### Get Feature Template Details by Name
```bash
ansible-playbook get_template_input.yml -e "template_name=VPN-Interface template_type=feature"
```

## Report Contents

The generated reports include:

- **Template Inventories:** Complete lists of available device and feature templates
- **Input Parameters:** Required and optional parameters for template configuration
- **Data Type Specifications:** Parameter data types, validation rules, and constraints
- **Default Values:** Pre-configured default values for template parameters
- **Template Metadata:** Template names, descriptions, device types, and update information
- **Configuration Requirements:** Essential parameters needed for successful template deployment

## Output Files

### JSON Files
- **device_templates.json:** Complete device template inventory with metadata
- **feature_templates.json:** Complete feature template inventory with specifications  
- **device_template_input_{template_id}.json:** Detailed input parameters for specific device template
- **feature_template_details_{template_id}.json:** Complete configuration details for specific feature template
- **feature_types.json:** Available feature template types and their definitions

### CSV Files
- **device_template_input_{template_id}.csv:** Tabular report of device template input parameters
- **feature_template_details_{template_id}.csv:** Summary report of feature template configuration

All files are generated in the **generated** directory and provide comprehensive template input information essential for SD-WAN configuration planning and deployment preparation.