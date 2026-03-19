# 示例

这份文档给第一次接触这个仓库的人使用。

如果你不想先读完整文档，而是想先跑通一遍，可以从这里开始。

## 最快跑通一次

先安装依赖：

```bash
npm install
python -m pip install -r requirements.txt
```

使用内置 source brief 生成一版 deck：

```bash
python py-generate-from-prompt.py --mock --prompt "Create an 8-slide AI workspace strategy deck for executives" --source sample-source-brief.md
```

预期输出：

- `output/py-generated-deck.json`
- `output/py-generated-deck.pptx`

## 使用 Deck Brief 文件

自然语言 brief 示例：

- `sample-deck-brief.md`

结构化 brief 示例：

- `sample-deck-brief.json`

把 brief 当作 source 输入的命令示例：

```bash
python py-generate-from-prompt.py --mock --prompt "Turn this brief into an 8-slide product deck" --source sample-deck-brief.md
```

## 修订已生成的 Deck

第一版生成完成后，可以继续修订：

```bash
python py-revise-deck.py --mock --deck output/py-generated-deck.json --prompt "Compress this deck to 6 slides and make it more conclusion-driven"
```

预期输出：

- `output/py-revised-deck.json`
- `output/py-revised-deck.pptx`

## JSON Skill 示例

如果你要把它接进别的 agent 或脚本流程，可以直接用 JSON 请求文件：

```bash
python py-agent-skill.py --request sample-agent-request.json --response output/py-agent-response.json
```

相关文件：

- `sample-agent-request.json`
- `output/py-agent-response.json`

## HTTP 示例

启动本地服务：

```bash
python py-skill-server.py
```

调用接口：

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
```

## 应该先看哪个示例

- 如果你只是想最快看到成功结果，先看 `sample-source-brief.md`
- 如果你想理解什么是 deck brief，先看 `sample-deck-brief.md`
- 如果你要集成进别的 agent 流程，先看 `sample-agent-request.json`
- 如果你更偏向本地服务调用，先看 `sample-http-request.json`
