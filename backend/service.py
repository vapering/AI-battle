from flask import jsonify
import math
import json
import os
import voice
import config
import random
from config import *
from agent import Agent,AgentTask
from config import COMMENTARY_INTERVAL
import threading
from pygame import mixer

# 游戏状态变量
current_turn = -1
cities = []
players = []
roads = []
armies = []
global_lines = []  # 全局台词列表
# 全局变量：存储当前回合简报
turn_report = ""
agents = {}

is_paused = True  # 添加游戏暂停状态变量
commentary_result=''
commentary_agent:Agent=None
commentary_working=False

command_history=[]
game_events = []  # 记录最近30条游戏事件

def reset_game_state():
    """重置游戏状态"""
    global cities, players, current_turn, armies, roads, global_lines
    cities = []
    players = []
    current_turn = -1
    armies = []
    roads = []
    global_lines = []  # 重置全局台词列表
    current_turn = 1
    cities = []
    players = []
    armies = []
    roads = []


def initialize_game_from_backend():
    """初始化游戏状态：生成20个城池和3个玩家"""
    global cities, players, current_turn, armies, roads, commentary_agent
    
    # 重置游戏状态
    reset_game_state()
    mixer.init()

    # 生成城池
    cities = generate_cities(config.CITY_COUNT)

    # 生成玩家并分配初始城池
    players = generate_players(cities, three_kingdoms_factions)

    # 使用Prim算法生成最小生成树，确保所有城池在同一道路网络中
    roads = generate_minimum_spanning_tree(cities)
    
    # 添加额外道路：连接距离小于阈值的城池对
    add_extra_roads(cities, roads, config.ROAD_DISTANCE_THRESHOLD)

    # 计算所有道路长度
    calculate_road_lengths(roads, cities)

    resume_game()


def initialize_game_from_frontend(citys_input:[],roads_input:[]):
    """
    从前端开始初始化城池和道路
    城池=city=state=州
    """
    global cities, players, current_turn, armies, roads, commentary_agent
    # 重置游戏状态
    mixer.init()
    reset_game_state()
    roads = roads_input
    cities = citys_input
    # 初始化玩家
    players = generate_players(cities, three_kingdoms_factions_2)
    # 初始化民兵
    for city in cities:
        if city['garrisons'] == {}:
            city['garrisons'] = {NEUTRAL_FACTION: math.floor(config.INITIAL_NPC_TROOPS * random.random())}
        # 初始化增长率
        city['growth_rate'] = math.floor(ARMY_TROOPS_GROW_RATE * (1+random.random()))

    resume_game()


def calculate_road_lengths(roads, cities):
    """计算所有道路的长度并添加到道路对象中"""
    import math
    city_coords = {city['id']: (city['x'], city['y']) for city in cities}
    for road in roads:
        x1, y1 = city_coords[road['city1_id']]
        x2, y2 = city_coords[road['city2_id']]
        road['length'] = round(math.sqrt((x2 - x1)**2 + (y2 - y1)** 2), 2)

def add_extra_roads(cities, roads, distance_threshold):
    """为距离小于阈值的城池对添加额外道路"""
    existing_roads = set()
    for road in roads:
        existing_roads.add(frozenset([road['city1_id'], road['city2_id']]))
    
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            city1 = cities[i]
            city2 = cities[j]
            dx = city1['x'] - city2['x']
            dy = city1['y'] - city2['y']
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < distance_threshold:
                road_pair = frozenset([city1['id'], city2['id']])
                if road_pair not in existing_roads:
                    # 生成贝塞尔曲线控制点，创建自然弯曲的道路
                    mid_x = (city1['x'] + city2['x']) / 2
                    mid_y = (city1['y'] + city2['y']) / 2
                    offset_range = int(distance * 0.3)  # 偏移范围与距离成正比
                    cp_x = mid_x + random.randint(-offset_range, offset_range)
                    cp_y = mid_y + random.randint(-offset_range, offset_range)
                    
                    roads.append({
                        "city1_id": city1["id"],
                        "city2_id": city2["id"],
                        "control_points": [(cp_x, cp_y)]
                    })
                    existing_roads.add(road_pair)

