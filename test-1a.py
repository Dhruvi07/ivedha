import subprocess
import json
import socket
from datetime import datetime

SERVICES = ["httpd", "rabbitmq-server", "postgresql"]

HOST_NAME = socket.gethostname()
TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")


def check_service(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True
        )

        status = result.stdout.strip()
        return "UP" if status == "active" else "DOWN"

    except Exception:
        return "DOWN"


def create_json(service_name, status):
    return {
        "service_name": service_name,
        "service_status": status,
        "host_name": HOST_NAME,
        "@timestamp": datetime.utcnow().isoformat()
    }


def write_json_file(service_name, payload):
    filename = f"{service_name}-status-{TIMESTAMP}.json"
    with open(filename, "w") as f:
        json.dump(payload, f, indent=4)
    print(f"Created: {filename}")


def main():
    for service in SERVICES:
        status = check_service(service)
        payload = create_json(service, status)
        write_json_file(service, payload)


if __name__ == "__main__":
    main()