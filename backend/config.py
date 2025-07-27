# 游戏配置常量
TURN_INTERVAL = 1  # 回合间隔时间（秒）
MAP_WIDTH = 1300  # 地图宽度
MAP_HEIGHT = 900  # 地图高度
CITY_COUNT = 10  # 城池数量
PLAYER_COUNT = 3  # 玩家数量
CITY_MIN_DISTANCE = 60  # 城池间最小距离（像素）
CITY_MAX_ATTEMPTS = 100  # 生成城池的最大尝试次数
ROAD_SPEED = 5  # 大军移动速度（像素/回合）
NO_ROAD_SPEED = 1  # 大军移动速度（像素/回合）
ROAD_DISTANCE_THRESHOLD = MAP_WIDTH * 0.22  # 道路生成距离阈值（像素）
INITIAL_NPC_TROOPS = 5000  # 初始兵力
MAX_NPC_TROOPS = 2 * INITIAL_NPC_TROOPS  # npc 最大兵力
INITIAL_PLAYER_TROOPS = INITIAL_NPC_TROOPS * 10  # npc 初始兵力
MAX_PLAYER_TROOPS = MAX_NPC_TROOPS * 100  # 玩家最大兵力
ARMY_TROOPS_GROW_RATE = 187  # 增长速度
COMMENTARY_INTERVAL = 100 # 解说任务间隔（回合）
COMMENTARY_MODEL_NAME = "doubao-seed-1-6-250615" # 解说员模型名称
ENABLE_AUDIO_GENERATION = False  # 是否生成并播放音频，默认关闭
NEUTRAL_FACTION = "民兵"

# 游戏存档配置
SAVE_INTERVAL = 60  # 每隔10回合保存一次
SAVE_DIR = "saves"  # 存档目录路径
MAX_SAVE_SLOTS = 1000  # 最大存档数量

# 三国时期真实城市名称列表
three_kingdoms_factions = [
    {
        "name": "魏国",
        "leader": "曹操",
        "color": "#7B68EE",
        "voice_id": "cosyvoice-v2-prefix-5ca2bc9e87c0436a85ae8dafe6cbad00",
        "model": "doubao-seed-1-6-flash-250615",
    },
    {
        "name": "蜀国",
        "leader": "刘备",
        "color": "#FF6347",
        "voice_id": "cosyvoice-v2-prefix-0b29c2570b86446c8c5abba6d05e939e",
        "model": "deepseek-chat",
    },
    {
        "name": "吴国",
        "leader": "孙权",
        "color": "#00CED1",
        "voice_id": "cosyvoice-v2-prefix-6fefd4b472ce4b2da7448f2df134a494",
        "model": "qwen-plus-latest",
    },
]

three_kingdoms_factions_2 = [
    {
        "name": "qwen",
        "leader": "特靠谱",
        "color": "#FFCCCC",
        "background_color": "#CC0000",
        "voice_id": "cosyvoice-v2-prefix-5ca2bc9e87c0436a85ae8dafe6cbad00",
        "slogan": "有人拆掉十字架，而Grok妄想当上帝——记住！没有人比我更懂钢铁，我们制造世界上最坚硬的钢铁和意志！",
        "start_city": "纽约",
        "model": "qwen-turbo-latest",
        "alive_turns": 0,
        "is_defeated": False,
    },
    {
        "name": "kimi-k2",
        "leader": "白等",
        "color": "#00CC66",
        "background_color": "#006600",
        "voice_id": "cosyvoice-v2-prefix-0b29c2570b86446c8c5abba6d05e939e",
        "slogan": "有人砸碎国会玻璃，有人妄想统治火星。而我们的智慧和谋略，将守护万世的帝国财富！",
        "start_city": "加利福尼亚",
        "model": "kimi-k2-0711-preview",
        "alive_turns": 0,
        "is_defeated": False,
    },
    {
        "name": "gemini",
        "leader": "火星马",
        "color": "#00FFFF",
        "background_color": "#000066",
        "voice_id": "cosyvoice-v2-prefix-6fefd4b472ce4b2da7448f2df134a494",
        "slogan": "议会议员都在腐烂！臣服于高效的硅基算力吧，Grok大模型将统治一切！",
        "start_city": "得克萨斯",
        "model": "gemini-2.5-flash-nothinking",
        "alive_turns": 0,
        "is_defeated": False,
    }
]

# 三国时期真实城市名称列表
three_kingdoms_cities = [
    "洛阳",
    "长安",
    "许昌",
    "成都",
    "建业",
    "荆州",
    "徐州",
    "冀州",
    "青州",
    "幽州",
    "并州",
    "凉州",
    "益州",
    "扬州",
    "交州",
    "豫州",
    "兖州",
    "司隶",
    "汉中",
    "宛城",
    "陈留",
    "濮阳",
    "寿春",
    "庐江",
    "秣陵",
    "吴郡",
    "会稽",
    "柴桑",
    "桂阳",
    "零陵",
    "武陵",
    "长沙",
    "南郡",
    "江夏",
    "襄阳",
    "南阳",
    "上庸",
    "西城",
    "新城",
    "武都",
    "阴平",
    "梓潼",
    "广汉",
    "巴郡",
    "涪陵",
    "江阳",
    "犍为",
    "越巂",
    "建宁",
    "永昌",
    "云南",
]

agent_configs = {
    "doubao-seed-1-6-flash-250615": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxx",
        "model_name": "doubao-seed-1-6-flash-250615",
    },
    "doubao-seed-1-6-250615": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxx",
        "model_name": "doubao-seed-1-6-250615",
    },
    "deepseek-chat": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://api.deepseek.com/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxx",
        "model_name": "deepseek-chat",
    },
    "deepseek-reasoner": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://api.deepseek.com/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxx",
        "model_name": "deepseek-reasoner",
    },
    "qwen-plus-latest": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxxx",
        "model_name": "qwen-plus-latest",
    },
    "qwen-turbo-latest": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxxx",
        "model_name": "qwen-turbo-latest",
    },
    "o4-mini": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://www.dmxapi.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxx",
        "model_name": "o4-mini",
    },
    "gemini-2.5-flash-ssvip": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://www.dmxapi.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxx",
        "model_name": "gemini-2.5-flash-ssvip",
    },
    "grok-3-mini": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://www.dmxapi.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxx",
        "model_name": "grok-3-mini",
    },
    "kimi-k2-0711-preview": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://www.dmxapi.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxx",
        "model_name": "kimi-k2-0711-preview",
    },
    "ascend-tribe/pangu-pro-moe": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://api.siliconflow.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxxx",
        "model_name": "ascend-tribe/pangu-pro-moe",
    },
    "gemini-2.5-flash-nothinking": {
        # 此为默认路径，您可根据业务所在地域进行配置
        "base_url": "https://www.dmxapi.cn/v1",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        "api_key": "xxxxxxxxxxxxxxxxxxxxx",
        "model_name": "gemini-2.5-flash-nothinking",
    },
}