def generate_minimum_spanning_tree(cities):
    """使用Prim算法生成城池间的最小生成树道路网络"""
    roads = []
    if len(cities) <= 1:
        # 若只有0或1个城池，无需生成道路
        return roads
    
    # Prim算法实现
    # 1. 初始化：选择第一个城池作为起点
    visited = set([cities[0]['id']])
    unvisited = set(city['id'] for city in cities[1:])
    
    # 2. 构建边集合
    edges = []
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            city1 = cities[i]
            city2 = cities[j]
            dx = city1['x'] - city2['x']
            dy = city1['y'] - city2['y']
            distance = math.sqrt(dx*dx + dy*dy)
            edges.append((distance, city1['id'], city2['id'], city1, city2))
    
    # 3. 按距离排序边
    edges.sort(key=lambda x: x[0])
    
    # 4. 选择最小生成树的边
    while unvisited and edges:
        # 找到连接已访问和未访问节点的最短边
        for i, (distance, id1, id2, city1, city2) in enumerate(edges):
            if (id1 in visited and id2 in unvisited) or (id2 in visited and id1 in unvisited):
                # 生成贝塞尔曲线控制点，创建自然弯曲的道路
                mid_x = (city1['x'] + city2['x']) / 2
                mid_y = (city1['y'] + city2['y']) / 2
                offset_range = int(distance * 0.3)  # 偏移范围与距离成正比
                cp_x = mid_x + random.randint(-offset_range, offset_range)
                cp_y = mid_y + random.randint(-offset_range, offset_range)
                
                roads.append({
                    "city1_id": id1,
                    "city2_id": id2,
                    "control_points": [(cp_x, cp_y)]
                })
                
                # 更新访问状态
                if id1 in unvisited:
                    visited.add(id1)
                    unvisited.remove(id1)
                else:
                    visited.add(id2)
                    unvisited.remove(id2)
                
                # 从边列表中移除已处理的边
                edges.pop(i)
                break
        else:
            # 没有找到可用边，退出循环（防止死循环）
            break
    
    return roads

def save_game_state():
    game_state = {
        'current_turn': current_turn,
        'cities': cities,
        'players': players,
        'armies': armies,
        'roads': roads,
        'global_lines': global_lines,
        'turn_report': turn_report,
        'is_paused': is_paused,
        'commentary_result': commentary_result,
        'command_history': command_history,
        'game_events': game_events
    }
    # 创建存档目录
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    # 生成带回合数的文件名
    save_filename = f"game_state_{current_turn}.json"
    save_path = os.path.join(config.SAVE_DIR, save_filename)
    # 保存当前状态
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(game_state, f, ensure_ascii=False, indent=2)
    # 清理旧存档
    clean_old_saves()

def clean_old_saves():
    # 获取所有存档文件
    save_files = [f for f in os.listdir(config.SAVE_DIR) if f.startswith('game_state_') and f.endswith('.json')]
    # 解析回合数并排序
    save_files_with_turns = []
    for filename in save_files:
        try:
            # 提取回合数，例如game_state_123.json -> 123
            turn_number = int(filename.split('_')[2].split('.')[0])
            save_files_with_turns.append((turn_number, filename))
        except (IndexError, ValueError):
            # 忽略不符合命名规范的文件
            continue
    # 按回合数排序
    save_files_with_turns.sort()
    # 如果超过最大存档数，删除最旧的
    if len(save_files_with_turns) > config.MAX_SAVE_SLOTS:
        # 需要删除的文件数量
        files_to_delete = len(save_files_with_turns) - config.MAX_SAVE_SLOTS
        # 删除最旧的文件
        for turn_number, filename in save_files_with_turns[:files_to_delete]:
            file_path = os.path.join(config.SAVE_DIR, filename)
            os.remove(file_path)

