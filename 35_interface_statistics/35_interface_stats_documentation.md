# Interface Statistics Configuration Playbook Documentation

## Overview

The **interface_statistics.yml** playbook is an Ansible automation script designed to collect comprehensive interface statistics and metrics from Cisco SD-WAN environments. This playbook leverages vManage REST API endpoints to extract detailed interface performance data, operational status, and health metrics for analysis, monitoring, and troubleshooting purposes.

## Use Case

**Use Case: Get interface statistics - Get interface metrics**

This playbook addresses the need to:

- Collect comprehensive interface statistics from all SD-WAN devices
- Monitor interface performance metrics and health status
- Export interface data for offline analysis and trend monitoring
- Provide automated interface monitoring for regular health checks
- Generate baseline reports for performance analysis and capacity planning

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | sandbox-sdwan-2.cisco.com |
| **VMANAGE_USERNAME** | Username for vManage authentication | automation |
| **VMANAGE_PASSWORD** | Password for vManage authentication | |

## Playbook Structure

### Variables Configuration

```yaml
vars:
  vmanage_host: "{{ lookup('env', 'VMANAGE_HOST') | default('vmanage-amfament-prod.sdwan.cisco.com') }}"
  vmanage_username: "{{ lookup('env', 'VMANAGE_USERNAME') | default('automation') }}"
  vmanage_password: "{{ lookup('env', 'VMANAGE_PASSWORD') | default('') }}"
  vmanage_port: "443"
  generated_dir: "{{ playbook_dir }}/../generated"
  interface_stats_dir: "{{ generated_dir }}/interface_statistics"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── interface_statistics.yml
└── generated/
    └── interface_statistics/
        ├── devices_list.json
        ├── interface_statistics_all.json
        ├── interface_counters.json
        ├── interface_operational.json
        ├── interface_health.json
        ├── tunnel_statistics.json
        ├── wan_interface_statistics.json
        ├── interface_stats_[deviceId].json
        └── execution_summary.txt
```

## Task Analysis

#### Task 1: Environment Variable Validation

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Validates that **VMANAGE_HOST**, **VMANAGE_USERNAME**, and **VMANAGE_PASSWORD** are set
- Fails immediately if any required environment variable is missing
- Prevents execution failures due to missing credentials
- Provides clear error messages for troubleshooting

#### Task 2: Directory Creation

**Purpose:** Creates the output directory for generated interface statistics

**What it does:**
- Creates the **interface_statistics** directory under the generated folder
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before data collection
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting data collection

**What it does:**
- Makes a REST API call to **/dataservice/system/device/controllers**
- Uses basic authentication with provided credentials
- Sets **60-second timeout** to handle slow connections
- Ignores SSL certificate validation for internal/self-signed certificates
- Stores connectivity results for validation

#### Task 4: Connectivity Status Logging

**Purpose:** Logs connectivity status without failing the playbook

**What it does:**
- Logs the connectivity test result (success or failure status)
- Continues execution regardless of connectivity status
- Provides diagnostic information for troubleshooting
- Enables graceful handling of sandbox environment limitations

#### Task 5: Get All Devices List

**Purpose:** Retrieves list of all devices in the SD-WAN fabric

**API Endpoint:** `/dataservice/device`

**What it does:**
- Fetches complete device inventory from vManage
- Collects device IDs, hostnames, and basic device information
- Only executes if initial connectivity test succeeds
- Provides device list for subsequent per-device statistics collection

#### Task 6: Save Devices List

**Purpose:** Stores device inventory data

**Generated file:** **devices_list.json**

**What it does:**
- Saves device inventory in JSON format for reference
- Contains device IDs, names, models, and status information
- Used as input for device-specific interface statistics collection

#### Task 7: Get Interface Statistics for All Devices

**Purpose:** Collects comprehensive interface statistics across the fabric

**API Endpoint:** `/dataservice/device/interface/stats`

**What it does:**
- Retrieves interface performance metrics for all devices
- Includes throughput, packet counts, error statistics
- Collects data for all interface types (physical, logical, tunnel)

#### Task 8: Save All Interface Statistics

**Purpose:** Stores comprehensive interface statistics

**Generated file:** **interface_statistics_all.json**

**What it does:**
- Saves aggregated interface performance data
- Contains throughput metrics, packet statistics, and error counters
- Provides fabric-wide interface performance overview

#### Task 9: Get Interface Counters

**Purpose:** Retrieves detailed interface counter information

**API Endpoint:** `/dataservice/device/counters`

