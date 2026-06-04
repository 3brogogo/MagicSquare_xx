# MagicSquare_xx (4×4, 빈칸 2개)

부분적으로 채워진 **4×4 마방진**에서 `0`인 **두 칸**에 누락된 수를 배정해 **10선**(행 4 + 열 4 + 대각선 2) 합이 모두 **34**가 되도록 완성하거나, 계약 위반·해 없음을 **표준 코드·문구**로 반환하는 **학습용** 프로젝트입니다.

Mom Test(과거 행동·검증 비용) → 문제 정의 → **PRD 계약** → Dual-Track TDD·ECB 순으로 진행합니다.  
**현재 단계**: STEP 3 **RED** — ECB Harness 준비됨. **진행 중 묶음**: `D-LOC-01` (FR-LOC-01) · [`docs/RED_TODO.md`](docs/RED_TODO.md) 체크리스트 병행.

---

## 한 줄 요약

| 항목 | 내용 |
|:---|:---|
| **도메인** | 4×4, 값 `0` 또는 `1..16`, `0` 정확히 2개, 완성 시 **10선 합 = 34** |
| **성공 출력** | `int[6]` — `[r1, c1, n1, r2, c2, n2]` (1-index) |
| **실패** | `error.code` + `message` (**완전 일치**), **첫 위반 1개만** |
| **학습 초점** | 불변식·계약·10선 검증(행→열→대각)·회귀 테스트 |

---

## 문서 읽는 순서

| 순서 | 문서 | 용도 |
|:---:|:---|:---|
| 1 | [`Report/01.MagicSquare_xx_STEP1_Mom_Test_Interview_Report.md`](Report/01.MagicSquare_xx_STEP1_Mom_Test_Interview_Report.md) | Mom Test 인터뷰·과거 사실·워크북 |
| 2 | [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) | 표면/진짜 문제·불변식·PRD 연결 |
| 3 | [`docs/PRD.md`](docs/PRD.md) | **기술 SSOT** — 입·출력·에러·스토리·ECB |
| 4 | [`docs/RED_TODO.md`](docs/RED_TODO.md) | **RED 단계** To-Do·픽스처·진행 순서 (상세) |
| 5 | [`Prompting/01.MagicSquare_xx_STEP1_Mom_Test_Interview_prompt.md`](Prompting/01.MagicSquare_xx_STEP1_Mom_Test_Interview_prompt.md) | STEP 1 Cursor 대화 Export |

---

## 저장소 구조

```
MagicSquare_xx/
├── README.md                 ← 이 파일
├── pyproject.toml            ← pytest Harness
├── .cursorrules
├── docs/
│   ├── PRD.md                ← 스펙 SSOT
│   └── RED_TODO.md           ← RED To-Do (상세)
├── src/
│   ├── boundary/             ← UI Track
│   ├── control/              ← Logic Track
│   └── entity/
├── tests/
│   ├── boundary/             ← test_u_*.py
│   ├── control/              ← test_d_*.py
│   └── entity/
├── Report/
└── Prompting/
```

---

## Mom Test → 제품 (요약)

**페르소나:** 4×4·빈칸 2·1~16·합 34(10선)을 맞추는 학습자.

**진짜 문제 (한 문장):**  
여러 줄·열·대각선 규칙이 동시에 걸릴 때, 깨진 축·칸·수정 시도를 찾지 못한 채 같은 부분만 고치다 검증에 시간을 쓰고, 확신 없이 제출한 뒤 틀려도 다시 검증할 동기가 끊긴다.

| 관찰 | PRD 반영 |
|:---|:---|
| 대각선 검사 누락·10선 확인 시간 | §5.4 행→열→대각 검사 순서 |
| 어디가 틀렸는지 모름 | §5.3 첫 위반 1개·에러 우선순위 |
| 감으로 제출 | 입력 계약 조기 거부 + 결정적 출력 |

자세한 인용·표면 문제(금지) 목록은 `Report/01.MagicSquare_*` 참고.

---

## 도메인 계약 (PRD 요약)

### 입력

- 4×4 정수 행렬
- `0` = 빈칸, **정확히 2개**
- 그 외 `1..16`, **0 제외 중복 없음**

### 성공 출력

```
[r1, c1, n1, r2, c2, n2]   # 길이 6, 좌표 1-index
```

### 에러 (우선순위 — 첫 위반만)

1. `UI_INVALID_SHAPE` — `Matrix must be 4x4.`
2. `UI_INVALID_EMPTY_COUNT` — `Matrix must contain exactly 2 empty cells (0).`
3. `UI_OUT_OF_RANGE` — `Cell values must be 0 or 1..16.`
4. `UI_DUPLICATE_NON_ZERO` — `Non-zero values must be unique.`
5. `UI_UNSOLVABLE` — `No magic square completion exists for this input.`
6. `UI_DATA_ERROR` — (선택) 저장/로드 실패

전체 표·불변식 I-01~I-10·스토리 AC는 [`docs/PRD.md`](docs/PRD.md).

---

## 개발 방법론

