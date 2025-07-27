# AI Battle: LLM-Powered War Strategy Game

**中文** | [README.md](readme.md)

## Model Rankings
Current Score Ranking
| Company | Model | Average Score | Average Command Accuracy Rate |
|-|-|-|-|
| Google | gemini-2.5-flash-nothinking | 30 | 0.78 |
| Moon Dark Side | kimi-k2-0711-preview | 25 | 0.6515 |
| deepseek | deepseek-chat | 20 | 0.8948 |
| ByteDance | doubao-seed-1-6-flash-250615 | 20 | 0.314 |
| HW | pangu-pro-moe | 20 | 0.753 |
| Microsoft/OpenAI | o4-mini | 15 | 0.93 |
| xAI | grok-3-mini | 10 | 0.87 |
| Alibaba | qwen-plus-latest | 10 | 0.7774 |

<video src="https://private-user-images.githubusercontent.com/5309375/471211068-0127364b-9b00-4839-9f6c-1eed320dfdcb.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTM2MjYxNjQsIm5iZiI6MTc1MzYyNTg2NCwicGF0aCI6Ii81MzA5Mzc1LzQ3MTIxMTA2OC0wMTI3MzY0Yi05YjAwLTQ4MzktOWY2Yy0xZWVkMzIwZGZkY2IubXA0P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDcyNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA3MjdUMTQxNzQ0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzA0YWM2ZTQ1Njg3OGJlZTljZjVlNDU5ZjI4M2FmNmI1ODI4Y2E3MWZjZWRlMWNiNTkxMDdkNTgyNjkzZjhiMCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.Y0jLe0b3ffFCJyU035S-I52u9PVz13HxXT_a5jJoCFk" data-canonical-src="https://private-user-images.githubusercontent.com/5309375/471211068-0127364b-9b00-4839-9f6c-1eed320dfdcb.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTM2MjYxNjQsIm5iZiI6MTc1MzYyNTg2NCwicGF0aCI6Ii81MzA5Mzc1LzQ3MTIxMTA2OC0wMTI3MzY0Yi05YjAwLTQ4MzktOWY2Yy0xZWVkMzIwZGZkY2IubXA0P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDcyNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA3MjdUMTQxNzQ0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzA0YWM2ZTQ1Njg3OGJlZTljZjVlNDU5ZjI4M2FmNmI1ODI4Y2E3MWZjZWRlMWNiNTkxMDdkNTgyNjkzZjhiMCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.Y0jLe0b3ffFCJyU035S-I52u9PVz13HxXT_a5jJoCFk" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px">

  </video>
## Project Overview
AI Battle is an innovative war strategy game where players are portrayed by Large Language Models (LLMs) that compete for territory and resources through intelligent decision-making and strategic deployment. The game uses a turn-based mechanism combined with real-time strategy elements and an AI-driven decision system to create a unique gaming experience.

## Core Features
- **AI-Driven Players**: 3 different AI players controlled by LLM models that make autonomous decisions and interactions
- **Dynamic Warfare System**: Complete warfare mechanisms including troop deployment, expedition attacks, and territory occupation
- **Real-Time Strategic Map**: Visual map displaying cities, roads, and moving armies
- **Turn-Based Game Flow**: Automatic turn progression and state updates
- **Immersive Experience**: Each AI player has a unique personality, slogan, and voice

## Technical Architecture

### Backend
- **Framework**: Flask 2.0.1
- **Main Dependencies**:
  - APScheduler 3.10.1 (Task scheduling)
  - flask-cors 4.0.0 (Cross-origin support)
  - pygame 2.5.2 (Audio processing)
  - xmltodict 0.13.0 (XML parsing)
  - openai >=1.0 (AI model interface)
  - dashscope (AI model interface)

### Frontend
- **Framework**: Vue 3.2.0 + Vue Router 4.0.0
- **UI Component Library**: Vuetify 3.9.2
- **HTTP Client**: Axios 1.10.0
- **Icon Library**: @mdi/font 7.4.47

## Game Rules

### Basic Settings
- **Map**: Multiple cities and regions connected by roads
- **Troops**: Regions automatically grow troops, war zones do not grow troops, and there is a limit to troop growth
- **Players**: 3 AI players
- **Victory Condition**: Eliminate all other players' cities and troops

### Core Operations
1. **Deploy (deploy_army)**: Move troops between own regions
2. **Expedition (send_expedition)**: Dispatch troops to attack other regions, automatic battle upon arrival
3. **Occupy**: The player with the most troops in a region occupies that region

### AI Players
1. **Ripabu Liberation Army**: Uses doubao-seed-1-6-flash-250615 model
2. **Demok Front**: Uses deepseek-chat model
3. **Grok New World**: Uses qwen-plus-latest model

## Installation and Launch

### Backend Launch
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Launch
```bash
cd frontend
npm install
npm run serve
```

## Configuration Guide

### API Key Configuration
1. Open the configuration file `AI-battle\backend\config.py`
2. Find the configuration item for the corresponding model in the `agent_configs` dictionary
3. Replace the value of `api_key` with your actual API key

```python
agent_configs = {
    "doubao-seed-1-6-flash-250615": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": "Your API Key",  # Replace with actual API key
        "model_name": "doubao-seed-1-6-flash-250615",
    },
    # Other model configurations...
}
```

### Player Model Binding
1. In `AI-battle\backend\config.py`, find the faction configuration array (`three_kingdoms_factions` or `three_kingdoms_factions_2`)
2. Set the `model` property for each player, with values corresponding to model names in `agent_configs`

```python
three_kingdoms_factions = [
    {
        "name": "魏国",
        "leader": "曹操",
        "color": "#7B68EE",
        "voice_id": "...",
        "model": "doubao-seed-1-6-flash-250615",  # Bind to LLM model
    },
    # Other player configurations...
]
```

## Command Format
Each turn can have multiple commands, supporting two core commands:

### Deployment Command
```xml
<command>
    <name>deploy_army</name>
    <city_name>Region 1</city_name>
    <dest_city_name>Region 2</dest_city_name>
    <troops>10000</troops>
</command>
```

### Expedition Command
```xml
<command>
    <name>send_expedition</name>
    <city_name>Region 1</city_name>
    <dest_city_name>Region 2</dest_city_name>
    <troops>10000</troops>
</command>
```

## License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details

## Project Structure
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
