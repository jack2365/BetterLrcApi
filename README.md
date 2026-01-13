# BetterLrcApi

[English](README.md) | [中文](README_zh-CN.md)

**BetterLrcApi** is a refactored and upgraded version based on the [HisAtri/LrcApi](https://github.com/HisAtri/LrcApi) project. We preserved the core philosophy of the original project while significantly optimizing cover art quality and performance.

Special thanks to the original author [HisAtri](https://github.com/HisAtri) for their open-source contribution.

## ✨ Key Features

*   **High-Res Covers (New)**: Integrated with **Apple Music (iTunes Search API)** to provide official album art up to **3000x3000** resolution, resolving blurry or mismatched cover issues.
*   **Multi-Source Lyrics**:
    *   **Netease**: Default source, high accuracy (Cookie configuration recommended for cloud deployment).
    *   **Kugou**: Automatic fallback source (Supports PC/App dual-interface fallback).
    *   **QQ Music**: **New** tertiary fallback source, cookie-free, ensuring high availability.
*   **High-Performance Architecture**: Migrated from Flask to **FastAPI**, fully supporting Async/Await concurrency for significantly improved response speed.

## 🚀 Quick Start

### Docker Deployment (Recommended)

> Supported Architectures: `linux/amd64`, `linux/arm64`

```bash
# Pull image
docker pull steelydk/betterlrcapi:latest

# Start container (No Auth)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  steelydk/betterlrcapi:latest
  
# Start container (With Auth - Recommended)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  -e API_AUTH="your_secret_key" \
  steelydk/betterlrcapi:latest
```

### Authentication & Configuration

#### 1. API Authentication (API_AUTH)
To prevent API abuse, you can set the `API_AUTH` environment variable.
*   Add `-e API_AUTH=your_secret_key` at startup.
*   Add `Authorization: your_secret_key` header when making requests.

#### 2. Netease Cookie (NETEASE_COOKIE)
**If you encounter 404 errors for lyrics when deploying on cloud servers (GitHub Codespaces, VPS)**, it is usually because the IP is restricted by Netease.
*   **Solution**: Set the `NETEASE_COOKIE` environment variable.
*   **How to get**: Log in to Netease Cloud Music in your browser, open the F12 console, type `document.cookie` and copy it.
*   **Example**:
    ```bash
    docker run -d ... -e NETEASE_COOKIE="MUSIC_U=..." ...
    ```

### Running from Source (Python)

1.  Clone or download this project.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the service:
    ```bash
    # No Auth
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    
    # With Auth
    API_AUTH=your_secret_key python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    ```

## 📚 API Documentation

### 1. Get Cover `/cover`

Get high-quality cover art from Apple Music.

*   **URL**: `/cover`
*   **Method**: `GET` or `POST`
*   **Parameters**:
    *   `keyword`: Song name and artist (Recommended)
    *   `title` + `artist`: Song title and artist name (Compatibility mode, automatically combined for search)
    *   `format`: `redirect` (Default, redirects to image) or `json` (Returns JSON data)

**Example**:
```bash
# Method 1: Keyword Search (Recommended)
GET /cover?keyword=Thinking Out Loud

# Method 2: Split Parameters (Compatible with Audio Station, etc.)
GET /cover?title=Thinking Out Loud&artist=Ed Sheeran
```

### 2. Get Lyrics `/lyrics`

Get lyrics in LRC format.

*   **URL**: `/lyrics`
*   **Method**: `GET` or `POST`
*   **Parameters**:
    *   `keyword`: Song name and artist
    *   `title` + `artist`: Song title and artist name (Compatibility mode)
    *   `format`: `text` (Default, returns plain text) or `json`

**Example**:
```bash
# Method 1: Keyword
GET /lyrics?keyword=Thinking Out Loud

# Method 2: Split Parameters
GET /lyrics?title=Thinking Out Loud&artist=Ed Sheeran
```

### 📱 Compatibility

Perfectly adapted for the following App API formats:
*   **Format 1**: `<url>?title=<title>&artist=<artist>`
*   **Format 2**: `<url>/<artist>/<title>` (Apps automatically convert parameters)
*   **Synology Audio Station**: Native support for its default POST request method.

## 📝 Development & Contribution

This project is licensed under the GPL-3.0 License. Issues and PRs are welcome.

*   Original Author: [HisAtri](https://github.com/HisAtri)
*   BetterLrcApi Developer: [steely/Antigravity]
