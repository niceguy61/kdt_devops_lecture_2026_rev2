# Week 1 Source Pack: Computing Fundamentals, DevOps, AI-Agent Verification

이 문서는 Week 1 강의안의 공식/학술 근거를 모은다. lesson 본문에는 학생이 당장 읽어야 할 핵심만 두고, 자세한 근거는 이 source pack과 각 day의 `academic-foundations.md`에서 확인한다.

## Computing Systems
| Source | Authority | Week 1 연결 |
|---|---|---|
| OSTEP: Operating Systems: Three Easy Pieces, https://pages.cs.wisc.edu/~remzi/OSTEP/ | University of Wisconsin-Madison OS textbook | process, memory, filesystem, persistence를 운영체제 abstraction으로 설명할 때 사용 |
| CS:APP, https://csapp.cs.cmu.edu/ | Carnegie Mellon systems textbook/course | 프로그램 실행, memory, storage, networked program이 DevOps 기초가 되는 이유 |
| MIT Missing Semester, https://missing.csail.mit.edu/ | MIT CSAIL course | shell, CLI, Git, debugging, automation을 실무형 computing literacy로 설명 |

## Network And HTTP
| Source | Authority | Week 1 연결 |
|---|---|---|
| Stanford CS144, https://stanford.edu/class/cs144/ | Stanford networking course | TCP/IP, reliability, routing, names/addressing 기초 |
| UC Berkeley CS168, https://www2.eecs.berkeley.edu/Courses/CS168/ | UC Berkeley networking course | Internet architecture, addressing, routing, TCP/UDP/IP/DNS/HTTP 흐름 |
| RFC 9110: HTTP Semantics, https://datatracker.ietf.org/doc/html/rfc9110 | IETF standard | request, response, method, status code, resource 개념의 공식 기준 |
| MDN HTTP Overview, https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview | MDN Web Docs | 초급자용 HTTP request/response 설명과 시각자료 후보 |

## Git, GitHub, README
| Source | Authority | Week 1 연결 |
|---|---|---|
| Pro Git: About Version Control, https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control | Official Git book | version control이 변경 이력과 협업에 필요한 이유 |
| GitHub Docs: About READMEs, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | GitHub official docs | README가 시작 방법, 도움 경로, maintainer 정보를 제공해야 하는 이유 |

## DevOps, SRE, Incident Learning
| Source | Authority | Week 1 연결 |
|---|---|---|
| AWS: What is DevOps?, https://aws.amazon.com/devops/what-is-devops/ | AWS official documentation | DevOps를 culture, practices, tools, automation, collaboration으로 설명 |
| Google Cloud DevOps guidance, https://docs.cloud.google.com/architecture/devops | Google Cloud / DORA guidance | delivery performance와 operational performance를 수업의 evidence/reproducibility 관점으로 낮춰 연결 |
| Google SRE Book: Introduction, https://sre.google/sre-book/introduction/ | Google SRE official book | availability, latency, performance, efficiency, change management, monitoring, emergency response, capacity planning |
| Google SRE Book: Postmortem Culture, https://sre.google/sre-book/postmortem-culture/ | Google SRE official book | RCA, timeline, impact, follow-up, blameless learning culture |

## Security, Secrets, AI Agent Governance
| Source | Authority | Week 1 연결 |
|---|---|---|
| OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | OWASP official cheat sheet | API key, DB credential, SSH key, certificate 등 secret을 코드/공개 문서에 넣지 않는 이유 |
| GitHub Secret Scanning, https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features | GitHub official docs | exposed secret 탐지와 push protection 개념 |
| NIST AI Risk Management Framework, https://www.nist.gov/itl/ai-risk-management-framework | NIST official framework | AI system 사용과 평가에서 risk management가 필요한 이유 |
| OpenAI: Running Codex Safely, https://openai.com/index/running-codex-safely/ | OpenAI official blog | coding agent의 access, approval, governance, telemetry 통제가 필요한 이유 |

## Learning Design
| Source | Authority | Week 1 연결 |
|---|---|---|
| CMU Eberly Center: Bloom's Taxonomy, https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html | Carnegie Mellon teaching center | 목표를 remember/understand/apply/analyze/evaluate 수준으로 구분 |
| CMU Eberly Center: Learning Objectives, https://www.cmu.edu/teaching/designteach/design/learningobjectives.html | Carnegie Mellon teaching center | 학습목표를 관찰 가능한 학생 행동으로 작성 |
| Monash Constructive Alignment, https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment | Monash University teaching guidance | 학습목표, 활동, 평가 증거를 서로 맞추는 기준 |
