 
 
 今天要体验的是 `softgen.ai` ，注册赠送 250k token。

支持纯前端或全栈项目。前端项目指定了使用的架构： `NextJS` / `TailwindCSS`，后端则是和 `Supabase` 深度绑定，提供 `鉴权`/`存储(PostgreSQL DB，文件存储，实时数据更新)`/`Api`/`AI特性`

## 创建项目

![[Pasted image 20250429102714.png]]
为减少干扰，我先创建一个纯前端项目，他那完后的界面如下：
![[Pasted image 20250429110114.png]]

一个非常常见的界面布局。
左侧是交互页面，可以看到有任务列表和历史两个 tab。
右侧是效果预览和代码编辑页，点开 Code Editor，可以看到是一个 nextjs 项目。

## 创建一个静态宣传页(landing page)

```markdown
帮我创建一个落地页，这是一个关于编程辅助工具的介绍页，这个工具是一个渐进式的，可自进化的项目上，它将会分两类，一个是无界面的使用 Kotlin MulitPlatform 实现的跨平台的 agent 及 agent 规范，一个是在 IDEA 上实现的 Agent Client ，未来会支持更多 Agent Client
```
生成效果

![[Pasted image 20250429112254.png]]

生成效果看起来不错。

## 全栈项目

上述页面，已经使用了 0.23/0.25M token 了，再想生成复杂的后台 api 估计已经不够了，按正常的项目流程，我们加一个“申请体验”情节吧：

```markdown
把立即体验和立即开始两个按钮改为“申请体验”并生成一个表单页面，这个页面需用户填三个信息：开发者/非开发者，邮箱，申请理由，填完后发送请求到 /earlyaccess api 并保存到 supabase 中
```

看生成的代码，显然是使用了 NextJS 本身所支持是 web api 能力，但是 supabase 相关的功能并没直接完成，事实上我也没配置过 supabase ，我以为会有个引导页提示我添加相关配置，但什么都没发生，看生成的 api 代码，提供了注释掉的代码，如下：

```typescript
// 这里是模拟保存到 Supabase 的逻辑
// 由于 Supabase 未连接，我们只返回成功响应
// 实际项目中，这里应该调用 Supabase 客户端保存数据
// 当 Supabase 连接后，可以使用类似以下代码：
// const { data: insertData, error } = await supabase
// .from('early_access_requests')
// .insert([
// {
// user_type: data.userType,
// email: data.email,
// reason: data.reason,
// created_at: new Date()
// }
// ]);
// if (error) throw error;
```

## 又一个 v0.dev ?

试试发布？然后那是订阅版的功能，也不能下载，很显然，它并不是另一个 [v0.dev](https://v0.dev) ，它（不像 v0 一样财大气粗）无法支持你白嫖。不过他的和 v0 不是的点是，它号称支持全栈。只是所给的 0.25M token 不足以深度体验。