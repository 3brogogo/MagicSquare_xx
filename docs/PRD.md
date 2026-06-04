# PRD — MagicSquare_xx (4×4, two missing numbers)

**작성일**: 2026-06-04  
**프로젝트명**: **MagicSquare_xx** (MagicSquare_1004)  
**도메인**: **4×4 Magic Square completion (two missing numbers)**  
**주 언어**: **Python 3.10+**  
**문제 정의 SSOT**: `Report/01.MagicSquare_ProblemDefinition_Report.md`  
**Mom Test 근거**: `Report/01.MagicSquare_1004_STEP1_Mom_Test_Interview_Report.md`

---

## 1. 제품 개요

### 1.1 문제 정의(요약)

- 본 제품은 \(4 \times 4\) 격자에서 **합의된 값 집합(1~16)** 과 **규칙(불변식)** 을 만족하는 **완성된 배치**를 산출하거나, 그러한 배치의 **존재 여부를 판정**하는 문제를 다룬다.
- 빈칸은 **`0`이 정확히 2개**이며, 완성 시 **10개 합**(행 4 + 열 4 + 대각선 2)은 모두 **34**이다.
- “마방진 앱을 만든다”가 아니라, Mom Test에서 확인된 **검증 비용·첫 위반 국소화**를 **입력/출력 계약**과 **검증 가능한 불변식**으로 고정하고 **TDD**로 보호하는 학습용 시스템이다.

### 1.2 Mom Test → 제품 연결(요약)

| 관찰(과거 사실) | 제품 요구로의 번역 |
|:---|:---|
| 대각선 검사 누락·10선 확인에 시간 소모 | `is_magic_square`: **행→열→대각** 고정 검사 순서 |
| 같은 줄만 수정·어디가 틀린지 모름 | 실패 시 **첫 위반 1개**만 반환(에러 우선순위 고정) |
| 감으로 제출·틀린 뒤 재시도 없음 | 입력 계약 **조기 거부** + 결정적 출력 + 회귀 테스트 |

### 1.3 목적(학습 목적)

- **Invariant 중심 설계**(10선·빈칸 2·34·값 집합)
- **Dual-Track TDD**(UI 계약 / Domain 규칙 병렬 RED→GREEN→REFACTOR)
- **입력/출력 계약 명확화**(첫 위반·`message` 완전 일치)
- **Clean Architecture(ECB)** 레이어 분리

---

## 2. 목표 / 비목표

### 2.1 목표(Goals)

- **Clean ECB layering**(boundary / control / entity)
- **TDD-first**(테스트 = 사양, 회귀 보호)
- **결정적 동작**(동일 입력 → 동일 출력)
- **10선 검증 명시**(행·열·두 대각선, 상수 34)

### 2.2 비목표(Non-goals)

- UI 스타일링·시각 디자인(필요 시에만)
- 성능 최적화 선제 도입
- 모든 해 열거(본 스코프: 빈칸 2개에 **2가지 배정 시도**)
- Mom Test **표면 문제** 구현: “자동 완성 앱만 있으면 된다” 수준의 요구

---

## 3. 사용자(페르소나) 및 사용 시나리오

### 3.1 페르소나

- 4×4·빈칸 2·1~16·**합 34(10선)** 를 손/코드로 다루는 **소프트웨어 개발 학습자**
- TDD·ECB 훈련 중
- 합 불일치 시 **어느 축/칸이 깨졌는지** 빠르게 알고 싶음(Mom Test 진짜 문제)

### 3.2 핵심 사용자 여정(Journey)

- **Step 1 — Mom Test / 문제 인식**: 과거 행동·검증 비용 수집 → 진짜 문제 한 문장
- **Step 2 — 계약 정의**: 입력/출력/에러·10선 검증 순서 확정
- **Step 3 — Domain 분리**: 빈칸·누락 수·마방진 판정·조합 시도 분리
- **Step 4 — Dual-Track**: UI RED + Logic RED 병렬
- **Step 5 — 회귀 보호**: 대각선 누락·첫 위반·감으로 제출류 시나리오 테스트 고정

