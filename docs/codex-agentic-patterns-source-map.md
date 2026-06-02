# Codex Agentic Patterns Source Map

이 문서는 Codex Agentic Patterns를 참조할 때 사용할 실제 페이지 링크와 source path를 기록한다. `.md` raw URL을 추측해서 호출하지 않는다. 먼저 공개 페이지의 navigation 또는 `mkdocs.yml`에서 경로를 확인한다.

확인 기준:
- 공개 사이트: `https://artvandelay.github.io/codex-agentic-patterns/`
- GitHub repository: `https://github.com/artvandelay/codex-agentic-patterns`
- `mkdocs.yml`의 `nav` 항목 기준

## Chapter Links

| Chapter | Page URL | Source path in repo |
|---|---|---|
| Home | https://artvandelay.github.io/codex-agentic-patterns/ | `docs/index.md` |
| Backstory | https://artvandelay.github.io/codex-agentic-patterns/context/ | `docs/context.md` |
| 1 Prompt Chaining | https://artvandelay.github.io/codex-agentic-patterns/learning-material/01-prompt-chaining/ | `docs/learning-material/01-prompt-chaining/README.md` |
| 2 Routing | https://artvandelay.github.io/codex-agentic-patterns/learning-material/02-routing/ | `docs/learning-material/02-routing/README.md` |
| 3 Parallelization | https://artvandelay.github.io/codex-agentic-patterns/learning-material/03-parallelization/ | `docs/learning-material/03-parallelization/README.md` |
| 4 Tool Use | https://artvandelay.github.io/codex-agentic-patterns/learning-material/05-tool-use/ | `docs/learning-material/05-tool-use/README.md` |
| 5 Planning | https://artvandelay.github.io/codex-agentic-patterns/learning-material/06-planning/ | `docs/learning-material/06-planning/README.md` |
| 6 Reflection | https://artvandelay.github.io/codex-agentic-patterns/learning-material/07-reflection/ | `docs/learning-material/07-reflection/README.md` |
| 7 Memory Management | https://artvandelay.github.io/codex-agentic-patterns/learning-material/08-memory-management/ | `docs/learning-material/08-memory-management/README.md` |
| 8 MCP Integration | https://artvandelay.github.io/codex-agentic-patterns/learning-material/10-mcp-integration/ | `docs/learning-material/10-mcp-integration/README.md` |
| 9 Exception Handling | https://artvandelay.github.io/codex-agentic-patterns/learning-material/12-exception-handling/ | `docs/learning-material/12-exception-handling/README.md` |
| 10 Human-in-the-Loop | https://artvandelay.github.io/codex-agentic-patterns/learning-material/13-human-in-the-loop/ | `docs/learning-material/13-human-in-the-loop/README.md` |
| 11 Knowledge Retrieval | https://artvandelay.github.io/codex-agentic-patterns/learning-material/14-knowledge-retrieval/ | `docs/learning-material/14-knowledge-retrieval/README.md` |
| 12 Reasoning | https://artvandelay.github.io/codex-agentic-patterns/learning-material/15-reasoning/ | `docs/learning-material/15-reasoning/README.md` |
| 13 Sandbox Escalation | https://artvandelay.github.io/codex-agentic-patterns/learning-material/16-sandbox-escalation/ | `docs/learning-material/16-sandbox-escalation/README.md` |
| 14 Turn Diff Tracking | https://artvandelay.github.io/codex-agentic-patterns/learning-material/17-turn-diff-tracking/ | `docs/learning-material/17-turn-diff-tracking/README.md` |
| 15 Rollout System | https://artvandelay.github.io/codex-agentic-patterns/learning-material/18-rollout-system/ | `docs/learning-material/18-rollout-system/README.md` |
| 16 Inter-Agent Communication | https://artvandelay.github.io/codex-agentic-patterns/learning-material/19-inter-agent-communication/ | `docs/learning-material/19-inter-agent-communication/README.md` |
| 17 Evaluation & Monitoring | https://artvandelay.github.io/codex-agentic-patterns/learning-material/20-evaluation-monitoring/ | `docs/learning-material/20-evaluation-monitoring/README.md` |
| Complete Agent Example | https://artvandelay.github.io/codex-agentic-patterns/learning-material/complete-agent-example/ | `docs/learning-material/complete-agent-example/README.md` |

## Link Verification Notes

Confirmed with `curl -I`:

- `https://artvandelay.github.io/codex-agentic-patterns/learning-material/20-evaluation-monitoring/` returned `HTTP/2 200`.
- `https://artvandelay.github.io/codex-agentic-patterns/learning-material/19-inter-agent-communication/` returned `HTTP/2 200`.
- `https://artvandelay.github.io/codex-agentic-patterns/learning-material/complete-agent-example/` returned `HTTP/2 200`.

## Rule

When adding or checking references:

1. Start from the page URL or `mkdocs.yml` nav.
2. Use GitHub API or `mkdocs.yml` to confirm source path when source text is needed.
3. Do not invent raw markdown paths.
4. If a guessed raw path returns 404, remove it from accepted sources and record the failed lookup as a discarded attempt, not as evidence.
