# BetterLrcApi

**BetterLrcApi** 是基于 [HisAtri/LrcApi](https://github.com/HisAtri/LrcApi) 项目的重构升级版本。我们保留了原项目的核心理念，并针对封面质量和性能进行了大幅优化。

特别感谢原作者 [HisAtri](https://github.com/HisAtri) 的开源贡献。

## ✨ 主要特性

*   **高清封面 (New)**: 接入 **Apple Music (iTunes Search API)**，提供高达 **3000x3000** 分辨率的官方正版专辑封面，彻底解决封面模糊或不匹配的问题。
*   **高性能架构 (New)**: 从 Flask 迁移至 **FastAPI**，完全支持异步 (Async/Await) 并发，响应速度大幅提升。
*   **智能缓存 (New)**: 内置 LRU 内存缓存机制，相同的请求直接从内存返回，毫秒级响应，减少 API 请求限制风险。
*   **歌词获取**: 集成 Netease (网易云音乐) 接口，支持精准歌词搜索。
*   **兼容性**: 保持简洁的 API 设计，易于集成到 StreamMusic、Navidrome 等各类音乐服务中。

## 🚀 快速开始

### Docker 部署 (推荐)

```bash
# 拉取镜像 (假设已推送)
docker pull yourusername/betterlrcapi:latest

# 启动容器
docker run -d \
  -p 8080:8080 \
  --name betterlrcapi \
  yourusername/betterlrcapi:latest
```

### Python 源码运行

1.  克隆或下载本项目
2.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```
3.  启动服务:
    ```bash
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
    ```

## 📚 API 文档

### 1. 获取封面 /cover

获取 Apple Music 高清封面。

*   **URL**: `/cover`
*   **Method**: `GET`
*   **参数**:
    *   `keyword`: 歌曲名和歌手名 (例如: `香水有毒`, `Taylor Swift Love Story`)
    *   `format`: `redirect` (默认，直接跳转图片) 或 `json` (返回 JSON 数据)

**示例**:
```
GET http://localhost:8080/cover?keyword=香水有毒
```

### 2. 获取歌词 /lyrics

获取 LRC 格式歌词。

*   **URL**: `/lyrics`
*   **Method**: `GET`
*   **参数**:
    *   `keyword`: 歌曲名和歌手名
    *   `format`: `text` (默认，返回纯文本) 或 `json`

**示例**:
```
GET http://localhost:8080/lyrics?keyword=香水有毒
```

## 📝 开发与贡献

本项目遵循 GPL-3.0 开源协议。欢迎提交 Issue 或 PR 帮助改进项目。

*   Original Author: [HisAtri](https://github.com/HisAtri)
*   BetterLrcApi Developer: [Your Name/Antigravity]
