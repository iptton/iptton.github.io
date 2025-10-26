---
title: "白嫖 Github Copilot 的大模型 Api"
date: "2025-05-26"
---

AI Coding 领域，Github Copilot 算是起个大早，赶了个晚集，Vibe Coding 现在成了追赶者，不过胜在财大气粗，今年开始提供了免费使用额度。

![[Pasted image 20250526133153.png]]免费用户可使用 Claude 3.5 / Gemini 2.0 Flash / GPT 4.1 / o3-min 等模型，其中 4.1 次数为 2000 次每月。而 Pro 订阅用户的使用次数为无限次，尽管其订阅是 10 刀一月，但很多开源库作者是被授权免费使用 Pro 版本的。尽管 Github Copilot 的使用不尽如人意，但它的模型不调用实在太可惜了。除了用 Github Copilot 插件和它的网页 ( github.com/copilot ) 外有没办法在我们自己的代码中使用这些模型呢？答案是有的。借助 AI ，查了下 zed 的源码，要调用 Github Copilot 的模型 API ，需要三个步骤：

- 在本地先登录 Github Copilot 插件（vscode 或 jetbrains）
- 从本地文件中读取 oauth_token 
- 根据此  oauth_token 获取 llm apiKey
- 根据 apiKey 调用模型 API

![[Pasted image 20250526135350.png]]
## 读取 oauth_token

配置文件在 mac 下是 `~/.config/github-copilot/apps.json`，windows 下**应该**是 `C:\Users\{username}\AppData\Roaming\GitHub Copilot\apps.json`。文件结构如下：

```json
{
  "github.com:Iv23ctfURkiMfJ4xr5mv":
  {
    "user":"xxx",
    "oauth_token":"xxx",
    "githubAppId":"xxx"
  },
  "github.com:Iv1.b507a08c87ecfe98":
  {
    "user":"xxxx",
    "oauth_token":"xxxxx",
    "githubAppId":"xxx"
  }
}
````

取其中一个 `oauth_token` 值即可（为什么会有两个，我也没搞明白）

## 根据 oauth_token 获取 apiKey

```http
### fetch apiToken  
GET https://api.github.com/copilot_internal/v2/token  
Authorization: token oauth_token  
Accept: application/json
```

返回的内容结构如下：
```json
{
  "token": "......",
  "expires_at": 1748239876,
  ...
}
```

## 通过 apiKey 调用模型 API

```http
### Send POST to github copilot  
POST https://api.githubcopilot.com/chat/completions  
Authorization: Bearer apiKey 
Editor-Version: Zed/1.89.3  
Content-Type: application/json  
Copilot-Integration-Id: vscode-chat

{
	"model": "claude-3.5-sonnet",
	"messages": [
		{
			"role": "user",
			"content": "Hello, how are you?"
		}
	],
	"max_tokens": 100,
	"temperature": 0.7,
	"stream": true
}
```

需要注意的是， stream 参数在 model 为 `o1` 时是无效的，它（当下）始终为 json 返回而非 SSE 返回。

