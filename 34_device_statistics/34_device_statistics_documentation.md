# SD-WAN Device Statistics Collection Playbook Documentation

## Overview

The **device_statistics.yml** playbook is an Ansible automation script designed to collect comprehensive device-specific statistics from Cisco SD-WAN environments. This playbook leverages REST API calls to extract detailed performance metrics, resource utilization, and operational statistics from individual devices managed by the vManage controller.

## Use Case

**Use Case: Get device statistics - Retrieve device-specific statistics**

This playbook addresses the need to:

- Collect detailed device-specific performance statistics
- Gather resource utilization metrics for individual devices
- Extract hardware status and environmental data
- Monitor network interface performance and tunnel statistics
- Provide automated device monitoring for operational insights
- Export device metrics for capacity planning and troubleshooting

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
  device_stats_dir: "{{ generated_dir }}/device_statistics"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── device_statistics.yml
└── generated/
    └── device_statistics/
        ├── device_list.json
        ├── interface_statistics.json
        ├── memory_statistics.json
        ├── cpu_statistics.json
        ├── disk_statistics.json
        ├── tunnel_statistics.json
        ├── app_route_statistics.json
        ├── hardware_statistics.json
        ├── environment_statistics.json
        └── uptime_statistics.json
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

**Purpose:** Creates the output directory for generated device statistics files

**What it does:**
- Creates the **device_statistics** directory under the **generated** folder
- Sets appropriate permissions (755) for file access
- Ensures the output location exists before statistics collection
- Creates parent directories if they don't exist

#### Task 3: vManage Connectivity Test

**Purpose:** Verifies the vManage controller is accessible before attempting statistics collection

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

#### Task 5: Get Device List

**Purpose:** Retrieves complete device inventory from vManage

**API endpoint:** `/dataservice/device`

**What it does:**
- Collects comprehensive device inventory information
- Gathers device status, reachability, and basic information
- Handles API errors gracefully with ignore_errors flag
- Provides foundation data for device-specific analysis

#### Task 6: Save Device List

**Purpose:** Saves device inventory to JSON file

**Generated file:** **device_list.json**

**What it does:**
- Converts device inventory to formatted JSON
- Saves file only if API call was successful (HTTP 200)
- Creates readable JSON format for analysis
- Stores complete device catalog information

#### Task 7: Get Device Interface Statistics

**Purpose:** Collects network interface performance metrics

**API endpoint:** `/dataservice/device/interface/stats`

**What it does:**
- Retrieves interface throughput, packet counts, and error statistics
- Gathers network performance metrics for all device interfaces
- Handles potential API errors without stopping execution
- Provides detailed network interface analytics

#### Task 8: Save Device Interface Statistics

**Purpose:** Saves interface statistics to JSON file

**Generated file:** **interface_statistics.json**

**What it does:**
- Stores network interface performance data
- Only creates file if API call succeeded
- Enables network performance analysis
- Supports interface troubleshooting activities

#### Task 9: Get Device Memory Statistics

**Purpose:** Collects memory utilization and availability metrics

**API endpoint:** `/dataservice/device/memory`

**What it does:**
- Retrieves memory usage statistics for all devices
- Gathers available, used, and free memory information
- Provides memory utilization trends and patterns
- Supports capacity planning and resource monitoring

#### Task 10: Save Device Memory Statistics

**Purpose:** Saves memory statistics to JSON file

**Generated file:** **memory_statistics.json**

**What it does:**
- Stores memory utilization data
- Enables memory usage analysis and trending
- Supports capacity planning decisions
- Provides resource monitoring insights

#### Task 11: Get Device CPU Statistics

**Purpose:** Collects processor utilization metrics

**API endpoint:** `/dataservice/device/cpu`

**What it does:**
- Retrieves CPU usage statistics for all devices
- Gathers processor load and utilization information
- Provides performance metrics for capacity planning
- Supports system performance monitoring

#### Task 12: Save Device CPU Statistics

**Purpose:** Saves CPU statistics to JSON file

**Generated file:** **cpu_statistics.json**

**What it does:**
- Stores processor utilization data
- Enables CPU performance analysis
- Supports system performance monitoring
- Provides capacity planning insights

#### Task 13: Get Device Disk Statistics

**Purpose:** Collects storage utilization and performance metrics

**API endpoint:** `/dataservice/device/disk`

**What it does:**
- Retrieves disk usage statistics for all devices
- Gathers storage capacity and utilization information
- Provides disk performance and space utilization data
- Supports storage capacity planning

