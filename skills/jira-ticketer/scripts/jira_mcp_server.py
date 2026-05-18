#!/usr/bin/env python3
"""
Jira MCP Server — programmatic Jira ticket management via MCP.

Provides tools for creating, updating, searching, and managing Jira issues
through the Jira REST API v3.
"""

import base64
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env
load_dotenv()

# Initialize MCP server
mcp = FastMCP("jira")

# Configuration from environment
JIRA_URL = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_USERNAME = os.getenv("JIRA_USERNAME", "")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")
JIRA_DEFAULT_PROJECT_KEY = os.getenv("JIRA_DEFAULT_PROJECT_KEY", "")
JIRA_DEFAULT_ISSUE_TYPE = os.getenv("JIRA_DEFAULT_ISSUE_TYPE", "Task")

# Validate required config
if not all([JIRA_URL, JIRA_USERNAME, JIRA_TOKEN]):
    raise RuntimeError(
        "Missing required Jira configuration: JIRA_URL, JIRA_USERNAME, JIRA_TOKEN"
    )


def get_auth_header() -> dict[str, str]:
    """Generate Basic Auth header for Jira API."""
    credentials = base64.b64encode(f"{JIRA_USERNAME}:{JIRA_TOKEN}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


def text_to_adf(text: str) -> dict:
    """Convert plain text to Atlassian Document Format (ADF)."""
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }


async def make_request(
    method: str,
    endpoint: str,
    data: dict | None = None,
    params: dict | None = None,
) -> dict[str, Any]:
    """Make authenticated request to Jira API v3."""
    url = f"{JIRA_URL}/rest/api/3{endpoint}"
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.text else {}
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if hasattr(e, "response") else str(e)
            raise RuntimeError(f"Jira API error: {e.response.status_code} — {error_detail}")


@mcp.tool()
async def create_issue(
    summary: str,
    description: str = "",
    project_key: str = "",
    issue_type: str = "",
) -> dict:
    """
    Create a new Jira issue.

    Args:
        summary: Issue title (required)
        description: Issue description
        project_key: Project key (e.g., CM). Uses JIRA_DEFAULT_PROJECT_KEY if not provided
        issue_type: Issue type (e.g., Task, Bug). Uses JIRA_DEFAULT_ISSUE_TYPE if not provided

    Returns:
        Created issue details including key and URL
    """
    if not summary:
        raise ValueError("summary is required")

    proj = project_key or JIRA_DEFAULT_PROJECT_KEY
    itype = issue_type or JIRA_DEFAULT_ISSUE_TYPE

    if not proj:
        raise ValueError(
            "project_key not provided and JIRA_DEFAULT_PROJECT_KEY not configured"
        )

    payload = {
        "fields": {
            "project": {"key": proj},
            "summary": summary,
            "issuetype": {"name": itype},
        }
    }

    if description:
        payload["fields"]["description"] = text_to_adf(description)

    result = await make_request("POST", "/issue", data=payload)
    return {
        "key": result.get("key"),
        "id": result.get("id"),
        "url": f"{JIRA_URL}/browse/{result.get('key')}",
    }


@mcp.tool()
async def get_issue(issue_key: str) -> dict:
    """
    Get details of a Jira issue.

    Args:
        issue_key: Issue key (e.g., CM-123)

    Returns:
        Full issue details
    """
    if not issue_key:
        raise ValueError("issue_key is required")

    result = await make_request("GET", f"/issue/{issue_key}")
    assignee_obj = result.get("fields", {}).get("assignee")
    priority_obj = result.get("fields", {}).get("priority")
    status_obj = result.get("fields", {}).get("status")

    return {
        "key": result.get("key"),
        "summary": result.get("fields", {}).get("summary"),
        "status": status_obj.get("name") if status_obj else None,
        "assignee": assignee_obj.get("displayName") if assignee_obj else None,
        "priority": priority_obj.get("name") if priority_obj else None,
        "description": result.get("fields", {}).get("description"),
        "created": result.get("fields", {}).get("created"),
        "updated": result.get("fields", {}).get("updated"),
        "url": f"{JIRA_URL}/browse/{result.get('key')}",
    }


