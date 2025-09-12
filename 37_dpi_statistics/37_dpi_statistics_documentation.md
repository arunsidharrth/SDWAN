# SD-WAN Get DPI Statistics Playbook Documentation

## Overview

The SD-WAN Get DPI Statistics playbook is an Ansible automation script designed to collect comprehensive Deep Packet Inspection (DPI) statistics from Cisco SD-WAN vManage controllers. This playbook retrieves application-aware networking data, traffic flow information, and performance metrics while handling API errors gracefully to ensure reliable data collection.

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

**Purpose:** Creates the complete directory hierarchy needed for organized DPI data storage

**Generated folders:**
- `{{ generated_dir }}` - Main generated folder (../generated)
- `{{ dpi_dir }}` - DPI statistics subfolder (../generated/dpi_statistics)

**Directory structure example:**
```
generated/
└── dpi_statistics/
    ├── devices_list.txt
    ├── dpi_summary_statistics.txt
    ├── dpi_applications_statistics.txt
    ├── dpi_flows_statistics.txt
    ├── dpi_top_applications.txt
    ├── device_dpi_stats_[hostname].txt
    └── execution_summary.txt
```

### Task 3: vManage Connectivity Testing
```yaml
- name: Test vManage connectivity
```

**Purpose:** Verifies the vManage controller is accessible before attempting DPI data collection

**What it does:**
- Makes a REST API call to `/dataservice/system/device/controllers`
- Uses basic authentication with provided credentials
- Sets 60-second timeout for network operations
- Accepts multiple status codes (200, 403, 404, 500, 503)
- Uses `failed_when: false` to prevent red error messages
- Stores connectivity results for validation

### Task 4: Connectivity Failure Handling
```yaml
- name: Fail if connectivity test failed
```

**Purpose:** Stops execution if connectivity test fails with non-200 status

**What it does:** Prevents unnecessary API attempts when vManage is unreachable or authentication fails

### Task 5: Device List Retrieval
```yaml
- name: Get list of all devices
```

**Purpose:** Retrieves complete device inventory for device-specific DPI statistics collection

**What it does:**
- Calls `/dataservice/device` endpoint to get all network devices
- Handles HTTP errors gracefully (403, 404, 500, 503)
- Uses `failed_when: false` to prevent fatal errors
- Collects device system IPs needed for individual DPI queries
- Provides device context for DPI data interpretation

### Task 6: Device List Error Handling
```yaml
- name: Handle devices list API errors gracefully
```

**Purpose:** Processes device list API response and determines data availability

**What it does:**
- Sets `devices_available` boolean based on HTTP 200 response
- Extracts devices data if available, otherwise sets empty array
- Enables conditional processing of device-specific DPI statistics

### Task 7: DPI Summary Statistics Retrieval
```yaml
- name: Get DPI summary statistics
```

**Purpose:** Collects high-level DPI summary data across the network

**What it does:**
- Calls `/dataservice/statistics/dpi/summary` endpoint
- Retrieves network-wide DPI summary metrics
- Handles API errors gracefully with multiple accepted status codes
- Collects total flows, applications, bytes, and packets data

### Task 8: DPI Applications Statistics Retrieval
```yaml
- name: Get DPI applications statistics
```

**Purpose:** Retrieves detailed application-level DPI statistics

**What it does:**
- Calls `/dataservice/statistics/dpi/applications` endpoint
- Collects per-application traffic statistics
- Gathers application family classifications
- Retrieves bandwidth usage and percentage data for applications

### Task 9: DPI Flows Statistics Retrieval
```yaml
- name: Get DPI flows statistics
```

**Purpose:** Collects individual network flow DPI information

**What it does:**
- Calls `/dataservice/statistics/dpi/flows` endpoint
- Retrieves detailed flow-level statistics
- Collects source/destination IP and port information
- Gathers protocol and application identification data

### Task 10: DPI Top Applications Retrieval
```yaml
- name: Get DPI top applications
```

**Purpose:** Retrieves ranked list of top applications by usage

**What it does:**
- Calls `/dataservice/statistics/dpi/top-applications` endpoint
- Collects top applications ranked by traffic volume
- Retrieves bandwidth utilization metrics
- Provides network usage prioritization data

### Task 11: Device List File Creation
```yaml
- name: Save devices list to file
```

**Purpose:** Creates comprehensive device inventory report

**Generated file:** `devices_list.txt`

**Report contents:**
- Timestamp and vManage host information
- API availability status
- Total device count
- Detailed device information:
  - Hostname, System IP, Device Type, and Model
  - Software Version and Site ID
  - Status, Reachability, and Uptime information
- Error details if device list API is unavailable

### Task 12: DPI Summary Statistics File Creation
```yaml
- name: Save DPI summary statistics to file
```

**Purpose:** Creates network-wide DPI summary report

**Generated file:** `dpi_summary_statistics.txt`

**Report contents:**
- Execution timestamp and connection details
- API endpoint availability status
- Per-device DPI summary data:
  - Device IP and Hostname identification
  - Total flows, applications, bytes, and packets
  - Data collection timestamps and entry times
- Comprehensive error logging for failed API calls

### Task 13: DPI Applications Statistics File Creation
```yaml
- name: Save DPI applications statistics to file
```

