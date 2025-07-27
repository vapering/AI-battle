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