# BetterLrcApi

**BetterLrcApi** 是基于 [HisAtri/LrcApi](https://github.com/HisAtri/LrcApi) 项目的重构升级版本。我们保留了原项目的核心理念，并针对封面质量和性能进行了大幅优化。

特别感谢原作者 [HisAtri](https://github.com/HisAtri) 的开源贡献。

## ✨ 主要特性

*   **高清封面 (New)**: 接入 **Apple Music (iTunes Search API)**，提供高达 **3000x3000** 分辨率的官方正版专辑封面，彻底解决封面模糊或不匹配的问题。
*   **多源歌词**: 
    *   **Netease (网易云)**: 默认源，精准度高 (云端部署建议配置 Cookie)。
    *   **Kugou (酷狗)**: 自动备选源 (支持 PC/App 双接口 fallback)。
    *   **QQ Music (QQ音乐)**: **新** 三级备选源，无需 Cookie，极高可用性。
*   **高性能架构**: 从 Flask 迁移至 **FastAPI**，完全支持异步 (Async/Await) 并发，响应速度大幅提升。

## 🚀 快速开始

### Docker 部署 (推荐)

> 支持架构: `linux/amd64`, `linux/arm64`

```bash
# 拉取镜像
docker pull steelydk/betterlrcapi:latest

# 启动容器 (无鉴权)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  steelydk/betterlrcapi:latest
  
# 启动容器 (带鉴权 - 推荐)
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  -e API_AUTH="your_secret_key" \
  steelydk/betterlrcapi:latest
```

### 鉴权说明 (Auth & Cookie)

#### 1. API 鉴权 (API_AUTH)
为了防止接口被滥用，您可以设置环境变量 `API_AUTH` 来启用鉴权。
*   启动时添加 `-e API_AUTH=your_secret_key`。
*   调用时 Header 添加 `Authorization: your_secret_key`。

#### 2. 网易云 Cookie (NETEASE_COOKIE)
**如果您在云服务器（GitHub Codespaces, VPS）上部署遇到歌词 404**，通常是因为 IP 被网易云限制。
*   **解决方案**: 设置 `NETEASE_COOKIE` 环境变量。
*   **获取方法**: 在浏览器登录网易云及其，F12 控制台输入 `document.cookie` 复制即可。
*   **启动示例**:
    ```bash
    docker run -d ... -e NETEASE_COOKIE="MUSIC_U=..." ...
    ```

### Python 源码运行

1.  克隆或下载本项目
2.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```
3.  启动服务:
    ```bash
    # 无鉴权
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    
    # 带鉴权
    API_AUTH=your_secret_key python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    ```

## 📚 API 文档

## 📚 API 文档
### 1. 获取封面 `/cover`

获取 Apple Music 高清封面。

*   **URL**: `/cover`
*   **Method**: `GET` 或 `POST`
*   **参数**:
    *   `keyword`: 歌曲名和歌手名 (推荐)
    *   `title` + `artist`: 歌曲名和歌手名 (兼容模式，会自动合并搜索)
    *   `format`: `redirect` (默认，直接跳转图片) 或 `json` (返回 JSON 数据)

**示例**:
```bash
# 方式 1: 关键字搜索 (推荐)
GET /cover?keyword=香水有毒

# 方式 2: 拆分参数 (兼容 Audio Station 等 APP)
GET /cover?title=Thinking Out Loud&artist=Ed Sheeran
```

### 2. 获取歌词 `/lyrics`

获取 LRC 格式歌词。

*   **URL**: `/lyrics`
*   **Method**: `GET` 或 `POST`
*   **参数**:
    *   `keyword`: 歌曲名和歌手名
    *   `title` + `artist`: 歌曲名和歌手名 (兼容模式)
    *   `format`: `text` (默认，返回纯文本) 或 `json`

**示例**:
```bash
# 方式 1: 关键字
GET /lyrics?keyword=香水有毒

# 方式 2: 拆分参数
GET /lyrics?title=Thinking Out Loud&artist=Ed Sheeran
```

### 📱 兼容性 (Compatibility)

完美适配以下 APP 的 API 格式：
*   **Format 1**: `<url>?title=<title>&artist=<artist>`
*   **Format 2**: `<url>/<artist>/<title>` (APP 会自动转换参数)
*   **Synology Audio Station**: 原生支持其默认的 POST 请求方式。

## 📝 开发与贡献

本项目遵循 GPL-3.0 开源协议。欢迎提交 Issue 或 PR 帮助改进项目。

*   Original Author: [HisAtri](https://github.com/HisAtri)
*   BetterLrcApi Developer: [steely/Antigravity]
