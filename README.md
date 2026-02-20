# Test Runbook

This repository contains solutions for:
- TEST1 – Service Monitoring + REST API + Elasticsearch Integration
- TEST2 – Ansible Automation (Installation, Disk Monitoring, Application Health Check)
- TEST3 – Python Data Processing (CSV Filtering by Average Price/Sq Ft)

This readme.md is split into two required parts:

1. How can you set up and test everything
2. How I did the setup

## Part 1: How Can You Set Up and Test Everything

### A) Prerequisites

- Python 3.9+
- `pip` (or `uv`)
- Ansible
- Linux host for `test-1a.py` (it uses `systemctl`)
- Network access to configured Elasticsearch and target hosts

Project:

```bash
git clone https://github.com/Dhruvi07/ivedha
```

### B) Install Dependencies(`venv` + `pip`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install ansible
```

### C) Test 1 (Service Status + API + Elasticsearch)

Add correct ES_HOST, ES_USERNAME and ES_PASSWORD in test-1b.py.

1. Generate service status JSON files:

```bash
python3 test-1a.py
```

Expected result:
- Creates:
  - `httpd-status-<timestamp>.json`
  - `rabbitmq-server-status-<timestamp>.json`
  - `postgresql-status-<timestamp>.json`

- `test-1a.py` calls `systemctl`, so run it on a Linux machine (or through your Linux servers)

2. Start API service:

```bash
uvicorn test-1b:app --host 0.0.0.0 --port 8000 --reload
```

3. Upload generated files:

```bash
curl -X POST "http://localhost:8000/add" -F "file=@httpd-status-<timestamp>.json"
curl -X POST "http://localhost:8000/add" -F "file=@rabbitmq-server-status-<timestamp>.json"
curl -X POST "http://localhost:8000/add" -F "file=@postgresql-status-<timestamp>.json"
```

Expected result:
- `{"message":"Document indexed successfully"}`

4. Validate health endpoints:

```bash
curl "http://localhost:8000/healthcheck"
curl "http://localhost:8000/healthcheck/httpd"
```

Expected result:
- `/healthcheck` returns latest service map.
- `/healthcheck/<service>` returns latest status of one service.

### D) Test 2 (Ansible Multi-Host Operations)

Inventory file: `inventory.ini`  
update inventory file with monitoring server IPs, users and SSH key path.

Playbook file: `test-2.yml`

Add relevant sender's email id and password and receivers's email id in vars in test-2.yml.

1. Verify httpd, if not found, install:

```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=verify_install"
```

2. Check disk usage and alert on >80%:

```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=check-disk"
```


3. Check application status from API:

```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=check-status"
```

Expected result:
1. verify_install - will check if httpd is already isntalled. If not, it will install.
  ok: [host1]
  host1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0 

2. check-disk - will send out an alert if any resource uses more than 80% of the disk.

3. check-status - Prints overall app status (`UP` or `DOWN`) and service-level details.
  ok: [host1] => {
    "msg": [
        "rbcapp1 Status:  DOWN ",
        "Service Status Details: {'httpd': 'UP', 'postgresql': 'UP', 'rabbitmq-server': 'DOWN'}"
    ]
}

### E) Test 3 (CSV Data Processing)

```bash
python3 test-3.py
```

Expected result:
- Reads `Assignment python.csv`
- Computes `price_per_sqft`
- Writes below-average rows to `filtered-sales-data.csv`
- Prints average and number of rows written

### F) Troubleshooting

1. Missing upload dependency:

```bash
pip install python-multipart
```

2. EC2 SSH checks:

```bash
chmod 400 /Users/dhruvi/Downloads/Poc-dhruvi.pem
```


---

## Part 2: How I Did the Setup

This is the setup and implementation flow reflected by repository files and history.

### 1) Created Test 1 implementation

- SSH into the EC2 instance(as I am working on MacOS, created an AWS EC2 instance to work on Linux).
- Added `test-1a.py` to collect service statuses using `systemctl is-active` and generate timestamped JSON output files.
- Added `requirements.txt` with FastAPI + Elasticsearch stack
  - `pip install requirements.txt`
- Added `test-1b.py` as FastAPI service with endpoints:
  - `POST /add`
  - `GET /healthcheck`
  - `GET /healthcheck/{service_name}`

- Run `python3 test1a.py` to run the file
- Run `uvicorn test1b:app --host 0.0.0.0 --port 8000` to run the file

To post the files to Elasticsearch 
```bash
curl -v -X POST http://localhost:8000/add \
-F "file=@/home/ec2-user/httpd-status-2026-02-20T19-54-17Z.json"
```
similar for postgresql and rabbitmq-server

To GET:
```bash
curl localhost:8000/healthcheck
curl localhost:8000/healthcheck/postgresql
curl localhost:8000/healthcheck/rabbitmq
curl localhost:8000/healthcheck/rabbitmq-server
```

### 2) Added infrastructure inventory

- Added `inventory.ini` with `rbcapp1` target hosts and grouping for Ansible operations.

### 3) Built Test 2 automation playbook

- Added and iterated Ansible playbook (current file: `test-2.yml`).
- Implemented action-driven execution:
  - `verify_install`
  - `check-disk`
  - `check-status`
- Added disk usage parsing and alert email behavior.
- Added API health check integration into Ansible flow.
To test if the functionality is working, decreased the alert limit to 20% momentarily by changing the regex to [2-9][0-9]%
```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=verify_install"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=check-disk"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini test-2.yml -e "action=check-status"
```

### 4) Built Test 3 data script

- Added `test-3.py` to process `Assignment python.csv`, compute per-row `price_per_sqft`, calculate average, and export below-average rows to `filtered-sales-data.csv`.



### 5) Special run instructions

- `test-1a.py` requires Linux + systemd because it calls `systemctl`.
- Keep API running before executing `check-status` in Ansible.
- `inventory.ini` must point to valid reachable hosts and SSH key path.
- Replace hardcoded credentials/secrets in scripts/playbook with env vars or vault before production use.
- Add `ANSIBLE_HOST_KEY_CHECKING=False` to make that it skips fingerprint validation and automatically accepts unknown hosts.
- Added extra field of @timestamp in test-1a.py for the sorting to get the latest results.
