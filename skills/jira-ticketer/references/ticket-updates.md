# Jira Ticket Update Guide

## Basic Ticket Update

### Update Single Field

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "summary": "Updated title"
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

### Update Multiple Fields

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "summary": "New summary",
      "description": "Updated description",
      "priority": {"name": "High"},
      "assignee": {"accountId": "5f12a3c4b5d6e7f8g9h0i1j2"},
      "labels": ["urgent", "backend"]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

## Common Update Operations

### Change Priority

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "priority": {"name": "Critical"}
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

### Assign Ticket

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "assignee": {"accountId": "5f12a3c4b5d6e7f8g9h0i1j2"}
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

### Unassign Ticket

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "assignee": null
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

### Add Labels

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "labels": ["backend", "performance", "urgent"]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

### Update Due Date

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "duedate": "2026-06-15"
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

## Adding Comments

### Add a Comment

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "This issue has been fixed in the latest release. Please verify."
            }
          ]
        }
      ]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/comments"
```

### Add Comment with Mention

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Hi "
            },
            {
              "type": "mention",
              "attrs": {
                "id": "5f12a3c4b5d6e7f8g9h0i1j2"
              }
            },
            {
              "type": "text",
              "text": ", can you review this?"
            }
          ]
        }
      ]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/comments"
```

## Bulk Operations

### Bulk Update Multiple Tickets

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "issueIds": [10001, 10002, 10003],
    "operations": [
      {
        "operationType": "CHANGED",
        "field": "priority",
        "value": {"name": "High"}
      },
      {
        "operationType": "CHANGED",
        "field": "labels",
        "value": ["sprint-23", "qa-ready"]
      }
    ]
  }' \
  "$JIRA_URL/rest/api/3/issues/bulk"
```

### Update All Open Tickets in a Sprint

```bash
export $(cat .env | xargs)

# First, query all open tickets
JQL='project = PROJ AND status != Done AND sprint = "Sprint 23"'
TICKETS=$(curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=$JQL" | jq '.issues[].id')

# Then update each ticket
for TICKET_ID in $TICKETS; do
  curl -X PUT \
    -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
    -H "Content-Type: application/json" \
    -d '{
      "fields": {
        "labels": ["ready-for-deployment"]
      }
    }' \
    "$JIRA_URL/rest/api/3/issues/$TICKET_ID"
done
```

## Update Custom Fields

### Update Custom Field by ID

```bash
export $(cat .env | xargs)

curl -X PUT \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "customfield_10001": "Custom Value",
      "customfield_10002": {"name": "Option A"},
      "customfield_10003": ["Tag1", "Tag2"]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123"
```

## Response

Successful update returns 204 No Content:

```
HTTP/1.1 204 No Content
```

## Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `400 Bad Request` | Invalid field or value format | Check field type and value format |
| `401 Unauthorized` | Invalid credentials | Verify $JIRA_USERNAME and $JIRA_TOKEN |
| `403 Forbidden` | No permission to update | Check issue permissions |
| `404 Not Found` | Ticket doesn't exist | Verify ticket key |
| `409 Conflict` | Concurrent modification | Retry the operation |

## Tips

- **Batch Updates**: Use bulk endpoint for updating many tickets (more efficient)
- **Comment History**: Comments are stored separately; always use the comments endpoint
- **Field Validation**: Some fields may not be updatable in certain statuses (e.g., can't change priority after resolution)
- **Idempotency**: Updates are idempotent - updating with the same value twice has the same effect as once
- **Environment Variables**: Always load your .env file first: `export $(cat .env | xargs)`
