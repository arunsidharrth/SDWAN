#!/usr/bin/env python3
"""
SD-WAN Automation Post-Check Script
===================================

This script validates the results after running SD-WAN automation playbooks.
It checks:
- Backup completeness and integrity
- File sizes and counts
- Configuration item statistics
- Error detection and reporting
- Success metrics and recommendations

Author: SD-WAN Automation Team
Version: 1.0
"""

import os
import sys
import json
import tarfile
import glob
from datetime import datetime, timedelta
import platform
import re
import hashlib
from pathlib import Path
import argparse

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

class SDWANPostCheck:
    def __init__(self, operation_type="backup"):
        self.operation_type = operation_type.lower()
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'details': [],
            'metrics': {},
            'recommendations': []
        }
        self.base_dirs = {
            'backup': ['backups'],
            'list': ['lists'],
            'both': ['backups', 'lists']
        }
        
    def print_header(self):
        """Print script header"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("           SD-WAN AUTOMATION POST-CHECK")
        print(f"           Operation: {self.operation_type.upper()}")
        print("=" * 60)
        print(f"{Colors.END}")
        print(f"{Colors.WHITE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Working Directory: {os.getcwd()}")
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

    def format_file_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None

    def find_latest_operation_dir(self):
        """Find the most recent operation directory"""
        search_dirs = self.base_dirs.get(self.operation_type, self.base_dirs['both'])
        
        latest_dir = None
        latest_time = None
        
        for base_dir in search_dirs:
            if os.path.exists(base_dir):
                # Look for date-based subdirectories
                for item in os.listdir(base_dir):
                    item_path = os.path.join(base_dir, item)
                    if os.path.isdir(item_path):
                        try:
                            # Try to parse as date (YYYY-MM-DD format)
                            dir_date = datetime.strptime(item, '%Y-%m-%d')
                            if latest_time is None or dir_date > latest_time:
                                latest_time = dir_date
                                latest_dir = item_path
                        except ValueError:
                            # Not a date directory, skip
                            continue
        
        return latest_dir

    def check_backup_completion(self, backup_dir):
        """Check if backup completed successfully"""
        print(f"{Colors.BLUE}Checking Backup Completion...{Colors.END}")
        
        if not backup_dir or not os.path.exists(backup_dir):
            self.check_status(
                "Backup Directory", 
                False, 
                f"Backup directory not found: {backup_dir}"
            )
            return False
            
        # Check for data directory
        data_dirs = glob.glob(os.path.join(backup_dir, "data", "*"))
        if not data_dirs:
            self.check_status(
                "Backup Data", 
                False, 
                "No backup data directories found"
            )
            return False
            
        backup_data_dir = data_dirs[0]  # Get the most recent
        
        # Check for essential backup files
        essential_files = [
            'device_template.json',
            'feature_template.json', 
            'policy_definition.json',
            'policy_list.json'
        ]
        
        missing_files = []
        present_files = []
        
        for filename in essential_files:
            filepath = os.path.join(backup_data_dir, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                if file_size > 0:
                    present_files.append(f"{filename} ({self.format_file_size(file_size)})")
                else:
                    missing_files.append(f"{filename} (empty)")
            else:
                missing_files.append(f"{filename} (not found)")
        
        if missing_files:
            self.check_status(
                "Essential Backup Files", 
                len(present_files) > len(missing_files), 
                f"Missing: {', '.join(missing_files[:3])}{'...' if len(missing_files) > 3 else ''}",
                warning=True if present_files else False
            )
        else:
            self.check_status(
                "Essential Backup Files", 
                True, 
                f"All essential files present ({len(present_files)} files)"
            )
        
        # Check for compressed archive
        archives_dir = os.path.join(backup_dir, "archives")
        if os.path.exists(archives_dir):
            archives = glob.glob(os.path.join(archives_dir, "*.tar.gz"))
            if archives:
                archive_file = archives[0]
                archive_size = os.path.getsize(archive_file)
                self.check_status(
                    "Backup Archive", 
                    True, 
                    f"Created successfully ({self.format_file_size(archive_size)})"
                )
                self.results['metrics']['archive_size'] = archive_size
                self.results['metrics']['archive_path'] = archive_file
            else:
                self.check_status(
                    "Backup Archive", 
                    False, 
                    "No compressed archive found"
                )
        
        return len(present_files) > 0

    def check_list_completion(self, list_dir):
        """Check if configuration listing completed successfully"""
        print(f"{Colors.BLUE}Checking Configuration List Completion...{Colors.END}")
        
        if not list_dir or not os.path.exists(list_dir):
            self.check_status(
                "List Directory", 
                False, 
                f"List directory not found: {list_dir}"
            )
            return False
        
        # Check for data directory
        data_dir = os.path.join(list_dir, "data")
        if not os.path.exists(data_dir):
            self.check_status(
                "List Data Directory", 
                False, 
                "Data directory not found"
            )
            return False
        
        # Check for individual configuration type files
        config_types = [
            'device_template', 'feature_template', 'policy_definition',
            'policy_list', 'configuration_group'
        ]
        
        present_lists = []
        missing_lists = []
        
        for config_type in config_types:
            list_files = glob.glob(os.path.join(data_dir, f"{config_type}_list_*.txt"))
            if list_files:
                file_size = os.path.getsize(list_files[0])
                present_lists.append(f"{config_type} ({self.format_file_size(file_size)})")
            else:
                missing_lists.append(config_type)
        
        if missing_lists:
            self.check_status(
                "Configuration List Files", 
                len(present_lists) > 0,
                f"Missing: {', '.join(missing_lists[:3])}{'...' if len(missing_lists) > 3 else ''}",
                warning=True
            )
        else:
            self.check_status(
                "Configuration List Files", 
                True, 
                f"All configuration types listed ({len(present_lists)} types)"
            )
        
        # Check for consolidated inventory
        consolidated_files = glob.glob(os.path.join(data_dir, "consolidated_inventory_*.txt"))
        if consolidated_files:
            file_size = os.path.getsize(consolidated_files[0])
            self.check_status(
                "Consolidated Inventory", 
                True, 
                f"Created successfully ({self.format_file_size(file_size)})"
            )
        else:
            self.check_status(
                "Consolidated Inventory", 
                False, 
                "Consolidated inventory file not found"
            )
        
        return len(present_lists) > 0

    def analyze_backup_statistics(self, backup_dir):
        """Analyze backup statistics from reports"""
        print(f"\n{Colors.BLUE}Analyzing Backup Statistics...{Colors.END}")
        
        reports_dir = os.path.join(backup_dir, "reports")
        if not os.path.exists(reports_dir):
            self.check_status(
                "Backup Statistics", 
                False, 
                "Reports directory not found"
            )
            return
        
        # Find summary report
        summary_files = glob.glob(os.path.join(reports_dir, "backup_summary_*.txt"))
        if not summary_files:
            self.check_status(
                "Backup Statistics", 
                False, 
                "Summary report not found"
            )
            return
        
        summary_file = summary_files[0]
        
        try:
            with open(summary_file, 'r') as f:
                content = f.read()
            
            # Extract statistics using regex
            stats = {}
            patterns = {
                'device_templates': r'Device Templates:\s*(\d+)',
                'feature_templates': r'Feature Templates:\s*(\d+)',
                'policy_definitions': r'Policy Definitions:\s*(\d+)',
                'policy_lists': r'Policy Lists:\s*(\d+)',
                'config_groups': r'Configuration Groups:\s*(\d+)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    stats[key] = int(match.group(1))
                else:
                    stats[key] = 0
            
            # Calculate totals
            total_items = sum(stats.values())
            self.results['metrics']['backup_stats'] = stats
            self.results['metrics']['total_items'] = total_items
            
            if total_items > 0:
                self.check_status(
                    "Backup Statistics", 
                    True, 
                    f"Total items backed up: {total_items}"
                )
                
                # Detailed breakdown
                print(f"  {Colors.CYAN}Breakdown:{Colors.END}")
                for item_type, count in stats.items():
                    if count > 0:
                        print(f"    - {item_type.replace('_', '').title()}: {count}")
            else:
                self.check_status(
                    "Backup Statistics", 
                    False, 
                    "No configuration items found in backup"
                )
                
        except Exception as e:
            self.check_status(
                "Backup Statistics", 
                False, 
                f"Error reading summary report: {str(e)}"
            )

    def check_file_integrity(self, operation_dir):
        """Check file integrity and detect corruption"""
        print(f"\n{Colors.BLUE}Checking File Integrity...{Colors.END}")
        
        corrupted_files = []
        checked_files = 0
        total_size = 0
        
        # Check all files in the operation directory
        for root, dirs, files in os.walk(operation_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(filepath)
                    total_size += file_size
                    checked_files += 1
                    
                    # Check if file can be opened and read
                    with open(filepath, 'rb') as f:
                        # Try to read first and last 1KB to detect truncation
                        f.read(1024)
                        if file_size > 2048:
                            f.seek(-1024, 2)
                            f.read(1024)
                            
                except Exception as e:
                    corrupted_files.append(f"{os.path.basename(filepath)}: {str(e)}")
        
        self.results['metrics']['total_files'] = checked_files
        self.results['metrics']['total_size'] = total_size
        
        if corrupted_files:
            self.check_status(
                "File Integrity", 
                False, 
                f"{len(corrupted_files)} corrupted files detected"
            )
            for corrupted in corrupted_files[:3]:  # Show first 3
                print(f"    {Colors.RED}• {corrupted}{Colors.END}")
        else:
            self.check_status(
                "File Integrity", 
                True, 
                f"All {checked_files} files passed integrity check ({self.format_file_size(total_size)})"
            )

    def check_archive_integrity(self, backup_dir):
        """Check backup archive integrity"""
        print(f"\n{Colors.BLUE}Checking Archive Integrity...{Colors.END}")
        
        archives_dir = os.path.join(backup_dir, "archives")
        if not os.path.exists(archives_dir):
            self.check_status(
                "Archive Integrity", 
                False, 
                "Archives directory not found"
            )
            return
        
        archives = glob.glob(os.path.join(archives_dir, "*.tar.gz"))
        if not archives:
            self.check_status(
                "Archive Integrity", 
                False, 
                "No archive files found"
            )
            return
        
        archive_file = archives[0]
        
        try:
            # Test archive integrity
            with tarfile.open(archive_file, 'r:gz') as tar:
                members = tar.getmembers()
                file_count = len([m for m in members if m.isfile()])
                
                # Try to extract a few files to test
                test_members = members[:min(5, len(members))]
                for member in test_members:
                    if member.isfile():
                        tar.extractfile(member).read(1024)  # Read first 1KB
                
            self.check_status(
                "Archive Integrity", 
                True, 
                f"Archive is valid ({file_count} files, {self.format_file_size(os.path.getsize(archive_file))})"
            )
            self.results['metrics']['archive_files'] = file_count
            
        except Exception as e:
            self.check_status(
                "Archive Integrity", 
                False, 
                f"Archive corruption detected: {str(e)}"
            )

    def check_operation_timing(self, operation_dir):
        """Analyze operation timing and performance"""
        print(f"\n{Colors.BLUE}Analyzing Operation Performance...{Colors.END}")
        
        # Get directory creation time as start time approximation
        try:
            dir_stat = os.stat(operation_dir)
            start_time = datetime.fromtimestamp(dir_stat.st_ctime)
            
            # Find the newest file as end time approximation
            newest_time = start_time
            for root, dirs, files in os.walk(operation_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if file_time > newest_time:
                        newest_time = file_time
            
            duration = newest_time - start_time
            duration_minutes = duration.total_seconds() / 60
            
            self.results['metrics']['start_time'] = start_time.isoformat()
            self.results['metrics']['end_time'] = newest_time.isoformat() 
            self.results['metrics']['duration_minutes'] = duration_minutes
            
            # Performance assessment
            if duration_minutes < 5:
                performance = "Excellent"
                color = Colors.GREEN
            elif duration_minutes < 15:
                performance = "Good"
                color = Colors.GREEN
            elif duration_minutes < 30:
                performance = "Acceptable"
                color = Colors.YELLOW
            else:
                performance = "Slow"
                color = Colors.YELLOW
            
            self.check_status(
                "Operation Performance", 
                True, 
                f"Duration: {duration_minutes:.1f} minutes ({performance})"
            )
            
            # Add recommendation if slow
            if duration_minutes > 30:
                self.results['recommendations'].append(
                    "Operation took longer than expected. Consider checking network connectivity or vManage performance."
                )
                
        except Exception as e:
            self.check_status(
                "Operation Performance", 
                False, 
                f"Could not analyze timing: {str(e)}"
            )

    def generate_recommendations(self):
        """Generate recommendations based on results"""
        print(f"\n{Colors.BLUE}Generating Recommendations...{Colors.END}")
        
        # Size-based recommendations
        total_size = self.results['metrics'].get('total_size', 0)
        if total_size > 0:
            if total_size < 1024 * 1024:  # Less than 1MB
                self.results['recommendations'].append(
                    "⚠️  Backup size is very small. Verify all configurations were captured."
                )
            elif total_size > 1024 * 1024 * 1024:  # Greater than 1GB  
                self.results['recommendations'].append(
                    "💾 Large backup detected. Consider implementing backup rotation to manage disk space."
                )
        
        # File count recommendations
        total_files = self.results['metrics'].get('total_files', 0)
        if total_files < 5:
            self.results['recommendations'].append(
                "📁 Few files detected. Ensure backup completed successfully."
            )
        
        # Statistics-based recommendations
        backup_stats = self.results['metrics'].get('backup_stats', {})
        if backup_stats:
            total_items = sum(backup_stats.values())
            if total_items == 0:
                self.results['recommendations'].append(
                    "❌ No configuration items found. Check vManage connectivity and permissions."
                )
            elif total_items < 10:
                self.results['recommendations'].append(
                    "🔍 Very few configuration items found. Verify this is expected for your environment."
                )
        
        # Performance recommendations
        duration = self.results['metrics'].get('duration_minutes', 0)
        if duration > 30:
            self.results['recommendations'].append(
                "🚀 Consider optimizing network connection or running during off-peak hours."
            )
        
        # Archive recommendations
        if 'archive_size' in self.results['metrics']:
            self.results['recommendations'].append(
                "✅ Consider implementing automated backup verification and off-site storage."
            )
        
        # General recommendations
        if self.results['failed'] == 0 and self.results['warnings'] == 0:
            self.results['recommendations'].append(
                "🎉 Perfect execution! Consider scheduling this as a regular automated task."
            )

    def create_detailed_report(self, operation_dir):
        """Create a detailed post-check report"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f"postcheck_report_{self.operation_type}_{timestamp}.json"
            
            report_data = {
                'metadata': {
                    'operation_type': self.operation_type,
                    'timestamp': datetime.now().isoformat(),
                    'operation_directory': operation_dir,
                    'platform': f"{platform.system()} {platform.release()}",
                    'python_version': sys.version.split()[0]
                },
                'summary': {
                    'total_checks': self.results['passed'] + self.results['failed'] + self.results['warnings'],
                    'passed': self.results['passed'],
                    'failed': self.results['failed'],
                    'warnings': self.results['warnings'],
                    'success_rate': round((self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100), 2) if (self.results['passed'] + self.results['failed']) > 0 else 0
                },
                'metrics': self.results['metrics'],
                'detailed_results': self.results['details'],
                'recommendations': self.results['recommendations']
            }
            
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            print(f"\n{Colors.CYAN}📊 Detailed report saved to: {report_file}{Colors.END}")
            
            # Also create a human-readable text report
            text_report = f"postcheck_summary_{self.operation_type}_{timestamp}.txt"
            with open(text_report, 'w') as f:
                f.write(f"SD-WAN {self.operation_type.title()} Post-Check Summary\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Operation: {self.operation_type.upper()}\n")
                f.write(f"Directory: {operation_dir}\n\n")
                
                f.write("SUMMARY:\n")
                f.write(f"- Total Checks: {report_data['summary']['total_checks']}\n")
                f.write(f"- Passed: {report_data['summary']['passed']}\n")
                f.write(f"- Failed: {report_data['summary']['failed']}\n") 
                f.write(f"- Warnings: {report_data['summary']['warnings']}\n")
                f.write(f"- Success Rate: {report_data['summary']['success_rate']}%\n\n")
                
                if self.results['metrics']:
                    f.write("KEY METRICS:\n")
                    for key, value in self.results['metrics'].items():
                        f.write(f"- {key.replace('_', ' ').title()}: {value}\n")
                    f.write("\n")
                
                if self.results['recommendations']:
                    f.write("RECOMMENDATIONS:\n")
                    for i, rec in enumerate(self.results['recommendations'], 1):
                        f.write(f"{i}. {rec}\n")
                    f.write("\n")
                
                f.write("DETAILED RESULTS:\n")
                for detail in self.results['details']:
                    f.write(f"- {detail}\n")
            
            print(f"{Colors.CYAN}📄 Summary report saved to: {text_report}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}⚠️  Could not save detailed report: {str(e)}{Colors.END}")

    def print_summary(self):
        """Print final summary"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("                    SUMMARY")
        print("=" * 60)
        print(f"{Colors.END}")
        
        total_checks = self.results['passed'] + self.results['failed'] + self.results['warnings']
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100) if (self.results['passed'] + self.results['failed']) > 0 else 0
        
        print(f"{Colors.GREEN}✓  Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}✗  Failed: {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}⚠  Warnings: {self.results['warnings']}{Colors.END}")
        print(f"{Colors.WHITE}📊 Total Checks: {total_checks}{Colors.END}")
        print(f"{Colors.WHITE}🎯 Success Rate: {success_rate:.1f}%{Colors.END}")
        
        # Display key metrics
        if self.results['metrics']:
            print(f"\n{Colors.CYAN}📈 Key Metrics:{Colors.END}")
            metrics_display = {
                'total_size': lambda x: f"Total Size: {self.format_file_size(x)}",
                'total_files': lambda x: f"Total Files: {x}",
                'total_items': lambda x: f"Config Items: {x}",
                'duration_minutes': lambda x: f"Duration: {x:.1f} minutes",
                'archive_files': lambda x: f"Archive Files: {x}"
            }
            
            for key, formatter in metrics_display.items():
                if key in self.results['metrics']:
                    print(f"  • {formatter(self.results['metrics'][key])}")
        
        # Overall status
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 {self.operation_type.upper()} VALIDATION SUCCESSFUL!{Colors.END}")
            print(f"{Colors.GREEN}Your {self.operation_type} operation completed successfully!{Colors.END}")
            if self.results['warnings'] > 0:
                print(f"{Colors.YELLOW}Note: {self.results['warnings']} warning(s) detected. Review recommendations below.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ ISSUES DETECTED IN {self.operation_type.upper()}!{Colors.END}")
            print(f"{Colors.RED}Please review the {self.results['failed']} failed check(s) above.{Colors.END}")
        
        # Show recommendations
        if self.results['recommendations']:
            print(f"\n{Colors.CYAN}{Colors.BOLD}💡 RECOMMENDATIONS:{Colors.END}")
            for i, recommendation in enumerate(self.results['recommendations'], 1):
                print(f"  {i}. {recommendation}")

    def run_all_checks(self, operation_dir=None):
        """Run all post-checks"""
        self.print_header()
        
        # Find operation directory if not provided
        if not operation_dir:
            operation_dir = self.find_latest_operation_dir()
        
        if not operation_dir:
            print(f"{Colors.RED}❌ No recent {self.operation_type} directory found!{Colors.END}")
            print(f"{Colors.YELLOW}Make sure you've run the {self.operation_type} playbook first.{Colors.END}")
            return 1
        
        print(f"{Colors.CYAN}📂 Analyzing: {operation_dir}{Colors.END}\n")
        
        # Run appropriate checks based on operation type
        if self.operation_type in ['backup', 'both']:
            success = self.check_backup_completion(operation_dir)
            if success:
                self.analyze_backup_statistics(operation_dir)
                self.check_archive_integrity(operation_dir)
        
        if self.operation_type in ['list', 'both']:
            self.check_list_completion(operation_dir)
        
        # Common checks for all operations
        self.check_file_integrity(operation_dir)
        self.check_operation_timing(operation_dir)
        self.generate_recommendations()
        
        # Generate reports
        self.create_detailed_report(operation_dir)
        
        # Print summary
        self.print_summary()
        
        # Return exit code
        return 0 if self.results['failed'] == 0 else 1

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='SD-WAN Automation Post-Check Script')
    parser.add_argument('--operation', '-o', 
                       choices=['backup', 'list', 'both'], 
                       default='backup',
                       help='Type of operation to validate (default: backup)')
    parser.add_argument('--directory', '-d', 
                       help='Specific operation directory to check')
    
    try:
        args = parser.parse_args()
        
        checker = SDWANPostCheck(args.operation)
        exit_code = checker.run_all_checks(args.directory)
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Post-check interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()