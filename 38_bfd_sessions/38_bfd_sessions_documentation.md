# SD-WAN Get BFD Sessions Playbook Documentation

## Overview

The SD-WAN Get BFD Sessions playbook is an Ansible automation script designed to collect comprehensive Bidirectional Forwarding Detection (BFD) information from Cisco SD-WAN vManage controllers. This playbook retrieves BFD session details, summary statistics, historical data, and link performance metrics while handling API errors gracefully to ensure reliable data collection for network monitoring and troubleshooting.

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

**Purpose:** Creates the complete directory hierarchy needed for organized BFD data storage

**Generated folders:**
- `{{ generated_dir }}` - Main generated folder (../generated)
- `{{ bfd_dir }}` - BFD sessions subfolder (../generated/bfd_sessions)

**Directory structure example:**
```
generated/
└── bfd_sessions/
    ├── devices_list.txt
    ├── bfd_sessions.txt
    ├── bfd_summary.txt
    ├── bfd_history.txt
    ├── bfd_links.txt
    ├── device_bfd_sessions_[hostname].txt
    └── execution_summary.txt
```

### Task 3: vManage Connectivity Testing
```yaml
- name: Test vManage connectivity
```

**Purpose:** Verifies the vManage controller is accessible before attempting BFD data collection

**What it does:**
- Makes a REST API call to `/dataservice/system/device/controllers`
- Uses basic authentication with provided credentials
- Sets 60-second timeout for network operations
- Accepts multiple status codes (200, 403, 404, 500, 503)
- Uses `failed_when: false` to prevent red error messages
- Stores connectivity results for validation

### Task 4: Connectivity Status Handling
```yaml
- name: Handle connectivity test results
```

**Purpose:** Processes connectivity test results and sets status variables

**What it does:**
- Sets `vmanage_connected` boolean based on HTTP 200 response
- Sets `connectivity_status` with actual HTTP status code or default
- Enables conditional processing based on connectivity status
- Ensures variables are always defined for downstream tasks

### Task 5: Connectivity Status Display
```yaml
- name: Display connectivity status
```

**Purpose:** Provides visibility into connection status and execution approach

**What it does:**
- Shows connection success or failure with HTTP status
- Indicates that processing will continue with available endpoints
- Provides operational feedback during playbook execution

### Task 6: Device List Retrieval
```yaml
- name: Get list of all devices
```

**Purpose:** Retrieves complete device inventory for device-specific BFD analysis

**What it does:**
- Calls `/dataservice/device` endpoint to get all network devices
- Handles HTTP errors gracefully (403, 404, 500, 503)
- Uses `failed_when: false` to prevent fatal errors
- Collects device system IPs needed for individual BFD queries
- Provides device context for BFD session interpretation

### Task 7: Device List Error Handling
```yaml
- name: Handle devices list API errors gracefully
```

**Purpose:** Processes device list API response and determines data availability

**What it does:**
- Sets `devices_available` boolean based on HTTP 200 response
- Extracts devices data if available, otherwise sets empty array
- Enables conditional processing of device-specific BFD statistics

### Task 8: All BFD Sessions Retrieval
```yaml
- name: Get all BFD sessions
```

**Purpose:** Collects comprehensive BFD session information across the network

**What it does:**
- Calls `/dataservice/device/bfd/sessions` endpoint
- Retrieves network-wide BFD session details
- Handles API errors gracefully with multiple accepted status codes
- Collects session states, timing parameters, and packet statistics

### Task 9: BFD Summary Statistics Retrieval
```yaml
- name: Get BFD summary statistics
```

**Purpose:** Retrieves high-level BFD summary data per device

**What it does:**
- Calls `/dataservice/device/bfd/summary` endpoint
- Collects per-device BFD session counts and statistics
- Gathers session up/down counts and flap statistics
- Retrieves percentage availability metrics

### Task 10: BFD History Retrieval
```yaml
- name: Get BFD history
```

**Purpose:** Collects historical BFD state change information

**What it does:**
- Calls `/dataservice/device/bfd/history` endpoint
- Retrieves BFD session state transition history
- Collects timing information for state changes
- Gathers event details for troubleshooting purposes

### Task 11: BFD Links Status Retrieval
```yaml
- name: Get BFD links status
```

**Purpose:** Retrieves BFD link performance and status information

**What it does:**
- Calls `/dataservice/device/bfd/links` endpoint
- Collects link-level BFD status and performance metrics
- Retrieves bandwidth, latency, jitter, and loss statistics
- Gathers interface and tunnel information

### Task 12: Device List File Creation
```yaml
- name: Save devices list to file
```

**Purpose:** Creates comprehensive device inventory report with connectivity status

**Generated file:** `devices_list.txt`

**Report contents:**
- Timestamp and vManage host information
- vManage connectivity status
- API availability status
- Total device count
- Detailed device information:
  - Hostname, System IP, Device Type, and Model
  - Software Version and Site ID
  - Status, Reachability, and Uptime information
- Error details if device list API is unavailable

### Task 13: BFD Sessions File Creation
```yaml
- name: Save BFD sessions to file
```

**Purpose:** Creates comprehensive BFD sessions report

**Generated file:** `bfd_sessions.txt`

**Report contents:**
- Execution timestamp and connection details
- API endpoint availability status
- Total BFD sessions count
- Detailed session information:
  - System IP, hostname, and site identification
  - Local and remote color information
  - Source and destination IP addresses and ports
  - Protocol and timing parameters (detect multiplier, intervals)
  - Session state, transitions, and packet statistics
  - Uptime and downtime information
- Comprehensive error logging for failed API calls

### Task 14: BFD Summary Statistics File Creation
```yaml
- name: Save BFD summary to file
```

