---
title: "whose domain is it anyway"
date: "2020-02-26"
---

https://dannorth.net/2011/01/31/whose-domain-is-it-anyway/

```gherkin
Feature: User logs in
    Scenario: User with valid credentials

    Given an unauthenicated user
    When the user tries to navigate to the welcome page
    Then they should be redirected to the login page
    When the user enters a valid name in the Name field
    And the user enters the corresponding password in Password field
    And the user passes the Login button
    Then they should be directed to the welcome page
```

上例看起来没什么问题。描述一个小常见的登录场景。但让我们看看他使用的**词汇**，可以发现他涉及了好几个领域：

- `unauthenticated`,`valid`,`credentials` 是安全领域的名词，尤其是 unauthenticated user
- `name`,`password` 是基于密码的鉴权领域
- `enters`,`field`,`button` 这是 UI 组件领域
- `login page`, `welcome page` 这些是 web 资源领域

想象一下，如果我们使用这份需求文档，那么：当我们需要从基于密码的验证改为OpenID 或 CAS 验证时，当我们修改UI，从填写变为下拉菜单或单选项时，当我们网站跳转策略改变，登录成功后跳转到个人面板时，都需要对场景进行更新。

是不是觉得这有点太脆弱了？是的，我们犯了些错误，将太多域合并到一个场景里了，造成了意外的复杂性。因为我们没注意**场景的受众**。

### Unpacking the domain

仔细想想，这个场景的意图是：_有合法授权的用户有访问权限_ 。

当我们和产品讨论后台丢包，延时时，他们并不会感兴趣，但我们换个说法，页面会卡顿，那他就很感兴趣了。同样，如果我们发现有丢包问题，但没人关注，那这通常意味着，后台同学不在，或者这是一个多余的需求（比如，你问鉴权要不要有一个物理token卡呀，没人感兴趣，那这个应该就是多余的了）。所以，同一件事，在不同的领域，有不同的表述。

回到登录例子。例中每一个领域都会引入一个额外的相关方，而他们的需求随时都有可能会变化。所以，要避免脆弱，我们需要把相关方数量最小化。最简单最有用的的场景，应该只涉及两个领域（即两个相关方）：场景**标题领域**（问题 / What）及场景**步骤领域**（解决方案 / how）。我们不能把标题去掉，因为这样无法解释场景的价值/意图。任何额外的领域，都会导致场景的脆弱。

例中的 _what_ 为"使用合法鉴权进行登录"，_how_ 为“使用帐号密码验证用户身份”。 _how_ 中关于按钮如何点击，并没为我们的 _what_ 增加价值，因此，我们可以重新组织场景描述：

```gherkin
Feature: User Login

Scenario: User with valid credentials
Given an unauthenticated user
When the user tries to access a restricted asset
Then they should be directed to a login page
When the user submits valid credentials
Then they should be redirected back to the restricted content
```

现在，我们确实有两个领域了，即 _what_ 为 用户鉴权（words like _unauthenticated_, _user_, _credentials_），_how_ 为 基于网络的安全（_restricted asset_, _submits_, _redirected_, _content_）。这些领域变化时，我们的场景脚本也要跟着变。

注意，我们并没详细描述“submits valid credentials”，我们把这个放到步骤的定义中去。

### Chunking - or the myth of "declarative"

NLP 称一个技术为 “chunking"，在解决或提供选项时非常有用。对任何语句，你都可以在前面加个“为什么”(why or what for，中文，都是为什么...)或“如何”。why问得越多，涉及的面就越广，how 问得越多，细节就越丰富。你还可以通过问“如果不这样，还能怎样”得到更多。

本文例中登录场景，如果问一句“你要登录做什么”也许答案是出于限制原因或监管原因限制访问高级内容，如果是前者，可以继续问“你还能如何限制访问权限”，也许还能通过 ip 或 mac 地址限制或 cookie 或单点登录等方式来限制。然后，我们可以细分，考虑解决方案：如何过滤 mac 地址，会带来什么安全问题？

一旦意识到你可以问“为什么”，“如何”，那在任何抽象层次上，“声明式”或“命令式”之类的概念就变得有相对联系了。SQL 通常被描述为声明式语言，你描述了你需要**什么(what)**，但并没告诉 DB 要**如何(how)**找出来，但是 `select employee_id, salary from employees where salary > 100000` 又应当视为命令式的，因为它具体描述了what 以及 how 。

### 谨慎使用域语言

因此，在编写场景时要牢记，你要为两个受众编写，该功能所针对的人员及实现该功能的人。检查措辞看是否可以从问题或解决方案中发现任何东西。如果发现你使用的是这两个领域之外的语言，那可能是过于细节，也可能是指定了不必要的广泛需求。

如果你真的需要关注行为的实现细节，那可能应该在其他更细粒度的场景上进行。
