# Tunnel Statistics Configuration Playbook Documentation

## Overview

The **tunnel_statistics.yml** playbook is an Ansible automation script designed to collect comprehensive tunnel performance data and overlay network statistics from Cisco SD-WAN environments. This playbook leverages vManage REST API endpoints to extract detailed tunnel metrics, operational status, and performance indicators for analysis, monitoring, and troubleshooting SD-WAN overlay connectivity.

## Use Case

**Use Case: Get tunnel statistics - Retrieve tunnel performance data**

This playbook addresses the need to:

- Collect comprehensive tunnel statistics and performance metrics from SD-WAN overlay networks
- Monitor tunnel health, availability, and operational status across the fabric
- Export tunnel performance data for offline analysis and trend monitoring
- Provide automated tunnel monitoring for proactive network management
- Generate baseline reports for overlay network performance analysis and capacity planning
- Troubleshoot tunnel connectivity issues and performance degradation

## Prerequisites

### Environment Variables

The following environment variables must be set before running the playbook:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| **VMANAGE_HOST** | vManage controller hostname/IP | vmanage-amfament-prod.sdwan.cisco.com |
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
  tunnel_stats_dir: "{{ generated_dir }}/tunnel_statistics"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── tunnel_statistics.yml
└── generated/
    └── tunnel_statistics/
        ├── devices_list.json
        ├── tunnel_statistics_all.json
        ├── tunnel_interface.json
        ├── tunnel_operational_status.json
        ├── tunnel_performance.json
        ├── tunnel_health.json
        ├── bfd_sessions.json
        ├── omp_peers.json
        ├── tloc_statistics.json
        ├── control_connections.json
        ├── tunnel_stats_[deviceId].json
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

**Purpose:** Creates the output directory for generated tunnel statistics

**What it does:**
- Creates the **tunnel_statistics** directory under the generated folder
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
- Provides device list for subsequent per-device tunnel statistics collection

#### Task 6: Save Devices List

**Purpose:** Stores device inventory data

**Generated file:** **devices_list.json**

**What it does:**
- Saves device inventory in JSON format for reference
- Contains device IDs, names, models, and status information
- Used as input for device-specific tunnel statistics collection

#### Task 7: Get Tunnel Statistics for All Devices

**Purpose:** Collects comprehensive tunnel statistics across the SD-WAN fabric

**API Endpoint:** `/dataservice/device/tunnel/statistics`

**What it does:**
- Retrieves tunnel performance metrics for all devices
- Includes throughput, packet counts, and tunnel utilization statistics
- Collects data for all tunnel types (IPsec, GRE, overlay tunnels)
- Provides fabric-wide tunnel performance overview

#### Task 8: Save All Tunnel Statistics

**Purpose:** Stores comprehensive tunnel statistics

**Generated file:** **tunnel_statistics_all.json**

**What it does:**
- Saves aggregated tunnel performance data
- Contains throughput metrics, packet statistics, and tunnel utilization
- Provides overlay network performance overview across the entire fabric

#### Task 9: Get Tunnel Interface Data

**Purpose:** Retrieves tunnel interface configuration and status information

**API Endpoint:** `/dataservice/device/tunnel/interface`

**What it does:**
- Collects tunnel interface operational data
- Includes tunnel endpoint information and interface mappings
- Provides tunnel topology and connectivity details
- Contains tunnel configuration parameters and settings

#### Task 10: Save Tunnel Interface Data

**Purpose:** Stores tunnel interface information

**Generated file:** **tunnel_interface.json**

**What it does:**
- Saves tunnel interface configuration and operational data
- Contains tunnel endpoint details and interface mappings
- Enables tunnel topology analysis and connectivity troubleshooting

#### Task 11: Get Tunnel Operational Status

**Purpose:** Retrieves current operational status of all tunnels

**API Endpoint:** `/dataservice/device/tunnel/status`

**What it does:**
- Collects tunnel operational states (up/down/degraded)
- Includes tunnel availability and connectivity status
- Provides real-time tunnel health information
- Contains tunnel state change history and timestamps

#### Task 12: Save Tunnel Operational Status

**Purpose:** Stores tunnel operational status data

**Generated file:** **tunnel_operational_status.json**

**What it does:**
- Saves current tunnel operational states and availability
- Contains tunnel status history and state transitions
- Enables tunnel availability monitoring and alerting

#### Task 13: Get Tunnel Performance Metrics

**Purpose:** Retrieves detailed tunnel performance and quality metrics

**API Endpoint:** `/dataservice/device/tunnel/performance`

**What it does:**
- Collects tunnel latency, jitter, and loss statistics
- Includes bandwidth utilization and throughput metrics
- Provides quality of service (QoS) performance data
- Contains application-aware routing metrics

#### Task 14: Save Tunnel Performance Metrics

**Purpose:** Stores tunnel performance data

**Generated file:** **tunnel_performance.json**

**What it does:**
- Saves detailed tunnel performance metrics and quality indicators
- Contains latency, jitter, loss, and throughput statistics
- Enables performance trending and capacity planning

#### Task 15: Get Tunnel Health Data

**Purpose:** Retrieves tunnel health indicators and wellness metrics

**API Endpoint:** `/dataservice/device/tunnel/health`

