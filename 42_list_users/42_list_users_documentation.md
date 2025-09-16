# List Users Playbook Documentation

## Overview

The List Users playbook is an Ansible automation script designed to retrieve comprehensive user management information from Cisco SD-WAN vManage controllers. This playbook collects data from multiple API endpoints to provide a complete view of user accounts, roles, and permissions within the SD-WAN infrastructure.

## Detailed Task Analysis

### Task 1: Environment Variable Validation

**- name: Validate environment variables are set**

**Purpose:** Ensures all required credentials are available before proceeding

**What it does:**
- Checks that vmanage_host, vmanage_username, vmanage_password, and vmanage_port are set
- Fails the playbook immediately if any critical environment variables are missing
- Prevents failed execution attempts due to missing credentials

### Task 2: Directory Structure Creation

**- name: Create users directory**

**Purpose:** Creates the organized directory hierarchy needed for user data storage

**Generated folder:**
- {{ users_dir }} - User information data storage in generated/users/

**Directory structure example:**
```
generated/
└── users/
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

### Task 5: Get All Users

**- name: Get all users**

**Purpose:** Retrieves comprehensive list of all user accounts

**API Endpoint:** `/dataservice/admin/user`

**Generated content:** Complete user information including usernames, roles, permissions, status, and account details

### Task 6: Get User Groups

**- name: Get user groups**

**Purpose:** Collects user groups and role definitions

**API Endpoint:** `/dataservice/admin/usergroup`

**Generated content:** User group configurations, role assignments, and permission mappings for access control management

### Task 7: Save Users List

**- name: Save users list to file**

**Purpose:** Persists user account data to JSON file

**Generated file:** users_list.json in the users directory

### Task 8: Save User Groups

**- name: Save user groups to file**

**Purpose:** Stores user group and role information in JSON format

**Generated file:** user_groups.json in the users directory

### Task 9: Create Users Collection Summary

**- name: Create users collection summary**

**Purpose:** Generates a comprehensive summary report of the user data collection process

**Generated file:** collection_summary.txt in the users directory

## Generated Report Content

### Users Information Collection Summary

**Collection Date:** [ISO 8601 timestamp]
**vManage Host:** [vManage controller hostname/IP]
**Username:** [Authentication username]

**Successfully Retrieved User Information:**
- Users List: SUCCESS
- User Groups: SUCCESS

**Files Generated:**
- users_list.json
- user_groups.json

**Total Users Found:** [Number of user accounts]
**Total User Groups:** [Number of user groups/roles]

**Status:** All endpoints completed successfully with no errors.

The report provides a complete overview of the user management data collection process, confirming successful retrieval from all API endpoints and providing counts of users and groups for administrative reference and security auditing purposes.