| 트랙 | 역할 |
|:---|:---|
| **UI / Boundary** | UX Contract — `message`·첫 위반·성공 형식 |
| **Logic / Domain** | `find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution` |
| **ECB** | boundary → control → entity (역방향 의존 금지) |
| **TDD** | RED → GREEN → REFACTOR |

RED 규칙: **한 Phase = 한 Track + 한 Layer + RED 1건** · `skip`/`xfail`/assert 완화 금지 · RED 완료 = 해당 `pytest` **FAIL** 확인 후 **구현 없이** 체크.

상세 표·픽스처·에러 매핑은 [`docs/RED_TODO.md`](docs/RED_TODO.md).

---

## RED Test Plan — `D-LOC-01` (진행 중)

`Phase: RED` · `Layer: entity` · `Track: Logic`  
**이번 RED 묶음**: D-LOC-01 (FR-LOC-01) — [`RED_TODO`](docs/RED_TODO.md) **D-05**와 동일 범위  
**금지**: `src/` 수정 · GREEN/REFACTOR · `skip`/`xfail` · `tests/`·`src/` 파일은 `/red-skeleton`에서 생성

### 1. C2C 추적 (Rule 1~3)

| Rule | 적용 |
|:---|:---|
| **Rule 1** | FR마다 최소 1개 테스트 ID (`D-LOC-01`) |
| **Rule 2** | assert는 계약(좌표·개수·순서)만 — 구현 세부·E00x 문구 금지 |
| **Rule 3** | 테스트·docstring에 `FR-LOC-01` / `D-LOC-01` 명시 |

**PRD FR-LOC-01 인용** (`docs/PRD.md` — 본 ID는 §9.2·§5.2·§8.1 합성)

| 출처 | 인용 |
|:---|:---|
| §9.2 Story 2 — 빈칸 탐색 | Logic: **row-major**, **정확히 2좌표** |
| §5.2 출력 계약 | 빈칸 좌표: **row-major 스캔 순서** · `r1,c1,r2,c2`: **1-index** (1..4) |
| §8.1 entity | `find_blank_coords` — Logic Track |

**To-Do (판단 포함 1건)**

| 판단 | To-Do |
|:---|:---|
| RED-TODO **D-05** = **D-LOC-01** 동일 스펙으로 진행 | [ ] `find_blank_coords`(G1) → `[(2,2),(3,3)]` 1-index · `pytest` **FAIL** 후 체크 |

| Test ID | Given | When | Then |
|:---|:---|:---|:---|
| **D-LOC-01** | G1 — `[[16,3,2,13],[5,10,0,8],[9,6,0,12],[4,15,14,1]]` (`0`×2) | `find_blank_coords(grid)` 호출 | `[(2,2),(3,3)]` (1-index, row-major) |

### 2. Track B — RED 설계표

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|:---|:---|:---|:---|:---|
| **D-LOC-01** | `find_blank_coords` | G1 → `[(2,2),(3,3)]` | I-02 (EmptyCount=2), row-major·1-index | `ModuleNotFoundError` / `ImportError` |

### 3. 테스트 플랜

| 항목 | 내용 |
|:---|:---|
| **파일** | `tests/entity/test_d_loc_01.py` |
| **test 함수명 후보** | `test_d_loc_01_blank_coords_row_major` |
| **conftest 픽스처** | `grid_g1` — G1 격자만 (로직 없음, 상수 튜플/리스트) · 선택: `tests/conftest.py` 또는 동 파일 `@pytest.fixture` |
| **pytest** | `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v` |
| **RED 묶음 범위** | **D-LOC-01** (1건). 동일 파일에 D-LOC-02/03 예약 시 별도 RED 턴 |

**G1 (conftest)**

```python
# grid_g1 — 0-index 저장, 1-index 기대는 (2,2), (3,3)
[[16, 3, 2, 13], [5, 10, 0, 8], [9, 6, 0, 12], [4, 15, 14, 1]]
```

### 4. ECB·Mock 점검

| 점검 | 결과 |
|:---|:---|
| Logic Track → Domain Mock | **금지** — `find_blank_coords` 실 import |
| entity E001~E005 emit | **금지** — `False`/`Exception`만, PRD `message`·`UI_*` assert 없음 |
| import 방향 | entity → control/boundary **금지** |

---

## RED 단계 체크리스트

진행 시 항목을 `- [x]`로 갱신합니다. (권장 순서는 하단 **진행 순서** 참고)

### 공통 준비

- [ ] `tests/fixtures/` 또는 `tests/conftest.py`에 G0~G8·G6·G7 픽스처 정의
- [ ] entity MagicConstant SSOT — `34`, 격자 `16` (리터럴 산재 금지)
- [ ] boundary E001~E007 ↔ PRD `UI_*` 매핑 모듈 1곳만 정의

### Track B — Logic / Domain (`test_d_*.py`, Mock 금지)

**entity**

