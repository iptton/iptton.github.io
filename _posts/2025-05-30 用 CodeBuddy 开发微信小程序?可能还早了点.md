 最近公众号上看到很多**腾讯*悄悄*上线了 CodeBuddy 的博文**，想试试把昨天在 v0 上实现了的习惯积分系统，用 CodeBuddy 的看能不能搞掂，结果挺失望的。

创建一个小程序项目后，打开 `CodeBuddy`

![[Pasted image 20250530092456.png]]

 输入与 v0.dev 上用过的提示词（修改了指标*使用 web 界面*为*使用微信小程序页面*）

> Develop a habit tracking and reward system for a 7-year-old girl, accessible via a wechat mini program interface. The system should feature a daily view displaying the current date and a log of habit-related point additions and subtractions. Implement a settings page where users can define specific habits, assign positive or negative point values to each, and establish a list of rewards associated with cumulative point thresholds. The system should provide visual or auditory notifications when a user's accumulated points reach a reward threshold. Include a mechanism for redeeming rewards, which automatically deducts the corresponding points from the total and logs the redemption event. The design should be user-friendly and visually appealing for a child, with clear indicators for point values and reward statuses.

提示我任务太复杂，问我要从哪开始

![[Pasted image 20250530092658.png]]

面对 AI 时，人类从不做回答开放性问题，甚至不愿意做选择题。只希望先做一版出来体验得到再提意见（像不像你老板的要求？）

> 请帮我规划开发顺序并自动执行

![[Pasted image 20250530092851.png]]
AI 牛马被成功 PUA ，一顿操作后，页面还是那个演示页面。看了下目录结构，原来它没有把 index 替换掉。

> 请把首页替换成我所要的内容

内容出来了。至此为止，放弃吧。

![[Pasted image 20250530093811.png]]


----

换个  `Augument` 上吧

> 这是一个微信小程序，它是一个习惯/积分兑换应用，原代码有不少错误，请帮我修正，它的原始需求如下：  
>
> Develop a habit tracking and reward system for a 7-year-old girl, accessible via a wechat mini program interface. The system should feature a daily view displaying the current date and a log of habit-related point additions and subtractions. Implement a settings page where users can define specific habits, assign positive or negative point values to each, and establish a list of rewards associated with cumulative point thresholds. The system should provide visual or auditory notifications when a user's accumulated points reach a reward threshold. Include a mechanism for redeeming rewards, which automatically deducts the corresponding points from the total and logs the redemption event. The design should be user-friendly and visually appealing for a child, with clear indicators for point values and reward statuses.  

若干次调试后，功能基本可用了。

![[0f412c7f788535b4b88646880010bb0a.jpg]]