@mcp.tool()
async def update_issue(
    issue_key: str,
    summary: str = "",
    description: str = "",
    priority: str = "",
    assignee_email: str = "",
) -> dict:
    """
    Update a Jira issue.

    Args:
        issue_key: Issue key (e.g., CM-123)
        summary: New issue title
        description: New issue description
        priority: New priority (e.g., High, Medium, Low)
        assignee_email: Assignee email address

    Returns:
        Updated issue details
    """
    if not issue_key:
        raise ValueError("issue_key is required")

    payload: dict[str, Any] = {"fields": {}}

    if summary:
        payload["fields"]["summary"] = summary
    if description:
        payload["fields"]["description"] = text_to_adf(description)
    if priority:
        payload["fields"]["priority"] = {"name": priority}
    if assignee_email:
        payload["fields"]["assignee"] = {"name": assignee_email}

    if not payload["fields"]:
        raise ValueError("At least one field (summary, description, priority, assignee_email) required")

    await make_request("PUT", f"/issue/{issue_key}", data=payload)
    return await get_issue(issue_key)


@mcp.tool()
async def search_issues(jql: str, max_results: int = 20) -> dict:
    """
    Search Jira issues using JQL (Jira Query Language).

    Args:
        jql: JQL query string (e.g., 'project = CM ORDER BY created DESC')
        max_results: Maximum number of results to return (default: 20)

    Returns:
        List of matching issues
    """
    if not jql:
        raise ValueError("jql query is required")

    payload = {
        "jql": jql,
        "maxResults": max_results,
    }

    result = await make_request("GET", "/search/jql", params={"jql": payload["jql"], "maxResults": payload["maxResults"]})

    # Get full issue details for each result
    issues = []
    for issue in result.get("issues", []):
        issue_id_or_key = issue.get("key") or issue.get("id")
        if issue_id_or_key:
            try:
                full_issue = await get_issue(str(issue_id_or_key))
                issues.append(full_issue)
            except Exception:
                # Fallback to minimal info if get_issue fails
                issues.append({
                    "key": issue.get("key") or None,
                    "summary": "",
                    "status": "",
                    "assignee": "",
                    "priority": "",
                    "url": f"{JIRA_URL}/browse/{issue.get('key')}" if issue.get("key") else None,
                })

    return {
        "total": len(issues),
        "count": len(issues),
        "issues": issues,
    }


@mcp.tool()
async def transition_issue(issue_key: str, status_name: str) -> dict:
    """
    Transition a Jira issue to a new status.

    Args:
        issue_key: Issue key (e.g., CM-123)
        status_name: Target status name (e.g., In Progress, Done)

    Returns:
        Updated issue details
    """
    if not issue_key or not status_name:
        raise ValueError("issue_key and status_name are required")

    # Get available transitions
    transitions_result = await make_request("GET", f"/issue/{issue_key}/transitions")
    transitions = transitions_result.get("transitions", [])

    # Find matching transition
    transition_id = None
    for trans in transitions:
        if trans.get("to", {}).get("name").lower() == status_name.lower():
            transition_id = trans.get("id")
            break

    if not transition_id:
        available = [t.get("to", {}).get("name") for t in transitions]
        raise ValueError(
            f"Transition to '{status_name}' not available. "
            f"Available: {', '.join(available)}"
        )

    payload = {"transition": {"id": transition_id}}
    await make_request("POST", f"/issue/{issue_key}/transitions", data=payload)
    return await get_issue(issue_key)


@mcp.tool()
async def add_comment(issue_key: str, comment: str) -> dict:
    """
    Add a comment to a Jira issue.

    Args:
        issue_key: Issue key (e.g., CM-123)
        comment: Comment text

    Returns:
        Added comment details
    """
    if not issue_key or not comment:
        raise ValueError("issue_key and comment are required")

    payload = {"body": text_to_adf(comment)}
    result = await make_request("POST", f"/issue/{issue_key}/comment", data=payload)
    return {
        "id": result.get("id"),
        "author": result.get("author", {}).get("displayName"),
        "created": result.get("created"),
        "body": result.get("body"),
    }


@mcp.tool()
async def list_projects() -> dict:
    """
    List all Jira projects accessible to the authenticated user.

    Returns:
        List of projects with key and name
    """
    result = await make_request("GET", "/project")
    projects = []
    for project in result if isinstance(result, list) else []:
        projects.append(
            {
                "key": project.get("key"),
                "name": project.get("name"),
                "url": f"{JIRA_URL}/browse/{project.get('key')}",
            }
        )

    return {
        "total": len(projects),
        "projects": projects,
    }


if __name__ == "__main__":
    mcp.run()