---

## 4. Dual-Track TDD · Contract

### 4.1 Dual-Track 원리

- **UI Track (boundary)**: UX Contract(표준 `message`, 성공 형태, 첫 위반 1개 노출)
- **Logic Track (control + entity)**: Logic Rule(허용/거부/반환/10선 판정)
- **독립성**: UI 테스트는 도메인 내부에 의존하지 않음. Logic 테스트는 UI를 모름.

### 4.2 UX Contract 언어(boundary)

- 포함한다 / 포함하지 않는다(표준 `message`, `code`)
- 첫 위반만 노출(에러 리스트 금지)

### 4.3 Logic Rule 언어(control/entity)

- 허용/거부(입력 I-01~I-04)
- 계산/판정(10선 합, `is_magic_square`)
- 반환/차단(성공 `int[6]` vs `UI_UNSOLVABLE`)

### 4.4 UX Contract ↔ Logic Rule 매핑(요약)

| 시나리오(요약) | UX Contract | Logic Rule |
|:---|:---|:---|
| 4×4 아님 | `Matrix must be 4x4.` | `UI_INVALID_SHAPE` |
| 빈칸 2개 아님 | `Matrix must contain exactly 2 empty cells (0).` | `UI_INVALID_EMPTY_COUNT` |
| 범위 위반 | `Cell values must be 0 or 1..16.` | `UI_OUT_OF_RANGE` |
| 0 제외 중복 | `Non-zero values must be unique.` | `UI_DUPLICATE_NON_ZERO` |
| 해 없음 | `No magic square completion exists for this input.` | `UI_UNSOLVABLE` |
| 유효·해 있음 | 길이 6·1-index·`n1,n2` 순서 | 기본/반대 배정 **반환** |

---

## 5. 스코프(기능 요구사항)

### 5.1 입력 계약 — 고정

- **4×4** 정수 행렬
- 셀 값: **`0` 또는 `1..16`**
- **`0` = 빈칸, 정확히 2개**
- **`0` 제외 중복 없음**

### 5.2 출력 계약 — 고정(성공 시)

- **길이 6** 정수 배열: `[r1, c1, n1, r2, c2, n2]`
- `r1,c1,r2,c2`: **1-index** (1..4)
- `n1,n2`: 누락된 두 숫자
- 빈칸 좌표: **row-major** 스캔 순서
- `n1,n2` 순서: small→firstEmpty / large→secondEmpty 먼저; 실패 시 reverse; 둘 다 실패 시 해 없음

### 5.3 에러 계약 — 고정(실패 시)

- `error`: `{ code, message, details? }`
- **첫 위반 1개만** 반환
- **우선순위**: Shape → EmptyCount → Range → Duplicate → Unsolvable → Data

| code | message (완전 일치) | 발생 조건 |
|:---|:---|:---|
| `UI_INVALID_SHAPE` | `Matrix must be 4x4.` | 4×4 아님 |
| `UI_INVALID_EMPTY_COUNT` | `Matrix must contain exactly 2 empty cells (0).` | `0` 개수 ≠ 2 |
| `UI_OUT_OF_RANGE` | `Cell values must be 0 or 1..16.` | 범위 위반 |
| `UI_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` | 0 제외 중복 |
| `UI_UNSOLVABLE` | `No magic square completion exists for this input.` | 두 배정 모두 실패 |
| `UI_DATA_ERROR` | `Failed to persist or load the matrix.` | (선택) I/O 실패 |

- **I-05**는 별도 `code` 없음(I-02~I-04 만족 시 도출).

### 5.4 10선 검증(마방진 판정) — 고정

