# SD-WAN Get Configuration Group Status Playbook Documentation

## Overview

The SD-WAN Get Configuration Group Status playbook is an Ansible automation script designed to retrieve and monitor the status of configuration groups from Cisco SD-WAN vManage controllers. This playbook handles API errors gracefully and provides comprehensive status reporting for all configuration groups in the environment.

## Detailed Task Analysis

### Task 1: Environment Variable Validation
```yaml
- name: Validate environment variables are set
```

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Checks that vmanage_host, vmanage_username, and vmanage_password are set
- Fails the playbook immediately if any critical environment variables are missing
- Prevents failed API attempts due to missing credentials

### Task 2: Directory Structure Creation
```yaml
- name: Create generated directory structure
```

**Purpose:** Creates the complete directory hierarchy needed for organized output storage

**Generated folders:**
- `{{ generated_dir }}` - Main generated folder (../generated)
- `{{ config_group_dir }}` - Configuration groups subfolder (../generated/config_groups)

**Directory structure example:**
```
generated/
└── config_groups/
    ├── configuration_groups_list.txt
    ├── config_group_status_[name].txt
    ├── config_group_deploy_status_[name].txt
    └── execution_summary.txt
```

### Task 3: vManage Connectivity Testing
```yaml
- name: Test vManage connectivity
```

**Purpose:** Verifies the vManage controller is accessible before attempting API calls

**What it does:**
- Makes a REST API call to `/dataservice/system/device/controllers`
- Uses basic authentication with provided credentials
- Sets 60-second timeout
- Accepts multiple status codes (200, 403, 404, 500, 503)
- Uses `failed_when: false` to prevent red error messages
- Stores results in connectivity_test variable

### Task 4: Connectivity Failure Handling
```yaml
- name: Fail if connectivity test failed
```

**Purpose:** Stops execution if connectivity test fails with non-200 status

**What it does:** Prevents unnecessary API attempts when vManage is unreachable or authentication fails

### Task 5: Configuration Groups List Retrieval
```yaml
- name: Get list of all configuration groups
```

**Purpose:** Retrieves all configuration groups from vManage

**What it does:**
- Calls `/dataservice/template/config-group` endpoint
- Handles HTTP errors gracefully (403, 404, 500, 503)
- Uses `failed_when: false` to prevent fatal errors
- Stores complete list of configuration groups for further processing

### Task 6: API Error Handling
```yaml
- name: Handle configuration groups list API errors gracefully
```

**Purpose:** Processes API response and determines availability of configuration groups data

**What it does:**
- Sets `config_groups_available` boolean based on HTTP 200 response
- Extracts configuration groups data if available, otherwise sets empty array
- Enables conditional processing of subsequent tasks

### Task 7: Configuration Groups List File Creation
```yaml
- name: Save configuration groups list to file
```

**Purpose:** Creates comprehensive report of all configuration groups

**Generated file:** `configuration_groups_list.txt`

**Report contents:**
- Timestamp and vManage host information
- API availability status
- Total count of configuration groups
- Detailed information for each group:
  - Name, ID, Description
  - Solution and Profile Type
  - Creation and modification timestamps
  - Created By and Last Updated By information
- Error details if API is unavailable

### Task 8: Individual Configuration Group Status Retrieval
```yaml
- name: Get configuration group status for each group
```

**Purpose:** Retrieves detailed status information for each configuration group

**What it does:**
- Iterates through each configuration group found in Task 5
- Calls `/dataservice/template/config-group/{id}/status` for each group
- Handles API errors gracefully with multiple accepted status codes
- Only executes when configuration groups are available
- Uses `failed_when: false` to prevent execution failures

### Task 9: Status Results Processing
```yaml
- name: Process configuration group status results
```

**Purpose:** Processes and organizes individual status results for file creation

**What it does:**
- Builds array of status results from API calls
- Enables iteration over results in subsequent tasks
- Only processes when configuration groups are available

### Task 10: Individual Status File Creation
```yaml
- name: Save individual configuration group status to files
```

**Purpose:** Creates separate status file for each configuration group

**Generated files:** `config_group_status_[groupname].txt`

**Report contents for each group:**
- Timestamp and vManage host
- Group name and ID
- API availability status
- Detailed status information:
  - Device ID, IP, and Hostname
  - Status, Activity, and Action Status
  - Configuration Group Name and Template Type
  - Timing information (Start Time, End Time, Duration)
- Error details if API call failed

### Task 11: Configuration Group Deployment Status Retrieval
```yaml
- name: Get configuration group deployment status
```

**Purpose:** Retrieves deployment status information for each configuration group

**What it does:**
- Calls `/dataservice/template/config-group/{id}/deploy/status` for each group
- Provides additional deployment-specific status information
- Handles API errors gracefully
- Only executes when configuration groups are available

### Task 12: Deployment Status File Creation
```yaml
- name: Save configuration group deployment status
```

**Purpose:** Creates deployment status files for each configuration group

**Generated files:** `config_group_deploy_status_[groupname].txt`

**Report contents for each group:**
- Timestamp and connection details
- Group identification information
- Deployment status details:
  - Device identification (ID, IP, Hostname)
  - Status, Activity, and Config Group information
  - Status ID, Current Activity, and Validation status
- Error logging for failed API calls

### Task 13: Execution Summary Creation
```yaml
- name: Create execution summary
```

**Purpose:** Creates comprehensive summary of entire playbook execution

**Generated file:** `execution_summary.txt`

**Summary contents:**
- Execution timestamp and vManage host
- API endpoint results summary
- Count of total groups found and processed
- List of all created files
- Execution notes about error handling

## Generated Reports

The playbook creates comprehensive documentation in the `generated/config_groups/` directory:

### configuration_groups_list.txt
Complete inventory of all configuration groups with metadata including creation details, descriptions, and profile types.

### config_group_status_[name].txt (per group)
Individual status reports showing current operational state, device assignments, activities, and timing information for each configuration group.

### config_group_deploy_status_[name].txt (per group)  
Deployment-specific status information including validation status, current deployment activities, and device-level deployment states.

### execution_summary.txt
High-level summary of playbook execution including API availability, processed counts, created files list, and error handling notes.

## Error Handling Features

- **Graceful API Error Management**: Uses `failed_when: false` and multiple accepted status codes to prevent playbook failures
- **Comprehensive Error Logging**: Documents all API errors with status codes and error messages in output files
- **Conditional Processing**: Skips dependent tasks when prerequisite API calls fail
- **Clean Execution**: Eliminates red "fatal" error messages while maintaining full error visibility
- **Sandbox Environment Compatible**: Handles common sandbox limitations like HTTP 403/503 errors

## Pipeline Integration

**Manual Execution:** Navigate to GitLab project → Code → Pipelines → Run Pipeline → Select playbook

**Scheduled Execution:** Supports automated daily execution with artifact retention

**Variable Configuration:** Uses environment variables (VMANAGE_HOST, VMANAGE_USERNAME, VMANAGE_PASSWORD) for secure credential management