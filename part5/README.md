# Part 5 - ILM Policy + Index Template

This part contains Elasticsearch setup requests in `q1.json`:
- ILM policy: `service-status-policy`
- Index template: `service-status-template`

## What it configures

### ILM policy (`service-status-policy`)
- Hot phase: rollover after `1d`
- Warm phase: starts at `7d`
- Delete phase: delete at `30d`

### Index template (`service-status-template`)
- Applies to index pattern: `service-status-*`
- Field mappings:
  - `@timestamp` -> `date`
  - `service_name` -> `keyword`
  - `service_status` -> `keyword`
  - `host_name` -> `keyword`
- Attaches lifecycle policy `service-status-policy`


## How to apply

Recommended: Kibana Dev Tools (because `q1.json` includes two API requests).

1. Open Kibana -> Dev Tools -> Console.
2. Copy the ILM request block from `q1.json` and run it.
3. Copy the index template request block from `q1.json` and run it.

## Verification commands

In Kibana Dev Tools:

```http
GET _ilm/policy/service-status-policy
GET _index_template/service-status-template
```

To validate template application, create an index:

```http
PUT service-status-000001
GET service-status-000001/_settings
GET service-status-000001/_mapping
```

## Notes

- If using rollover, ensure alias/bootstrap strategy is aligned with your indexing flow.
