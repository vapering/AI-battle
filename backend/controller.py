from flask import Blueprint, request, jsonify
import service
import config
import datetime
import xmltodict
from service import command_history, current_turn

# 创建蓝图
game_bp = Blueprint('game', __name__)

@game_bp.route('/initialize_game', methods=['POST'])
def initialize_game():
    """初始化游戏"""
    service.initialize_game_from_backend()
    return jsonify({"status": "success", "message": "游戏初始化成功"})


@game_bp.route('/initialize_game_from_frontend', methods=['POST'])
def initialize_game_from_frontend():
    """初始化游戏"""
    data = request.json
    citys = data['stateInfo']
    roads = data['roads']
    # print(f"请求参数：{request.data}")
    service.initialize_game_from_frontend(citys,roads)
    return jsonify({"status": "success", "message": "游戏初始化成功"})



@game_bp.route('/get_game_state', methods=['GET'])
def get_game_state():
    """获取当前游戏状态"""
    return jsonify({
        "cities": service.cities,
        "players": service.players,
        "roads": service.roads,
        "armies": service.armies,
        "current_turn": service.current_turn,
        "mapSize":{
            "width": config.MAP_WIDTH,
            "height": config.MAP_HEIGHT
        },
        "turn_report": service.turn_report,
        "global_lines": service.global_lines,  # 返回全局台词列表
        "is_paused": service.is_paused,  # 添加游戏暂停状态
        "commentary_result": service.commentary_result,
        "command_history":service.command_history,
        "game_events":service.game_events,
    })


@game_bp.route('/update_game', methods=['POST'])
def update_game():
    """更新游戏状态（进行一回合）"""
    service.update_game_state()
    return jsonify({
        "status": "success",
        "current_turn": service.current_turn,
        "message": f"已完成第{service.current_turn - 1}回合更新"
    })

def execute_command(data):
    # 参数验证
    player_name = data["player_name"]
    if isinstance(data['troops'], str):
        data['troops'] = int(data['troops'])
    valid, message = service.validate_send_army_params(data)
    if not valid:
        return {"status": "error", "message": message}, 400

    city_name = data['city_name']
    dest_city_name = data['dest_city_name']
    troops = data['troops']
    
    # 查找城市
    start_city = service.get_city_by_name(city_name)
    dest_city = service.get_city_by_name(dest_city_name)

    if not start_city:
        print(f"{player_name}, 出发城市 '{city_name}' 不存在")
        return {"status": "error", "message": f"出发城市 '{city_name}' 不存在"}, 404
    if not dest_city:
        print(f"{player_name}, 目标城市 '{dest_city_name}' 不存在")
        return {"status": "error", "message": f"目标城市 '{dest_city_name}' 不存在"}, 404
    # 检查道路连接
    has_road = service.check_road_exists(start_city['id'], dest_city['id'])
    if not has_road:
        message=f"{player_name}, {start_city['name']} 与 {dest_city['name']} 没有道路"
        print(message)
        return {"status": "error", "message": message}, 400

    # 检查兵力
    valid, message = service.check_player_garrison(start_city, player_name, troops)
    if not valid:
        message=f"{player_name}, {start_city['name']} 兵力不足"
        print(message)
        return {"status": "error", "message": message}, 400

    # 减少出发城市兵力
    start_city['garrisons'][player_name] -= troops
    
    # 计算移动细节
    start_x, start_y, direction_x, direction_y, distance, required_turns, speed = service.calculate_movement_details(start_city, dest_city, has_road)
    
    # 创建大军
    army_id = service.create_army(start_city['id'], dest_city['id'], player_name, troops, start_x, start_y, direction_x, direction_y, distance, required_turns, speed)
    result = {
        "status": "success",
        "message": f"派遣{troops}兵力从{start_city['name']}前往{dest_city['name']}",
        "army_id": army_id,
        "required_turns": required_turns
    }
    return result,200

@game_bp.route('/send_army', methods=['POST'])
def send_army():
    """派遣大军"""
    xml_data = request.data
    try:
        data_origin = xmltodict.parse(xml_data).get('root', {}) if xml_data else {}
    except xml.parsers.expat.ExpatError as e:
        return jsonify({"status": "error", "message": f"XML解析错误: {str(e)}"}), 400
    
    player_name = data_origin['player_name']
    # 添加时间和玩家前缀到台词
    line = f"第{service.current_turn}回合 {player_name}: {data_origin['line']}"

    
    # 添加到全局台词列表并限制数量为100条
    service.global_lines.append(line)
    if len(service.global_lines) > 100:
        service.global_lines.pop(0)
    # 执行具体的命令
    if 'command' in data_origin["commandList"]:
        commandList = data_origin["commandList"]['command']
        # 确保即使单个命令也被处理为列表
        if not isinstance(commandList, list):
            commandList = [commandList]
        for command_data in commandList:
            command_data["player_name"] = player_name
            result,status = execute_command(command_data)
            # 存储命令历史
            service.add_command_history(service.current_turn, player_name, result["message"], result["status"])
            if status != 200:
                print(result) 
                print(status)
    else: 
        print("error")
    return "{}",200


# 添加暂停和恢复游戏的API端点
@game_bp.route('/pause_game', methods=['POST'])
def pause_game():
    service.pause_game()
    return jsonify({"status": "success", "message": "游戏已暂停"})

@game_bp.route('/resume_game', methods=['POST'])
def resume_game():
    service.resume_game()
    return jsonify({"status": "success", "message": "游戏已恢复"})

@game_bp.route('/load_game', methods=['POST'])
def load_game():
    success = service.load_game_state()
    if success:
        return jsonify({"status": "success", "message": "游戏已从存档加载"})
    else:
        return jsonify({"status": "error", "message": "加载存档失败"}), 500