def load_game_state():
    global current_turn, cities, players, armies, roads, global_lines, turn_report, is_paused, commentary_result, command_history, game_events
    try:
        # 获取所有存档文件
        save_files = [f for f in os.listdir(config.SAVE_DIR) if f.startswith('game_state_') and f.endswith('.json')]
        if not save_files:
            print("没有找到存档文件")
            return False
        
        # 解析回合数并找到最新的
        latest_turn = -1
        latest_file = None
        for filename in save_files:
            try:
                turn_number = int(filename.split('_')[2].split('.')[0])
                if turn_number > latest_turn:
                    latest_turn = turn_number
                    latest_file = filename
            except (IndexError, ValueError):
                continue
        
        if not latest_file:
            print("没有有效的存档文件")
            return False
        
        # 加载最新的存档
        save_path = os.path.join(config.SAVE_DIR, latest_file)
        with open(save_path, 'r', encoding='utf-8') as f:
            game_state = json.load(f)
        
        # 更新全局变量
        current_turn = game_state['current_turn']
        cities = game_state['cities']
        players = game_state['players']
        armies = game_state['armies']
        roads = game_state['roads']
        global_lines = game_state['global_lines']
        turn_report = game_state['turn_report']
        is_paused = game_state['is_paused']
        commentary_result = game_state['commentary_result']
        command_history = game_state['command_history']
        game_events = game_state['game_events']
        return True
    except Exception as e:
        print(f"加载存档失败: {e}")
        return False

def generate_players(cities, players):
    for i in range(PLAYER_COUNT):
        # 获取对应势力信息
        faction = players[i]
        if faction["start_city"]:
            start_city = [c for c in cities if c["name"] == faction["start_city"]][0]
        else:        
            # 随机选择一个未被占用的城池
            available_cities = [c for c in cities if all(pid == NEUTRAL_FACTION for pid in c["garrisons"])]
            start_city = random.choice(available_cities)
        # 移除无主标记并设置玩家初始兵力
        if NEUTRAL_FACTION in start_city["garrisons"]:
            del start_city["garrisons"][NEUTRAL_FACTION]
        start_city["garrisons"][faction["name"]] = config.INITIAL_PLAYER_TROOPS  # 使用势力名称作为键
        # 初始化玩家状态属性
        faction.setdefault("is_defeated", False)
        faction.setdefault("alive_turns", 0)
    return players


def generate_cities(count):
    """生成指定数量的城池并返回城池列表"""
    cities = []
    for i in range(count):
        # 随机城池大小：小型(1)、中型(2)、大型(3)
        size = random.choice([1, 2, 3])
        
        # 根据大小设置增长速度：小型1/秒，中型2/秒，大型3/秒
        growth_rate = math.floor(ARMY_TROOPS_GROW_RATE * (1+random.random()))
        
        # 网格划分法生成均匀分布的城池位置
        # 确保城池在地图内可见（考虑最大半径16px）
        min_distance = config.CITY_MIN_DISTANCE  # 城池间最小距离（像素）
        max_attempts = config.CITY_MAX_ATTEMPTS  # 最大尝试次数
        grid_rows = 3  # 网格行数
        grid_cols = 4  # 网格列数
        grid_width = (config.MAP_WIDTH - 40) // grid_cols
        grid_height = (config.MAP_HEIGHT - 40) // grid_rows
        attempts = 0
        x, y = 0, 0
        placed = False
        
        # 为当前城池分配网格位置
        grid_index = i % (grid_rows * grid_cols)
        grid_x = grid_index % grid_cols
        grid_y = grid_index // grid_cols
        
        while attempts < max_attempts and not placed:
            # 在分配的网格内随机生成位置，增加随机扰动
            x = 20 + grid_x * grid_width + random.randint(int(grid_width * 0.2), int(grid_width * 0.8))
            y = 20 + grid_y * grid_height + random.randint(int(grid_height * 0.2), int(grid_height * 0.8))
            too_close = False
        
            # 检查与现有城池的距离
            for city in cities:
                dx = x - city['x']
                dy = y - city['y']
                distance = (dx**2 + dy**2)**0.5
                if distance < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                placed = True
                break
            
            attempts += 1
        
        # 如果在指定网格内无法放置，则回退到随机放置
        if not placed:
            while attempts < max_attempts:
                x = random.randint(20, config.MAP_WIDTH - 20)
                y = random.randint(20, config.MAP_HEIGHT - 20)
                too_close = False
        
                for city in cities:
                    dx = x - city['x']
                    dy = y - city['y']
                    distance = (dx**2 + dy**2)**0.5
                    if distance < min_distance:
                        too_close = True
                        break
                
                if not too_close:
                    placed = True
                    break
                
                attempts += 1
        
        cities.append({
            "id": i,
            "name": three_kingdoms_cities[i],
            "size": size,
            "garrisons": {NEUTRAL_FACTION: 50 if size == 3 else (30 if size == 2 else 10)},
            "growth_rate": growth_rate,
            "x": x,
            "y": y
        })
    return cities


