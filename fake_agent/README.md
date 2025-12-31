# Fake Agent Test Client Generator

Test client generator for testing the Nyarlathotep backend.

## Usage

### Single Run - Generate and push JSON once
```bash
python test_client_generator.py
```

### Continuous Mode - Send data every 10 seconds
```bash
python test_client_generator.py --continuous
```

### Dry-Run Mode (generate JSON without pushing)
```bash
python test_client_generator.py --dry-run
```

### Continuous Dry-Run (useful for testing without backend)
```bash
python test_client_generator.py --dry-run --continuous
```

### Generate and save JSON files
```bash
python test_client_generator.py --save-json
```

### Combinations
```bash
# Save JSON without pushing to server, single run
python test_client_generator.py --dry-run --save-json

# Continuous mode with local file saving
python test_client_generator.py --save-json --continuous
```

## Configuration

Modify the constants in `test_client_generator.py` to customize:

- `NUM_CLIENTS`: number of clients to generate (default: 50)
- `NUM_PROJECTS`: number of project_names (default: 5, which is 10% of 50)
- `BACKEND_URL`: backend URL (default: http://localhost:5000)
- `ENDPOINT`: backend endpoint (default: /client_update)
- `interval`: time in seconds between updates in continuous mode (default: 10)

## Output

When JSON files are saved with `--save-json`, they are created in:
```
fake_agent/generated_test_clients/
```

Each file is named: `client_XXX_<client_name>.json`

## Features

✅ Generates 50+ clients with realistic data
✅ Groups by `project_name` (max 10%)
✅ Respects the `agent_json_schema.json` schema
✅ **Continuous mode**: sends updated data every 10 seconds
✅ Persistent client identities: same clients in each update cycle
✅ Generates fake data for:
  - Private IPv4 addresses
  - MAC addresses
  - Hostnames
  - OS information (Windows)
  - Hardware (CPU, RAM, Disk) - updated each cycle
  - Logged-in users - updated each cycle
  - Software versions
