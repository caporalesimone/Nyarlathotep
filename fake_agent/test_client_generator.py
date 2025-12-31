#!/usr/bin/env python3
"""
Test client generator - Generates fake JSON payloads based on agent_json_schema.json
and pushes them to the backend server.

Uses Faker library to generate realistic test data.
"""

import json
import math
import random
import requests
import time
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

# Configuration
NUM_CLIENTS = 100
MIN_GROUP_RATIO = 0.10  # Min 10% of NUM_CLIENTS
MAX_GROUP_RATIO = 0.50  # Max 50% of NUM_CLIENTS
GROUP_PREFIX = "group"  # Prefix for project/group names
INTERVAL_SECONDS = 10  # Interval used in continuous mode
BACKEND_URL = "http://localhost:8080"
ENDPOINT = "/client_update"


fake = Faker()

# Project names will be generated at runtime per execution
PROJECT_NAMES = []
PROJECT_COUNT = 0


def compute_group_bounds():
    """Return (min_groups, max_groups) based on configured ratios."""
    min_groups = max(1, math.ceil(NUM_CLIENTS * MIN_GROUP_RATIO))
    max_groups = max(min_groups, math.floor(NUM_CLIENTS * MAX_GROUP_RATIO))
    return min_groups, max_groups


def generate_project_names(count):
    """Generate unique project names with fixed 'group-' prefix."""
    names = set()
    while len(names) < count:
        names.add(f"{GROUP_PREFIX}-{fake.word()}")
    return list(names)

# List of Windows OS versions
OS_VERSIONS = ["Windows 10", "Windows 11", "Windows Server 2019", "Windows Server 2022"]


def generate_mac_address():
    """Generate a fake MAC address in format XX-XX-XX-XX-XX-XX"""
    return "-".join([fake.hexify(text="^" * 2).upper() for _ in range(6)])


def generate_ipv4():
    """Generate a fake IPv4 address"""
    return fake.ipv4(private=True)


def generate_network_interfaces(num_interfaces=2):
    """Generate fake network interfaces"""
    interfaces = []
    for i in range(num_interfaces):
        interfaces.append({
            "interface": f"Ethernet {i}",
            "ip_addresses": [generate_ipv4() for _ in range(random.randint(1, 2))],
            "mac": generate_mac_address()
        })
    return interfaces


def generate_users(num_users=2):
    """Generate fake user sessions"""
    users = []
    for _ in range(num_users):
        login_time = fake.date_time_this_year()
        idle_minutes = random.randint(0, 480)
        idle_time = f"{idle_minutes // 60}:{idle_minutes % 60:02d}"
        
        users.append({
            "username": fake.user_name(),
            "session_id": fake.uuid4(),
            "session_name": f"Session_{random.randint(1, 5)}",
            "logged": random.choice([True, False]),
            "status": random.choice(["Active", "Idle", "Disconnected"]),
            "login_time": login_time.strftime("%d/%m/%Y %H:%M"),
            "idle_time": idle_time
        })
    return users


def generate_hardware_info():
    """Generate fake hardware information"""
    return {
        "cpu_usage": round(random.uniform(0, 100), 2),
        "ram_total_MB": random.choice([4096, 8192, 16384, 32768]),
        "ram_used_MB": random.randint(1024, 24576),
        "disk_total_GB": random.choice([256, 512, 1024, 2048]),
        "disk_used_GB": random.randint(50, 1500)
    }


def generate_os_info():
    """Generate fake OS information"""
    uptime_days = random.randint(1, 365)
    uptime_hours = random.randint(0, 23)
    uptime_minutes = random.randint(0, 59)
    
    return {
        "os_name": random.choice(OS_VERSIONS),
        "os_platform": "win32",
        "uptime": f"{uptime_days}d {uptime_hours}h {uptime_minutes}m"
    }


