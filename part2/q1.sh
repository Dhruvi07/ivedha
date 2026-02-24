#!/bin/bash

hosts=("10.0.1.10" "10.0.1.11" "10.0.1.12")

failure=0

for host in "${hosts[@]}"; do
    ssh_status="DOWN"

    if nc -z -w3 $host 22; then
        ssh_status="UP"
    else
        failure=1
    fi

    port80=$(nc -z -w3 $host 80 && echo "OPEN" || echo "CLOSED") 
    port5672=$(nc -z -w3 $host 5672 && echo "OPEN" || echo "CLOSED")
    port5432=$(nc -z -w3 $host 5432 && echo "OPEN" || echo "CLOSED")

    echo "$host | SSH: $ssh_status | 80: $port80 | 5672: $port5672 | 5432: $port5432"
done

exit $failure