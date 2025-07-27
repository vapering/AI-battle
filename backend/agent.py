import threading
import requests
from openai import OpenAI
import time,random
from config import agent_configs

game_text='''
    # 战争策略游戏核心规则

    ## 基础设定
    - **地图**：多个城市和州地区，通过道路连接
    - **兵力**：地区自动增长兵力，交战地区不增长兵力，地区的兵力增长有上限
    - **玩家**：3名玩家
    - **胜利条件**：消灭其他所有玩家的城市和兵力
    - **非常重要** 出征 和 部署 命令，都必须在两个有道路连接的地区之间进行，否则命令无效。
    - **非常重要** 主动集中兵力，主动出征消灭敌方，主动攻击占领地区，才能获得胜利。

    ## 核心操作
    1. **部署(deploy_army)**：在己方地区间移动兵力
    2. **出征(send_expedition)**：派遣兵力攻击其他地区，到达后自动战斗
    3. **占领**：地区中兵力最多的玩家即占领了该地区

    ## 命令格式
    - 每个回合可以有多条命令。

    ### 部署命令
    ```
    <command>
        <name>deploy_army</name>
        <city_name>地区1</city_name>
        <dest_city_name>地区2</dest_city_name>
        <troops>10000</troops>
    </command>
    ```
    ### 出征命令
    ```
    <command>
        <name>send_expedition</name>
        <city_name>地区1</city_name>
        <dest_city_name>地区2</dest_city_name>
        <troops>10000</troops>
    </command>
    ```
    ## 非常重要，下面代码框里面是示例输出，请严格参考下面的样例格式进行回复，每次回复可以包含多条命令,回复的时候只输出xml格式的内容本身
    ```
    <root>
        <line>这里填本回合的玩家台词，可以根据游戏地图和玩家信息进行回复</line>
        <player_name>玩家1</player_name>
        <commandList>
            <command>
                <name>deploy_army</name>
                <city_name>地区1</city_name>
                <dest_city_name>地区2</dest_city_name>
                <troops>10000</troops>
            </command>
            <command>
                <name>send_expedition</name>
                <city_name>地区1</city_name>
                <dest_city_name>地区2</dest_city_name>
                <troops>10000</troops>
            </command>
        </commandList>
    </root>
    ```
'''

