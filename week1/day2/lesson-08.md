<sub>[🏠 과정 목차](../../README.md) › [1주차](../README.md) › [2일차](README.md) › 8/8교시</sub>

# 8교시 · 자원과 성능 — 병목 읽기 (강사 시연)

> [!NOTE]
> **이번 시간에 할 일**
>
> - "서버가 느려요"를 **CPU · 메모리 · 디스크 · 네트워크** 네 자원으로 나눠 묻습니다.
> - 자원마다 **사용률 · 포화 · 오류**(USE)를 확인하는 순서를 압니다.
> - `top` · `free` · `df`의 출력에서 숫자 몇 개만 골라 읽습니다.
> - 메모리가 모자라면 무슨 일이 생기는지(OOM Killer), 그게 2~3주차의 어떤 에러로 다시 나오는지 압니다.

> [!WARNING]
> **오늘도 따라 치지 않습니다**
>
> 5교시처럼 강사가 시연하고, 여러분은 **출력에서 어디를 보는지**에 집중합니다. 같은 명령은 2주차 1일차 이후 직접 실행합니다.

## "느려요"는 증상이지 원인이 아니다

1교시에 컴퓨터를 **CPU · 메모리 · 저장장치 · 네트워크**로 나눴습니다. 프로그램이 느려지는 이유는 거의 언제나 이 넷 중 하나가 **줄을 서기 시작했기** 때문입니다. 줄이 생긴 자원을 **병목(bottleneck)**이라고 합니다. 병 입구가 좁으면 병이 아무리 커도 천천히 나오는 것과 같습니다.

> **🧩 비유 — 식당 주방**
>
> 손님(요청)이 몰렸을 때 음식이 늦게 나오는 이유는 여러 가지입니다. 요리사(CPU)가 모자라거나, 조리대(메모리)가 좁아서 재료를 냉장고에 넣었다 뺐다 하거나, 냉장고 문(디스크)이 하나뿐이거나, 서빙 통로(네트워크)가 막혔을 수 있습니다. **요리사를 더 뽑는 것**(서버 증설)은 원인이 요리사일 때만 효과가 있습니다.

## 순서 정하기 — USE 방법

막연히 이것저것 보는 대신, 자원 하나마다 **세 가지 질문**을 똑같이 던집니다.

| 질문 | 뜻 | 주방 비유 |
|---|---|---|
| **U**tilization (사용률) | 그 자원이 얼마나 바쁜가 (%) | 요리사가 쉬는 시간 없이 일하나? |
| **S**aturation (포화) | 처리하지 못해 **기다리는 일**이 쌓였나 | 주문표가 몇 장 밀려 있나? |
| **E**rrors (오류) | 실패가 생기고 있나 | 접시를 떨어뜨리고 있나? |

사용률 100%는 그 자체로는 나쁘지 않습니다(돈 낸 만큼 쓰는 중). **포화**가 생기면 그때부터 사용자가 기다립니다.

| 자원 | 사용률 | 포화 | 오류 |
|---|---|---|---|
| CPU | `top`의 `%Cpu` (us+sy) | load average > 코어 수 | — |
| 메모리 | `free`의 used / available | swap 사용 증가 | **OOM Killer** 로그 |
| 디스크 | `df`의 Use% · I/O 대기(`wa`) | I/O 대기열 | `No space left on device` |
| 네트워크 | 송수신 바이트 | 재전송 · 버려진 패킷 | 연결 실패 (3일차) |

## 시연 1 — CPU: `top`

```text
top - 14:02:11 up 3 days,  2:10,  1 user,  load average: 7.85, 6.12, 3.40
Tasks: 212 total,   5 running, 207 sleeping,   0 stopped,   0 zombie
%Cpu(s): 92.3 us,  5.1 sy,  0.0 ni,  0.4 id,  2.2 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7843.2 total,    312.4 free,   6120.5 used,   1410.3 buff/cache
MiB Swap:   2048.0 total,   1980.1 free,     67.9 used.   1402.7 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   4821 app       20   0 2214.3m 1.2g   18.4m R 389.7  15.6  41:02.18 python3
```

| 어디를 보나 | 읽는 법 |
|---|---|
| `load average: 7.85, 6.12, 3.40` | 최근 **1분 · 5분 · 15분** 동안 "실행 중 + 실행을 기다리는" 일의 평균 개수. 1분 값이 커지는 중이면 상황이 나빠지는 중 |
| 코어 수와 비교 | 이 서버는 4코어(`nproc` → `4`). load 7.85 ÷ 4 ≈ 2 → **일이 코어보다 두 배 많아 줄을 선다** = CPU 포화 |
| `us` · `sy` | 프로그램(user) · 커널(system)이 쓰는 비율. 92.3 us → 앱 코드가 CPU를 다 쓰는 중 |
| `wa` | CPU가 **디스크를 기다리며** 노는 비율. 이 값이 크면 CPU가 아니라 디스크가 범인 |
| `st` | 가상 머신에서 **옆 VM에게 CPU를 뺏긴** 비율 (6교시 하이퍼바이저). 클라우드에서 가끔 본다 |
| `%CPU 389.7` | 코어 하나를 100%로 센다. 389.7% ≈ 코어 4개를 거의 다 씀 |

