# AI Battle: LLM大模型战争策略游戏

**English** | [README_en.md](readme_en.md)

<video src="https://private-user-images.githubusercontent.com/5309375/471211068-0127364b-9b00-4839-9f6c-1eed320dfdcb.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTM2MjYxNjQsIm5iZiI6MTc1MzYyNTg2NCwicGF0aCI6Ii81MzA5Mzc1LzQ3MTIxMTA2OC0wMTI3MzY0Yi05YjAwLTQ4MzktOWY2Yy0xZWVkMzIwZGZkY2IubXA0P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDcyNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA3MjdUMTQxNzQ0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzA0YWM2ZTQ1Njg3OGJlZTljZjVlNDU5ZjI4M2FmNmI1ODI4Y2E3MWZjZWRlMWNiNTkxMDdkNTgyNjkzZjhiMCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.Y0jLe0b3ffFCJyU035S-I52u9PVz13HxXT_a5jJoCFk" data-canonical-src="https://private-user-images.githubusercontent.com/5309375/471211068-0127364b-9b00-4839-9f6c-1eed320dfdcb.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTM2MjYxNjQsIm5iZiI6MTc1MzYyNTg2NCwicGF0aCI6Ii81MzA5Mzc1LzQ3MTIxMTA2OC0wMTI3MzY0Yi05YjAwLTQ4MzktOWY2Yy0xZWVkMzIwZGZkY2IubXA0P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDcyNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA3MjdUMTQxNzQ0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzA0YWM2ZTQ1Njg3OGJlZTljZjVlNDU5ZjI4M2FmNmI1ODI4Y2E3MWZjZWRlMWNiNTkxMDdkNTgyNjkzZjhiMCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.Y0jLe0b3ffFCJyU035S-I52u9PVz13HxXT_a5jJoCFk" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px">

  </video>

## 项目概述
AI Battle是一款创新的战争策略游戏，玩家由大型语言模型(LLM)扮演，通过智能决策和战略部署争夺领土和资源。游戏采用回合制机制，结合了实时策略元素和AI驱动的决策系统，创造出独特的游戏体验。

## 核心功能
- **AI驱动的玩家**：3个不同LLM模型控制的AI玩家自主决策和互动
- **动态战争系统**：兵力部署、出征攻击、领土占领等完整战争机制
- **实时战略地图**：可视化地图展示城市、道路和移动中的军队
- **回合制游戏流程**：自动回合推进与状态更新
- **沉浸式体验**：每个AI玩家拥有独特的个性、口号和语音

## 技术架构

### 后端
- **框架**：Flask 2.0.1
- **主要依赖**：
  - APScheduler 3.10.1 (任务调度)
  - flask-cors 4.0.0 (跨域支持)
  - pygame 2.5.2 (音频处理)
  - xmltodict 0.13.0 (XML解析)
  - openai >=1.0 (AI模型接口)
  - dashscope (AI模型接口)

### 前端
- **框架**：Vue 3.2.0 + Vue Router 4.0.0
- **UI组件库**：Vuetify 3.9.2
- **HTTP客户端**：Axios 1.10.0
- **图标库**：@mdi/font 7.4.47

## 游戏规则

### 基础设定
- **地图**：多个城市和州地区，通过道路连接
- **兵力**：地区自动增长兵力，交战地区不增长兵力，地区的兵力增长有上限
- **玩家**：3名AI玩家
- **胜利条件**：消灭其他所有玩家的城市和兵力

### 核心操作
1. **部署(deploy_army)**：在己方地区间移动兵力
2. **出征(send_expedition)**：派遣兵力攻击其他地区，到达后自动战斗
3. **占领**：地区中兵力最多的玩家即占领了该地区

### AI玩家
1. **里帕布自由军**：使用doubao-seed-1-6-flash-250615模型
2. **得莫克阵线**：使用deepseek-chat模型
3. **Grok新世界**：使用qwen-plus-latest模型

## 安装与启动

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端启动
```bash
cd frontend
npm install
npm run serve
```

## 配置指南

### API密钥配置
1. 打开配置文件 `AI-battle\backend\config.py`
2. 在 `agent_configs` 字典中找到对应模型的配置项
3. 替换 `api_key` 的值为您的实际API密钥

```python
agent_configs = {
    "doubao-seed-1-6-flash-250615": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": "您的API密钥",  # 替换为实际API密钥
        "model_name": "doubao-seed-1-6-flash-250615",
    },
    # 其他模型配置...
}
```

### 玩家模型绑定
1. 在 `AI-battle\backend\config.py` 中找到派系配置数组（`three_kingdoms_factions` 或 `three_kingdoms_factions_2`）
2. 为每个玩家设置 `model` 属性，值对应 `agent_configs` 中的模型名称

```python
three_kingdoms_factions = [
    {
        "name": "魏国",
        "leader": "曹操",
        "color": "#7B68EE",
        "voice_id": "...",
        "model": "doubao-seed-1-6-flash-250615",  # 绑定到大模型
    },
    # 其他玩家配置...
]
```

## 命令格式
每个回合可以有多条命令，支持两种核心命令：

### 部署命令
```xml
<command>
    <name>deploy_army</name>
    <city_name>地区1</city_name>
    <dest_city_name>地区2</dest_city_name>
    <troops>10000</troops>
</command>
```

### 出征命令
```xml
<command>
    <name>send_expedition</name>
    <city_name>地区1</city_name>
    <dest_city_name>地区2</dest_city_name>
    <troops>10000</troops>
</command>
```

## 许可证
本项目采用Apache License 2.0许可证 - 详见LICENSE文件

## 项目结构
```
AI-battle/
├── .gitignore
├── LICENSE
├── README.md
├── backend/
│   ├── agent.py
│   ├── app.py
│   ├── config.py
│   ├── controller.py
│   ├── music/
│   ├── requirements.txt
│   ├── service.py
│   └── voice.py
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.vue
│   │   ├── assets/
│   │   ├── components/
│   │   ├── main.js
│   │   ├── router/
│   │   └── views/
│   └── vue.config.js
├── game.md
└── gameState.md
```
