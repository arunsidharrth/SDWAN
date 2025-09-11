# SD-WAN Statistics Collection Playbook Documentation

## Overview

The **statistics.yml** playbook is an Ansible automation script designed to collect comprehensive statistics from Cisco SD-WAN environments. This playbook leverages REST API calls to extract detailed statistical information from the vManage controller and produces organized statistics files for analysis, monitoring, and operational insights.

## Use Case

**Use Case: Get statistics - Get general statistics**

This playbook addresses the need to:

- Collect comprehensive statistics from the SD-WAN environment
- Gather device status and operational metrics
- Extract system information for monitoring and troubleshooting
- Provide automated statistics collection for regular operational reviews
- Export statistical data for offline analysis and reporting

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
  statistics_dir: "{{ generated_dir }}/statistics"
```

### Directory Structure

The playbook creates the following directory structure:

```
playbook_directory/
├── statistics.yml
└── generated/
    └── statistics/
        ├── device_statistics.json
        ├── control_connections.json
        ├── bfd_sessions.json
        ├── omp_peers.json
        ├── system_info.json
        ├── vsmarts.json
        └── vbonds.json
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

**Purpose:** Creates the output directory for generated statistics files

**What it does:**
- Creates the **statistics** directory under the **generated** folder
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

#### Task 5: Get Device Statistics

**Purpose:** Collects comprehensive device inventory and status information

**API endpoint:** `/dataservice/device`

**What it does:**
- Retrieves complete device inventory from vManage
- Collects device status, reachability, and basic metrics
- Handles API errors gracefully with ignore_errors flag
- Stores results for conditional file saving

#### Task 6: Save Device Statistics

**Purpose:** Saves device statistics to JSON file

**Generated file:** **device_statistics.json**

**What it does:**
- Converts API response to formatted JSON
- Saves file only if API call was successful (HTTP 200)
- Creates readable JSON format for analysis
- Stores in the statistics subdirectory

#### Task 7: Get Control Connections Statistics

**Purpose:** Collects control plane connectivity information

**API endpoint:** `/dataservice/device/control/connections`

**What it does:**
- Retrieves control connection status between devices
- Gathers control plane topology information
- Handles potential API errors without stopping execution
- Provides insights into control plane health

#### Task 8: Save Control Connections Statistics

**Purpose:** Saves control connections data to JSON file

**Generated file:** **control_connections.json**

**What it does:**
- Saves control plane connectivity data
- Only creates file if API call succeeded
- Provides formatted JSON for analysis
- Enables control plane troubleshooting

#### Task 9: Get BFD Sessions Statistics

**Purpose:** Collects Bidirectional Forwarding Detection session information

**API endpoint:** `/dataservice/device/bfd/sessions`

**What it does:**
- Retrieves BFD session status and metrics
- Gathers fast failure detection information
- Provides network convergence insights
- Handles API availability gracefully

#### Task 10: Save BFD Sessions Statistics

**Purpose:** Saves BFD session data to JSON file

**Generated file:** **bfd_sessions.json**

**What it does:**
- Stores BFD session statistics
- Enables network health monitoring
- Provides failure detection metrics
- Supports troubleshooting activities

#### Task 11: Get OMP Peers Statistics

**Purpose:** Collects Overlay Management Protocol peer information

**API endpoint:** `/dataservice/device/omp/peers`

**What it does:**
- Retrieves OMP peer relationships
- Gathers overlay network topology data
- Collects route advertisement information
- Provides control plane peer status

#### Task 12: Save OMP Peers Statistics

**Purpose:** Saves OMP peer data to JSON file

**Generated file:** **omp_peers.json**

**What it does:**
- Stores OMP peer relationship data
- Enables overlay network analysis
- Supports routing troubleshooting
- Provides peer connectivity insights

#### Task 13: Get System Information

**Purpose:** Collects vEdge system details and metrics

**API endpoint:** `/dataservice/system/device/vedges`

**What it does:**
- Retrieves comprehensive vEdge system information
- Gathers hardware and software details
- Collects performance metrics
- Provides system health indicators

#### Task 14: Save System Information

**Purpose:** Saves system information to JSON file

**Generated file:** **system_info.json**

**What it does:**
- Stores detailed system metrics
- Enables system health monitoring
- Provides hardware inventory data
- Supports capacity planning activities

#### Task 15: Get vSmart Controllers Statistics

**Purpose:** Collects control plane component statistics

**API endpoint:** `/dataservice/system/device/vsmarts`

**What it does:**
- Retrieves vSmart controller information
- Gathers control plane component status
- Collects controller performance metrics
- Provides control plane health data

#### Task 16: Save vSmart Controllers Statistics

**Purpose:** Saves vSmart statistics to JSON file

**Generated file:** **vsmarts.json**

**What it does:**
- Stores vSmart controller metrics
- Enables control plane monitoring
- Provides component health insights
- Supports infrastructure analysis

#### Task 17: Get vBond Orchestrators Statistics

**Purpose:** Collects orchestration component statistics

**API endpoint:** `/dataservice/system/device/vbonds`

**What it does:**
- Retrieves vBond orchestrator information
- Gathers orchestration component status
- Collects orchestrator performance metrics
- Provides orchestration health data

#### Task 18: Save vBond Orchestrators Statistics

**Purpose:** Saves vBond statistics to JSON file

**Generated file:** **vbonds.json**

**What it does:**
- Stores vBond orchestrator metrics
- Enables orchestration monitoring
- Provides component health insights
- Supports infrastructure analysis

#### Task 19: Completion Notification

**Purpose:** Provides execution status and file location

**What it displays:**
- Full path to the generated statistics directory
- Success confirmation message
- Location reference for users

## Report Contents

The generated statistics files typically include:

- **Device Statistics:** Complete device inventory, status, reachability, and basic performance metrics
- **Control Connections:** Control plane connectivity status, tunnel information, and topology data
- **BFD Sessions:** Bidirectional Forwarding Detection session status, timers, and failure detection metrics
- **OMP Peers:** Overlay Management Protocol peer relationships, route advertisements, and overlay topology
- **System Information:** vEdge system details, hardware specifications, software versions, and performance metrics
- **vSmart Controllers:** Control plane component status, resource utilization, and policy distribution metrics
- **vBond Orchestrators:** Orchestration component status, device onboarding metrics, and certificate management data