**What it does:**
- Collects detailed packet counters and statistics
- Includes input/output packets, bytes, errors, and drops
- Provides granular interface performance data

#### Task 10: Save Interface Counters

**Purpose:** Stores interface counter data

**Generated file:** **interface_counters.json**

**What it does:**
- Saves detailed counter information for analysis
- Contains packet-level statistics and error counters
- Enables detailed performance troubleshooting

#### Task 11: Get Interface Operational Data

**Purpose:** Retrieves operational status of all interfaces

**API Endpoint:** `/dataservice/device/interface`

**What it does:**
- Collects interface operational states (up/down)
- Includes administrative status and physical layer information
- Provides interface availability and status data

#### Task 12: Save Interface Operational Data

**Purpose:** Stores interface operational status

**Generated file:** **interface_operational.json**

**What it does:**
- Saves interface status and configuration information
- Contains operational states, speeds, and interface types
- Enables interface availability monitoring

#### Task 13: Get Device-Specific Interface Statistics

**Purpose:** Collects interface statistics for each individual device

**API Endpoint:** `/dataservice/device/interface/stats?deviceId={deviceId}`

**What it does:**
- Iterates through each device from the devices list
- Retrieves interface statistics specific to each device
- Provides per-device interface performance breakdown
- Only executes for devices successfully retrieved in earlier tasks

#### Task 14: Save Device-Specific Interface Statistics

**Purpose:** Stores per-device interface statistics

**Generated files:** **interface_stats_{deviceId}.json**

**What it does:**
- Creates separate files for each device's interface statistics
- Enables device-specific performance analysis
- Provides isolated view of each device's interface metrics

#### Task 15: Get Interface Health Statistics

**Purpose:** Retrieves interface health and status metrics

**API Endpoint:** `/dataservice/device/interface/health`

**What it does:**
- Collects interface health indicators and status
- Includes availability metrics and health scores
- Provides interface wellness assessment data

#### Task 16: Save Interface Health Statistics

**Purpose:** Stores interface health data

**Generated file:** **interface_health.json**

**What it does:**
- Saves interface health metrics and availability data
- Contains health scores and status indicators
- Enables interface health monitoring and alerting

#### Task 17: Get Tunnel Interface Statistics

**Purpose:** Retrieves tunnel-specific interface metrics

**API Endpoint:** `/dataservice/device/tunnel/statistics`

**What it does:**
- Collects statistics specific to tunnel interfaces
- Includes tunnel performance and connectivity metrics
- Provides SD-WAN overlay network performance data

#### Task 18: Save Tunnel Interface Statistics

**Purpose:** Stores tunnel interface performance data

**Generated file:** **tunnel_statistics.json**

**What it does:**
- Saves tunnel-specific performance metrics
- Contains overlay network statistics and tunnel health
- Enables SD-WAN overlay performance monitoring

#### Task 19: Get WAN Interface Statistics

**Purpose:** Retrieves WAN interface specific metrics

**API Endpoint:** `/dataservice/device/wan/interface/stats`

**What it does:**
- Collects statistics specific to WAN interfaces
- Includes WAN link performance and utilization data
- Provides underlay network performance metrics

#### Task 20: Save WAN Interface Statistics

**Purpose:** Stores WAN interface performance data

**Generated file:** **wan_interface_statistics.json**

**What it does:**
- Saves WAN-specific interface metrics
- Contains underlay network performance data
- Enables WAN link performance analysis

#### Task 21: Create Execution Summary

**Purpose:** Generates comprehensive execution report

**Generated file:** **execution_summary.txt**

**What it does:**
- Creates detailed summary of playbook execution
- Shows success/failure status for each API endpoint
- Lists all generated files and their contents
- Provides troubleshooting information for failed endpoints

#### Task 22: Display Completion Message

**Purpose:** Provides execution status and file location

**What it displays:**
- Full path to the generated interface statistics directory
- Success confirmation message
- Location reference for user access

## Report Contents

The generated interface statistics collection typically includes:

- **Device Inventory:** Complete list of devices in the SD-WAN fabric
- **Interface Statistics:** Comprehensive performance metrics for all interfaces
- **Interface Counters:** Detailed packet-level statistics and error counters
- **Operational Data:** Interface status, configuration, and availability information
- **Health Metrics:** Interface health scores and wellness indicators
- **Tunnel Statistics:** SD-WAN overlay network performance data
- **WAN Statistics:** Underlay network interface performance metrics
- **Device-Specific Data:** Per-device interface performance breakdown
- **Execution Summary:** Detailed report of collection results and status