def validate_send_army_params(data):
    """验证派遣大军的参数"""
    required_fields = ['city_name', 'dest_city_name', 'player_name', 'troops']
    if not all(field in data for field in required_fields):
        print("缺少必要参数")
        return False, "缺少必要参数"
    if not isinstance(data['troops'], int) or data['troops'] <= 0:
        print("兵力必须为正整数")
        return False, "兵力必须为正整数"
    return True, "参数验证通过"


def get_city_by_id(city_id):
    """根据ID查找城市"""
    return next((c for c in cities if c['id'] == city_id), None)


def get_city_by_name(city_name):
    """根据名称查找城市"""
    return next((c for c in cities if c['name'] == city_name), None)


def check_road_exists(city1_id, city2_id):
    """检查两个城市之间是否有道路连接"""
    for road in roads:
        if (road['city1_id'] == city1_id and road['city2_id'] == city2_id) or \
           (road['city1_id'] == city2_id and road['city2_id'] == city1_id):
            return True
    return False


def check_player_garrison(city, player_name, required_troops):
    """检查玩家是否拥有城市且有足够兵力"""
    if not city:
        return False, "城市不存在"
    if player_name not in city['garrisons']:
        return False, f"{player_name}不拥有该城市"
    if city['garrisons'][player_name] < required_troops:
        return False, "兵力不足"
    return True, "验证通过"


def calculate_movement_details(start_city, dest_city, has_road):
    """计算大军移动细节（距离、方向、所需回合）"""
    start_x, start_y = start_city['x'], start_city['y']
    end_x, end_y = dest_city['x'], dest_city['y']
    dx = end_x - start_x
    dy = end_y - start_y
    distance = (dx**2 + dy**2)**0.5
    
    if distance == 0:
        return 0, 0, 0, 0, 1
        
    direction_x = dx / distance
    direction_y = dy / distance
    speed = ROAD_SPEED if has_road else NO_ROAD_SPEED
    required_turns = int(distance / speed) + 1
    return start_x, start_y, direction_x, direction_y, distance, required_turns, speed


def create_army(start_city_id, dest_city_id, player_name, troops, start_x, start_y, direction_x, direction_y, distance, required_turns, speed):
    """创建新大军并添加到军队列表"""
    army_id = len(armies)
    army = {
        "id": army_id,
        "player_name": player_name,
        "troops": troops,
        "start_city_id": start_city_id,
        "dest_city_id": dest_city_id,
        "current_x": start_x,
        "current_y": start_y,
        "direction_x": direction_x,
        "direction_y": direction_y,
        "distance_remaining": distance,
        "required_turns": required_turns,
        "speed": speed
    }
    armies.append(army)
    return army_id


def process_army_movement():
    global armies, cities
    armies_to_remove = []
    for army in armies:
        # 计算本回合移动距离
        move_distance = army['speed']
        if army['distance_remaining'] <= move_distance:
            # 大军到达目的地
            dest_city = next((c for c in cities if c['id'] == army['dest_city_id']), None)
            if dest_city:
                # 将大军兵力加入目标城池
                player_name = army['player_name']
                if player_name in dest_city['garrisons']:
                    # 两军汇合
                    dest_city['garrisons'][player_name] += army['troops']
                else:
                    # 发生战斗
                    dest_city['garrisons'][player_name] = army['troops']
                    # 异步播放战斗音频
                    threading.Thread(target=play_random_battle_audio).start()
            armies_to_remove.append(army)
        else:
            # 大军继续移动
            army['current_x'] += army['direction_x'] * move_distance
            army['current_y'] += army['direction_y'] * move_distance
            army['distance_remaining'] -= move_distance
            army['required_turns'] -= 1

    # 移除已到达目的地的大军
    for army in armies_to_remove:
        if army in armies:
            armies.remove(army)

