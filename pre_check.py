#!/usr/bin/env python3
"""
SD-WAN Automation Pre-Check Script
==================================

This script validates that all requirements are met before running
SD-WAN automation playbooks. It checks:
- Environment variables
- Network connectivity
- Required tools
- Directory structure
- Permissions

Author: SD-WAN Automation Team
Version: 1.0
"""

import os
import sys
import subprocess
import socket
import requests
from urllib3.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
import platform

# Suppress SSL warnings for internal certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Colors:
    """Color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SDWANPreCheck:
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'details': []
        }
        self.required_env_vars = [
            'VMANAGE_HOST',
            'VMANAGE_USERNAME', 
            'VMANAGE_PASSWORD'
        ]
        self.optional_env_vars = [
            'VMANAGE_PORT'
        ]
        self.required_tools = [
            'ansible-playbook',
            'sastre',
            'python3'
        ]

    def print_header(self):
        """Print script header"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("           SD-WAN AUTOMATION PRE-CHECK")
        print("=" * 60)
        print(f"{Colors.END}")
        print(f"{Colors.WHITE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"{Colors.END}\n")

    def check_status(self, test_name, status, message="", warning=False):
        """Print check status and update results"""
        if status:
            if warning:
                print(f"{Colors.YELLOW}⚠  WARNING{Colors.END} - {test_name}: {message}")
                self.results['warnings'] += 1
                self.results['details'].append(f"WARNING: {test_name} - {message}")
            else:
                print(f"{Colors.GREEN}✓  PASS{Colors.END} - {test_name}: {message}")
                self.results['passed'] += 1
                self.results['details'].append(f"PASS: {test_name} - {message}")
        else:
            print(f"{Colors.RED}✗  FAIL{Colors.END} - {test_name}: {message}")
            self.results['failed'] += 1
            self.results['details'].append(f"FAIL: {test_name} - {message}")

    def check_python_version(self):
        """Check Python version compatibility"""
        print(f"{Colors.BLUE}Checking Python Version...{Colors.END}")
        
        version_info = sys.version_info
        if version_info.major >= 3 and version_info.minor >= 6:
            self.check_status(
                "Python Version", 
                True, 
                f"Python {version_info.major}.{version_info.minor}.{version_info.micro} (Compatible)"
            )
        else:
            self.check_status(
                "Python Version", 
                False, 
                f"Python {version_info.major}.{version_info.minor} (Requires Python 3.6+)"
            )

    def check_environment_variables(self):
        """Check required environment variables"""
        print(f"\n{Colors.BLUE}Checking Environment Variables...{Colors.END}")
        
        # Check required variables
        for var in self.required_env_vars:
            value = os.environ.get(var)
            if value:
                # Mask password in output
                display_value = "***PROTECTED***" if "PASSWORD" in var else value
                self.check_status(
                    f"Environment Variable: {var}", 
                    True, 
                    f"Set to: {display_value}"
                )
            else:
                self.check_status(
                    f"Environment Variable: {var}", 
                    False, 
                    "Not set - Required for authentication"
                )
        
        # Check optional variables
        for var in self.optional_env_vars:
            value = os.environ.get(var)
            if value:
                self.check_status(
                    f"Optional Variable: {var}", 
                    True, 
                    f"Set to: {value}",
                    warning=False
                )
            else:
                self.check_status(
                    f"Optional Variable: {var}", 
                    True, 
                    "Not set - Will use default (443)",
                    warning=True
                )

    def check_required_tools(self):
        """Check if required command-line tools are available"""
        print(f"\n{Colors.BLUE}Checking Required Tools...{Colors.END}")
        
        for tool in self.required_tools:
            try:
                # Try to run the tool with --version or --help
                if tool == 'sastre':
                    result = subprocess.run([tool, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                elif tool == 'ansible-playbook':
                    result = subprocess.run([tool, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                else:
                    result = subprocess.run([tool, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    # Extract version info from output
                    version_line = result.stdout.split('\n')[0] if result.stdout else "Version info not available"
                    self.check_status(
                        f"Tool: {tool}", 
                        True, 
                        version_line[:50] + "..." if len(version_line) > 50 else version_line
                    )
                else:
                    self.check_status(
                        f"Tool: {tool}", 
                        False, 
                        f"Tool found but returned error code {result.returncode}"
                    )
            except subprocess.TimeoutExpired:
                self.check_status(
                    f"Tool: {tool}", 
                    False, 
                    "Tool timed out (may be installed but not responding)"
                )
            except FileNotFoundError:
                self.check_status(
                    f"Tool: {tool}", 
                    False, 
                    "Tool not found - Please install"
                )
            except Exception as e:
                self.check_status(
                    f"Tool: {tool}", 
                    False, 
                    f"Error checking tool: {str(e)}"
                )

    def check_network_connectivity(self):
        """Check network connectivity to vManage"""
        print(f"\n{Colors.BLUE}Checking Network Connectivity...{Colors.END}")
        
        vmanage_host = os.environ.get('VMANAGE_HOST')
        vmanage_port = os.environ.get('VMANAGE_PORT', '443')
        
        if not vmanage_host:
            self.check_status(
                "Network Connectivity", 
                False, 
                "Cannot test - VMANAGE_HOST not set"
            )
            return
        
        # Basic hostname resolution
        try:
            socket.gethostbyname(vmanage_host)
            self.check_status(
                "DNS Resolution", 
                True, 
                f"Successfully resolved {vmanage_host}"
            )
        except socket.gaierror as e:
            self.check_status(
                "DNS Resolution", 
                False, 
                f"Cannot resolve {vmanage_host}: {str(e)}"
            )
            return
        
        # Port connectivity
        try:
            sock = socket.create_connection((vmanage_host, int(vmanage_port)), timeout=10)
            sock.close()
            self.check_status(
                "Port Connectivity", 
                True, 
                f"Can connect to {vmanage_host}:{vmanage_port}"
            )
        except Exception as e:
            self.check_status(
                "Port Connectivity", 
                False, 
                f"Cannot connect to {vmanage_host}:{vmanage_port} - {str(e)}"
            )
            return

    def check_vmanage_api(self):
        """Check vManage API accessibility"""
        print(f"\n{Colors.BLUE}Checking vManage API Access...{Colors.END}")
        
        vmanage_host = os.environ.get('VMANAGE_HOST')
        vmanage_port = os.environ.get('VMANAGE_PORT', '443')
        vmanage_username = os.environ.get('VMANAGE_USERNAME')
        vmanage_password = os.environ.get('VMANAGE_PASSWORD')
        
        if not all([vmanage_host, vmanage_username, vmanage_password]):
            self.check_status(
                "vManage API Access", 
                False, 
                "Cannot test - Missing required environment variables"
            )
            return
        
        try:
            # Test API endpoint
            url = f"https://{vmanage_host}:{vmanage_port}/dataservice/system/device/controllers"
            
            response = requests.get(
                url,
                auth=(vmanage_username, vmanage_password),
                verify=False,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    device_count = len(data.get('data', []))
                    self.check_status(
                        "vManage API Access", 
                        True, 
                        f"Successfully authenticated - Found {device_count} controllers"
                    )
                except json.JSONDecodeError:
                    self.check_status(
                        "vManage API Access", 
                        True, 
                        "Authentication successful but response not JSON",
                        warning=True
                    )
            elif response.status_code == 401:
                self.check_status(
                    "vManage API Access", 
                    False, 
                    "Authentication failed - Check username/password"
                )
            elif response.status_code == 403:
                self.check_status(
                    "vManage API Access", 
                    False, 
                    "Access forbidden - Check user permissions"
                )
            else:
                self.check_status(
                    "vManage API Access", 
                    False, 
                    f"API returned status code {response.status_code}"
                )
                
        except requests.exceptions.SSLError:
            self.check_status(
                "vManage API Access", 
                False, 
                "SSL Certificate error - Check vManage certificate"
            )
        except requests.exceptions.ConnectTimeout:
            self.check_status(
                "vManage API Access", 
                False, 
                "Connection timeout - Check network connectivity"
            )
        except requests.exceptions.ConnectionError as e:
            self.check_status(
                "vManage API Access", 
                False, 
                f"Connection error: {str(e)}"
            )
        except Exception as e:
            self.check_status(
                "vManage API Access", 
                False, 
                f"Unexpected error: {str(e)}"
            )

    def check_directory_structure(self):
        """Check and create required directory structure"""
        print(f"\n{Colors.BLUE}Checking Directory Structure...{Colors.END}")
        
        current_dir = os.getcwd()
        required_dirs = [
            'backups',
            'lists', 
            'reports',
            'logs'
        ]
        
        for dir_name in required_dirs:
            dir_path = os.path.join(current_dir, dir_name)
            if os.path.exists(dir_path):
                if os.access(dir_path, os.W_OK):
                    self.check_status(
                        f"Directory: {dir_name}", 
                        True, 
                        "Exists and writable"
                    )
                else:
                    self.check_status(
                        f"Directory: {dir_name}", 
                        False, 
                        "Exists but not writable"
                    )
            else:
                try:
                    os.makedirs(dir_path)
                    self.check_status(
                        f"Directory: {dir_name}", 
                        True, 
                        "Created successfully"
                    )
                except Exception as e:
                    self.check_status(
                        f"Directory: {dir_name}", 
                        False, 
                        f"Failed to create: {str(e)}"
                    )

    def check_playbook_files(self):
        """Check if playbook files exist"""
        print(f"\n{Colors.BLUE}Checking Playbook Files...{Colors.END}")
        
        playbook_files = [
            'usecase1.yml',
            'sdwan_list_config.yml'
        ]
        
        current_dir = os.getcwd()
        
        for playbook in playbook_files:
            # Check in current directory first
            if os.path.exists(playbook):
                self.check_status(
                    f"Playbook: {playbook}", 
                    True, 
                    f"Found in {current_dir}"
                )
            else:
                # Check in subdirectories
                found = False
                for root, dirs, files in os.walk(current_dir):
                    if playbook in files:
                        rel_path = os.path.relpath(root, current_dir)
                        self.check_status(
                            f"Playbook: {playbook}", 
                            True, 
                            f"Found in {rel_path}/",
                            warning=True
                        )
                        found = True
                        break
                
                if not found:
                    self.check_status(
                        f"Playbook: {playbook}", 
                        False, 
                        "Not found in project directory"
                    )

    def print_summary(self):
        """Print final summary"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("                    SUMMARY")
        print("=" * 60)
        print(f"{Colors.END}")
        
        total_checks = self.results['passed'] + self.results['failed'] + self.results['warnings']
        
        print(f"{Colors.GREEN}✓  Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}✗  Failed: {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}⚠  Warnings: {self.results['warnings']}{Colors.END}")
        print(f"{Colors.WHITE}📊 Total Checks: {total_checks}{Colors.END}")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CRITICAL CHECKS PASSED!{Colors.END}")
            print(f"{Colors.GREEN}Your environment is ready for SD-WAN automation!{Colors.END}")
            if self.results['warnings'] > 0:
                print(f"{Colors.YELLOW}Note: {self.results['warnings']} warning(s) detected. Review above for details.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ CRITICAL ISSUES DETECTED!{Colors.END}")
            print(f"{Colors.RED}Please resolve the {self.results['failed']} failed check(s) before proceeding.{Colors.END}")
        
        # Save results to file
        self.save_results()

    def save_results(self):
        """Save results to a log file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f"precheck_results_{timestamp}.txt"
            
            with open(log_file, 'w') as f:
                f.write("SD-WAN Automation Pre-Check Results\n")
                f.write("=" * 40 + "\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Platform: {platform.system()} {platform.release()}\n")
                f.write(f"Python: {sys.version.split()[0]}\n\n")
                
                f.write("Summary:\n")
                f.write(f"- Passed: {self.results['passed']}\n")
                f.write(f"- Failed: {self.results['failed']}\n")
                f.write(f"- Warnings: {self.results['warnings']}\n\n")
                
                f.write("Detailed Results:\n")
                for detail in self.results['details']:
                    f.write(f"- {detail}\n")
            
            print(f"\n{Colors.CYAN}📄 Results saved to: {log_file}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}⚠  Could not save results: {str(e)}{Colors.END}")

    def run_all_checks(self):
        """Run all pre-checks"""
        self.print_header()
        
        # Run all checks
        self.check_python_version()
        self.check_environment_variables()
        self.check_required_tools()
        self.check_directory_structure()
        self.check_playbook_files()
        self.check_network_connectivity()
        self.check_vmanage_api()
        
        # Print summary
        self.print_summary()
        
        # Return exit code
        return 0 if self.results['failed'] == 0 else 1

def main():
    """Main function"""
    try:
        checker = SDWANPreCheck()
        exit_code = checker.run_all_checks()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Pre-check interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()