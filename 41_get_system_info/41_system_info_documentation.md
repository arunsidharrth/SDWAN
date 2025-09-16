# Get System Info Playbook Documentation

## Overview

The Get System Info playbook is an Ansible automation script designed to retrieve comprehensive system information from Cisco SD-WAN vManage controllers. This playbook collects data from multiple API endpoints to provide a complete view of the SD-WAN infrastructure status and device inventory.

## Detailed Task Analysis

### Task 1: Environment Variable Validation

**- name: Validate environment variables are set**

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Checks that vmanage_host, vmanage_username, vmanage_password, and vmanage_port are set
- Fails the playbook immediately if any critical environment variables are missing
- Prevents failed execution attempts due to missing credentials

### Task 2: Directory Structure Creation

**- name: Create system info directory**

**Purpose:** Creates the organized directory hierarchy needed for system info storage

**Generated folder:**
- {{ system_info_dir }} - System information data storage in generated/system_info/

**Directory structure example:**
```
generated/
└── system_info/
```

### Task 3: vManage Connectivity Testing

**- name: Test vManage connectivity**

**Purpose:** Verifies the vManage controller is accessible before attempting data retrieval

**What it does:**
- Makes a REST API call to /dataservice/system/device/controllers
- Uses basic authentication with provided credentials
- Sets 60-second timeout
- Ignores SSL certificate validation for internal certificates
- Stores results in connectivity_test variable

### Task 4: Connectivity Failure Handling

**- name: Fail if connectivity test failed**

**Purpose:** Stops execution if connectivity test fails

**What it does:** Prevents unnecessary API calls when vManage is unreachable

### Task 5: Device System Information Retrieval

**- name: Get device system information**

**Purpose:** Retrieves comprehensive device system information

**API Endpoint:** `/dataservice/device/system/info`

**Generated content:** Complete system information including device details, status, and configuration data

### Task 6: System Counters Retrieval

**- name: Get system counters**

**Purpose:** Collects system performance counters and metrics

**API Endpoint:** `/dataservice/device/counters`

**Generated content:** Performance statistics, counters, and monitoring data for system analysis

### Task 7: Device Models Retrieval

**- name: Get device models**

**Purpose:** Gathers device inventory and model information

**API Endpoint:** `/dataservice/device/models`

**Generated content:** Complete device inventory including models, types, and hardware specifications

### Task 8: Device Controllers Retrieval

**- name: Get device controllers**

**Purpose:** Retrieves information about controller devices in the SD-WAN fabric

**API Endpoint:** `/dataservice/system/device/controllers`

**Generated content:** Controller device status, roles, and configuration details

### Task 9: Device vEdges Retrieval

**- name: Get device vedges**

**Purpose:** Collects information about vEdge devices in the network

**API Endpoint:** `/dataservice/system/device/vedges`

**Generated content:** vEdge device inventory, status, and operational data

### Task 10: Save Device System Information

**- name: Save device system information to file**

**Purpose:** Persists device system data to JSON file

**Generated file:** device_system_info.json in the system_info directory

### Task 11: Save System Counters

**- name: Save system counters to file**

**Purpose:** Stores system performance counters in JSON format

**Generated file:** system_counters.json in the system_info directory

### Task 12: Save Device Models

**- name: Save device models to file**

**Purpose:** Saves device inventory data to JSON file

**Generated file:** device_models.json in the system_info directory

### Task 13: Save Device Controllers

**- name: Save device controllers to file**

**Purpose:** Persists controller device information to JSON file

**Generated file:** device_controllers.json in the system_info directory

### Task 14: Save Device vEdges

**- name: Save device vedges to file**

**Purpose:** Stores vEdge device data in JSON format

**Generated file:** device_vedges.json in the system_info directory

### Task 15: Create System Info Summary

**- name: Create system info summary**

**Purpose:** Generates a comprehensive summary report of the collection process

**Generated file:** collection_summary.txt in the system_info directory

## Generated Report Content

### System Information Collection Summary

**Collection Date:** [ISO 8601 timestamp]
**vManage Host:** [vManage controller hostname/IP]
**Username:** [Authentication username]

**Successfully Retrieved System Information:**
- Device System Info: SUCCESS
- System Counters: SUCCESS  
- Device Models: SUCCESS
- Device Controllers: SUCCESS
- Device vEdges: SUCCESS

**Files Generated:**
- device_system_info.json
- system_counters.json
- device_models.json
- device_controllers.json
- device_vedges.json

**Status:** All endpoints completed successfully with no errors.

The report provides a complete overview of the data collection process, confirming successful retrieval from all API endpoints and listing all generated files for reference and further analysis.