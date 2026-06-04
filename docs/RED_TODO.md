# MagicSquare_xx — Dual-Track RED To-Do List

**작성일**: 2026-06-04  
**범위**: STEP 3 — RED 단계 테스트·픽스처·진행 순서  
**SSOT**: [`PRD.md`](PRD.md), [`.cursorrules`](../.cursorrules), [`reference.md`](../.cursor/skills/magic-square-tdd/reference.md)  
**상태**: Harness만 존재 (`test_*`·도메인 구현 없음) → 첫 RED는 대부분 `ModuleNotFoundError` / `ImportError` 예상

---

## 사용 방법

- 한 Phase = **한 Track + 한 Layer + RED 1건** (`skip`·`xfail`·assert 완화 금지)
- RED 완료: 해당 `pytest` 노드 **FAIL** 확인 후 **구현 없이** 체크
- GREEN/REFACTOR는 별도 문서·이슈로 진행 (본 목록은 RED만)

```bash
# 예: Logic entity 첫 RED
pytest tests/entity/test_d_blank_coords.py::test_d05 -ra
```

---

## 공통 준비 (픽스처·계약)

### 픽스처 (Given)

| ID | 설명 | 격자 (4×4) |
|:---|:---|:---|
| **G0** | 완성 마방진 (`0` 없음, 10선=34) | `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` |
| **G1** | 유효 부분 입력 (`0`×2, 기본 배정 성공용) | `[[16,3,2,13],[5,10,0,8],[9,6,0,12],[4,15,14,1]]` — 빈칸 (2,2),(3,3) 1-index, 누락 [7,10] |
| **G2** | Shape 위반 | `3×4` 행렬 |
| **G3** | EmptyCount 위반 | G1 기반 `0`×3 |
| **G4** | Range 위반 | G1 + `1..16` 밖 값 |
| **G5** | Duplicate 위반 | G1 + non-zero 중복 |
| **G6** | Mom Test — 대각선만 34 깨짐 | `tests/fixtures/mom_diag_bad` (파일로 고정) |
| **G7** | Unsolvable | `tests/fixtures/unsolvable_two_blanks` |
| **G8** | 복합 위반 (우선순위) | Shape+EmptyCount 동시 → **E001만** |

### To-Do — 픽스처·상수

- [ ] `tests/fixtures/` (또는 `tests/conftest.py`)에 G0~G8·G6·G7 픽스처 정의
- [ ] entity MagicConstant SSOT — `34`, 격자 `16` (리터럴 산재 금지)
- [ ] boundary E001~E007 ↔ PRD `UI_*` 매핑 모듈 1곳만 정의 (STEP 3)

### boundary 에러 매핑 (참고)

| E00x | PRD `code` | `message` (완전 일치) |
|:---|:---|:---|
| E001 | `UI_INVALID_SHAPE` | `Matrix must be 4x4.` |
| E002 | `UI_INVALID_EMPTY_COUNT` | `Matrix must contain exactly 2 empty cells (0).` |
| E003 | `UI_OUT_OF_RANGE` | `Cell values must be 0 or 1..16.` |
| E004 | `UI_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` |
| E005 | `UI_UNSOLVABLE` | `No magic square completion exists for this input.` |
| E006 | `UI_DATA_ERROR` | `Failed to persist or load the matrix.` |
| E007 | (확장) | `None`/비정형 입력 등 — boundary에서 1규칙만 고정 |

> `grid=None`은 E003(Range)이 아님. E006 또는 E007 중 **한 가지만** SSOT로 선택.

---

## Track A — Boundary / UI RED

**레이어**: `src/boundary` · **테스트**: `tests/boundary/test_u_*.py` · **Mock**: control/entity 스텁 허용

### To-Do — 입력 검증 (`test_u_input.py`)

| ID | Given | Then | Expected RED Failure |
|:---|:---|:---|:---|
| U-IN-01 | `grid=None` | E006 또는 E007 + `message` | `ModuleNotFoundError` |
| U-IN-02 | G2 (`3×4`) | E001 · `Matrix must be 4x4.` | `AssertionError` |
| U-IN-03 | G3 (`0`×3) | E002 · empty cells 문구 | `AssertionError` |
| U-IN-04 | G4 | E003 · range 문구 | `AssertionError` |
| U-IN-05 | G5 | E004 · duplicate 문구 | `AssertionError` |

- [ ] **U-IN-01** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-IN-02** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-IN-03** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-IN-04** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-IN-05** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-MSG-01** — U-IN-02~05 각각 PRD `message` 1자 일치 assert 포함

### To-Do — 우선순위 (`test_u_priority.py`)

| ID | Given | Then | Expected RED Failure |
|:---|:---|:---|:---|
| U-PRI-01 | G8 | **E001만** (에러 1개) | `AssertionError` (2개 반환 시) |

