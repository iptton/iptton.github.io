---
title: "BDD 反模式二则(from cucumber)"
date: "2020-03-05"
---

https://cucumber.io/docs/guides/anti-patterns/

cucumber 官网描述的一些反模式：

## 与 Feture 绑定的步骤定义(Feature-coupled step defineinions)

这类步骤定义无法跨 Feature 或 Scenario 使用。会导致产生大量，重复的代码，进而影响维护成本 。

**例：假设一个简历应用，可能有以下 Feature 与 步骤定义**

```
features/
+--edit_work_experience.feature
+--edit_languages.feature
+--edit_education.feature
+--steps/
   +--edit_work_experience_steps.java
   +--edit_languages_steps.java
   +--edit_education_steps.java
```

`edit_work_experience.feature` 可能有以下场景：

```gherkin
Feature: x
    Scenario: add description
        Given I have a CV and I'm on the edit description page
        And I fill in "Description" with "Cucumber BDD tool"
        When I press "Save"
        Then I should see "Cucumber BDD tool" under "Descriptions"
```

步骤实现 `edit_work_experience_steps.java` ：

```kotlin
init{
  Given("I have a CV and I'm on the edit description page"){
    val employee = Employee("Sally")
    employee.createCV()
  }
}
```

**如何避免**

- 通过领域概念来组织你的步骤定义
- 使用领域相关的命名（而不是和 feature, scenario 相关）你的步骤定义文件

## 组合步骤 （ Conjunction steps )

不要在一个步骤定义中做太多事情，这会使得步骤难以复用。Cucumber 提供了 `And` , `But` 就是为了解决这个问题。

```gherkin
Given I have shades
And I have a brand new Mustang
```

Cucumber 设计成不允许在 feature 中进行步骤互相调用，因此，如果要复用，要考虑在步骤定义代码中抽象出复用的部分到类，方法。

http://www.thinkcode.se/blog/2016/06/22/cucumber-antipatterns
