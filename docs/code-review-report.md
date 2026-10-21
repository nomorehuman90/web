# 프론트엔드·백엔드 코드 리뷰 보고서

- 검토일: 2026-10-20
- 범위: `frontend` Vue 앱, `app` FastAPI 앱, Kakao 로그인 연동 및 주변 인증 설정
- 방식: 프론트엔드·백엔드 독립 읽기 전용 리뷰 후 취합
- 코드 변경: 없음
- 테스트: 프로젝트 지침에 따라 실행하지 않음

## 요약

카카오 로그인의 401을 일으킬 수 있는 직접 원인이 프론트엔드와 백엔드 양쪽에 있습니다. 프론트엔드는 닉네임 동의만 요청하지만 백엔드는 이메일과 이메일 검증 상태를 필수로 검사합니다. 또한 현재 백엔드 실행 환경에는 `KAKAO_CLIENT_SECRET`이 없고, Kakao 문서상 REST API 키의 Client Secret은 기본 활성화되므로 토큰 교환이 실패할 가능성이 높습니다.

우선순위가 높은 항목은 다음과 같습니다.

1. 이메일 scope를 요청하고 Kakao 동의 항목 설정을 맞춥니다.
2. Client Secret을 백엔드 환경변수로 설정합니다.
3. REST API 키와 리다이렉트 URI 하드코딩을 설정값으로 대체합니다.
4. 인증 오류를 단계별로 구분해 진단할 수 있게 합니다.

## 프론트엔드 발견 사항

### 높음 — 이메일 동의 scope가 누락됨

- 위치: `frontend/src/App.vue:136`
- 현재 Kakao 로그인 요청은 `profile_nickname`만 요청합니다. 백엔드 `app/api/routers/user.py:97-98`은 이메일, `is_email_valid`, `is_email_verified`가 모두 있어야 로그인합니다. 따라서 이메일 동의를 새로 받지 못한 사용자는 백엔드에서 401을 받습니다.
- 조치: `account_email,profile_nickname` scope를 요청하고 Kakao Developers에서 두 동의 항목을 설정합니다. 이메일 동의를 거부하거나 Kakao가 검증된 이메일을 제공하지 않는 경우 로그인을 거절하는 현재 정책은 유지됩니다.

### 낮음 — JavaScript 키가 소스에 고정됨

- 위치: `frontend/src/App.vue:10`
- JavaScript 키가 코드에 직접 지정되어 환경별 키 변경과 회전이 불편합니다.
- 조치: `VITE_KAKAO_JS_KEY` 환경변수에서 읽고, Kakao Developers에서 사용할 웹 도메인만 허용합니다. JavaScript 키는 브라우저에서 보이는 키이므로 도메인 제한이 중요합니다.

### 낮음 — 예외적인 OAuth callback에서 로그인 state가 남음

- 위치: `frontend/src/App.vue:201-221`
- `/login`으로 돌아왔지만 `code`와 `error`가 모두 없는 경우 `kakao_login_state`가 `sessionStorage`에 남고 사용자에게 오류가 표시되지 않습니다.
- 조치: `/login` callback을 처리할 때 state를 항상 정리하고, 예상하지 못한 callback에는 재시도 안내를 표시합니다.

## 백엔드 발견 사항

### 높음 — Client Secret 미설정으로 토큰 교환 실패 가능