- [ ] **D-LOC-01** / **D-05** — `find_blank_coords` (G1 → `[(2,2),(3,3)]`) · `test_d_loc_01.py` · `pytest` FAIL
- [ ] **D-06** — `find_not_exist_nums` (G1 → `[7,10]`) · `pytest` FAIL
- [ ] **D-07** — `is_magic_square` (G0 → `True`) · `pytest` FAIL
- [ ] **D-08** — `is_magic_square` (G1 → `False`) · `pytest` FAIL
- [ ] **D-09** — `is_magic_square` (G6 Mom Test 대각) · `pytest` FAIL

**control — 입력 거부** (`False`/`None`만, E00x·message assert 금지)

- [ ] **D-01** — Shape (G2) · `pytest` FAIL
- [ ] **D-02** — EmptyCount (G3) · `pytest` FAIL
- [ ] **D-03** — Range (G4) · `pytest` FAIL
- [ ] **D-04** — Duplicate (G5) · `pytest` FAIL

**control — 유스케이스**

- [ ] **D-10** — `solve` / G1 Step A `int[6]` · `pytest` FAIL
- [ ] **D-11** — reverse 배정만 성공 · `pytest` FAIL
- [ ] **D-12** — G7 해 없음 · `pytest` FAIL
- [ ] **D-13** — control E2E (G1 파이프라인) · `pytest` FAIL

**Logic RED 완료 조건**

- [ ] entity/control에 E001~E005·UX `message` 문자열 없음
- [ ] Logic Track 도메인 Mock 없음
- [ ] `is_magic_square` 검사 순서: 행 → 열 → 대각

### Track A — Boundary / UI (`test_u_*.py`, Mock 허용)

**입력·메시지**

- [ ] **U-IN-02** — G2 → E001 · `pytest` FAIL
- [ ] **U-IN-03** — G3 → E002 · `pytest` FAIL
- [ ] **U-IN-04** — G4 → E003 · `pytest` FAIL
- [ ] **U-IN-05** — G5 → E004 · `pytest` FAIL
- [ ] **U-MSG-01** — U-IN-02~05 PRD `message` 1자 일치
- [ ] **U-IN-01** — `grid=None` → E006 또는 E007 · `pytest` FAIL

**우선순위·출력·흐름·해 없음**

- [ ] **U-PRI-01** — G8 → **E001만** (첫 위반 1개) · `pytest` FAIL
- [ ] **U-OUT-01** — G1 성공 `len(result)==6` · `pytest` FAIL
- [ ] **U-OUT-02** — G1 → `[2,2,7,3,3,10]` · `pytest` FAIL
- [ ] **U-FLOW-02** — `grid=None` → control 0회 · `pytest` FAIL
- [ ] **U-FLOW-01** — G1 → control 1회 · `pytest` FAIL
- [ ] **U-ERR-05** — G7 → E005 · `pytest` FAIL

**Boundary RED 완료 조건**

- [ ] assert: `code`, `message`, 성공 `len==6`, 첫 위반 1개
- [ ] 에러 우선순위: Shape → EmptyCount → Range → Duplicate → Unsolvable → Data
- [ ] entity/control 실구현 의존 없음 (Mock/페이크만)

### 권장 진행 순서 (RED 1건씩)

| 순번 | Track | ID |
|:---:|:---|:---|
| 1–9 | Logic | **D-LOC-01** (D-05) → D-06 → D-07 → D-08 → D-09 → D-10 → D-11 → D-12 → D-13 |
| 10–20 | Boundary | U-IN-02 → U-IN-03 → U-IN-04 → U-IN-05 → U-PRI-01 → U-OUT-01 → U-OUT-02 → U-FLOW-02 → U-FLOW-01 → U-ERR-05 → U-IN-01 |

- [ ] 순번 1~9 Logic RED 전부 완료 (각각 FAIL 확인)
- [ ] 순번 10~20 Boundary RED 전부 완료 (각각 FAIL 확인)

### RED 단계 전체 완료

- [ ] 모든 D-01~D-13 RED 테스트 존재 · 노드별 FAIL 확인
- [ ] 모든 U-* RED 테스트 존재 · 노드별 FAIL 확인
- [ ] G0~G8·G6·G7 픽스처 SSOT 고정
- [ ] RED 중 `src/` 프로덕션 구현 추가 없음 (GREEN은 다음 단계)
- [ ] `pytest tests/ -ra` — 신규 테스트 수집·의도된 FAIL
- [ ] PRD·`.cursorrules`·Mom Test와 불일치 없음

---

## 실행

Python 3.10+ · pytest 8.x (`pyproject.toml`).

```bash
cd c:\DEV\MagicSquare_xx
python -m pip install "pytest>=8.0,<9"
python -m pytest -ra                    # 전체
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v   # RED 진행 중
```

Harness만 있을 때는 테스트 0건(exit 5)일 수 있습니다. RED 테스트 추가 후에는 의도된 **FAIL**이 정상입니다.

---

## 관련 프로젝트

- [MagicSquare_16](https://github.com/fullaheadkoko-source/MagicSquare_16) — 동일 도메인 계약의 구현·Dual-Track TDD 참고 저장소

---

## 라이선스 / 기여

*(미정 — 필요 시 추가)*