#### Task 14: Save Device Disk Statistics

**Purpose:** Saves disk statistics to JSON file

**Generated file:** **disk_statistics.json**

**What it does:**
- Stores storage utilization data
- Enables disk usage analysis and monitoring
- Supports storage capacity planning
- Provides disk performance insights

#### Task 15: Get Device Tunnel Statistics

**Purpose:** Collects IPsec tunnel performance metrics

**API endpoint:** `/dataservice/device/tunnel/statistics`

**What it does:**
- Retrieves tunnel throughput and performance statistics
- Gathers IPsec tunnel operational metrics
- Provides tunnel health and performance data
- Supports network connectivity analysis

#### Task 16: Save Device Tunnel Statistics

**Purpose:** Saves tunnel statistics to JSON file

**Generated file:** **tunnel_statistics.json**

**What it does:**
- Stores tunnel performance data
- Enables tunnel health monitoring
- Supports connectivity troubleshooting
- Provides network performance insights

#### Task 17: Get Device App-Route Statistics

**Purpose:** Collects application-aware routing statistics

**API endpoint:** `/dataservice/device/app-route/statistics`

**What it does:**
- Retrieves application routing performance metrics
- Gathers application-specific traffic statistics
- Provides application performance insights
- Supports application optimization decisions

#### Task 18: Save Device App-Route Statistics

**Purpose:** Saves app-route statistics to JSON file

**Generated file:** **app_route_statistics.json**

**What it does:**
- Stores application routing data
- Enables application performance analysis
- Supports application optimization
- Provides traffic pattern insights

#### Task 19: Get Device Hardware Statistics

**Purpose:** Collects hardware component status information

**API endpoint:** `/dataservice/device/hardware/status`

**What it does:**
- Retrieves hardware component health status
- Gathers device hardware operational information
- Provides hardware failure detection data
- Supports preventive maintenance planning

#### Task 20: Save Device Hardware Statistics

**Purpose:** Saves hardware statistics to JSON file

**Generated file:** **hardware_statistics.json**

**What it does:**
- Stores hardware status data
- Enables hardware health monitoring
- Supports preventive maintenance
- Provides component failure insights

#### Task 21: Get Device Environment Statistics

**Purpose:** Collects environmental monitoring data

**API endpoint:** `/dataservice/device/hardware/environment`

**What it does:**
- Retrieves temperature, power, and fan status information
- Gathers environmental sensor data
- Provides device environmental health metrics
- Supports environmental monitoring and alerting

#### Task 22: Save Device Environment Statistics

**Purpose:** Saves environment statistics to JSON file

**Generated file:** **environment_statistics.json**

**What it does:**
- Stores environmental monitoring data
- Enables environmental health tracking
- Supports environmental alerting
- Provides thermal and power insights

#### Task 23: Get Device Uptime Statistics

**Purpose:** Collects system uptime and status information

**API endpoint:** `/dataservice/device/system/status`

**What it does:**
- Retrieves device uptime and system status information
- Gathers system availability metrics
- Provides device reliability data
- Supports availability analysis

#### Task 24: Save Device Uptime Statistics

**Purpose:** Saves uptime statistics to JSON file

**Generated file:** **uptime_statistics.json**

**What it does:**
- Stores system uptime and status data
- Enables availability analysis
- Supports reliability monitoring
- Provides system health insights

#### Task 25: Completion Notification

**Purpose:** Provides execution status and file location

**What it displays:**
- Full path to the generated device statistics directory
- Success confirmation message
- Location reference for users

## Report Contents

The generated device statistics files typically include:

- **Device List:** Complete device inventory with status, model, software version, and reachability information
- **Interface Statistics:** Network interface performance metrics including throughput, packet counts, error rates, and utilization statistics
- **Memory Statistics:** Memory utilization data including total, used, free, and available memory for each device
- **CPU Statistics:** Processor utilization metrics including CPU load, usage percentages, and performance statistics
- **Disk Statistics:** Storage utilization data including disk capacity, used space, free space, and I/O performance metrics
- **Tunnel Statistics:** IPsec tunnel performance data including throughput, packet counts, latency, and tunnel health metrics
- **App-Route Statistics:** Application-aware routing metrics including application-specific traffic patterns and performance data
- **Hardware Statistics:** Hardware component status including power supplies, fans, temperature sensors, and component health
- **Environment Statistics:** Environmental monitoring data including temperature readings, power consumption, and environmental alerts
- **Uptime Statistics:** System uptime, availability metrics, boot time, and system status information