- [ ] **U-PRI-01** — RED 테스트 작성 · `pytest` FAIL 확인

### To-Do — 출력 계약 (`test_u_output.py`)

| ID | Given | Then | Expected RED Failure |
|:---|:---|:---|:---|
| U-OUT-01 | G1 | `len(result)==6` | `pytest.fail("RED")` / `AssertionError` |
| U-OUT-02 | G1 | `[2,2,7,3,3,10]` (1-index, row-major, small→first) | `AssertionError` |

- [ ] **U-OUT-01** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-OUT-02** — RED 테스트 작성 · `pytest` FAIL 확인

### To-Do — 흐름 (`test_u_flow.py`)

| ID | Given | Then | Expected RED Failure |
|:---|:---|:---|:---|
| U-FLOW-01 | G1 | control 유스케이스 **1회** 호출 | `AssertionError` (mock) |
| U-FLOW-02 | `grid=None` | control **0회** 호출 | `pytest.fail("RED")` |

- [ ] **U-FLOW-01** — RED 테스트 작성 · `pytest` FAIL 확인
- [ ] **U-FLOW-02** — RED 테스트 작성 · `pytest` FAIL 확인

### To-Do — 해 없음 (`test_u_unsolvable.py`)

| ID | Given | Then | Expected RED Failure |
|:---|:---|:---|:---|
| U-ERR-05 | G7 | E005 · unsolvable 문구 | `AssertionError` |

- [ ] **U-ERR-05** — RED 테스트 작성 · `pytest` FAIL 확인

### Boundary RED 완료 조건 (매 항목)

- [ ] assert: `code`, `message`, 성공 `len==6`, **첫 위반 1개**
- [ ] 우선순위: Shape → EmptyCount → Range → Duplicate → Unsolvable → Data
- [ ] entity/control 실구현 의존 없음 (Mock/페이크만)

---

## Track B — Logic / Domain RED

**레이어**: `src/entity`, `src/control` · **테스트**: `tests/entity/test_d_*.py`, `tests/control/test_d_*.py` · **Mock 금지**

### To-Do — entity (`tests/entity/`)

| ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|:---|:---|:---|:---|:---|
| D-05 | `find_blank_coords` | G1 → `[(2,2),(3,3)]` 1-index | I-02, row-major | `ModuleNotFoundError` |
| D-06 | `find_not_exist_nums` | G1 → `[7,10]` 오름차순 | I-05, I-10 | `ModuleNotFoundError` |
| D-07 | `is_magic_square` | G0 → `True` | I-06~I-09, 10선=34 | `ModuleNotFoundError` |
| D-08 | `is_magic_square` | G1 → `False` | `0` 존재 시 False | `AssertionError` |
| D-09 | `is_magic_square` | G6 → `False` | 행→열→**대각** (Mom Test) | `AssertionError` |

- [ ] **D-05** — `test_d_blank_coords.py` RED · `pytest` FAIL
- [ ] **D-06** — `test_d_missing_nums.py` RED · `pytest` FAIL
- [ ] **D-07** — `test_d_magic_square.py` (G0 True) RED · `pytest` FAIL
- [ ] **D-08** — `test_d_magic_square.py` (G1 False) RED · `pytest` FAIL
- [ ] **D-09** — `test_d_magic_square.py` (G6 Mom) RED · `pytest` FAIL

### To-Do — control 입력 거부 (`test_d_input_rules.py`)

> E001~E005·PRD `message` **assert 금지** — `False`/`None`만.

| ID | 대상 | Given → Then | Invariant |
|:---|:---|:---|:---|
| D-01 | validate/can_process | G2 → `False` | I-01 |
| D-02 | 동일 | G3 → `False` | I-02 |
| D-03 | 동일 | G4 → `False` | I-03 |
| D-04 | 동일 | G5 → `False` | I-04 |

- [ ] **D-01** — RED · `pytest` FAIL
- [ ] **D-02** — RED · `pytest` FAIL
- [ ] **D-03** — RED · `pytest` FAIL
- [ ] **D-04** — RED · `pytest` FAIL

### To-Do — control 유스케이스 (`tests/control/`)

| ID | 대상 | Given → Then | Invariant | Expected RED Failure |
|:---|:---|:---|:---|:---|
| D-10 | `solve` / `solution` | G1 → Step A `int[6]` | I-10, I-08 | `ModuleNotFoundError` |
| D-11 | `solve` | reverse만 성공 픽스처 → `int[6]` | reverse 배정 | `AssertionError` |
| D-12 | `solve` | G7 → `None`/`False` | 결정적·해 없음 | `AssertionError` |
| D-13 | control E2E | G1 전체 파이프라인 | entity 실구현 연동 | `ImportError` / `AssertionError` |