def play_random_battle_audio():
    battle_dir = os.path.join(os.path.dirname(__file__), 'music', 'battle')
    if not os.path.exists(battle_dir):
        return
    mp3_files = [f for f in os.listdir(battle_dir) if f.endswith('.mp3')]
    if not mp3_files:
        return
    selected_file = random.choice(mp3_files)
    file_path = os.path.join(battle_dir, selected_file)
    try:
        mixer.music.load(file_path)
        mixer.music.play()
    except Exception as e:
        print(f"Error playing audio: {e}")

def process_city_troop_growth():
    global cities
    for city in cities:
        # 获取城池的主人势力（兵力最多的势力）
        if not city['garrisons']:
            continue  # 无主城池不增长兵力
        # 找出兵力最多的势力作为城池主人
        owner_name = max(city['garrisons'], key=city['garrisons'].get)
        
        # 为城池主人增长兵力
        if owner_name == NEUTRAL_FACTION:
            # 中立城池，兵力上限为MAX_NPC_TROOPS
            MAX_NPC_TROOPS_temp = math.floor(MAX_NPC_TROOPS * (1+random.random()))
            if city['garrisons'][owner_name] < MAX_NPC_TROOPS_temp:
                # 降低中立城池的兵力增长
                city['garrisons'][owner_name] += math.floor((city['growth_rate']) * 0.3)
                if city['garrisons'][owner_name] > MAX_NPC_TROOPS_temp:
                    city['garrisons'][owner_name] = MAX_NPC_TROOPS_temp + math.floor(city['growth_rate'] * random.random())
        else:
            # 玩家城池，兵力上限为MAX_PLAYER_TROOPS
            if city['garrisons'][owner_name] < MAX_PLAYER_TROOPS:
                city['garrisons'][owner_name] += city['growth_rate']
                if city['garrisons'][owner_name] > MAX_PLAYER_TROOPS:
                    city['garrisons'][owner_name] = MAX_PLAYER_TROOPS + math.floor(city['growth_rate'] * random.random())


def process_city_battles():
    global cities
    for city in cities:
        # 只有一个势力或无主城池不发生战斗
        if len(city['garrisons']) <= 1:
            continue

        # 多个势力，基于总兵力计算固定损耗
        losses = {}
        total_troops = sum(city['garrisons'].values())  # 计算总兵力

        loss_amount = total_troops * 0.01
        if loss_amount < ARMY_TROOPS_GROW_RATE * 2:
            loss_amount = ARMY_TROOPS_GROW_RATE * 2
        
        loss_amount = math.floor(loss_amount)
        # 为每个势力分配相同的损失数量
        for player_id in city['garrisons']:
            losses[player_id] = loss_amount

        # 应用兵力损失
        for player_id, loss in losses.items():
            city['garrisons'][player_id] -= loss
            # 移除兵力为0的势力
            if city['garrisons'][player_id] <= 0:
                # 记录军队被消灭事件
                event_content = f'{player_id} 的军队在 {city['name']} 阵亡'
                # 保持最近30条事件
                if len(game_events) > 30:
                    game_events.pop(0)
                del city['garrisons'][player_id]
                if len(city['garrisons']) == 1:
                    for player_id in city['garrisons']:
                        event_content += f"，{player_id} 占领了 {city['name']} "
                event = {
                    "type": "army_death",
                    "turn": current_turn,
                    "player_id": player_id,
                    "city_id": city['id'],
                    "content": event_content,
                }
                game_events.append(event)


def check_player_defeat_status():
    global players, cities, armies, is_paused
    # 检查玩家是否还有城池，没有则标记为失败
    for player in players:
        has_city = any(player['name'] in city['garrisons'] for city in cities)
        if not has_city:
            # 如果已经失败，不更新存活回合数
            if not player['is_defeated']:
                player['alive_turns'] = current_turn
            player['is_defeated'] = True
            # 清理该玩家的所有出征军队
            armies[:] = [army for army in armies if army['player_name'] != player['name']]
    
    # 检查游戏是否结束并保存存档
    alive_players = [p for p in players if not p.get('is_defeated', False)]
    if len(alive_players) <= 1:
        save_game_state()
        is_paused = True


