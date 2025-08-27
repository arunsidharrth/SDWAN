# SD-WAN Get Template State Playbook Documentation

## Overview

The **get_template_state.yml** playbook is an Ansible automation script designed to retrieve comprehensive template state information from Cisco SD-WAN environments. This playbook leverages multiple vManage REST API endpoints to extract detailed template configurations, metadata, input variables, and attachment status for analysis, monitoring, and documentation purposes.

## Use Case

**Use Case #20: Get template state - Retrieve comprehensive template state information**

This playbook addresses the need to:

- Retrieve current state and configuration details for device templates
- Extract template metadata including attachment status and last modification details
- Gather template input variables and requirements
- Document template objects and their associated feature templates
- Monitor template usage and device associations
- Generate comprehensive template state reports for auditing and compliance

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | sandbox-sdwan-2.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | devnetuser |
| **VMANAGE_PASSWORD** | Password for vManage authentication | |
| **TEMPLATE_ID** | (Optional) Specific template ID to query | |
| **TEMPLATE_NAME** | (Optional) Specific template name to query | |

### Optional Configuration

- If neither **TEMPLATE_ID** nor **TEMPLATE_NAME** is specified, the playbook processes all available templates
- If **TEMPLATE_NAME** is provided, the playbook will locate the corresponding template ID automatically

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated/templates"
  template_id: "{{ lookup('env', 'TEMPLATE_ID') | default('') }}"
  template_name: "{{ lookup('env', 'TEMPLATE_NAME') | default('') }}"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── get_template_state.yml
└── generated/
    └── templates/
        ├── template_state_[templateId].json (for each template)
        ├── all_template_states.json (consolidated file)
        └── template_state_summary.txt
