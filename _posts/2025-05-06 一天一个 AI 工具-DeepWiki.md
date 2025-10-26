DeepWiki 的官方介绍：DeepWiki provides up-to-date documentation you can talk to, for every repo in the world. Think Deep Research for GitHub.
> 一款辅助你了解  Github 代码仓库的工具，Github 上的 DeepResearch。

这是一款 Web 工具，它可以缓存全网使用者的查询和索引，因此一些流行的代码仓库查询会非常快。

以下是一个使用场景，我希望快速理解开源的 AI 辅助工具 `AutoDev`的 sketch 逻辑
p
1. 点击 **Add repo** 
2. 输入 AutoDev 点击出现的第一个结果

![[Pasted image 20250506222426.png]]

3. 此时，如果仓库已经被索引，相当于已经进入了一个结构化了的 Wiki
![[Pasted image 20250506223244.png]]
4. 但这个 wiki 是用英文显示的，而且内容实在太多了，如果你要了解具体某个话题的内容，可以在在底部用中文输入你所想要了解的问题，比如：Sketch 是如何工作的
5. DeepWiki 会搜索相关的文件并做出总结，在左侧显示结果，右侧显示相应的文件（这非常重要）
![[Pasted image 20250506222759.png]]
与多数 AI 对话平台一样，你可以持续地进行追问，这对了解一个开源库非常有用。

不过这个平台有一个限制，它不会对所有仓库都进行索引（也许是根据流行程度来决定，比如 star 数），如果公开仓库未符合它的要求，你需要填写需求
![[Pasted image 20250506223651.png]]

而如果你需要对自己的私有仓库进行索引，那就需要付费了（但个人认为，如果代码质量一般，AI 也许生成的效果也不太行）

