# Part 2 - Network Reachability Check

This part contains a Bash script (`q1.sh`) that checks host and service reachability.

## What it checks

For each host in the script, it verifies:
- SSH on port `22`
- HTTP on port `80`
- RabbitMQ on port `5672`
- PostgreSQL on port `5432`

The script exits with:
- `0` if all SSH checks pass
- `1` if any SSH check fails

## Prerequisites

- Linux/macOS shell
- `nc` (netcat) installed
- Network access to the target hosts

## How to run

From repository root:

```bash
cd part2
chmod +x q1.sh
./q1.sh
```

## Expected output

Example line:

```text
10.0.1.10 | SSH: UP | 80: CLOSED | 5672: CLOSED | 5432: CLOSED
```

## Notes

- Port `OPEN/CLOSED` output only confirms TCP reachability, not application health.