def calculate_player_stats():
    global players, cities
    # 计算玩家总军力和占领城池数量
    for player in players:
        total_troops = 0
        city_count = 0
        for city in cities:
            if player['name'] in city['garrisons']:
                total_troops += city['garrisons'][player['name']]
                city_count += 1
        player['total_troops'] = total_troops
        player['city_count'] = city_count  # 新增：统计玩家占领城池数量


def generate_turn_report():
    global cities, current_turn, armies, players, turn_report
    
    # 构建回合简报内容
    report = f"第 {current_turn} 回合简报：\n\n"
    
    # 1. 回合基本信息
    report += "=== 基本信息 ===\n"
    report += f"当前回合：{current_turn}\n"
    report += f"活跃玩家数：{len([p for p in players if not p.get('is_defeated', False)])}\n"
    report += f"城池总数：{len(cities)}\n"
    report += f"移动中军队数：{len(armies)}\n\n"
    
    # 2. 玩家状态详情
    report += "=== 玩家状态 ===\n"
    for player in players:
        status = "活跃" if not player.get('is_defeated', False) else "已被击败"
        report += f"- {player['name']}：{status}，总兵力 {player.get('total_troops', 0)}，占领城池 {player.get('city_count', 0)} 座\n"
    
    # 3. 城池详情
    report += "\n=== 城池情况 ===\n"
    for city in cities:
        garrisons = city.get('garrisons', {})
        if garrisons:
            controller = ", ".join([f"{p}（{int(t)}兵力）" for p, t in garrisons.items()])
        else:
            controller = "无主"
        # 检查是否有多个玩家军队，添加交战状态
        battle_status = "，正在交战中" if len(garrisons) > 1 else ""
        report += f"- {city['name']}：{controller} {battle_status}，增长率 {city.get('growth_rate', 0)} \n"
    
    # 4. 军队移动情况
    report += "\n=== 军队移动 ===\n"
    if armies:
        for army in armies:
            start_city = get_city_by_id(army['start_city_id'])
            dest_city = get_city_by_id(army['dest_city_id'])
            # report += f"- 军队{army['id']}（{army['player_name']}）：从 {start_city['name']} 前往 {dest_city['name']}，当前位置（{army['current_x']:.1f},{army['current_y']:.1f}），剩余距离{army['distance_remaining']:.1f}，需{army['required_turns']}回合，兵力{army['troops']}\n"
            report += f"- 军队{army['id']}（{army['player_name']}）：从 {start_city['name']} 到 {dest_city['name']}，{army['required_turns']}个回合后到达，兵力{army['troops']}\n"
    else:
        report += "- 无移动中的军队\n"
    
    # 5. 道路情况
    report += "\n=== 道路情况（邻接列表）：每个城市及其相邻城市 ===\n"
    if 'roads' in globals() and roads:
        # 构建邻接列表
        adjacency_list = {}
        for road in roads:
            start_id = road.get('city1_id', '未知')
            dest_id = road.get('city2_id', '未知')
            start_city = get_city_by_id(start_id)['name']
            dest_city = get_city_by_id(dest_id)['name']
            
            # 添加双向连接
            if start_city not in adjacency_list:
                adjacency_list[start_city] = set()
            adjacency_list[start_city].add(dest_city)
            
            if dest_city not in adjacency_list:
                adjacency_list[dest_city] = set()
            adjacency_list[dest_city].add(start_city)
        
        # 转换为排序后的列表并生成报告
        for city in sorted(adjacency_list.keys()):
            neighbors = sorted(adjacency_list[city])
            report += f"- {city}: [{', '.join(neighbors)}]\n"
    else:
        report += "- 无道路信息\n"
    
    # 6. 玩家台词历史
    report += "\n=== 玩家台词历史 ===\n"
    # 获取最近10条台词
    recent_lines = global_lines[-20:] if len(global_lines) >= 20 else global_lines
    for line in recent_lines:
        report += f"- {line}\n"

    # 7. 玩家命令历史
    report += "\n=== 玩家命令历史 ===\n"
    for cmd in command_history[-20:]:
        comand_result=""
        if cmd['result'] == "success":
            comand_result = "有效命令"
        else:
            comand_result = "无效命令"
            
        report += f"- 回合: {cmd['turn']}, 玩家: {cmd['player_name']} 执行: {comand_result}: {cmd['command']}\n"

    # 8. 游戏事件历史
    report += "\n=== 游戏事件历史 ===\n"
    for event in game_events[-20:]:
        report += f"- {event}\n"

    # 保存简报到全局变量
    turn_report = report