- 위치: `app/api/routers/user.py:68-69`, `app/core/config.py:14`
- 프로젝트 `.env`와 백엔드 프로세스 환경에서 `KAKAO_CLIENT_SECRET`을 찾지 못했습니다. 설정이 비어 있으면 토큰 요청에 `client_secret`을 넣지 않습니다. Kakao는 REST API 키의 Client Secret을 기본 활성화 상태로 제공하며, 활성화된 키는 토큰 요청에 secret이 필수입니다.
- 조치: Kakao Developers에서 해당 REST API 키의 Client Secret을 확인해 백엔드 `.env`에 `KAKAO_CLIENT_SECRET`으로 설정하고 백엔드를 재시작합니다. 비밀값은 프론트엔드나 문서에 넣지 않습니다.
- 참고: [Kakao 토큰 요청 문서](https://developers.kakao.com/docs/ko/kakaologin/rest-api)

### 높음 — REST API 키와 redirect URI가 코드에 고정됨

- 위치: `app/api/routers/user.py:59-65`
- REST API 키 설정값은 존재 여부만 확인하고 실제 토큰 요청은 코드에 직접 지정된 키를 사용합니다. `KAKAO_REDIRECT_URI` 설정도 무시됩니다. 다른 앱 키나 프론트 callback 주소를 설정해도 토큰 교환에 반영되지 않습니다.
- 조치: 코드의 고정값을 `settings.KAKAO_REST_API_KEY`, `settings.KAKAO_REDIRECT_URI`로 교체합니다. 인가 요청, Kakao Developers 등록값, 토큰 교환의 URI는 프로토콜·호스트·포트·경로까지 정확히 같아야 합니다.
- 참고: [Kakao 리다이렉트 URI FAQ](https://developers.kakao.com/docs/ko/kakaologin/faq)

### 중간 — Kakao 오류를 모두 같은 401로 변환

- 위치: `app/api/routers/user.py:86-87`
- 토큰 교환 또는 사용자 정보 조회의 `HTTPError`가 모두 `Kakao authorization failed.`로 바뀝니다. 원래 Kakao 오류 코드와 실패 단계가 사라져 Client Secret, redirect URI, 만료된 인가 코드 등을 구분하기 어렵습니다.
- 조치: 로그에는 실패 단계와 Kakao 오류 코드만 남기고, 인가 코드·토큰·키·이메일은 기록하지 않습니다. 사용자 응답은 안전한 안내 문구로 유지합니다.

### 높음 — 기본 JWT 서명 키가 고정값임

- 위치: `app/core/config.py:10`
- `SECRET_KEY`가 설정되지 않으면 소스에 있는 고정 기본값으로 JWT를 서명합니다. 이 값으로 운영하면 외부인이 위조 토큰을 만들 수 있습니다.
- 조치: 운영 환경에서 강한 임의 `SECRET_KEY`를 필수화하고 기본값이면 시작을 거부합니다.

### 높음 — 로컬 계정 비밀번호를 평문 저장·비교

- 위치: `app/api/routers/user.py:19`, `app/api/routers/user.py:41`, `app/api/routers/user.py:47`
- 회원가입 비밀번호를 그대로 저장하고 로그인에서 평문 문자열을 비교합니다. DB가 노출되면 계정 비밀번호도 그대로 노출됩니다.
- 조치: Argon2id 또는 bcrypt 해시로 저장하고 검증 함수로 비교합니다. 기존 평문 계정은 안전한 재설정 또는 단계적 해시 전환 계획이 필요합니다.

### 중간 — 동시 첫 카카오 로그인에서 DB 오류가 처리되지 않음

- 위치: `app/api/routers/user.py:102-115`
- 같은 Kakao 계정의 첫 로그인이 동시에 처리되면 두 요청이 모두 신규 계정이라고 판단할 수 있습니다. `kakao_id` unique 인덱스 충돌을 처리하지 않아 요청이 500으로 끝날 수 있습니다.
- 조치: `IntegrityError`를 rollback한 뒤 이미 생성된 계정을 다시 조회하거나, DB의 원자적 upsert를 사용합니다.

### 중간 — 이메일 정규화와 중복 조회 기준이 완전히 같지 않음

- 위치: `app/api/routers/user.py:100-103`
- 입력은 Python `casefold()`로 정규화하지만 기존 이메일 조회는 SQLite `lower(trim(...))`에 의존합니다. SQLite `lower()`는 일반적으로 ASCII 위주라 일부 유니코드 주소의 대소문자 변형을 같은 값으로 판정하지 못할 수 있습니다. 이메일 고유 인덱스도 없습니다.
- 조치: 로컬·카카오 계정 생성과 로그인에서 동일한 정규화 규칙을 적용하고, 데이터 정리 후 정규화 이메일에 고유 제약을 둡니다.

### 중간 — 인증 쿠키가 항상 `Secure` 없이 발급됨

- 위치: `app/api/routers/user.py:24-29`, `app/api/routers/user.py:117-122`
- `secure=False`로 설정되어 HTTPS 운영 환경에서도 쿠키가 보안 연결에 제한되지 않습니다.
- 조치: 개발·운영 설정에 따라 HTTPS 운영에서는 `Secure`를 켭니다.

### 낮음 — 문서의 DB 파일명과 실제 기본값이 다름

- 위치: `AGENTS.md`의 SQLite 설명, `app/core/config.py:12`
- 프로젝트 지침은 `app.db`를 설명하지만 앱 기본 URL은 `db.sqlite3`입니다. 기존 데이터를 `app.db`에 보관하고 있다면 앱이 다른 DB를 사용할 수 있습니다.
- 조치: 의도한 DB 파일을 확인하고 `DATABASE_URL`을 명시합니다.

## 권장 처리 순서

1. Kakao scope와 동의 항목, Client Secret, redirect URI를 설정과 코드에서 일치시킵니다.
2. 인증 경로의 Kakao 오류를 안전하게 진단할 수 있도록 보완합니다.
3. 운영 전 JWT 기본 키, 평문 비밀번호, HTTPS 쿠키 문제를 처리합니다.
4. DB 이메일 정규화·고유성 및 동시 로그인 처리를 보완합니다.

