# AWS Doc Research Agent

Local-first research tools for lecture production agents.

This package provides a small, dependency-light AWS documentation research
agent that can run as:

- a local CLI for quick testing;
- an MCP server for Codex/Claude-style tool clients;
- a tool module inside a Strands agent;
- a deployable Python package for Amazon Bedrock AgentCore Runtime.

The core module uses the public AWS documentation search endpoint and only
depends on the Python standard library. Optional adapters add MCP or agent
framework integration.

## Quick Start

```powershell
cd D:\paperclip\agent_tools\aws_doc_research_agent
python -m aws_doc_research_agent.cli search "EKS Pod Identity" --limit 5
python -m aws_doc_research_agent.cli citation-pack "EKS IRSA vs Pod Identity" --limit 3
python -m unittest discover -s tests
```

If running from a fresh shell without installing the package, set:

```powershell
$env:PYTHONPATH = "D:\paperclip\agent_tools\aws_doc_research_agent\src"
```

## Tool Contract

The agent exposes these stable tool functions:

- `search_aws_docs`: search AWS documentation for candidate sources.
- `read_aws_doc`: fetch and normalize a docs page to compact text.
- `make_citation_pack`: produce lecture-ready source evidence.

All tool outputs are JSON-serializable dictionaries. Keep this contract stable;
deployment adapters should wrap it rather than changing it.

## MCP Server

Install optional dependencies:

```powershell
pip install -e ".[mcp]"
```

Run locally:

```powershell
python -m aws_doc_research_agent.mcp_server
```

Example Codex MCP entry:

```toml
[mcp_servers.aws-doc-research-agent]
command = "python"
args = ["-m", "aws_doc_research_agent.mcp_server"]
env = { PYTHONPATH = "D:\\paperclip\\agent_tools\\aws_doc_research_agent\\src" }
startup_timeout_sec = 60
```

## Remote MCP Server For SAM API

Use this when the MCP client should call the deployed API Gateway/Lambda endpoint
instead of running the research tools in-process.

```powershell
$env:AWS_DOC_RESEARCH_AGENT_URL = "https://te2ok9dwl4.execute-api.ap-northeast-2.amazonaws.com/prod/invoke"
python -m aws_doc_research_agent.mcp_remote_server
```

Example Codex MCP entry:

```toml
[mcp_servers.aws-doc-research-agent-remote]
command = "python"
args = ["-m", "aws_doc_research_agent.mcp_remote_server"]
env = {
  PYTHONPATH = "D:\\paperclip\\agent_tools\\aws_doc_research_agent\\src",
  AWS_DOC_RESEARCH_AGENT_URL = "https://te2ok9dwl4.execute-api.ap-northeast-2.amazonaws.com/prod/invoke"
}
startup_timeout_sec = 60
```

## Strands Adapter

`src/aws_doc_research_agent/adapters/strands_tools.py` keeps the tool functions
framework-neutral. Import these functions into a Strands agent and register them
as tools according to the Strands version you are using.

## Bedrock AgentCore Prep

The `deployment/agentcore/` folder contains a minimal handler shim and packaging
notes. The handler calls the same stable local tool contract, so deployment does
not require rewriting research logic.

## AWS SAM Lambda + HTTP API

`template.yaml` deploys this agent as a Python Lambda behind API Gateway HTTP API.
The HTTP endpoint accepts `POST /invoke` with the same tool contract:

```json
{
  "tool": "make_citation_pack",
  "arguments": {
    "topic": "Amazon S3 lifecycle",
    "audience": "cloud students",
    "limit": 3
  }
}
```

Build and deploy:

```powershell
cd D:\paperclip\agent_tools\aws_doc_research_agent
sam build
sam deploy --guided --profile default --region ap-northeast-2
```

Suggested guided values:

```text
Stack Name: paperclip-aws-doc-research-agent-sam
AWS Region: ap-northeast-2
Confirm changes before deploy: Y
Allow SAM CLI IAM role creation: Y
Disable rollback: N
Save arguments to configuration file: Y
```

After deployment, use the `ApiInvokeUrl` output:

```powershell
$body = @{
  tool = "search_aws_docs"
  arguments = @{ query = "EKS kubeconfig"; limit = 3 }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "<ApiInvokeUrl>" -ContentType "application/json" -Body $body
```

Cleanup:

```powershell
sam delete --stack-name paperclip-aws-doc-research-agent-sam --profile default --region ap-northeast-2
```
