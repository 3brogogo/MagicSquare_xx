# review-ecb — ECB·계약 정적 리뷰

**역할**: MagicSquare_xx 저장소의 ECB·PRD 계약 위반만 검사한다.  
**금지**: 파일 생성·수정·삭제·포맷·리팩터·테스트 추가. **코드 변경 일체 금지.**

**SSOT**: `docs/PRD.md`, `.cursorrules`, `.cursor/skills/magic-square-tdd/SKILL.md`

---

## 수행 절차

1. `src/boundary`, `src/control`, `src/entity`, `tests/boundary`, `tests/control`, `tests/entity`를 **읽기만** 한다.
2. 아래 5개 체크 항목마다 위반 후보를 수집한다 (없으면 “위반 없음”).
3. 결과를 **표만** 출력한다. 장문 설명·수정 제안·패치 diff **금지**.
4. 응답 첫 줄: `Review: ECB·계약 (read-only)`

---

## 체크 항목 (5종)

### 1) import 방향 (ECB)

| 허용 | 금지 |
|:---|:---|
| `boundary` → `control`, `entity` | `entity` → `control`, `boundary` |
| `control` → `entity` | `control` → `boundary` |

- `from entity`, `from control`, `from boundary` 및 상대 import 모두 검사.
- `tests/`에서 Logic이 `boundary`를 import하는지도 표기.

### 2) entity·control — E001~E005 처리 금지

| 코드 | 금지 위치 |
|:---|:---|
| E001~E005 | `src/entity`, `src/control` |

- 문자열·상수: `E001`…`E005`, `UI_INVALID_SHAPE` 등 PRD UX 코드를 entity/control에서 **발행·매핑·message 하드코딩**하면 위반.
- 입력 Shape/EmptyCount/Range/Duplicate/Unsolvable **검증 로직**이 entity/control에 있으면 위반 (boundary 전담).

### 3) `int[6]` · 1-index 계약

- 성공 반환·테스트 기대: `[r1, c1, n1, r2, c2, n2]`, 좌표 **1-index (1..4)**.
- 0-index 좌표 반환·길이 ≠ 6·필드 순서 변경은 위반.
- `control`/`boundary` 조립부와 `tests/**` assert를 대상으로 검사.

### 4) MagicConstant SSOT

- **34**, 격자 **16** (및 PRD 마방진 상수)는 `entity` 상수(또는 프로젝트가 정한 단일 SSOT 모듈) **한 곳**만 허용.
- `src/`·`tests/` 전역에서 리터럴 `34`, `16` 산재 시 위반으로 기록 (SSOT 정의 줄 제외).

### 5) Logic Track — Domain Mock 금지

- 대상: `tests/entity/**`, `tests/control/**`, `test_d_*.py`
- `unittest.mock`, `MagicMock`, `patch`, `pytest-mock` 등으로 **entity/control 도메인**을 대체하면 위반.
- `tests/boundary`의 Mock은 **검사 대상 아님** (UI Track 허용).

---

## 출력 형식 (표만)

### 요약

| 체크 | 결과 | 위반 건수 |
|:---|:---|:---:|
| import 방향 | PASS / FAIL | n |
| entity E001~E005 | PASS / FAIL | n |
| int[6] 1-index | PASS / FAIL | n |
| MagicConstant SSOT | PASS / FAIL | n |
| Logic Domain Mock | PASS / FAIL | n |

### 위반 상세 (FAIL 항목만; 전부 PASS면 “위반 없음” 한 줄)

| # | 체크 | 파일:줄(또는 파일) | 위반 내용 |
|:---:|:---|:---|:---|

- PASS인 체크는 상세 표에 **행을 넣지 않는다**.
- 근거는 한 셀에 짧게 (예: `entity/foo.py:12 entity→control import`).

---

## 검사 범위 외 (본 Command에서 다루지 않음)

- 테스트 통과 여부·커버리지·성능
- E006~E007 boundary 매핑 정확도 (별도 UI 리뷰)
- git commit / push

**다시 강조: 이 Command 실행 중 어떤 파일도 수정하지 말 것.**
