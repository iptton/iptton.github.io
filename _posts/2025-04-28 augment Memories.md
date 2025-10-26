
## Memories

Augment Memories 会自动记录用户每次会话的“requirement”，应该是预期解决反复出现 bug 的问题。其内容类似

```markdown
# Project Requirements
- session summary 1
- session summary 2
- ...
```
但估计实现没写好，导致新会话的需求，会受旧会话的影响。比如我所遇到的，前一次会话，要求 Augment 帮我把一个 icon 修改为 `Run`，下一个新起的会话里要求它修复一个 dialog 不显示问题，结果在新会话中，它把前一次修改 icon 的事又做了一遍（并且最后，产生了严重的幻觉，icon 改了没改对，而所提的 bug 并没解决）

也许的解决方法：

- 用 prompt 指示 LLM 分析 memories 的相关度，降低其权重 
- 让用户自行选择任务是否需要关注历史会话