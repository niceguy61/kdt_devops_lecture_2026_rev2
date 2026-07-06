# PRD: AWS Documentation Research Agent

## 1. Summary

AWS Documentation Research Agent는 강의 제작용 agentic AI 시스템의 근거 수집 도구다. AWS 공식 문서를 검색하고, 문서 내용을 읽고, 강의 자료에 바로 사용할 수 있는 citation pack을 생성한다.

초기 목표는 로컬에서 안정적으로 테스트 가능한 agent tool을 만들고, 이후 MCP, Strands Agents, Amazon Bedrock AgentCore Runtime으로 배포 가능한 구조를 준비하는 것이다.

## 2. Background

기존 AWS Labs MCP 서버를 Codex에 직접 붙이는 방식은 다음 문제가 있었다.

- `codex mcp list`에는 서버가 enabled로 표시되지만, 현재 Codex 세션의 callable tool로 노출되지 않는 경우가 있었다.
- `wsl.exe -> uvx -> MCP server` 실행 체인이 길어 startup, env 전달, tool discovery 디버깅이 어렵다.
- 여러 MCP 서버를 각각 붙이면 세션별 gateway indexing 상태를 추적하기 어렵다.

따라서 AWS 문서 검색 기능을 독립적인 local-first agent tool로 만들고, transport layer는 MCP/HTTP/Strands/AgentCore 어댑터로 분리한다.

## 3. Goals

- AWS 공식 문서를 검색하는 안정적인 로컬 tool 제공
- 검색 결과를 강의 제작에 맞는 citation pack 형태로 정리
- Codex, Claude, Strands, Bedrock AgentCore에서 재사용 가능한 tool contract 정의
- 로컬 smoke test로 배포 전 동작 확인
- 향후 lecture production agent pipeline의 research layer로 확장

## 4. Non-Goals

- AWS 계정 리소스 조작
- EKS 클러스터 변경, 배포, 삭제 같은 mutating action
- AWS Pricing, Well-Architected, What's New 전체 통합의 완성
- 완전한 RAG 시스템 구축
- 최종 슬라이드/문서 자동 생성까지 한 번에 처리

## 5. Target Users

- AWS/Kubernetes 강의 제작자
- 실습형 클라우드 교육 콘텐츠 작성자
- Agentic AI 기반 강의 제작 파이프라인 개발자
- Codex/Claude/MCP 기반 도구 실험자

## 6. Use Cases

### 6.1 Topic Research

사용자가 `EKS Pod Identity` 같은 주제를 입력하면 agent는 관련 AWS 공식 문서를 검색하고, 제목, URL, 요약, 관련도 정보를 반환한다.

### 6.2 Citation Pack Generation

사용자가 강의 주제와 대상 학습자를 입력하면 agent는 강의에 사용할 수 있는 출처 묶음을 생성한다.

출력에는 다음이 포함된다.

- topic
- audience
- source title
- source URL
- context
- usable_for
- confidence
- teaching_angles
- risks

### 6.3 Document Reading

검색 결과 URL을 입력하면 agent는 AWS 문서 HTML을 읽고, 강의 제작에 쓰기 쉬운 compact text로 변환한다.

### 6.4 Agent Pipeline Integration

Research Agent가 citation pack을 만들고, 이후 Curriculum Agent, Lab Agent, Slide Agent, Review Agent가 이를 재사용한다.

## 7. Functional Requirements

### 7.1 `search_aws_docs`

AWS 공식 문서 검색 결과를 반환한다.

Input:

```json
{
  "query": "EKS Pod Identity",
  "limit": 5,
  "product_types": [],
  "guide_types": [],
  "search_intent": ""
}
```

Output:

```json
{
  "query": "EKS Pod Identity",
  "query_id": "...",
  "results": [
    {
      "rank": 1,
      "title": "Understand how EKS Pod Identity works - Amazon EKS",
      "url": "https://docs.aws.amazon.com/eks/latest/userguide/pod-id-how-it-works.html",
      "context": "...",
      "sections": [],
      "recommended_sections": []
    }
  ],
  "facets": {},
  "metadata": {}
}
```

### 7.2 `read_aws_doc`

AWS 문서 페이지를 읽고 compact text를 반환한다.

Input:

```json
{
  "url": "https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html",
  "max_chars": 12000,
  "start_index": 0
}
```

Output:

```json
{
  "url": "...",
  "start_index": 0,
  "end_index": 12000,
  "total_chars": 9675,
  "truncated": false,
  "content": "..."
}
```

### 7.3 `make_citation_pack`

강의 제작에 바로 사용할 수 있는 출처 묶음을 생성한다.

Input:

```json
{
  "topic": "EKS Pod Identity vs IRSA",
  "audience": "cloud engineering students",
  "limit": 5
}
```

Output:

```json
{
  "topic": "EKS Pod Identity vs IRSA",
  "audience": "cloud engineering students",
  "summary": "...",
  "sources": [
    {
      "title": "IAM roles for service accounts - Amazon EKS",
      "url": "https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html",
      "context": "...",
      "usable_for": ["concept", "security note"],
      "confidence": 1.0
    }
  ],
  "teaching_angles": [],
  "risks": [],
  "search_query_id": "..."
}
```

## 8. Non-Functional Requirements