**Purpose:** Creates BFD summary statistics report per device

**Generated file:** `bfd_summary.txt`

**Report contents:**
- Per-device BFD summary statistics:
  - Device identification (system IP, hostname, site ID)
  - Total session counts and state breakdown
  - Sessions up, down, and flap counts
  - Percentage availability calculations
  - Last updated and entry time information
- API availability and error handling information

### Task 15: BFD History File Creation
```yaml
- name: Save BFD history to file
```

**Purpose:** Creates BFD state change history report

**Generated file:** `bfd_history.txt`

**Report contents:**
- Historical BFD session state transitions:
  - Device and remote system identification
  - Local and remote color information
  - Source and destination IP details
  - Event type and timing information
  - State change details and timing parameters
- Complete error logging for unavailable endpoints

### Task 16: BFD Links File Creation
```yaml
- name: Save BFD links to file
```

**Purpose:** Creates BFD link performance and status report

**Generated file:** `bfd_links.txt`

**Report contents:**
- Link-level BFD information:
  - Device identification and interface details
  - Public and private IP addresses and ports
  - Color and state information (admin/operational)
  - Remote system and connection details
  - Performance metrics (loss percentage, latency, jitter)
  - Bandwidth utilization (TX/RX bandwidth)
  - Protocol, encapsulation, and quality metrics
- Comprehensive error handling and status reporting

### Task 17: Device-Specific BFD Sessions Retrieval
```yaml
- name: Get device-specific BFD sessions for each device
```

**Purpose:** Collects detailed BFD session information for individual network devices

**What it does:**
- Iterates through each device found in the device inventory
- Calls `/dataservice/device/bfd/sessions?deviceId={system-ip}` for each device
- Handles API errors gracefully with multiple accepted status codes
- Only executes when device list is successfully retrieved
- Uses `failed_when: false` to prevent execution failures

### Task 18: Device-Specific BFD Files Creation
```yaml
- name: Save device-specific BFD sessions to files
```

**Purpose:** Creates individual BFD session reports for each network device

**Generated files:** `device_bfd_sessions_[hostname].txt`

**Report contents for each device:**
- Device identification (hostname, system IP, device type)
- API availability status for the specific device
- Detailed per-device BFD session information:
  - Local and remote color assignments
  - Remote system IP and connection details
  - Source/destination IP addresses and ports
  - Protocol and timing parameters
  - Session state, transitions, and statistics
  - Packet transmission and reception counts
  - Uptime, downtime, and failure reason information
- Error details for devices with unavailable BFD data

### Task 19: Execution Summary Creation
```yaml
- name: Create execution summary
```

**Purpose:** Creates comprehensive summary of entire BFD data collection process

**Generated file:** `execution_summary.txt`

**Summary contents:**
- Execution timestamp and vManage host
- vManage connectivity status
- API endpoint results summary for all BFD endpoints
- Total device count and BFD session counts
- Complete list of all generated files
- Execution notes about error handling, data availability, and BFD state meanings

## Generated Reports

The playbook creates comprehensive BFD documentation in the `generated/bfd_sessions/` directory:

### devices_list.txt
Complete network device inventory with hardware details, software versions, operational status, and connectivity information essential for interpreting BFD session data.

### bfd_sessions.txt
Network-wide BFD session details including all active sessions with timing parameters, packet statistics, state information, and connectivity details for comprehensive tunnel monitoring.

### bfd_summary.txt
Per-device BFD summary statistics showing session counts, availability percentages, flap statistics, and health metrics for quick network status assessment.

### bfd_history.txt
Historical BFD state change information including transition events, timing data, and troubleshooting details for analyzing network stability patterns.

### bfd_links.txt
BFD link performance metrics including bandwidth utilization, latency, jitter, packet loss, and quality measurements for network optimization and troubleshooting.

### device_bfd_sessions_[hostname].txt (per device)
Device-specific BFD session breakdowns showing per-device tunnel status, session parameters, connectivity details, and performance metrics for targeted analysis.

### execution_summary.txt
Comprehensive execution report including API availability, connectivity status, processing results, file inventory, and operational notes for complete visibility.

## Error Handling Features

- **Graceful API Error Management**: Uses `failed_when: false` and multiple accepted status codes to prevent playbook failures during BFD data collection
- **Comprehensive Error Logging**: Documents all API errors with detailed status codes and error messages in output files
- **Conditional Processing**: Skips device-specific tasks when device inventory or connectivity fails
- **Clean Execution**: Eliminates red "fatal" error messages while maintaining complete error visibility
- **Sandbox Environment Compatible**: Handles common sandbox limitations like HTTP 403/503 errors for BFD endpoints
- **Connection Resilience**: Continues processing even when initial connectivity tests fail

## Pipeline Integration

**Manual Execution:** Navigate to GitLab project → Code → Pipelines → Run Pipeline → Select playbook

**Scheduled Execution:** Supports automated daily execution with artifact retention for trend analysis and monitoring

**Variable Configuration:** Uses environment variables (VMANAGE_HOST, VMANAGE_USERNAME, VMANAGE_PASSWORD) for secure credential management

## BFD Data Analysis Notes

- **Session States**: BFD sessions can be in states: UP, DOWN, ADMIN_DOWN, INIT - critical for tunnel health assessment
- **Timing Parameters**: TX/RX intervals and detect multipliers determine failure detection speed and sensitivity
- **Performance Metrics**: Latency, jitter, and packet loss data provide insights into link quality and performance
- **Historical Analysis**: State transition history helps identify patterns and recurring issues
- **Network Resilience**: BFD statistics are essential for understanding SD-WAN fabric health and tunnel reliability
- **Troubleshooting Context**: Combines session data with link performance for comprehensive network diagnostics