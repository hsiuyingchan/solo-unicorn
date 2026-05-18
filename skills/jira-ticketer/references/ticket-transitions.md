# Jira Ticket Transitions & Closure Guide

## Ticket Workflow States

Common Jira workflow states:

- **To Do**: Initial state, not started
- **In Progress**: Currently being worked on
- **In Review**: Awaiting code/design review
- **Done**: Completed and merged
- **Closed**: Resolved and archived

(Your project may have custom states - check your Jira workflow configuration)

## Get Available Transitions

Before moving a ticket, check what transitions are allowed:

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions" | jq '.transitions'
```

Response:
```json
{
  "transitions": [
    {
      "id": "11",
      "name": "Start Progress",
      "to": {
        "self": "...",
        "description": "",
        "iconUrl": "...",
        "name": "In Progress",
        "id": "3"
      }
    },
    {
      "id": "21",
      "name": "Move to Review",
      "to": {
        "name": "In Review",
        "id": "5"
      }
    }
  ]
}
```

## Move Ticket to New State

### Start Progress

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "11"
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

### Move to Review

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "21"
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

### Transition with Fields

Some transitions require or allow additional fields:

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "31"
    },
    "fields": {
      "resolution": {"name": "Fixed"},
      "comment": {
        "body": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Resolved in version 2.0.1"
                }
              ]
            }
          ]
        }
      }
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

## Common Resolution Types

When closing/resolving a ticket, set a resolution:

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "31"
    },
    "fields": {
      "resolution": {"name": "Fixed"}
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

Common resolutions:
- **Fixed**: Bug was fixed
- **Won't Fix**: Decided not to fix
- **Duplicate**: Duplicate of another ticket
- **Cannot Reproduce**: Can't reproduce the issue
- **By Design**: Behavior is intentional
- **Done**: Task completed

## Close a Ticket

### Close as Resolved

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "41"
    },
    "fields": {
      "resolution": {"name": "Fixed"},
      "comment": {
        "body": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Deployed to production on 2026-05-15"
                }
              ]
            }
          ]
        }
      }
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

### Close as Won't Fix

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "41"
    },
    "fields": {
      "resolution": {"name": "Won'\''t Fix"},
      "comment": {
        "body": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "This feature is out of scope for the current release."
                }
              ]
            }
          ]
        }
      }
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

### Close as Duplicate

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {
      "id": "41"
    },
    "fields": {
      "resolution": {"name": "Duplicate"},
      "comment": {
        "body": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Duplicate of PROJ-100"
                }
              ]
            }
          ]
        }
      }
    }
  }' \
  "$JIRA_URL/rest/api/3/issues/PROJ-123/transitions"
```

## Bulk Transitions

### Transition Multiple Tickets

```bash
export $(cat .env | xargs)

# Query tickets to transition
JQL='project = PROJ AND status = "In Review"'
TICKETS=$(curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=$JQL" | jq '.issues[].key' | tr -d '"')

# Transition each
for TICKET in $TICKETS; do
  curl -X POST \
    -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
    -H "Content-Type: application/json" \
    -d '{
      "transition": {
        "id": "31"
      }
    }' \
    "$JIRA_URL/rest/api/3/issues/$TICKET/transitions"
  sleep 1
done
```

## Response

Successful transition returns 204 No Content:

```
HTTP/1.1 204 No Content
```

## Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `400 Bad Request` | Invalid transition ID or missing required fields | Check available transitions and required fields |
| `401 Unauthorized` | Invalid credentials | Verify $JIRA_USERNAME and $JIRA_TOKEN |
| `403 Forbidden` | No permission to transition | Check workflow permissions |
| `404 Not Found` | Ticket doesn't exist | Verify ticket key |
| `409 Conflict` | Can't transition from current state | Use GET /transitions to see allowed transitions |

## Tips

- **Always Check Transitions First**: Use GET /transitions to find the correct transition ID
- **Transition ID != Status ID**: Transition ID is used in POST, not status ID
- **Required Fields**: Some transitions require additional fields (resolution, comment, etc.)
- **Workflow Validation**: Jira validates workflow rules - not all transitions are always available
- **Idempotency**: Transitioning to the same state twice may fail on the second attempt
- **Maintain Audit Trail**: Always add comments when transitioning, especially for closure
- **Environment Variables**: Always load your .env file first: `export $(cat .env | xargs)`