- [ ] **D-10** — `test_d_solution.py` RED · `pytest` FAIL
- [ ] **D-11** — reverse 성공 픽스처 RED · `pytest` FAIL
- [ ] **D-12** — G7 RED · `pytest` FAIL
- [ ] **D-13** — `test_d_control_e2e.py` RED · `pytest` FAIL

### Logic RED 완료 조건 (매 항목)

- [ ] entity/control에 E001~E005·UX `message` 문자열 없음
- [ ] Logic Track 도메인 Mock 없음
- [ ] `is_magic_square` 검사 순서: 행 → 열 → 대각

---

## 권장 RED 진행 순서

병렬 트랙은 **파일만** 분리; 한 번에 RED는 **1건**.

| 순번 | Track | ID | pytest 예시 |
|:---:|:---|:---|:---|
| 1 | Logic | D-05 | `pytest tests/entity/test_d_blank_coords.py::test_d05 -ra` |
| 2 | Logic | D-06 | `pytest tests/entity/test_d_missing_nums.py::test_d06 -ra` |
| 3 | Logic | D-07 | `pytest tests/entity/test_d_magic_square.py::test_d07_g0_true -ra` |
| 4 | Logic | D-08 | `pytest tests/entity/test_d_magic_square.py::test_d08_g1_false -ra` |
| 5 | Logic | D-09 | `pytest tests/entity/test_d_magic_square.py::test_d09_mom_diag -ra` |
| 6 | Logic | D-10 | `pytest tests/control/test_d_solution.py::test_d10_g1 -ra` |
| 7 | Logic | D-11 | `pytest tests/control/test_d_solution.py::test_d11_reverse -ra` |
| 8 | Logic | D-12 | `pytest tests/control/test_d_solution.py::test_d12_g7 -ra` |
| 9 | Logic | D-13 | `pytest tests/control/test_d_control_e2e.py::test_d13 -ra` |
| 10 | Boundary | U-IN-02 | `pytest tests/boundary/test_u_input.py::test_u_in_02 -ra` |
| 11 | Boundary | U-IN-03 | `pytest tests/boundary/test_u_input.py::test_u_in_03 -ra` |
| 12 | Boundary | U-IN-04 | `pytest tests/boundary/test_u_input.py::test_u_in_04 -ra` |
| 13 | Boundary | U-IN-05 | `pytest tests/boundary/test_u_input.py::test_u_in_05 -ra` |
| 14 | Boundary | U-PRI-01 | `pytest tests/boundary/test_u_priority.py::test_u_pri_01 -ra` |
| 15 | Boundary | U-OUT-01 | `pytest tests/boundary/test_u_output.py::test_u_out_01 -ra` |
| 16 | Boundary | U-OUT-02 | `pytest tests/boundary/test_u_output.py::test_u_out_02 -ra` |
| 17 | Boundary | U-FLOW-02 | `pytest tests/boundary/test_u_flow.py::test_u_flow_02 -ra` |
| 18 | Boundary | U-FLOW-01 | `pytest tests/boundary/test_u_flow.py::test_u_flow_01 -ra` |
| 19 | Boundary | U-ERR-05 | `pytest tests/boundary/test_u_unsolvable.py::test_u_err_05 -ra` |
| 20 | Boundary | U-IN-01 | `pytest tests/boundary/test_u_input.py::test_u_in_01 -ra` |

- [ ] 순번 1~9 Logic RED 전부 완료 (각각 FAIL 확인)
- [ ] 순번 10~20 Boundary RED 전부 완료 (각각 FAIL 확인)

---

## RED 단계 전체 완료 체크리스트

- [ ] 모든 D-01~D-13 RED 테스트 존재 · 노드별 FAIL 확인
- [ ] 모든 U-* RED 테스트 존재 · 노드별 FAIL 확인
- [ ] G0~G8·G6·G7 픽스처 SSOT 고정
- [ ] RED 중 `src/` 프로덕션 구현 **추가 없음** (GREEN은 다음 단계)
- [ ] `pytest tests/ -ra` — RED만 있을 때: 신규 테스트 수집·의도된 FAIL (exit ≠ 0)
- [ ] PRD·`.cursorrules`·Mom Test(대각선·첫 위반·조기 거부)와 표 불일치 없음

---

## 추적

| 문서 | 역할 |
|:---|:---|
| [`PRD.md`](PRD.md) | 입·출력·에러·불변식 SSOT |
| [`RED_TODO.md`](RED_TODO.md) | 본 RED To-Do |
| [`../Report/02.MagicSquare_xx_STEP2_Harness_Engineering_Report.md`](../Report/02.MagicSquare_xx_STEP2_Harness_Engineering_Report.md) | Harness·STEP 3 안내 |
| [`../.cursor/skills/magic-square-tdd/reference.md`](../.cursor/skills/magic-square-tdd/reference.md) | D-* ID 요약 |

*GREEN/REFACTOR To-Do는 RED 완료 후 별도 문서로 분리 예정.*
