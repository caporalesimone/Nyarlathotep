# Fake Agent Test Client Generator

Test client generator for testing the Nyarlathotep backend.

## Installation

### Local Python

```bash
pip install -r requirements.txt
```

### Docker

Build image:
```bash
docker build -t fake-agent .
```

Or from project root:
```bash
docker build -f fake_agent/Dockerfile -t fake-agent .
```

## Usage

### Local Python

Show help:
```bash
python test_client_generator.py
```

Single run - generate and push JSON once:
```bash
python test_client_generator.py --single
```

Continuous mode - send data every 10 seconds:
```bash
python test_client_generator.py --continuous
```

Dry-run mode (generate JSON without pushing):
```bash
python test_client_generator.py --dry-run --single
```

Continuous dry-run (useful for testing without backend):
```bash
python test_client_generator.py --dry-run --continuous
```

Generate and save JSON files:
```bash
python test_client_generator.py --single --save-json
```

Combinations:
```bash
# Save JSON without pushing to server, single run
python test_client_generator.py --dry-run --save-json --single

# Continuous mode with local file saving
python test_client_generator.py --save-json --continuous
```

## Configuration

Modify the constants in `test_client_generator.py` to customize:

- `NUM_CLIENTS`: number of clients to generate (default: 100)
- `MIN_GROUP_RATIO`: min groups as % of clients (default: 0.10 = 10%)
- `MAX_GROUP_RATIO`: max groups as % of clients (default: 0.50 = 50%)
- `GROUP_PREFIX`: prefix for project/group names (default: "Group")
- `BACKEND_URL`: backend URL (default: http://localhost:8080)
- `ENDPOINT`: backend endpoint (default: /client_update)
- `INTERVAL_SECONDS`: seconds between updates in continuous mode (default: 10)

## Output

When JSON files are saved with `--save-json`, they are created in:
```
fake_agent/generated_test_clients/
```

Each file is named: `client_XXX_<client_name>.json`

## Features

✅ Generates 100+ clients with realistic data
✅ Random number of groups (10%-50% of clients)
✅ Respects the `agent_json_schema.json` schema with full validation
✅ **Continuous mode**: sends updated data every N seconds (configurable)
✅ Persistent client identities: same clients in each update cycle
✅ Generates fake data for:
  - Serial numbers (unique per client)
  - Private IPv4 addresses
  - MAC addresses
  - Hostnames
  - OS information (Windows)
  - Hardware (CPU, RAM, Disk) - updated each cycle
  - Logged-in users - updated each cycle
  - Software versions
