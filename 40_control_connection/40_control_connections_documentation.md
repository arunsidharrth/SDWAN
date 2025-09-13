# SD-WAN Control Connections Playbook Documentation

## Overview

The SD-WAN Control Connections playbook (Use Case 40) is an Ansible automation script designed to collect comprehensive control plane connectivity information from Cisco SD-WAN environments. This playbook retrieves control connection states, statistics, and security details from the vManage controller and creates organized reports for control plane monitoring and troubleshooting.

## Detailed Task Analysis

### Task 1: Environment Variable Validation
```yaml
- name: Validate environment variables are set
```
**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Checks that vmanage_host, vmanage_username, and vmanage_password are set
- Fails the playbook immediately if any critical environment variables are missing
- Prevents failed execution attempts due to missing credentials

### Task 2: Directory Structure Creation
```yaml
- name: Create generated directory structure
```
**Purpose:** Creates the complete directory hierarchy needed for organized control connection data storage

**Generated folders:**
- `{{ generated_dir }}` - Base generated content folder
- `{{ control_dir }}` - Control connections-specific data storage (generated/control_connections)

**Directory structure example:**
```
generated/
└── control_connections/
    ├── devices_list.txt
    ├── control_connections.txt
    ├── control_summary.txt
    └── [device-specific files]
```

### Task 3: vManage Connectivity Testing
```yaml
- name: Test vManage connectivity
```
**Purpose:** Verifies the vManage controller is accessible before attempting data collection

**What it does:**
- Makes a REST API call to `/dataservice/system/device/controllers`
- Uses basic authentication with provided credentials
- Sets 60-second timeout
- Ignores SSL certificate validation for internal certificates
- Accepts multiple status codes (200, 403, 404, 500, 503) for graceful error handling

### Task 4: Connectivity Results Handling
```yaml
- name: Handle connectivity test results
```
**Purpose:** Processes connectivity test results and sets status variables

**Generated variables:**
- `vmanage_connected`: Boolean indicating successful connection
- `connectivity_status`: HTTP status code for troubleshooting

### Task 5: Connectivity Status Display
```yaml
- name: Display connectivity status
```
**Purpose:** Shows connection test results for immediate feedback

**Generated output:** Connection status message with success/failure indication

### Task 6: Device Inventory Collection
```yaml
- name: Get list of all devices
```
**Purpose:** Retrieves complete device inventory from SD-WAN fabric

**API endpoint:** `/dataservice/device`
**Generated data:** Complete list of all devices with their properties

### Task 7: Device List Error Handling
```yaml
- name: Handle devices list API errors gracefully
```
**Purpose:** Processes device list results and handles API failures

**Generated variables:**
- `devices_available`: Boolean indicating successful device data retrieval
- `devices_data`: Array of device information or empty list on failure

### Task 8: Control Connections Collection
```yaml
- name: Get all control connections
```
**Purpose:** Retrieves all control plane connections across the SD-WAN fabric

**API endpoint:** `/dataservice/device/control/connections`
**Generated data:** Complete control connection information including states, protocols, and endpoints

### Task 9: Control Connections Summary Collection
```yaml
- name: Get control connections summary
```
**Purpose:** Collects summarized control connection statistics

**API endpoint:** `/dataservice/device/control/summary`
**Generated data:** Control connection summary including up/down counts and operational states

### Task 10: Control Connection Statistics Collection
```yaml
- name: Get control connection statistics
```
**Purpose:** Retrieves detailed control connection statistics and counters

**API endpoint:** `/dataservice/device/control/stats`
**Generated data:** Detailed statistics including packet counts, error counts, and communication metrics

### Task 11: DTLS Connections Collection
```yaml
- name: Get DTLS connections
```
**Purpose:** Collects DTLS-specific control connection information

**API endpoint:** `/dataservice/device/control/connections/dtls`
**Generated data:** DTLS connection details including encryption parameters and queue statistics

### Task 12: TLS Connections Collection
```yaml
- name: Get TLS connections
```
**Purpose:** Retrieves TLS-specific control connection information

**API endpoint:** `/dataservice/device/control/connections/tls`
**Generated data:** TLS connection details including cipher suites and certificate information

### Task 13: Device List File Creation
```yaml
- name: Save devices list to file
```
**Purpose:** Creates structured text file with device inventory

**Generated file:** `devices_list.txt`
**Content includes:**
- Device hostname, system IP, device type and model
- Software version and site ID
- Device status and reachability
- Uptime information

### Task 14: Control Connections File Creation
```yaml
- name: Save control connections to file
```
**Purpose:** Creates detailed control connections report