def generate_client_payload(client_num, base_client_name=None):
    """Generate a complete client payload matching agent_json_schema.json
    
    Args:
        client_num: Client number
        base_client_name: If provided, use this as client_name (for persistent clients)
    """
    if base_client_name is None:
        base_client_name = f"workstation-{client_num:03d}-{fake.word()}"
    
    return {
        "client_name": base_client_name,
        "client_sw_version": f"{random.randint(1, 2)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "hostname": f"HOST-{client_num:03d}",
        "json_version": "1.0",
        "local_time": datetime.now().isoformat(),
        "network_name": f"Network-{random.choice(['A', 'B', 'C', 'D'])}",
        "project_name": random.choice(PROJECT_NAMES),
        "hardware": generate_hardware_info(),
        "os": generate_os_info(),
        "net_interfaces": generate_network_interfaces(random.randint(1, 3)),
        "users": generate_users(random.randint(1, 4))
    }


def validate_payload(payload, schema):
    """Validate payload against JSON schema"""
    try:
        # Simple validation: check that all required fields are present
        required = schema.get("required", [])
        for field in required:
            if field not in payload:
                return False, f"Missing required field: {field}"
        return True, "Valid"
    except Exception as e:
        return False, str(e)


def load_schema(schema_path):
    """Load the JSON schema"""
    with open(schema_path, 'r') as f:
        return json.load(f)


def push_payload(payload, dry_run=False):
    """Push payload to backend server"""
    if dry_run:
        print(f"  [DRY RUN] Would push: {payload['client_name']}")
        return True
    
    try:
        response = requests.post(
            f"{BACKEND_URL}{ENDPOINT}",
            json=payload,
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"  ⚠️  Cannot connect to {BACKEND_URL}. Use --dry-run to generate without pushing.")
        return False
    except Exception as e:
        print(f"  ❌ Error pushing {payload['client_name']}: {str(e)}")
        return False


def print_help():
    """Print help message"""
    min_groups, max_groups = compute_group_bounds()
    help_text = f"""
╔════════════════════════════════════════════════════════════════╗
║         Fake Agent Test Client Generator                       ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python test_client_generator.py [OPTIONS]

Options:
    --single          Run once and send all clients (required for single shot)
    --continuous      Continuous mode - send data every {INTERVAL_SECONDS} seconds (Ctrl+C to stop)
    --dry-run         Generate JSON without pushing to backend
    --save-json       Save generated JSON files to generated_test_clients/
    --help            Show this help message

Examples:
    # Single run - send all clients once
    python test_client_generator.py --single

    # Continuous mode - send every 10 seconds
    python test_client_generator.py --continuous

    # Test without backend server
    python test_client_generator.py --dry-run --single

    # Continuous test with file saving
    python test_client_generator.py --continuous --save-json

Configuration (current run):
    NUM_CLIENTS        = {NUM_CLIENTS}
    GROUPS (random)    = between {min_groups} and {max_groups} (10%-50% of clients)
    BACKEND_URL        = {BACKEND_URL}
    ENDPOINT           = {ENDPOINT}
    interval           = {INTERVAL_SECONDS} seconds (continuous mode)

Edit these constants in test_client_generator.py to customize.
"""
    print(help_text)