**What it does:**
- Collects tunnel health scores and wellness indicators
- Includes tunnel reliability and stability metrics
- Provides health trending and degradation alerts
- Contains predictive health analytics data

#### Task 16: Save Tunnel Health Data

**Purpose:** Stores tunnel health information

**Generated file:** **tunnel_health.json**

**What it does:**
- Saves tunnel health scores and wellness metrics
- Contains health trending data and degradation indicators
- Enables proactive tunnel health monitoring

#### Task 17: Get BFD Session Statistics

**Purpose:** Retrieves Bidirectional Forwarding Detection session data

**API Endpoint:** `/dataservice/device/bfd/sessions`

**What it does:**
- Collects BFD session status and statistics
- Includes session state information and failure detection metrics
- Provides tunnel keepalive and failure detection data
- Contains BFD session configuration and timing parameters

#### Task 18: Save BFD Session Statistics

**Purpose:** Stores BFD session data

**Generated file:** **bfd_sessions.json**

**What it does:**
- Saves BFD session statistics and status information
- Contains failure detection metrics and session health data
- Enables tunnel keepalive monitoring and troubleshooting

#### Task 19: Get OMP Peer Statistics

**Purpose:** Retrieves Overlay Management Protocol peer information

**API Endpoint:** `/dataservice/device/omp/peers`

**What it does:**
- Collects OMP peer relationship status and statistics
- Includes route exchange and control plane connectivity data
- Provides overlay control plane health information
- Contains OMP session state and routing table synchronization status

#### Task 20: Save OMP Peer Statistics

**Purpose:** Stores OMP peer data

**Generated file:** **omp_peers.json**

**What it does:**
- Saves OMP peer relationship and routing information
- Contains control plane connectivity and route exchange data
- Enables overlay control plane monitoring and troubleshooting

#### Task 21: Get Device-Specific Tunnel Statistics

**Purpose:** Collects tunnel statistics for each individual device

**API Endpoint:** `/dataservice/device/tunnel/statistics?deviceId={deviceId}`

**What it does:**
- Iterates through each device from the devices list
- Retrieves tunnel statistics specific to each device
- Provides per-device tunnel performance breakdown
- Only executes for devices successfully retrieved in earlier tasks

#### Task 22: Save Device-Specific Tunnel Statistics

**Purpose:** Stores per-device tunnel statistics

**Generated files:** **tunnel_stats_{deviceId}.json**

**What it does:**
- Creates separate files for each device's tunnel statistics
- Enables device-specific tunnel performance analysis
- Provides isolated view of each device's tunnel metrics

#### Task 23: Get TLOC Statistics

**Purpose:** Retrieves Transport Locator (TLOC) information and statistics

**API Endpoint:** `/dataservice/device/tloc`

**What it does:**
- Collects TLOC configuration and operational data
- Includes transport interface and path information
- Provides underlay transport connectivity details
- Contains TLOC preference and path selection metrics

#### Task 24: Save TLOC Statistics

**Purpose:** Stores TLOC data

**Generated file:** **tloc_statistics.json**

**What it does:**
- Saves TLOC configuration and operational information
- Contains transport path and connectivity data
- Enables underlay transport analysis and path optimization

#### Task 25: Get Control Connection Statistics

**Purpose:** Retrieves control plane connection information

**API Endpoint:** `/dataservice/device/control/connections`

**What it does:**
- Collects control plane connectivity status and statistics
- Includes controller-to-device connection health
- Provides control plane session information
- Contains authentication and session management data

#### Task 26: Save Control Connection Statistics

**Purpose:** Stores control plane connection data

**Generated file:** **control_connections.json**

**What it does:**
- Saves control plane connectivity and session information
- Contains controller relationship and authentication data
- Enables control plane health monitoring and troubleshooting

#### Task 27: Create Execution Summary

**Purpose:** Generates comprehensive execution report

**Generated file:** **execution_summary.txt**

**What it does:**
- Creates detailed summary of playbook execution
- Shows success/failure status for each API endpoint
- Lists all generated files and their contents
- Provides troubleshooting information for failed endpoints
- Includes device-specific collection results

#### Task 28: Display Completion Message

**Purpose:** Provides execution status and file location

**What it displays:**
- Full path to the generated tunnel statistics directory
- Success confirmation message
- Location reference for user access

## Report Contents

The generated tunnel statistics collection typically includes:

- **Device Inventory:** Complete list of devices in the SD-WAN fabric
- **Tunnel Statistics:** Comprehensive performance metrics for all overlay tunnels
- **Tunnel Interface Data:** Interface configuration and operational information
- **Operational Status:** Current tunnel states and availability across the fabric
- **Performance Metrics:** Detailed latency, jitter, loss, and throughput statistics
- **Health Data:** Tunnel wellness indicators and health scoring
- **BFD Sessions:** Bidirectional Forwarding Detection session status and statistics
- **OMP Peers:** Overlay Management Protocol peer relationships and routing data
- **TLOC Statistics:** Transport Locator configuration and path information
- **Control Connections:** Control plane connectivity and session management data
- **Device-Specific Data:** Per-device tunnel performance and status breakdown
- **Execution Summary:** Detailed report of collection results and endpoint status