## 시연 2 — 메모리: `free -h`

```text
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       6.0Gi       305Mi        12Mi       1.4Gi       1.4Gi
Swap:          2.0Gi        66Mi       1.9Gi
```

> **❓ free가 305Mi뿐이니 메모리가 없다?**
>
> 아닙니다. Linux는 남는 메모리를 **파일 캐시(buff/cache)**로 써서 디스크 읽기를 빠르게 합니다. 프로그램이 필요하면 캐시를 바로 내줍니다. 그래서 봐야 할 칸은 `free`가 아니라 **`available`**(새 프로그램이 실제로 쓸 수 있는 양)입니다.

메모리가 정말 모자라면 두 단계로 나빠집니다.

1. **스왑(swap)** — 메모리 내용을 디스크로 내려 둡니다. 1교시의 속도 표를 떠올리면, 메모리보다 수천 배 느린 곳을 메모리처럼 쓰는 셈이라 **갑자기 모든 게 느려집니다.**
2. **OOM Killer** — 그래도 모자라면 커널이 **프로세스 하나를 강제로 죽입니다.** (OOM = Out Of Memory)

```text
$ sudo dmesg | grep -i "killed process"
Out of memory: Killed process 4821 (python3) total-vm:2267440kB, anon-rss:1258320kB
```

> [!IMPORTANT]
> **이 메시지는 이름만 바꿔 다시 나온다**
>
> | 어디서 | 보이는 모습 |
> |---|---|
> | Linux 서버 | `dmesg`의 `Killed process` |
> | 2주차 Docker | 컨테이너 종료 코드 **137** (= 128 + 9, SIGKILL) |
> | 3주차 Kubernetes | Pod 상태 **`OOMKilled`**, 재시작 반복 |
>
> 7교시의 **cgroups**가 컨테이너마다 메모리 한도를 걸기 때문에, 서버 전체가 넉넉해도 **컨테이너 하나는 한도에 걸려 죽을 수 있습니다.** 3주차 5일차에 `limits`로 직접 만들어 봅니다.

## 시연 3 — 디스크: `df -h` · `du`

```text
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G   30G     0 100% /

$ sudo du -sh /var/log/* | sort -h | tail -3
1.2G    /var/log/journal
4.8G    /var/log/nginx
19G     /var/log/app
```

- 디스크가 100%가 되면 새 파일을 못 써서 `No space left on device` 에러가 나고, **로그를 못 쓰는 앱은 멈추기도 합니다.**
- 범인은 대개 **지워지지 않고 쌓인 로그**입니다. 4교시의 `/var/log`가 여기서 다시 나옵니다. 그래서 운영에서는 로그를 일정 크기마다 잘라 오래된 것을 지우는 **로그 순환(logrotate)**을 반드시 켭니다.
- `df -i`는 공간이 아니라 **파일 개수(inode)**를 봅니다. 작은 파일이 수백만 개 쌓이면 공간이 남아도 같은 에러가 납니다.

## 증상에서 명령으로

| 증상 | 먼저 볼 것 | 이런 숫자면 |
|---|---|---|
| 모든 요청이 느리다 | `top`의 load average와 `nproc` | load가 코어 수를 오래 넘음 → CPU 포화 |
| 갑자기 프로세스가 사라졌다 | `dmesg \| grep -i killed` | `Killed process` → 메모리 부족 |
| 가끔 아주 느리다, CPU는 한가하다 | `top`의 `wa`, `free`의 Swap used | `wa`가 높거나 swap이 늘어남 → 디스크 · 메모리 |
| 로그가 안 남고 저장이 실패한다 | `df -h`, `df -i` | Use% 100% |
| 클라우드 VM만 들쭉날쭉 | `top`의 `st` | 옆 VM과 CPU 경쟁 |