- 완성 보드에서 검사 대상: **4행 + 4열 + 2대각선 = 10선**
- 각 선의 합 = **34** (`I-06`~`I-09`)
- Logic 구현 시 **권장 검사 순서**: 행 → 열 → 대각선(Mom Test: 대각선 누락 방지)
- 미완성(`0` 존재) 보드는 `is_magic_square` = **False**(정책 고정·테스트로 보호)

---

## 6. 도메인 불변식(Invariants)

### 6.1 입력(Preconditions)

- **I-01** Shape: 4×4
- **I-02** EmptyCount: `0` 정확히 2개
- **I-03** Range: `0` 또는 `1..16`
- **I-04** UniqNonZero: 0 제외 중복 없음
- **I-05** MissingExactly2: 누락 값 2개(도출)

### 6.2 마방진(Domain Rules)

- **I-06** MagicConstant: 34
- **I-07** RowSum
- **I-08** ColSum
- **I-09** DiagSum
- **I-10** DeterministicOrderRule

---

## 7. 비기능 요구사항(NFR)

### 7.1 결정성

- 동일 입력 → 동일 출력(좌표·`n1,n2` 순서 포함)

### 7.2 테스트/품질 목표

- 최소 커버리지 **80%+**
- Domain Logic **95%+**, UI Boundary **85%+**

### 7.3 변경 금지(회귀 보호)

- 입력 계약·출력 `int[6]`·에러 **문구 1자**·우선순위·10선=34

---

## 8. 아키텍처 요구사항(ECB)

### 8.1 레이어

- **boundary**: 파싱·스키마·`message` 매핑 — UI Track
- **control**: 유스케이스·조합 시도 — Logic Track
- **entity**: `find_blank_coords`, `find_not_exist_nums`, `is_magic_square` — Logic Track

### 8.2 의존성

- 허용: boundary → control → entity
- 금지: entity → control/boundary, control → boundary

---

## 9. 사용자 스토리 및 AC(요약)

### 9.1 Story 1 — 입력 검증

- Logic: I-01~I-04 위반 시 **거부**
- UI: §5.3 `message` **완전 일치**, **첫 위반 1개**

### 9.2 Story 2 — 빈칸 탐색

- Logic: row-major, 정확히 2좌표

### 9.3 Story 3 — 누락 숫자

- Logic: 1..16 중 2개, 오름차순 내부 사용

### 9.4 Story 4 — 마방진 판정(10선)

- Logic: **10선** 합 34 **계산·판정**; 검사 순서 행→열→대각 **고정**(Mom Test)
- UI: (직접 노출 시) 판정 실패 이유가 첫 위반과 일치

### 9.5 Story 5 — 두 조합 시도·출력

- Logic: small/large 배정 → reverse → `int[6]` 또는 `UI_UNSOLVABLE`
- UI: 성공 형식·실패 `message`

---

## 10. 검증 계획(요약)

### 10.1 통합 시나리오(필수)

- 정상: 기본 배정 성공 / reverse 성공
- 실패: 빈칸 3개, 두 배정 실패, **한 대각선만 틀린 완성 보드**(10선 RED)
- Mom Test 회귀: **대각선 누락**·**첫 위반 우선순위**·입력 조기 거부

### 10.2 Traceability

- 모든 I-xx → 최소 1 테스트
- Mom Test 사실 → Story 4·§5.4·에러 우선순위 테스트로 추적

---

## 11. 가정 / 리스크

### 11.1 가정

- 값 집합 **1..16**, 빈칸 **`0`×2**
- 해결: 두 빈칸에 두 수 **2조합 시도**로 충분

### 11.2 리스크

- `message`·우선순위 변경 시 대규모 회귀(의도된 보호)
- 10선 중 **대각선만** 테스트하지 않으면 Mom Test 사례 재발

---

*본 PRD는 초안이다. 구현 To-Do·RED 상세는 이후 `docs/` 또는 `Report/` 보조 문서로 분리한다.*
