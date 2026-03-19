# 使用说明（中文版）

这份文档面向使用者，而不是开发者。

如果你想知道这个项目现在能怎么用、适合什么场景、每一步怎么操作，看这份就够了。

## 这是什么

这是一个可被 AI Agent 调用的 PPT 生成后端原型。

它不是单纯的 PPT 模板脚本，也不是完整的 research agent。

你可以把它理解成：

- 上游 AI Agent：负责理解需求、收集资料、做研究、整理上下文
- 这个项目：负责把输入整理成 deck JSON，并生成 PowerPoint 文件

也就是：

`需求 + 资料 -> deck JSON -> PPTX`

## 适合什么场景

现在比较适合这些场景：

- 产品规划汇报
- 管理层汇报
- 销售方案 deck
- 项目复盘 deck
- 培训课件初稿
- 基于官网资料、PDF、DOCX、Markdown 生成演示文稿
- 先生成一版，再反复修订优化

## 现在能做什么

### 1. 从现成 JSON 直接生成 PPT

适合你已经有结构化 deck 数据的情况。

命令：

```bash
npm run generate
```

输入文件：

- `sample-input.json`

输出文件：

- `output/sample-deck.pptx`

### 2. 从一句自然语言生成 PPT

适合你只有一个大致需求描述的情况。

命令：

```bash
npm run generate:mock
```

如果你已经配置了模型，也可以用：

```bash
npm run generate:prompt
```

手动命令示例：

```bash
node generate-from-prompt.js --prompt "Create an 8-slide AI product strategy deck for executives in a professional tone"
```

### 3. 带资料来源一起生成 PPT

这是现在更推荐的方式。

适合你除了需求描述之外，还能提供一些资料，例如：

- 产品介绍文档
- 官网链接
- PDF
- DOCX
- Markdown 说明文档

命令：

```bash
npm run generate:source
```

它会读取：

- `sample-source-brief.md`

你也可以自己传资料：

```bash
node generate-from-prompt.js --mock --prompt "Create an 8-slide strategy deck" --source your-brief.md --source https://example.com/product
```

### 4. 修订已有 deck

适合你已经生成了一版 PPT，接下来想继续优化。

比如你可以要求它：

- 压缩页数
- 更结论导向
- 强调执行计划
- 调整结构
- 让内容更适合管理层汇报

命令：

```bash
npm run revise:mock
```

手动命令：

```bash
node revise-deck.js --deck output/generated-deck.json --prompt "Compress this deck, make it more conclusion-driven, and emphasize the execution plan"
```

### 5. 作为 skill 被其他 agent 调用

适合你把这个项目接进别的 agent 流程。

命令：

```bash
npm run skill:create
npm run skill:revise
```

相关文件：

- `agent-skill.js`
- `sample-agent-request.json`
- `sample-agent-revise-request.json`
- `skill-manifest.json`

### 6. 作为 HTTP 服务使用

适合你希望通过本地 API 的方式调用它。

启动服务：

```bash
npm run skill:server
```

健康检查：

```bash
curl http://localhost:3010/health
```

调用接口：

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
```

## 资料来源现在怎么处理

这是当前产品里比较重要的一部分。

现在支持的来源包括：

- 本地文本文件：`txt`、`md`、`csv`、`json`、`yaml`、`xml`
- 本地 HTML
- 本地 PDF
- 本地 DOCX
- 图片文件引用
- HTTP / HTTPS URL

### 当前来源展示策略

默认情况下：

- slide 页面正文不显示来源
- presenter notes 里显示来源
- 每一页的来源也会保存在结构化元数据里

也就是说：

- 观众看到的页面是干净的
- 讲解者在 presenter notes 里能看到来源依据
- 系统后续还能继续利用这些来源做 revise 或审计

## 最推荐的使用方式

如果你真要用这个项目做相对严谨的 PPT，不建议只给一句 prompt。

更推荐的流程是：

1. 明确你要做什么 PPT
2. 提供资料来源
3. 先生成一版
4. 再做 1 到 3 轮 revise

例如：

1. 你提供目标：
   - 我要做一个给管理层看的 8 页产品规划汇报

2. 你提供资料：
   - 产品 brief
   - 官网链接
   - 市场分析 PDF
   - 现有项目说明文档

3. 生成第一版：
   - 用 `generate-from-prompt.js`

4. 做修订：
   - 压缩到 6 页
   - 更偏结论导向
   - 加强执行计划
   - 面向投资人重新组织

## 新手最容易上手的 3 个命令

如果你只是想快速试一下，按这个顺序就行。

### 第一步：直接试 source 模式

```bash
npm run generate:source
```

### 第二步：看 skill 模式

```bash
npm run skill:create
```

### 第三步：试 revise

```bash
npm run revise:mock
```

## 主要文件是干什么的

### 面向使用者最相关的文件

- `README.md`
  - 英文总说明
- `PRODUCT.en.md`
  - 英文产品概览和项目定位说明
- `USER_GUIDE.zh-CN.md`
  - 当前这份中文使用说明
- `sample-input.json`
  - 现成 deck 示例
- `sample-source-brief.md`
  - 来源材料示例
- `sample-agent-request.json`
  - skill create 请求示例
- `sample-agent-revise-request.json`
  - skill revise 请求示例
- `sample-http-request.json`
  - HTTP 请求示例

### 面向技术接入的核心文件

- `generate-ppt.js`
  - 把 deck JSON 渲染成 PPT
- `generate-from-prompt.js`
  - 从 prompt 生成 deck 和 PPT
- `revise-deck.js`
  - 修订已有 deck
- `deck-agent-core.js`
  - planning / revise / schema 校验核心
- `source-loader.js`
  - 来源读取和提取
- `agent-skill.js`
  - JSON skill 入口
- `skill-server.js`
  - HTTP skill 入口
- `deck-schema.json`
  - deck JSON 的约束定义
- `skill-manifest.json`
  - skill 接入契约

## 现在还不够强的地方

这个项目已经能跑通完整原型链路，但还不是生产级成品。

当前还不够强的地方包括：

- 不是完整 research agent
- 图片 OCR 和多模态理解还没有真正做完
- slide 级来源绑定还不够精细
- 品牌模板和视觉控制还比较基础
- 真正复杂场景下仍然依赖上游模型和 agent 质量

## 最后怎么理解这个项目

你可以把它理解成一个：

- 可接 AI Agent 的 PPT skill backend
- 可读来源资料的 deck planning engine
- 能输出 `.pptx` 的 PowerPoint 原型系统

它现在最核心的价值不是“本地命令行很好用”，而是：

**它已经具备了被更大一层 AI Agent 工作流调用的结构。**

## 一句话总结

现在这个文件夹已经可以完成：

- `prompt -> deck -> pptx`
- `prompt + sources -> deck -> pptx`
- `existing deck + revise prompt -> revised deck -> pptx`
- `agent request -> skill response`
- `HTTP request -> generated PPT artifacts`

如果你接下来是想真正拿它做产品，最合理的方向是继续强化：

- 资料理解
- 来源追踪
- revise 质量
- 模型接入
- 模板化能力