> **🎓 학술 노트 — USE 방법 (Gregg, 2013)**
>
> 넷플릭스의 성능 엔지니어였던 **브렌던 그레그(Brendan Gregg)**는 2012년 ACM Queue에 싣고 이듬해 Communications of the ACM에 다시 실린 「Thinking Methodically about Performance」에서, 많은 엔지니어가 성능 문제를 만나면 **익숙한 도구부터 아무거나 켜 보는** 습관이 있다고 지적했습니다. 그는 이것을 "가로등 아래에서 열쇠 찾기"라는 반(反)패턴으로 부르고, 대신 **모든 자원에 대해 사용률 · 포화 · 오류를 빠짐없이 확인하는 체크리스트**를 제안했습니다. 이 방법은 도구가 아니라 **질문의 순서**를 정해 주기 때문에, 처음 보는 시스템에서도 빠진 곳 없이 원인 후보를 좁힐 수 있습니다.
>
> 같은 생각은 4주차 관찰 가능성 수업의 **RED 방법**(요청 수 · 오류 · 지연, 서비스 쪽 관점)과 짝을 이룹니다. USE는 **자원**을, RED는 **서비스**를 봅니다.
>
> - Gregg, B. (2013). Thinking methodically about performance. *Communications of the ACM*, 56(2), 45–51.

> **📈 트렌드 — '얼마나 썼나'에서 '얼마나 기다렸나'로**
>
> 사용률만으로는 사용자가 실제로 기다렸는지 알기 어렵습니다. Linux 커널 4.20(2018)부터는 **PSI(Pressure Stall Information)**가 들어와 `/proc/pressure/cpu`, `memory`, `io` 파일에서 "일이 자원을 **기다리느라 멈춘 시간의 비율**"을 바로 읽을 수 있습니다. USE의 **포화**를 커널이 직접 재 주는 셈입니다. Kubernetes도 kubelet이 PSI 지표를 내보내도록 기능을 넓히고 있어, 앞으로는 "CPU 80%"보다 "CPU를 기다린 시간 5%" 같은 지표로 경보를 거는 일이 늘어납니다. 커널 안에서 안전하게 작은 프로그램을 돌려 이런 지표를 모으는 **eBPF**도 관찰 도구의 기본기가 되고 있습니다.

## 정리

- "느려요"는 **CPU · 메모리 · 디스크 · 네트워크** 중 어디에 **줄이 생겼는지**의 문제입니다.
- 자원마다 **사용률 · 포화 · 오류**를 같은 순서로 묻습니다(USE).
- CPU 포화는 **load average > 코어 수**, 메모리는 **`available`**과 **OOM Killer**, 디스크는 **`df`의 Use%**와 **`wa`**로 봅니다.
- OOM은 Docker의 **137**, Kubernetes의 **OOMKilled**로 다시 만납니다.

> **✅ 확인 문제**
>
> 1. 8코어 서버의 load average가 `2.1, 2.0, 1.9`입니다. CPU가 포화 상태인가요?
> 2. `free -h`에서 free는 200Mi, available은 3.1Gi입니다. 메모리가 부족한가요?
> 3. CPU 사용률은 낮은데 `top`의 `wa`가 40%입니다. 어느 자원을 의심하나요?
> 4. 컨테이너가 종료 코드 137로 끝났습니다. 가장 먼저 떠올릴 원인은?
> 5. USE의 세 글자는 각각 무엇인가요?
>
> <details><summary>정답</summary>
>
> 1. 아닙니다. 코어 8개에 일이 평균 2개뿐이라 여유가 있습니다.
> 2. 아닙니다. 캐시로 쓰던 메모리를 바로 내줄 수 있어 실제로 쓸 수 있는 양(available)이 3.1Gi입니다.
> 3. 디스크(I/O) — CPU가 디스크를 기다리며 놀고 있습니다.
> 4. 메모리 한도 초과로 강제 종료(SIGKILL, OOM).
> 5. Utilization(사용률), Saturation(포화), Errors(오류)
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - 오늘 가장 "아하!" 했던 순간 하나 (예: 컨테이너가 그냥 프로세스였다니)
> - 아직 헷갈리는 개념 하나와 그 이유 (예: 커널과 셸의 차이)
> - 내일(네트워크 기초) 수업 전에 궁금한 것 하나

## 참고 문헌

- Gregg, B. (2013). Thinking methodically about performance. *Communications of the ACM*, 56(2).
- Gregg, B. (2020). *Systems Performance: Enterprise and the Cloud* (2nd ed.). Addison-Wesley.
- Linux Kernel Documentation. *PSI — Pressure Stall Information*. docs.kernel.org/accounting/psi.html
- man7.org. *top(1), free(1), df(1), proc(5)*.
- Kubernetes Documentation. *Node-pressure Eviction*; *Resource Management for Pods and Containers*.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · VM에서 컨테이너로 (2주차 예고)](lesson-07.md) | [⬆️ 2일차 목차](README.md) | [1주차 3일차 목차](../day3/README.md) ➡️ |
