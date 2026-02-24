# Part 3 - Scheduler + Elasticsearch Watcher

This part includes:
- `q1`: a cron schedule entry
- `q2.json`: an Elasticsearch Watcher definition for service-down alerts

## Prerequisites

- Linux host with `cron` service running
- Python 3 installed at `/usr/bin/python3` (or update path)
- Elasticsearch cluster running on cloud with Watcher enabled 

## Q1: Cron job setup

File: `q1`

Current cron entry:

```cron
*/5 * * * * /usr/bin/python3 /home/ec2-user/test.py >> /home/ec2-user/test.log
```

### Apply it

From repository root:

```bash
cd part3
crontab -e
```

### Validate it

After 5-10 minutes:

```bash
tail -n 50 /home/ec2-user/test.log
```

## Q2: Watcher setup

File: `q2.json`

What it does:
- Runs every `1m`
- Reads latest status per service from index `rbcapp1-health`
- If any latest status is `DOWN`, sends an email alert
- Applies a throttle window (`300000 ms`) to reduce repeated emails

### Apply it (Kibana Dev Tools method)

1. Open Kibana -> Dev Tools -> Console.
2. Copy contents of `q2.json`.
3. Run the request to create/update the watcher.

### Verify watcher exists

Run in Dev Tools:

```http
GET _watcher/watch/service-down-watch
```

### Optional manual trigger

Run in Dev Tools:

```http
POST _watcher/watch/service-down-watch/_execute
```

## Notes

- Update alert recipient email in `q2.json` if needed.