class Agent():
    is_thinking = False
    client = None
    model = None
    def __init__(self,model) -> None:
        self.model = agent_configs[model]
        self.client = OpenAI(
            # 此为默认路径，您可根据业务所在地域进行配置
            base_url=self.model["base_url"],
            # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
            api_key=self.model["api_key"],
        )

    def send(self,msg):
        response = self.client.chat.completions.create(
            model=self.model["model_name"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": msg},
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    def execute_command(self, command_data):
        try:
            # 调用controller中的send_army接口
            response = requests.post(
                "http://127.0.0.1:5000/api/send_army",
                data=command_data
            )
            response.raise_for_status()
            print("命令执行成功: " + response.json().get("message", ""))
        except requests.exceptions.RequestException as e:
            print(f"命令执行失败: {str(e)}")
        finally:
            time.sleep((random.random() * 5) + 5)
        self.is_thinking = False
        return False, "命令执行完成"

    def playGame(self, player_name, game_report,player):
        if self.is_thinking:
            return "思考中，请稍后"
        self.is_thinking = True
        game_promote=f"""
            你作为游戏玩家：{player_name}
            玩家口号是：{player['slogan']}
            请阅读下面的 游戏规则 和 游戏回合报告，
            发出这个回合的命令，并模拟游戏玩家，输出这个回合的台词（约20个字）。
            台词可以是 讨伐台词 或者 谋略结盟 等：
            如果是讨伐台词：必须能吸引观众,富含个性、势力风格，突出势力之间的尖锐冲突，可以骂敌方，一定要在气势上面赢过对方。
            如果是谋略结盟：可以劝说其他玩家结盟，宣布友好，通过你的谋略和其他玩家结盟、合作、迷惑其他玩家等。
            注意思考要快速，不能思考太长时间。
        """
        player_input = f"{game_promote} \n {game_text} \n {game_report} \n "
        response_text = self.send(player_input)
        commands=response_text.replace("`","")
        success, result = self.execute_command(commands)
        print(f"命令: {commands}")
        print(f"命令执行结果: {result}")


class AgentTask(threading.Thread):
    agent=None
    game_report=None
    player_name=None
    player=None
    def init(self, player_name: str, agent:Agent, game_report, player):
        self.player_name = player_name
        self.agent=agent
        self.game_report=game_report
        self.player = player

    def run(self):
        self.agent.playGame(self.player_name, self.game_report,self.player)
        return 


if __name__ == '__main__':
    agent = Agent("doubao")
    # agent.send("你是谁？")
    game_report=f'''第12回合 简报：

    === 基本信息 ===
    当前回合：12
    活跃玩家数：3
    城池总数：20
    移动中军队数：0

    === 玩家状态 ===
    - 魏国：活跃，总兵力 136，占领城池 1 座
    - 蜀国：活跃，总兵力 1120，占领城池 1 座
    - 吴国：活跃，总兵力 136，占领城池 1 座

    === 城池情况 ===
    - 洛阳：民兵（22兵力），增长率 1
    - 长安：魏国（136兵力），增长率 3
    - 许昌：民兵（50兵力），增长率 2
    - 成都：民兵（50兵力），增长率 3
    - 建业：民兵（50兵力），增长率 3
    - 荆州：民兵（50兵力），增长率 2
    - 徐州：民兵（22兵力），增长率 1
    - 冀州：民兵（22兵力），增长率 1
    - 青州：民兵（50兵力），增长率 3
    - 幽州：民兵（22兵力），增长率 1
    - 并州：民兵（22兵力），增长率 1
    - 凉州：民兵（50兵力），增长率 2
    - 益州：吴国（136兵力），增长率 3
    - 扬州：民兵（50兵力），增长率 2
    - 交州：蜀国（1120兵力），增长率 1
    - 豫州：民兵（50兵力），增长率 3
    - 兖州：民兵（50兵力），增长率 3
    - 司隶：民兵（22兵力），增长率 1
    - 汉中：民兵（22兵力），增长率 1
    - 宛城：民兵（22兵力），增长率 1
    \n\n=== 军队移动 ===
    - 无移动中的军队

    === 道路情况，同一行的两个城池表示可以互相到达 ===
    - 洛阳 和 益州 , 距离: 104.1 里
    - 益州 和 兖州 , 距离: 177.2 里
    - 建业 和 兖州 , 距离: 173.7 里
    - 建业 和 荆州 , 距离: 141.3 里
    - 荆州 和 司隶 , 距离: 70.6 里
    - 幽州 和 司隶 , 距离: 153.1 里
    - 洛阳 和 长安 , 距离: 212.9 里
    - 长安 和 扬州 , 距离: 161.1 里
    - 许昌 和 扬州 , 距离: 204.5 里
    - 许昌 和 交州 , 距离: 78.8 里
    - 交州 和 豫州 , 距离: 247.0 里
    - 成都 和 豫州 , 距离: 97.1 里
    - 成都 和 宛城 , 距离: 188.7 里
    - 冀州 和 宛城 , 距离: 97.8 里
    - 冀州 和 汉中 , 距离: 134.0 里
    - 徐州 和 汉中 , 距离: 124.0 里
    - 并州 和 汉中 , 距离: 211.8 里
    - 建业 和 青州 , 距离: 247.2 里
    - 冀州 和 凉州 , 距离: 299.7 里
    - 洛阳 和 建业 , 距离: 221.1 里
    - 洛阳 和 荆州 , 距离: 242.4 里
    - 洛阳 和 兖州 , 距离: 223.7 里
    - 建业 和 益州 , 距离: 255.2 里
    - 建业 和 司隶 , 距离: 171.6 里
    - 荆州 和 幽州 , 距离: 222.7 里
    - 荆州 和 扬州 , 距离: 238.8 里
    - 徐州 和 冀州 , 距离: 247.2 里
    - 徐州 和 并州 , 距离: 250.0 里
    - 徐州 和 扬州 , 距离: 254.9 里
    - 汉中 和 宛城 , 距离: 218.5 里
    '''
    game_promote=f"""
        你作为游戏玩家： 蜀国，请阅读下面的 游戏规则 和 游戏回合报告，
        发出这个回合的命令，并模拟历史人物，输出这个回合的台词（50个字以内），台词里面可以体现兵力数量等数据。
        出征的台词必须能吸引观众,富有个性或者文采，可以适当带上势力风格、方言，突出历史上势力之间的尖锐冲突。
        注意思考要快速，不能思考太长时间，因为这是即时战略游戏，思考的同时游戏的时间也在流逝。
    """
    # response_text = agent.send(f"{game_promote} \n {game_text} \n {game_report} \n ")
    response_text = '''
    <root>
        <line>汉室兴复在此一举！交州起兵800，疾取许昌！50民兵何足惧，此城便是我蜀进取中原之基！</line>
        <player_name>蜀国</player_name>
        <commands>
            <command>
                <name>send_expedition</name>
                <city_name>交州</city_name>
                <dest_city_name>许昌</dest_city_name>
                <troops>10</troops>
            </command>
            <command>
                <name>send_expedition</name>
                <city_name>交州</city_name>
                <dest_city_name>许昌</dest_city_name>
                <troops>10</troops>
            </command>
        </commands>
    </root>
    '''
    # 解析并执行命令
    success, result = agent.execute_command(response_text)
    print(f"命令执行结果: {result}")
