# MagicSquare_xx (4×4, 빈칸 2개)

부분적으로 채워진 **4×4 마방진**에서 `0`인 **두 칸**에 누락된 수를 배정해 **10선**(행 4 + 열 4 + 대각선 2) 합이 모두 **34**가 되도록 완성하거나, 계약 위반·해 없음을 **표준 코드·문구**로 반환하는 **학습용** 프로젝트입니다.

Mom Test(과거 행동·검증 비용) → 문제 정의 → **PRD 계약** → Dual-Track TDD·ECB 순으로 진행합니다.  
**구현 코드는 아직 없으며**, 현재 단계는 문서·스펙 고정입니다.

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
| 4 | [`Prompting/01.MagicSquare_xx_STEP1_Mom_Test_Interview_prompt.md`](Prompting/01.MagicSquare_xx_STEP1_Mom_Test_Interview_prompt.md) | STEP 1 Cursor 대화 Export |

---

## 저장소 구조

```
MagicSquare_xx/
├── README.md                 ← 이 파일
├── docs/
│   └── PRD.md                ← 스펙 SSOT
├── Report/
│   ├── 01.MagicSquare_xx_STEP1_Mom_Test_Interview_Report.md
│   └── 01.MagicSquare_ProblemDefinition_Report.md
└── Prompting/
    └── 01.MagicSquare_xx_STEP1_Mom_Test_Interview_prompt.md
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

## 개발 방법론 (예정)

| 트랙 | 역할 |
|:---|:---|
| **UI / Boundary** | UX Contract — `message`·첫 위반·성공 형식 |
| **Logic / Domain** | `find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution` |
| **ECB** | boundary → control → entity (역방향 의존 금지) |
| **TDD** | RED → GREEN → REFACTOR (구현 단계에서 적용) |

---

## 실행 (구현 후)

Python 3.10+ · `pytest` 기준으로 문서화되어 있습니다.  
코드·`tests/`·`pyproject.toml`이 추가되면 아래를 채웁니다.

```bash
# 예정
python -m pytest
```

---

## 관련 프로젝트

- [MagicSquare_16](https://github.com/fullaheadkoko-source/MagicSquare_16) — 동일 도메인 계약의 구현·Dual-Track TDD 참고 저장소

---

## 라이선스 / 기여

*(미정 — 필요 시 추가)*
