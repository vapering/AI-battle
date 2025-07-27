from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from config import *
from controller import game_bp
from service import update_game_state

app = Flask(__name__)
CORS(app)

# 注册游戏蓝图
app.register_blueprint(game_bp, url_prefix='/api')

def init_scheduler():
    # 初始化调度器
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_game_state, 'interval', seconds=TURN_INTERVAL)
    scheduler.start()
    # 确保在应用退出时关闭调度器
    atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    init_scheduler()
    app.run(debug=True, port=5000)

def init_scheduler():
    # 初始化调度器
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_game_state, 'interval', seconds=TURN_INTERVAL)
    scheduler.start()
    # 确保在应用退出时关闭调度器
    atexit.register(lambda: scheduler.shutdown())

init_scheduler()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    init_scheduler()