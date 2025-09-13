# SD-WAN OMP Peers Playbook Documentation

## Overview

The SD-WAN OMP Peers playbook (Use Case 39) is an Ansible automation script designed to collect comprehensive OMP (Overlay Management Protocol) information from Cisco SD-WAN environments. This playbook retrieves OMP peer relationships, routing information, and statistics from the vManage controller and creates organized reports for network monitoring and troubleshooting.

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
**Purpose:** Creates the complete directory hierarchy needed for organized OMP data storage

**Generated folders:**
- `{{ generated_dir }}` - Base generated content folder
- `{{ omp_dir }}` - OMP-specific data storage (generated/omp_peers)

**Directory structure example:**
```
generated/
└── omp_peers/
    ├── devices_list.txt
    ├── omp_peers.txt
    ├── omp_summary.txt
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

### Task 8: OMP Peers Collection
```yaml
- name: Get all OMP peers
```
**Purpose:** Retrieves global OMP peer information

**API endpoint:** `/dataservice/device/omp/peers`
**Generated data:** All OMP peer relationships across the SD-WAN fabric

### Task 9: OMP Summary Statistics Collection
```yaml
- name: Get OMP summary statistics
```
**Purpose:** Collects OMP operational statistics and counters

**API endpoint:** `/dataservice/device/omp/summary`
**Generated data:** OMP summary including peer counts, route counts, and operational status

### Task 10: OMP Routes Collection
```yaml
- name: Get OMP routes
```
**Purpose:** Retrieves all OMP route information

**API endpoint:** `/dataservice/device/omp/routes`
**Generated data:** Complete OMP routing table information

### Task 11: OMP Advertised Routes Collection
```yaml
- name: Get OMP advertised routes
```
**Purpose:** Collects routes being advertised via OMP

**API endpoint:** `/dataservice/device/omp/advertised-routes`
**Generated data:** Routes advertised by devices to peers

### Task 12: OMP Received Routes Collection
```yaml
- name: Get OMP received routes
```
**Purpose:** Retrieves routes received via OMP

**API endpoint:** `/dataservice/device/omp/received-routes`
**Generated data:** Routes learned from OMP peers

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

### Task 14: OMP Peers File Creation
```yaml
- name: Save OMP peers to file
```
**Purpose:** Creates detailed OMP peer relationship report

**Generated file:** `omp_peers.txt`
**Content includes:**
- Peer system IP and hostname
- Peer type and state information
- Domain and overlay IDs
- Communication statistics (hellos, handshakes, updates)
- Administrative and operational states

### Task 15: OMP Summary File Creation
```yaml
- name: Save OMP summary to file
```
**Purpose:** Creates OMP operational summary report

**Generated file:** `omp_summary.txt`
**Content includes:**
- Device personality and role information
- Peer up/down counts
- Route advertisement and reception statistics
- TLOC and service information
- Multicast route statistics

### Task 16: OMP Routes File Creation
```yaml
- name: Save OMP routes to file
```
**Purpose:** Creates comprehensive routing table report

**Generated file:** `omp_routes.txt`
**Content includes:**
- Route prefixes and VPN information
- Path preferences and attributes
- TLOC information (IP, color, encapsulation)
- Origin and originator details

### Task 17: OMP Advertised Routes File Creation
```yaml
- name: Save OMP advertised routes to file
```
**Purpose:** Creates report of routes being advertised

**Generated file:** `omp_advertised_routes.txt`
**Content includes:**
- Advertised route details
- To/from peer information
- Path attributes and preferences
- TLOC and encapsulation data

### Task 18: OMP Received Routes File Creation
```yaml
- name: Save OMP received routes to file
```
**Purpose:** Creates report of routes received from peers

**Generated file:** `omp_received_routes.txt`
**Content includes:**
- Received route information
- Source peer details
- Route status and attributes
- Installation status

### Task 19: Device-Specific OMP Peers Collection
```yaml
- name: Get device-specific OMP peers for each device
```
**Purpose:** Retrieves OMP peer information for each individual device

**API endpoint:** `/dataservice/device/omp/peers?deviceId={{ system-ip }}`
**What it does:**
- Loops through all discovered devices
- Queries OMP peers for each device individually
- Provides device-specific peer relationship details

### Task 20: Device-Specific OMP Peers File Creation
```yaml
- name: Save device-specific OMP peers to files
```
**Purpose:** Creates individual OMP peer files for each device

**Generated files:** `device_omp_peers_{{ hostname }}.txt` (one per device)
**Content includes:**
- Device identification information
- Individual peer relationships
- Peer communication statistics
- Device-specific OMP operational data

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
SD-WAN OMP Peers Collection - Execution Summary
==============================================
Execution Time: [ISO8601 timestamp]
vManage Host: [hostname]
vManage Connectivity: Connected/Failed

API Endpoint Results:
- Devices List: SUCCESS/FAILED
- OMP Peers: SUCCESS/FAILED
- OMP Summary: SUCCESS/FAILED
- OMP Routes: SUCCESS/FAILED
- OMP Advertised Routes: SUCCESS/FAILED
- OMP Received Routes: SUCCESS/FAILED
- Device-Specific OMP Peers: [count] devices processed

Total Devices Found: [number]
Total OMP Peers: [number]
Total OMP Routes: [number]

Files Created:
- devices_list.txt
- omp_peers.txt
- omp_summary.txt
- omp_routes.txt
- omp_advertised_routes.txt
- omp_received_routes.txt
- device_omp_peers_[hostname].txt (per device)

Directory Structure:
- Base Directory: [path]
- OMP Data Directory: [path]

Playbook Execution: COMPLETED
```

### Key Report Features

**Device Inventory Report:**
- Complete device list with system information
- Device types, models, and software versions
- Operational status and reachability
- Site IDs and uptime data

**OMP Peer Analysis:**
- Global peer relationships
- Peer states and administrative status
- Communication statistics and counters
- Domain and overlay mapping

**Routing Information:**
- Complete OMP routing tables
- Route advertisements and receptions
- Path preferences and attributes
- TLOC information and encapsulation

**Per-Device Analysis:**
- Individual device peer relationships
- Device-specific OMP operational data
- Granular peer communication statistics

**Operational Statistics:**
- Peer up/down counts
- Route installation statistics
- Service and multicast information
- TLOC advertisement data

The reports provide comprehensive visibility into SD-WAN OMP operations, enabling network administrators to monitor peer relationships, troubleshoot routing issues, and analyze overlay network performance.