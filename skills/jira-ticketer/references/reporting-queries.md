# Jira Reporting & Query Guide

## JQL (Jira Query Language) Basics

JQL lets you query and filter tickets. Use it with the Search API or in Jira UI.

### Basic Syntax

```
field operator value
field1 = value1 AND field2 = value2
field CONTAINS "text"
```

### Common Fields

| Field | Description | Example |
|-------|-------------|---------|
| `project` | Project key | `project = PROJ` |
| `status` | Current status | `status = "In Progress"` |
| `assignee` | Assigned user | `assignee = currentUser()` |
| `reporter` | Who created ticket | `reporter = "email@domain.com"` |
| `created` | Creation date | `created >= -7d` |
| `updated` | Last update date | `updated >= -24h` |
| `duedate` | Due date | `duedate <= now()` |
| `priority` | Priority level | `priority >= High` |
| `issuetype` | Type of issue | `issuetype = Bug` |
| `component` | Component name | `component = "API"` |
| `labels` | Labels | `labels = backend` |
| `text` | Full-text search | `text ~ "payment"` |

### Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equals |
| `!=` | Not equals |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |
| `~` | Contains (text search) |
| `!~` | Does not contain |
| `IN` | In list |
| `NOT IN` | Not in list |
| `AND` | Both conditions true |
| `OR` | Either condition true |

## Basic Queries

### Search All Open Tickets

```bash
export $(cat .env | xargs)
PROJECT_KEY="MC"  # Replace with your project key

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search/jql?query=project%3D$PROJECT_KEY%20AND%20status%20!%3D%20Done" | jq '.issues'
```

### My Assigned Tickets

```bash
export $(cat .env | xargs)
PROJECT_KEY="MC"  # Replace with your project key

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search/jql?query=project%3D$PROJECT_KEY%20AND%20assignee%3DcurrentUser()%20AND%20status%20!%3D%20Done" | jq '.issues'
```

### Tickets in Current Sprint

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=sprint%20%3D%20FUTUR%20AND%20status%20!%3D%20Done" | jq '.issues'
```

### High Priority Bugs

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=project%20%3D%20PROJ%20AND%20type%20%3D%20Bug%20AND%20priority%20%3E%3D%20High" | jq '.issues'
```

### Overdue Tickets

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=duedate%20%3C%20now()%20AND%20status%20!%3D%20Done" | jq '.issues'
```

### Tickets Updated This Week

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=updated%20%3E%3D%20-7d" | jq '.issues'
```

## Advanced Reporting

### Count Open Tickets by Status

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=project%20%3D%20PROJ%20AND%20status%20!%3D%20Done&fields=status" | \
  jq -r '.issues[].fields.status.name' | sort | uniq -c
```

Output:
```
  5 In Progress
  8 In Review
  3 To Do
```

### Tickets by Priority

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=project%20%3D%20PROJ&fields=priority" | \
  jq -r '.issues[].fields.priority.name' | sort | uniq -c
```

### Tickets by Assignee

```bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=project%20%3D%20PROJ&fields=assignee&maxResults=100" | \
  jq -r '.issues[].fields.assignee.displayName' | grep -v null | sort | uniq -c
```

### Average Resolution Time

```bash
#!/bin/bash
export $(cat .env | xargs)

curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=project%20%3D%20PROJ%20AND%20status%20%3D%20Done&fields=created,updated&maxResults=100" | \
  jq -r '.issues[] | .fields as $f | ($f.updated | strptime("%Y-%m-%dT%H:%M:%S.%fZ") | mktime) - ($f.created | strptime("%Y-%m-%dT%H:%M:%S.%fZ") | mktime) | . / 86400 | floor' | \
  awk '{sum+=$1; count++} END {if (count > 0) print "Average: " sum/count " days"}'
```

## Common Reports

### Sprint Summary

```bash
#!/bin/bash
export $(cat .env | xargs)

SPRINT="Sprint 23"
PROJECT="PROJ"

echo "=== Sprint Summary: $SPRINT ==="
echo ""

# Total tickets
echo "Total Tickets:"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=sprint%20%3D%20%22$SPRINT%22" | \
  jq '.total'

# Completed
echo ""
echo "Completed:"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=sprint%20%3D%20%22$SPRINT%22%20AND%20status%20%3D%20Done" | \
  jq '.total'

# In Progress
echo ""
echo "In Progress:"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=sprint%20%3D%20%22$SPRINT%22%20AND%20status%20%3D%20%22In%20Progress%22" | \
  jq '.total'

# To Do
echo ""
echo "To Do:"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=sprint%20%3D%20%22$SPRINT%22%20AND%20status%20%3D%20%22To%20Do%22" | \
  jq '.total'
```

### Daily Standup Report

```bash
#!/bin/bash
export $(cat .env | xargs)

echo "=== Daily Standup Report ==="
echo ""

echo "My Assigned Work (Not Done):"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=assignee%20%3D%20currentUser()%20AND%20status%20!%3D%20Done&fields=key,summary,status,priority" | \
  jq -r '.issues[] | "\(.key): \(.fields.summary) (\(.fields.status.name))"'

echo ""
echo "Blocking Issues (High Priority, Not Started):"
curl -s \
  -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
  "$JIRA_URL/rest/api/3/search?jql=priority%20%3E%3D%20High%20AND%20status%20%3D%20%22To%20Do%22&fields=key,summary" | \
  jq -r '.issues[] | "\(.key): \(.fields.summary)"'
```

## Pagination

### Get All Results (With Pagination)

```bash
#!/bin/bash
export $(cat .env | xargs)

JQL="project = PROJ AND status = Done"
START_AT=0
MAX_RESULTS=50
ALL_ISSUES=()

while true; do
  RESPONSE=$(curl -s \
    -H "Authorization: Basic $(echo -n "$JIRA_USERNAME:$JIRA_TOKEN" | base64)" \
    "$JIRA_URL/rest/api/3/search?jql=$JQL&startAt=$START_AT&maxResults=$MAX_RESULTS")

  ISSUES=$(echo "$RESPONSE" | jq '.issues')
  TOTAL=$(echo "$RESPONSE" | jq '.total')

  if [ $(echo "$ISSUES" | jq 'length') -eq 0 ]; then
    break
  fi

  ALL_ISSUES+=($(echo "$ISSUES" | jq -r '.[].key'))
  START_AT=$((START_AT + MAX_RESULTS))

  echo "Fetched $((START_AT)) / $TOTAL"
done

echo "Total issues fetched: ${#ALL_ISSUES[@]}"
```

## Tips

- **Date Functions**: `now()`, `startOfDay()`, `-1d`, `-1w`, `-1m` (1 day, week, month ago)
- **User Functions**: `currentUser()`, `currentLogin()`
- **Empty Fields**: Use `EMPTY` to check: `assignee = EMPTY`
- **Logical Groups**: Use parentheses: `(status = "To Do" OR status = "In Progress") AND priority = High`
- **URL Encoding**: Remember to URL-encode JQL queries in curl: spaces = `%20`, `=` = `%3D`, etc.
- **Max Results**: Default is 50, max is 100. Use pagination for more.
- **Performance**: Complex queries with full-text search (`text ~`) are slower
- **Environment Variables**: Always load your .env file first: `export $(cat .env | xargs)`