```

## API Endpoints Used

The playbook utilizes the following vManage REST API endpoints:

- **GET** `/dataservice/template/device` - Retrieve all device templates
- **GET** `/dataservice/template/device/object/{templateId}` - Get detailed template object
- **POST** `/dataservice/template/device/config/input` - Get template input variables
- **GET** `/dataservice/template/device/config/attached/{templateId}` - Get attached devices

## Task Analysis

### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, **VMANAGE_PASSWORD**, and **VMANAGE_PORT** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

### Task 2: Connection Information Display

**Purpose:** Provides visibility into connection parameters while protecting sensitive data

**What it displays:**
- vManage host and connection details
- Username and port information
- Output directory location
- Masks password for security

### Task 3: Directory Creation

**Purpose:** Creates the output directory for generated template state files

**What it does:**
- Creates the **generated/templates** directory relative to the playbook location
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before data collection
- Uses organized subdirectory structure to separate template files from other use case outputs

### Task 4: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting template queries

**What it does:**
- Makes a REST API call to **/dataservice/system/device/controllers**
- Uses basic authentication with provided credentials
- Sets **60-second timeout** to handle slow connections
- Ignores SSL certificate validation for internal/self-signed certificates
- Stores connectivity results for validation

### Task 5: Connectivity Validation

**Purpose:** Stops execution if connectivity test fails

**What it does:**
- Checks if the connectivity test returned **HTTP 200** status
- Fails the playbook with descriptive error if vManage is unreachable
- Prevents unnecessary API calls when connectivity issues exist
- Provides clear failure messaging for troubleshooting

### Task 6: Retrieve All Device Templates

**Purpose:** Gets the complete list of device templates from vManage

**API Endpoint:** `GET /dataservice/template/device`

**What it does:**
- Queries vManage for all available device templates
- Retrieves template metadata including names, IDs, types, and basic status
- Stores template list for subsequent processing
- Handles authentication and SSL verification

### Task 7: Template Selection by Name (Optional)

**Purpose:** Locates a specific template when template name is provided

**What it does:**
- Searches the template list for templates matching the specified name
- Uses Ansible's `selectattr` filter to find exact name matches
- Sets the template ID for subsequent processing
- Ignores errors if template name is not found

### Task 8: Template ID Assignment (Optional)

**Purpose:** Sets the template ID from the found template when searching by name

**What it does:**
- Extracts the template ID from the template found by name
- Updates the template_id variable for consistent processing
- Only executes when a template was successfully found by name

### Task 9: Template Filtering

**Purpose:** Creates a filtered list of templates to process based on selection criteria

**What it does:**
- If a specific template ID is provided, filters to only that template
- If no specific template is specified, includes all available templates
- Uses Jinja2 templating to create the appropriate template list
- Ensures proper list formatting for subsequent loop operations

### Task 10: Retrieve Template Object Details

**Purpose:** Gets detailed configuration information for each target template

**API Endpoint:** `GET /dataservice/template/device/object/{templateId}`

**What it does:**
- Queries detailed template object information for each template
- Retrieves complete template configurations including feature templates
- Handles both feature-based and CLI-based template types
- Stores results with error handling for inaccessible templates
- Uses loop controls for clear progress indication

### Task 11: Retrieve Template Input Variables

**Purpose:** Gets required input variables and parameters for each template

**API Endpoint:** `POST /dataservice/template/device/config/input`

**What it does:**
- Sends POST request with template ID and empty device list
- Retrieves template variable definitions and requirements
- Identifies customizable parameters within templates
- Handles permission errors gracefully (403 Forbidden common in sandbox environments)
- Stores input variable schema for each template

### Task 12: Retrieve Attached Device Information

**Purpose:** Gets information about devices currently using each template

**API Endpoint:** `GET /dataservice/template/device/config/attached/{templateId}`

**What it does:**
- Queries for devices currently attached to each template
- Retrieves device-template association information
- Provides insight into template usage and deployment status
- Handles service availability issues (503 errors) gracefully
- Maps template deployment across the SD-WAN fabric

### Task 13: Initialize Template States List

**Purpose:** Prepares an empty list to collect comprehensive template state information

**What it does:**
- Creates an empty list variable to store processed template data
- Provides a clean starting point for data aggregation
- Ensures consistent data structure initialization

### Task 14: Build Comprehensive Template State Information

**Purpose:** Combines all collected data into structured template state objects

**What it does:**
- Iterates through each target template using loop controls
- Combines basic template metadata with detailed API responses
- Creates comprehensive template state objects including:
  - Basic template information (name, ID, description, type)
  - Configuration details (factory default, draft mode, attachment counts)
  - Template object details (complete configuration)
  - Input variables (required parameters)
  - Attached device information
- Uses `ansible_loop.index0` for proper data alignment
- Handles missing or failed API responses with default empty objects
- Builds cumulative list of complete template state information

### Task 15: Save Individual Template State Files

**Purpose:** Creates individual JSON files for each template's complete state information

**Generated files:** `template_state_[templateId].json`

**What it does:**
- Creates separate JSON file for each processed template
- Uses template ID in filename for unique identification
- Formats JSON with proper indentation for readability
- Stores complete template state including all collected information
- Provides per-template access to state data

### Task 16: Save Consolidated Template States File

**Purpose:** Creates a single file containing all template states for batch processing

**Generated file:** `all_template_states.json`

**What it does:**
- Combines all template states into a single JSON array
- Only creates file when processing multiple templates (no specific template ID)
- Enables bulk analysis and processing of all template data
- Provides consolidated view of entire template infrastructure

### Task 17: Create Comprehensive Template State Summary

**Purpose:** Generates human-readable summary report of template state analysis

**Generated file:** `template_state_summary.txt`

**What it does:**
- Creates detailed text summary of the template state retrieval operation
- Includes execution metadata (timestamp, vManage host, request details)
- Provides statistics on successful and failed API operations
- Lists all processed templates with key information:
  - Template names and IDs
  - Configuration types and device types  
  - Factory default status and attachment counts
  - Last modification details
  - Data availability status for each information type
- Shows required input variables for templates that have them
- Lists all generated output files for easy reference
- Formats information for easy reading and reporting

### Task 18: Display Completion Status

**Purpose:** Provides execution summary and file location information

**What it displays:**
- Success confirmation message
- Output directory location
- Summary of processing results:
  - For specific templates: template name and file location
  - For all templates: total count and file descriptions
- Description of included template state information
- File locations for easy access

## Generated Template State Information

Each template state object contains comprehensive information:

### Basic Template Metadata
- **templateName**: Human-readable template name
- **templateId**: Unique template identifier
- **templateDescription**: Template description
- **deviceType**: Target device type (vedge-C8000V, vsmart, etc.)
- **configType**: Configuration method (template or file)
- **factoryDefault**: Whether template is factory-provided
- **devicesAttached**: Number of devices currently using the template
- **templateAttached**: Total attachment count
- **lastUpdatedBy**: User who last modified the template
- **lastUpdatedOn**: Timestamp of last modification
- **draftMode**: Current draft status

### Template Object Details
- Complete template configuration
- Associated feature templates
- Template structure and hierarchy
- Configuration parameters and settings

### Input Variables (when available)
- Required template variables
- Variable definitions and constraints
- Default values and validation rules
- Customizable parameters for template deployment

### Attached Device Information (when available)
- List of devices using the template
- Device attachment status
- Deployment information

## Output Files

### Individual Template Files
**Format:** `template_state_[templateId].json`
- One file per processed template
- Complete template state information in JSON format
- Directly accessible by template ID

### Consolidated File
**Format:** `all_template_states.json`
- Single file containing all template states
- JSON array format for batch processing
- Created only when processing multiple templates

### Summary Report
**Format:** `template_state_summary.txt`
- Human-readable summary of the operation
- Execution statistics and results
- Template information overview
- File listing and descriptions

## Error Handling

The playbook includes comprehensive error handling:

- **Permission Errors (403)**: Common in sandbox environments, gracefully ignored
- **Service Unavailable (503)**: Handled when vManage is busy, operation continues
- **Connectivity Issues**: Fail-fast approach with clear error messages
- **Missing Templates**: Graceful handling when templates are not found
- **API Failures**: Individual API failures don't stop overall processing

## Usage Examples

### Process All Templates
```bash
export VMANAGE_HOST="sandbox-sdwan-2.cisco.com"
export VMANAGE_USERNAME="devnetuser" 
export VMANAGE_PASSWORD="your_password"
ansible-playbook get_template_state.yml
```

### Process Specific Template by ID
```bash
export VMANAGE_HOST="sandbox-sdwan-2.cisco.com"
export VMANAGE_USERNAME="devnetuser"
export VMANAGE_PASSWORD="your_password"
export TEMPLATE_ID="a5e2ba39-87a6-4d38-9053-7ca4c781857d"
ansible-playbook get_template_state.yml
```

### Process Specific Template by Name
```bash
export VMANAGE_HOST="sandbox-sdwan-2.cisco.com"
export VMANAGE_USERNAME="devnetuser"
export VMANAGE_PASSWORD="your_password"
export TEMPLATE_NAME="DC_cEdge_Template"
ansible-playbook get_template_state.yml
```

## Integration and Automation

This playbook can be integrated into:
- CI/CD pipelines for template monitoring
- Scheduled jobs for regular template auditing  
- Change management workflows
- Compliance reporting systems
- Template lifecycle management processes

The standardized output format enables easy integration with other automation tools and reporting systems.