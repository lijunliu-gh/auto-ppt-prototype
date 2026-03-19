# 产品概览

## 当前产品定位

Auto PPT Prototype 是一个面向 AI Agent 的开源 PowerPoint 生成后端。

它目前提供：

- 基于 prompt 的 deck planning
- 基于自然语言指令的 deck revise
- 基于 JSON Schema 的结构校验
- `.pptx` 渲染能力
- 可被 agent 调用的 JSON 请求和响应流程
- 本地 HTTP skill 接口

## 它是什么

它本质上是一个 planning-and-rendering engine。

它适合放在一个 AI Agent 后面，由上游 agent 负责：

- 收集需求
- 追问缺失信息
- 获取可信资料
- 读取用户上传文档
- 查看截图或图片
- 决定每一页应该放什么内容

## 它不是什么

它本身不是一个完整的 research agent。

它也不应该被描述成“网页搜索直接生成幻灯片”的简单工具。

如果用于相对严肃的场景，系统应优先依赖：

1. 官方来源
2. 用户上传资料
3. 明确的用户指令
4. 网页搜索仅作为兜底

## 当前对外接口

- CLI create
- CLI revise
- JSON request/response skill wrapper
- HTTP service wrapper

## 目前仍存在的产品缺口

- 对 PDF、DOCX、HTML、CSV、表格类资料的更强 ingestion 能力
- 图片与截图理解
- 更精细的 provenance tracking
- 更强的主题和模板支持
- 更好的版式质量和字体控制
- 自动化测试
- 面向托管部署的工程化加固

## 建议的开源定位描述

建议 GitHub 简介使用：

> Open-source PowerPoint planning and rendering backend for AI agents working from trusted sources, uploaded materials, and explicit user requirements.