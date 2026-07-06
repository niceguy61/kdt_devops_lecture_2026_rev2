# Bedrock AgentCore Deployment Notes

This folder is intentionally thin. The package keeps research logic in
`aws_doc_research_agent.tools`; deployment code should only adapt request and
response shapes.

## Direct Code Deployment Shape

Amazon Bedrock AgentCore Runtime supports direct code deployment by packaging
agent code and dependencies into a zip archive. Keep the stable tool contract
unchanged and expose a small handler such as `handler.py`.

Suggested packaging flow:

```powershell
cd D:\paperclip\agent_tools\aws_doc_research_agent
python -m pip install -t build\package .
Copy-Item deployment\agentcore\handler.py build\package\handler.py
Compress-Archive -Path build\package\* -DestinationPath build\aws-doc-research-agent.zip -Force
```

Then deploy the zip with the AgentCore CLI or the AWS workflow chosen for the
lecture platform.

## Runtime Contract

Input:

```json
{
  "tool": "make_citation_pack",
  "arguments": {
    "topic": "EKS Pod Identity",
    "audience": "Kubernetes students"
  }
}
```

Output:

```json
{
  "ok": true,
  "result": {}
}
```