def update_game_state():
    global is_paused, current_turn, commentary_result
    if is_paused:
        return
    
    current_turn += 1
    process_army_movement()

    # 2. 处理城池兵力增长
    process_city_troop_growth()

    # 3. 处理城池战斗
    process_city_battles()

    # 4. 检查玩家失败状态
    check_player_defeat_status()

    # 5. 计算玩家统计数据
    calculate_player_stats()

    # 6. 生成回合简报
    generate_turn_report()

    # 7. 通知AI玩家进行处理操作
    notify_ai_players()

    # 生成解说
    if current_turn % COMMENTARY_INTERVAL == 0 and not commentary_working:
        threading.Thread(target=generate_commentary, args=(turn_report,)).start()
    
    # 保存游戏进度
    if current_turn % config.SAVE_INTERVAL == 0:
        save_game_state()
    
def get_player_by_name(player_name):
    for player in players:
        if player['name'] == player_name:
            return player
    return None


# 添加暂停和恢复游戏的函数
def pause_game():
    global is_paused
    is_paused = True

def resume_game():
    global is_paused
    is_paused = False


def notify_ai_players():
    """通知所有活跃的AI玩家进行回合操作"""
    global players, agents, turn_report
    if current_turn > 10:
        for player in players:
            if not player.get('is_defeated', False):
                player_name = player["name"]
                if player_name not in agents:
                    agents[player_name] = Agent(player["model"])
                agentTask = AgentTask()
                agentTask.init(player_name, agents[player_name], turn_report, player)
                agentTask.start()
        

class CommentaryTask(threading.Thread):
    agent=None
    message=''
    def init(self, agent:Agent, message:str):
        self.agent=agent
        self.message = message

    def run(self):
        global commentary_result,commentary_working
        if self.agent == None :
            # 初始化解说员
            self.agent = Agent(config.COMMENTARY_MODEL_NAME)
        commentary_result_output = self.agent.send(self.message)
        commentary_result = commentary_result_output
        # 根据配置决定是否生成并播放音频
        if config.ENABLE_AUDIO_GENERATION:
            voice_file_name = voice.generate_voice_by_tongyi_tts(commentary_result_output)
            voice.play_voice_file(voice_file_name) 
        commentary_working = False
        return

def generate_commentary(game_report):
    global commentary_agent,commentary_working
    if commentary_working :
        return
    else:
        commentary_working = True
    game_commentary = f"""
        你是一名幽默的游戏解说员，请根据下面的战况生成约50字的解说词。
        禁止出现总结性语言，直接呈现解说词！
        {game_report}
    """
    task = CommentaryTask()
    task.init(commentary_agent,game_commentary)
    task.start()

# 记录玩家历史命令
def add_command_history(turn, player_name, command, result):
    global command_history, players
    # 存储命令历史
    if len(command_history) > 30:
        command_history.pop(0)  # 移除最旧的记录
    command_history.append({
        "turn": turn,
        "player_name": player_name,
        "command": command,
        "result": result
    })
    
    # 更新玩家命令统计
    for player in players:
        if player["name"] == player_name:
            # 初始化统计字段（如果不存在）
            if "total_commands" not in player:
                player["total_commands"] = 0
            if "successful_commands" not in player:
                player["successful_commands"] = 0
            
            # 增加总命令数
            player["total_commands"] += 1
            
            # 如果命令成功，增加成功命令数
            if result == "success":
                player["successful_commands"] += 1
            break


        