- Local-first: 로컬 CLI 테스트가 MCP 없이도 동작해야 한다.
- Stable contract: Python, TypeScript, MCP, Strands, AgentCore 어디서 실행해도 동일한 JSON shape을 유지한다.
- Read-only: 초기 버전은 외부 상태를 변경하지 않는다.
- Citation-first: 모든 research 결과는 source URL을 포함해야 한다.
- Low dependency: core는 Python standard library만 사용한다.
- Adapter isolation: MCP/Strands/AgentCore 의존성은 core logic과 분리한다.

## 9. Architecture

```text
agent_tools/aws_doc_research_agent
  tool_schema.json
  src/aws_doc_research_agent
    aws_docs_client.py
    tools.py
    cli.py
    mcp_server.py
    adapters/
      strands_tools.py
  deployment/
    agentcore/
      handler.py
  scripts/
    smoke_test.ps1
    check_mcp_import.ps1
```

### 9.1 Core Layer

`aws_docs_client.py`가 AWS documentation search endpoint와 docs page read를 담당한다.

### 9.2 Tool Contract Layer

`tools.py`가 agent tool로 노출되는 안정적인 함수 계약을 제공한다.

### 9.3 Transport Adapters

- `cli.py`: 로컬 테스트
- `mcp_server.py`: Codex/Claude MCP integration
- `adapters/strands_tools.py`: Strands Agents integration
- `deployment/agentcore/handler.py`: Bedrock AgentCore Runtime integration

## 10. Current Implementation Status

Implemented:

- Python local package
- AWS docs search client
- AWS docs page reader
- citation pack generator
- CLI
- MCP server wrapper
- Strands adapter skeleton
- AgentCore handler skeleton
- tool schema
- unit tests
- PowerShell smoke tests

Verified:

- `python -m unittest discover -s tests` passes
- live search for `EKS Pod Identity` works
- live citation pack generation works
- direct MCP `initialize` works
- direct MCP `tools/list` returns:
  - `search_aws_docs`
  - `read_aws_doc`
  - `make_citation_pack`
- direct MCP `tools/call search_aws_docs` works

Known issue:

- Current Codex session did not expose the newly registered MCP server as callable tools via `tool_search`.
- Server implementation is healthy; likely Codex session/gateway hot-load behavior.
- New Codex session or app refresh may be required.

## 11. Testing Plan

### 11.1 Unit Tests

```powershell
cd D:\paperclip\agent_tools\aws_doc_research_agent
$env:PYTHONPATH = "D:\paperclip\agent_tools\aws_doc_research_agent\src"
python -m unittest discover -s tests
```

### 11.2 Smoke Test

```powershell
cd D:\paperclip\agent_tools\aws_doc_research_agent
.\scripts\smoke_test.ps1 -Topic "EKS Pod Identity" -Limit 2
```

### 11.3 MCP Import Check

```powershell
.\scripts\check_mcp_import.ps1
```

### 11.4 Codex MCP Registration

```powershell
codex mcp add aws-doc-research-agent `
  --env PYTHONPATH=D:\paperclip\agent_tools\aws_doc_research_agent\src `
  -- python -m aws_doc_research_agent.mcp_server
```

Expected:

```text
search_aws_docs
read_aws_doc
make_citation_pack
```

## 12. Deployment Plan

### Phase 1: Local MCP

- Keep Python MCP server registered in Codex
- Validate from fresh Codex session
- Confirm tool calls from actual Codex tool gateway

### Phase 2: TypeScript Gateway Evaluation

If Python stdio MCP remains unstable in Codex sessions, add a TypeScript MCP gateway.

Options:

- TypeScript MCP server calls Python CLI as subprocess
- TypeScript MCP server calls Python HTTP local service
- TypeScript implements AWS docs search directly against the same endpoint

### Phase 3: Strands Agent

Wrap the stable tool contract as Strands tools and compose a `Research Agent`.

Candidate agent responsibilities:

- topic research
- citation pack generation
- source quality review
- teaching angle extraction

### Phase 4: Bedrock AgentCore

Package the same tool contract for AgentCore Runtime.

Deployment artifact:

```text
build/aws-doc-research-agent.zip
```

Entry:

```text
deployment/agentcore/handler.py
```

## 13. Future Extensions

- AWS What's New search
- AWS Pricing lookup
- Well-Architected guidance search
- EKS/Kubernetes lab validation helper
- source freshness scoring
- Korean lecture summary generation
- slide outline generator
- lab guide generator
- quiz and rubric generator
- citation deduplication
- saved research cache

## 14. Open Questions

- Should the primary runtime stay Python, or should MCP gateway move to TypeScript?
- Should AWS docs search use the public docs search endpoint directly or AWS Labs MCP as an upstream source?
- Should citation packs store local cache for reproducibility?
- How should source freshness be scored for rapidly changing AWS services?
- What is the minimum interface needed for AgentCore deployment tests?

## 15. Success Criteria

- Fresh Codex session can call `search_aws_docs` through MCP.
- `make_citation_pack` returns at least 3 relevant official AWS sources for common lecture topics.
- Research output can be consumed by a later Curriculum Agent without manual reformatting.
- AgentCore deployment test can invoke the same tool contract.
- No AWS write permissions are required for research-only usage.