**Generated file:** `control_connections.txt`
**Content includes:**
- System IP and hostname information
- Peer type and peer system IP
- Protocol and color information
- Connection states and administrative status
- IP addresses and port information
- Domain and organization details

### Task 15: Control Summary File Creation
```yaml
- name: Save control connections summary to file
```
**Purpose:** Creates control connections summary report

**Generated file:** `control_summary.txt`
**Content includes:**
- Device personality and type information
- Connection up/down counts
- Administrative and operational states
- Domain and organization mapping
- Version and last update information

### Task 16: Control Statistics File Creation
```yaml
- name: Save control connection statistics to file
```
**Purpose:** Creates detailed statistics report

**Generated file:** `control_statistics.txt`
**Content includes:**
- Packet and byte transmission statistics
- Hello and handshake message counts
- Alert and error statistics
- Communication protocol details

### Task 17: DTLS Connections File Creation
```yaml
- name: Save DTLS connections to file
```
**Purpose:** Creates DTLS-specific connections report

**Generated file:** `dtls_connections.txt`
**Content includes:**
- DTLS connection endpoints and ports
- Protocol version and cipher suite information
- Queue sizes and interface details
- Connection state and uptime data

### Task 18: TLS Connections File Creation
```yaml
- name: Save TLS connections to file
```
**Purpose:** Creates TLS-specific connections report

**Generated file:** `tls_connections.txt`
**Content includes:**
- TLS connection endpoints and ports
- Protocol version and cipher suite details
- Certificate serial numbers
- Session reuse information

### Task 19: Device-Specific Control Connections Collection
```yaml
- name: Get device-specific control connections for each device
```
**Purpose:** Retrieves control connection information for each individual device

**API endpoint:** `/dataservice/device/control/connections?deviceId={{ system-ip }}`
**What it does:**
- Loops through all discovered devices
- Queries control connections for each device individually
- Provides device-specific connection details

### Task 20: Device-Specific Control Connections File Creation
```yaml
- name: Save device-specific control connections to files
```
**Purpose:** Creates individual control connection files for each device

**Generated files:** `device_control_connections_{{ hostname }}.txt` (one per device)
**Content includes:**
- Device identification information
- Individual control connections
- Connection statistics and states
- Device-specific operational data

### Task 21: Execution Summary Creation
```yaml
- name: Create execution summary
```
**Purpose:** Creates comprehensive execution report

**Generated file:** `execution_summary.txt`

## Report Content

The playbook generates the following comprehensive reports:

### Execution Summary Report
```
SD-WAN Control Connections Collection - Execution Summary
========================================================
Execution Time: [ISO8601 timestamp]
vManage Host: [hostname]
vManage Connectivity: Connected/Failed

API Endpoint Results:
- Devices List: SUCCESS/FAILED
- Control Connections: SUCCESS/FAILED
- Control Summary: SUCCESS/FAILED
- Control Statistics: SUCCESS/FAILED
- DTLS Connections: SUCCESS/FAILED
- TLS Connections: SUCCESS/FAILED
- Device-Specific Control Connections: [count] devices processed

Total Devices Found: [number]
Total Control Connections: [number]
Total DTLS Connections: [number]
Total TLS Connections: [number]

Files Created:
- devices_list.txt
- control_connections.txt
- control_summary.txt
- control_statistics.txt
- dtls_connections.txt
- tls_connections.txt
- device_control_connections_[hostname].txt (per device)

Directory Structure:
- Base Directory: [path]
- Control Connections Directory: [path]

Playbook Execution: COMPLETED
```

### Key Report Features

**Device Inventory Report:**
- Complete device list with system information
- Device types, models, and software versions
- Operational status and reachability
- Site IDs and uptime data

**Control Connections Analysis:**
- Global control connection states
- Peer relationships and protocols
- Public and private IP/port mappings
- Connection uptime and preferences

**Security Connection Details:**
- DTLS connection parameters
- TLS connection specifications
- Cipher suite information
- Protocol versions and encryption details

**Statistical Information:**
- Packet and byte transmission counters
- Hello and handshake message statistics
- Error counts and alert information
- Queue sizes and performance metrics

**Per-Device Analysis:**
- Individual device control connections
- Device-specific operational data
- Granular connection statistics
- Device-level troubleshooting information

**Operational Monitoring:**
- Connection up/down counts
- Administrative and operational states
- Domain and organizational mapping
- Version compatibility information

The reports provide comprehensive visibility into SD-WAN control plane operations, enabling network administrators to monitor control connection health, troubleshoot connectivity issues, analyze encryption status, and ensure proper control plane functionality across the entire SD-WAN fabric.