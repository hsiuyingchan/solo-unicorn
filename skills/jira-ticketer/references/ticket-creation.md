# Jira Ticket Creation Guide

## Basic Ticket Creation

### Simple Create Request

```bash
# Load environment variables from .env file
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {
        "key": "PROJ"
      },
      "summary": "Fix login button styling",
      "description": "The login button is not properly aligned on mobile devices",
      "issuetype": {
        "name": "Bug"
      }
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

### Response

```json
{
  "id": "10001",
  "key": "PROJ-123",
  "self": "https://your-domain.atlassian.net/rest/api/3/issues/10001"
}
```

## Common Fields

### Required Fields (depends on project configuration)

- **project**: Project key or ID where ticket belongs
- **summary**: Brief title of the issue
- **issuetype**: Type of issue (Bug, Task, Story, Epic, etc.)

### Common Optional Fields

| Field | Type | Example |
|-------|------|---------|
| `description` | String | Full description with details |
| `priority` | Object | `{"name": "High"}` or `{"id": "2"}` |
| `assignee` | Object | `{"accountId": "user-id"}` |
| `labels` | Array | `["backend", "urgent"]` |
| `components` | Array | `[{"name": "API"}, {"name": "Auth"}]` |
| `duedate` | String (YYYY-MM-DD) | `"2026-05-30"` |
| `customfield_*` | Varies | Custom field values |
| `parent` | Object | For subtasks: `{"key": "PROJ-100"}` |

## Examples

### Create a Bug Ticket

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Login page crashes on Safari",
      "description": "When users access the login page in Safari, the page crashes with a JavaScript error",
      "issuetype": {"name": "Bug"},
      "priority": {"name": "High"},
      "labels": ["critical", "browser-issue"]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

### Create a Task with Assignee

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Update API documentation",
      "description": "Add examples for new endpoints in the authentication section",
      "issuetype": {"name": "Task"},
      "assignee": {"accountId": "5f12a3c4b5d6e7f8g9h0i1j2"},
      "duedate": "2026-05-30"
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

### Create a Story with Subtasks

```bash
export $(cat .env | xargs)

# First create the parent story
curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Implement two-factor authentication",
      "description": "As a user, I want to enable 2FA for my account to improve security",
      "issuetype": {"name": "Story"},
      "priority": {"name": "Medium"}
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

Response:
```json
{
  "key": "PROJ-456"
}
```

Then create subtasks:
```bash
curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Design 2FA UI mockups",
      "issuetype": {"name": "Subtask"},
      "parent": {"key": "PROJ-456"}
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

### Create with Custom Fields

```bash
export $(cat .env | xargs)

curl -X POST \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Optimize database queries",
      "issuetype": {"name": "Task"},
      "customfield_10001": "Performance",
      "customfield_10002": "5",
      "customfield_10003": ["Option A", "Option B"]
    }
  }' \
  "$JIRA_URL/rest/api/3/issues"
```

## Tips

- **Find Custom Field IDs**: Use GET `/rest/api/3/issue/{issueIdOrKey}` to see field IDs in responses
- **Project Key**: Visible in Jira URL bar (e.g., PROJ in `https://domain.atlassian.net/browse/PROJ-123`)
- **Issue Type**: Common types are Bug, Task, Story, Epic, Subtask (check your project configuration)
- **Account ID**: Find user account IDs with `/rest/api/3/users/search?query=email@domain.com`
- **Priority Levels**: Common names are Lowest, Low, Medium, High, Highest (check your Jira instance)

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid credentials | Check email and API token |
| `400 Bad Request` | Missing required field | Verify project key, summary, issuetype |
| `403 Forbidden` | No permission for project | Check project permissions |
| `404 Not Found` | Project doesn't exist | Verify project key spelling |
| `Field configuration invalid` | Wrong field type | Use correct format for field type |

### Retry Logic

Implement exponential backoff for transient errors (429 - Rate Limited):

```bash
max_retries=3
retry_delay=1

for attempt in $(seq 1 $max_retries); do
  response=$(curl -s -w "\n%{http_code}" ...)
  status=$(echo "$response" | tail -1)

  if [ "$status" = "201" ]; then
    echo "$response" | head -1 | jq .
    break
  elif [ "$status" = "429" ]; then
    sleep $retry_delay
    retry_delay=$((retry_delay * 2))
  else
    echo "Error: $status"
    break
  fi
done
```
