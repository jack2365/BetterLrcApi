# BetterLrcApi

[English](README.md) | [中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Русский](README_ru.md)

**BetterLrcApi**는 [HisAtri/LrcApi](https://github.com/HisAtri/LrcApi) 프로젝트를 기반으로 리팩토링 및 업그레이드된 버전입니다. 원본 프로젝트의 핵심 철학을 유지하면서 커버 아트 품질과 성능을 크게 최적화했습니다.

오픈 소스 기여에 대해 원작자 [HisAtri](https://github.com/HisAtri) 님께 특별히 감사드립니다.

## ✨ 주요 기능

*   **고해상도 커버 (New)**: **Apple Music (iTunes Search API)** 과 연동하여 최대 **3000x3000** 해상도의 공식 앨범아트를 제공하며, 흐릿하거나 일치하지 않는 커버 문제를 완벽하게 해결했습니다.
*   **멀티 소스 가사**:
    *   **Netease (넷이즈)**: 기본 소스, 높은 정확도 (클라우드 배포 시 쿠키 설정 권장).
    *   **Kugou (쿠거우)**: 자동 대체 소스 (PC/App 듀얼 인터페이스 폴백 지원).
    *   **QQ Music (QQ뮤직)**: **신규** 3차 대체 소스, 쿠키 불필요, 고가용성 보장.
*   **고성능 아키텍처**: Flask에서 **FastAPI**로 마이그레이션하여 Async/Await 동시성을 완벽하게 지원, 응답 속도를 대폭 향상시켰습니다.

## 🚀 빠른 시작

### Docker 배포 (권장)

> 지원 아키텍처: `linux/amd64`, `linux/arm64`

```bash
# 이미지 풀
docker pull steelydk/betterlrcapi:latest

# 컨테이너 시작 (인증 없음)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  steelydk/betterlrcapi:latest
  
# 컨테이너 시작 (인증 포함 - 권장)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  -e API_AUTH="your_secret_key" \
  steelydk/betterlrcapi:latest
```

### 인증 및 구성

#### 1. API 인증 (API_AUTH)
API 남용을 방지하기 위해 `API_AUTH` 환경 변수를 설정할 수 있습니다.
*   시작 시 `-e API_AUTH=your_secret_key` 추가.
*   요청 시 헤더에 `Authorization: your_secret_key` 추가.

#### 2. Netease 쿠키 (NETEASE_COOKIE)
**클라우드 서버(GitHub Codespaces, VPS)에 배포할 때 가사 404 오류가 발생하는 경우**, 일반적으로 Netease에 의해 IP가 제한되기 때문입니다.
*   **해결책**: `NETEASE_COOKIE` 환경 변수를 설정합니다.
*   **가져오는 방법**: 브라우저에서 넷이즈 클라우드 뮤직에 로그인하고 F12 콘솔을 열어 `document.cookie`를 입력하고 복사합니다.
*   **예시**:
    ```bash
    docker run -d ... -e NETEASE_COOKIE="MUSIC_U=..." ...
    ```

### 소스 코드에서 실행 (Python)

1.  이 프로젝트를 복제하거나 다운로드합니다.
2.  의존성 설치:
    ```bash
    pip install -r requirements.txt
    ```
3.  서비스 시작:
    ```bash
    # 인증 없음
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    
    # 인증 포함
    API_AUTH=your_secret_key python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    ```

## 📚 API 문서

### 1. 커버 가져오기 `/cover`

Apple Music에서 고품질 커버 아트를 가져옵니다.

*   **URL**: `/cover`
*   **Method**: `GET` 또는 `POST`
*   **Parameters**:
    *   `keyword`: 노래 제목 및 아티스트 (권장)
    *   `title` + `artist`: 노래 제목 및 아티스트 이름 (호환성 모드, 검색을 위해 자동으로 결합됨)
    *   `format`: `redirect` (기본값, 이미지로 리디렉션) 또는 `json` (JSON 데이터 반환)

**예시**:
```bash
# 방법 1: 키워드 검색 (권장)
GET /cover?keyword=Thinking Out Loud

# 방법 2: 매개변수 분할 (Audio Station 등과 호환)
GET /cover?title=Thinking Out Loud&artist=Ed Sheeran
```

### 2. 가사 가져오기 `/lyrics`

LRC 형식으로 가사를 가져옵니다.

*   **URL**: `/lyrics`
*   **Method**: `GET` 또는 `POST`
*   **Parameters**:
    *   `keyword`: 노래 제목 및 아티스트
    *   `title` + `artist`: 노래 제목 및 아티스트 이름 (호환성 모드)
    *   `format`: `text` (기본값, 일반 텍스트 반환) 또는 `json`

**예시**:
```bash
# 방법 1: 키워드
GET /lyrics?keyword=Thinking Out Loud

# 방법 2: 매개변수 분할
GET /lyrics?title=Thinking Out Loud&artist=Ed Sheeran
```

### 📱 호환성

다음 앱 API 형식에 완벽하게 적용됩니다:
*   **Format 1**: `<url>?title=<title>&artist=<artist>`
*   **Format 2**: `<url>/<artist>/<title>` (앱이 자동으로 매개변수 변환)
*   **Synology Audio Station**: 기본 POST 요청 방식을 기본적으로 지원합니다.

## 📝 개발 및 기여

이 프로젝트는 GPL-3.0 라이선스에 따라 라이선스가 부여됩니다. 문제(Issue) 및 PR 제출을 환영합니다.

*   Original Author: [HisAtri](https://github.com/HisAtri)
*   BetterLrcApi Developer: [steely/Antigravity]