def main():
    """Main function"""
    import sys
    
    # Check if help is requested or no arguments provided
    if "--help" in sys.argv or len(sys.argv) == 1:
        print_help()
        return
    
    dry_run = "--dry-run" in sys.argv
    save_json = "--save-json" in sys.argv
    continuous = "--continuous" in sys.argv
    single = "--single" in sys.argv
    interval = INTERVAL_SECONDS  # seconds between updates
    
    # If neither --single nor --continuous specified, show error
    if not continuous and not single:
        print("❌ Error: You must specify either --single or --continuous")
        print("\nUse 'python test_client_generator.py --help' for usage information.")
        return
    
    # Load schema
    schema_path = Path(__file__).parent.parent / "agent_json_schema.json"
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        return
    
    print(f"Loading schema from {schema_path}")
    schema = load_schema(schema_path)
    
    print(f"\n{'='*60}")
    print("Test Client Generator")
    print(f"{'='*60}")
    min_groups, max_groups = compute_group_bounds()
    project_count = random.randint(min_groups, max_groups)
    global PROJECT_NAMES, PROJECT_COUNT
    PROJECT_COUNT = project_count
    PROJECT_NAMES = generate_project_names(project_count)
    print(f"Clients: {NUM_CLIENTS}")
    print(f"Groups (projects): {PROJECT_COUNT} (range {min_groups}-{max_groups})")
    print(f"Projects: {PROJECT_NAMES}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Dry run: {dry_run}")
    print(f"Save JSON: {save_json}")
    print(f"Mode: {'Continuous' if continuous else 'Single'}")
    if continuous:
        print(f"Update interval: {interval} seconds")
    print(f"{'='*60}\n")
    
    # Generate initial client names (they will be reused)
    client_names = [f"workstation-{i:03d}-{fake.word()}" for i in range(1, NUM_CLIENTS + 1)]
    
    # Assign projects to clients with random distribution (each group has at least one)
    client_projects = {}
    shuffled_clients = client_names.copy()
    random.shuffle(shuffled_clients)
    # Ensure each project gets one client
    for project in PROJECT_NAMES:
        if shuffled_clients:
            client_projects[shuffled_clients.pop()] = project
    # Distribute remaining clients randomly among projects
    for client in shuffled_clients:
        client_projects[client] = random.choice(PROJECT_NAMES)
    
    output_dir = Path(__file__).parent / "generated_test_clients"
    if save_json:
        output_dir.mkdir(exist_ok=True)
    
    iteration = 0
    
    # Continuous mode: keep sending updates every `interval` seconds
    if continuous:
        print(f"Starting continuous mode. Press Ctrl+C to stop.\n")
        try:
            while True:
                iteration += 1
                successful = 0
                failed = 0
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Iteration {iteration} - Sending {NUM_CLIENTS} clients...")
                
                for i, client_name in enumerate(client_names, 1):
                    payload = generate_client_payload(i + 1, base_client_name=client_name)
                    # Assign the pre-determined project
                    payload["project_name"] = client_projects[client_name]
                    
                    valid, msg = validate_payload(payload, schema)
                    
                    if not valid:
                        print(f"  ❌ Client {i}: {msg}")
                        failed += 1
                        continue
                    
                    # Push to server or just show info
                    if push_payload(payload, dry_run):
                        print(f"  ✅ {client_name} ({payload['project_name']})")
                        successful += 1
                        
                        # Save JSON if requested
                        if save_json:
                            output_file = output_dir / f"client_{i:03d}_{client_name}.json"
                            with open(output_file, 'w') as f:
                                json.dump(payload, f, indent=2)
                    else:
                        failed += 1
                
                print(f"  Results: {successful}/{NUM_CLIENTS} successful\n")
                print(f"  Waiting {interval} seconds until next update...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n\nStopped by user.")
            return
    # Single run mode
    else:
        successful = 0
        failed = 0
        
        for i, client_name in enumerate(client_names, 1):
            payload = generate_client_payload(i, base_client_name=client_name)
            # Assign the pre-determined project
            payload["project_name"] = client_projects[client_name]
            
            valid, msg = validate_payload(payload, schema)
            
            if not valid:
                print(f"❌ Client {i}: {msg}")
                failed += 1
                continue
            
            # Push to server or just show info
            if push_payload(payload, dry_run):
                print(f"✅ Client {i:2d}: {payload['client_name']} ({payload['project_name']})")
                successful += 1
                
                # Save JSON if requested
                if save_json:
                    output_file = output_dir / f"client_{i:03d}_{client_name}.json"
                    with open(output_file, 'w') as f:
                        json.dump(payload, f, indent=2)
            else:
                failed += 1
        
        print(f"\n{'='*60}")
        print(f"Results: {successful} successful, {failed} failed")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