**Purpose:** Creates detailed application-level DPI analysis report

**Generated file:** `dpi_applications_statistics.txt`

**Report contents:**
- Application-specific traffic statistics
- Per-application data including:
  - Application name and family classification
  - Bytes, packets, and flows metrics
  - Traffic percentage calculations
  - Device-level application usage breakdown
- Timestamp and error handling information

### Task 14: DPI Flows Statistics File Creation
```yaml
- name: Save DPI flows statistics to file
```

**Purpose:** Creates individual network flow DPI report

**Generated file:** `dpi_flows_statistics.txt`

**Report contents:**
- Individual flow-level DPI data:
  - Flow ID and device identification
  - Source and destination IP addresses and ports
  - Protocol and application classification
  - Traffic volume (bytes and packets)
  - Flow duration and timing information
- Complete error logging for unavailable endpoints

### Task 15: DPI Top Applications File Creation
```yaml
- name: Save DPI top applications to file
```

**Purpose:** Creates ranked top applications usage report

**Generated file:** `dpi_top_applications.txt`

**Report contents:**
- Ranked list of top applications by usage
- Per-application metrics:
  - Application name and family
  - Total bytes, packets, and flows
  - Percentage of total network traffic
  - Average and peak bandwidth utilization
  - Number of devices using each application
- Network usage prioritization insights

### Task 16: Device-Specific DPI Statistics Retrieval
```yaml
- name: Get device-specific DPI statistics for each device
```

**Purpose:** Collects detailed DPI statistics for individual network devices

**What it does:**
- Iterates through each device found in the device inventory
- Calls `/dataservice/statistics/dpi/device/{system-ip}` for each device
- Handles API errors gracefully with multiple accepted status codes
- Only executes when device list is successfully retrieved
- Uses `failed_when: false` to prevent execution failures

### Task 17: Device-Specific DPI Files Creation
```yaml
- name: Save device-specific DPI statistics to files
```

**Purpose:** Creates individual DPI reports for each network device

**Generated files:** `device_dpi_stats_[hostname].txt`

**Report contents for each device:**
- Device identification (hostname, system IP, device type)
- API availability status for the specific device
- Detailed per-device DPI statistics:
  - Application-level traffic breakdown
  - Bytes sent and received per application
  - Packets sent and received metrics
  - Session and flow counts
  - Average session duration
  - Peak bandwidth utilization
- Error details for devices with unavailable DPI data

### Task 18: Execution Summary Creation
```yaml
- name: Create execution summary
```

**Purpose:** Creates comprehensive summary of entire DPI statistics collection

**Generated file:** `execution_summary.txt`

**Summary contents:**
- Execution timestamp and vManage host
- API endpoint results summary for all DPI endpoints
- Total device count and processing results
- Complete list of all generated files
- Execution notes about error handling and data availability

## Generated Reports

The playbook creates comprehensive DPI documentation in the `generated/dpi_statistics/` directory:

### devices_list.txt
Complete network device inventory with hardware details, software versions, operational status, and reachability information essential for interpreting DPI statistics.

### dpi_summary_statistics.txt
Network-wide DPI summary providing high-level traffic statistics including total flows, applications, data volumes, and packet counts across all devices.

### dpi_applications_statistics.txt
Detailed application-level analysis showing traffic patterns, application families, bandwidth utilization, and percentage breakdowns for network visibility.

### dpi_flows_statistics.txt
Individual network flow details including source/destination information, protocols, applications, traffic volumes, and flow durations for granular traffic analysis.

### dpi_top_applications.txt
Ranked list of top applications by network usage, including bandwidth metrics, device counts, and traffic percentages for network optimization insights.

### device_dpi_stats_[hostname].txt (per device)
Device-specific DPI breakdowns showing per-device application usage, session statistics, bandwidth utilization, and traffic patterns for targeted analysis.

### execution_summary.txt
Comprehensive execution report including API availability, processing results, file inventory, and error handling notes for operational visibility.

## Error Handling Features

- **Graceful API Error Management**: Uses `failed_when: false` and multiple accepted status codes to prevent playbook failures during data collection
- **Comprehensive Error Logging**: Documents all API errors with detailed status codes and error messages in output files
- **Conditional Processing**: Skips device-specific tasks when device inventory retrieval fails
- **Clean Execution**: Eliminates red "fatal" error messages while maintaining complete error visibility
- **Sandbox Environment Compatible**: Handles common sandbox limitations like HTTP 403/503 errors for DPI endpoints

## Pipeline Integration

**Manual Execution:** Navigate to GitLab project → Code → Pipelines → Run Pipeline → Select playbook

**Scheduled Execution:** Supports automated daily execution with artifact retention for trend analysis

**Variable Configuration:** Uses environment variables (VMANAGE_HOST, VMANAGE_USERNAME, VMANAGE_PASSWORD) for secure credential management

## DPI Data Analysis Notes

- **Traffic Patterns**: DPI statistics reflect current network traffic patterns and may vary based on time of day and business operations
- **Application Visibility**: Provides deep insight into application usage across the SD-WAN fabric for optimization and policy decisions
- **Performance Metrics**: Includes bandwidth utilization, session durations, and flow characteristics for performance analysis
- **Security Context**: Application identification supports security policy enforcement and threat detection capabilities