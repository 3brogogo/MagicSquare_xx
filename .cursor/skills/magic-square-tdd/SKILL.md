---
name: magic-square-tdd
description: MagicSquare_xx Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. entity/control/boundary 구현, RED/GREEN/REFACTOR, test_d_*·test_u_*, pytest, E001~E007·10선 검증 시 사용.
---

# MagicSquare_xx — Dual-Track TDD·ECB Skill

**SSOT**: `docs/PRD.md`, `.cursorrules`, `Report/01·02`  
**D-* ID**: [reference.md](reference.md)

---

## 언제 Skill을 켜는지

| 상황 | 적용 |
|:---|:---|
| `src/entity`, `src/control`, `src/boundary` 구현·수정 | ✅ |
| `tests/**/test_d_*.py`, `test_u_*.py` 작성·수정 | ✅ |
| RED / GREEN / REFACTOR 요청 | ✅ |
| PRD 계약·E001~E007·10선=34·`int[6]` 회귀 | ✅ |
| Mom Test 회귀(대각선·첫 위반·입력 조기 거부) | ✅ |
| Report·README 등 문서만 | ❌ |
| git commit / push | 사용자 요청 시만 |

매 응답 **첫 줄**: `Phase: RED | Layer: entity | Track: Logic` (실제 값).

---

## Logic Track vs UI Track

| 항목 | Logic Track | UI Track |
|:---|:---|:---|
| 레이어 | `entity`, `control` | `boundary` |
| 테스트 ID | `D-*` | `U-*` |
| 파일명 | `test_d_*.py` | `test_u_*.py` |
| 디렉터리 | `tests/entity`, `tests/control` | `tests/boundary` |
| Mock | **금지** | **허용** (control/entity 스텁) |
| 관심사 | 10선·빈칸 2·누락 수·배정·`int[6]` | E001~E007·message 일치·첫 위반 1개 |
| 기본 pytest | `pytest tests/entity tests/control -ra` | `pytest tests/boundary -ra` |

한 Phase = **한 Track + 한 Layer**만 수정 (병렬 RED는 파일·트랙 분리).

---

## ECB·Mock·E001~E007

```
boundary → control → entity   (역방향 import 금지)
```

| | entity | control | boundary |
|:---|:---|:---|:---|
| import | control/boundary ❌ | boundary ❌ | control·entity ✅ |
| E001~E005 | **처리 금지** | **처리 금지** | **전담** |
| E006~E007 | 금지 | 금지 | 전담 |
| 테스트 Mock | 실구현 | 실구현 | 스텁·페이크 ✅ |

- entity/control 실패: `False` / `None` / 도메인 값 — **E00x·PRD message 문자열 금지**
- **34**, **16**: entity 상수 SSOT — 리터럴 산재 금지

---

## RED (7단계)

1. Track·Layer 확정 (`D-*` / `U-*`, entity / control / boundary)
2. SSOT 확인 (PRD, `.cursorrules`, `reference.md`)
3. 테스트 ID·경로 고정 (예: `D-07` → `tests/entity/test_d_....py`)
4. **실패 테스트 1건** — 최종 계약 assert; `skip`·`xfail`·완화 금지
5. `pytest <파일>::<노드> -ra` → **FAIL** 확인
6. 다른 레이어·트랙 파일 미변경 확인
7. 완료 보고 — **구현 코드 추가 금지** (GREEN은 다음 턴)

---

## GREEN (7단계)

1. Phase=GREEN, 동일 Track·Layer 선언
2. RED 1건 통과 **최소** `src/` 구현
3. ECB·E001~E005 in entity/control 없음 확인
4. 동일 노드 `pytest` → **PASS**
5. Track 전체 회귀 `pytest`
6. UI↔Logic 의존·역import 없음 확인
7. 완료 보고 (추가 RED 혼입 금지, 병렬 요청 제외)

---

## REFACTOR (6단계)

1. Phase=REFACTOR 선언
2. 공개 API·assert·PRD message **불변**
3. 중복·이름·상수 SSOT·private 추출만
4. Track 전체 `pytest` + 직전 GREEN 노드
5. 필요 시 `pytest -ra` 스모크
6. 완료 보고 + 다음 RED ID 1개 제안 (코드 없음)

---

## Test / Review Loop

| 시점 | 명령 | 기대 |
|:---|:---|:---|
| RED 직후 | `pytest <파일>::<노드> -ra` | FAIL |
| GREEN 직후 | 동일 노드 | PASS |
| GREEN 회귀 | Track 전체 (`entity`+`control` 또는 `boundary`) | 전부 PASS |
| REFACTOR 후 | Track 전체 → `pytest -ra` | 전부 PASS |
| 양 트랙 변경 후 | `pytest -ra` | 전부 PASS |
| 커밋 전 (사용자 요청) | `pytest -ra` | exit 0 |

- cwd: 프로젝트 루트
- `skip`·`xfail`·assert 완화로 GREEN **금지**
- 테스트 0건(exit 5)은 Harness만 있을 때만 정상

---

## 완료 보고 항목

| # | 항목 |
|:---:|:---|
| 1 | Phase · Track · Layer |
| 2 | 테스트 ID·파일 경로 |
| 3 | pytest 명령·결과 (PASS/FAIL, n) |
| 4 | 수정 `src/`·`tests/` 목록 |
| 5 | ECB·Mock·E001~E005 위반 여부 |
| 6 | PRD/.cursorrules 충돌 여부 |
| 7 | 다음 Phase·ID 제안 |

---

## 금지 요약

- RED 없이 GREEN · GREEN 중 새 RED (병렬 명시 제외)
- Logic Track 도메인 Mock
- entity/control의 E001~E005·message 하드코딩
- 첫 위반 2개 이상
- 10선 검사 **행→열→대각** 순서 이탈
