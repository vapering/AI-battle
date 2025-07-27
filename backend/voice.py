import os,uuid,requests
import dashscope
import pygame
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer
from dashscope.audio.qwen_tts import SpeechSynthesizer
from collections import deque
import threading
import time

dashscope.api_key = 'xxxxxxxxxxxxxxxxxxxxxxx'  # 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
prefix = 'prefix'
target_model = "cosyvoice-v2"
voice_working = False

# 创建语音注册服务实例
service = VoiceEnrollmentService()

# 调用create_voice方法复刻声音，并生成voice_id
def create_voice(url):
    # 请按实际情况进行替换
    # url = 'https://hxntest.oss-cn-beijing.aliyuncs.com/%E6%9B%B9%E6%93%8D-%E8%AF%AD%E9%9F%B3.mp3'  
    # 避免频繁调用 create_voice 方法。每次调用都会创建新音色，每个阿里云主账号最多可复刻 1000 个音色，超额时请删除不用的音色或申请扩容。
    voice_id = service.create_voice(target_model=target_model, prefix=prefix, url=url)
    print("requestId: ", service.get_last_request_id())
    print(f"your voice id is {voice_id}")

# 全局语音队列，最多存储10个台词任务
voice_queue = deque(maxlen=10)
# 线程停止事件
stop_event = threading.Event()

def generate_voice_file(voice_id, text)->str:
    # 使用复刻的声音进行语音合成
    synthesizer = SpeechSynthesizer(model=target_model, voice=voice_id)
    audio = synthesizer.call(text)
    print("requestId: ", synthesizer.get_last_request_id())
    uuid_filename = str(uuid.uuid4())
    voice_file_name = f"D:/tmp/{uuid_filename}.mp3"
    with open(voice_file_name,'wb') as f:
        f.write(audio)
    return voice_file_name

def play_voice_file(voice_file_name):
    # 使用pygame播放音频
    pygame.mixer.init()
    pygame.mixer.music.load(voice_file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and not stop_event.is_set():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(voice_file_name)

def voice_real_work(voice_id, text):
    # 使用复刻的声音进行语音合成
    voice_file_name = generate_voice_file(voice_id, text)
    play_voice_file(voice_file_name)

def voice_worker():
    """后台线程处理语音队列任务"""
    while not stop_event.is_set():
        if voice_queue:
            # 获取队列中的第一个任务
            voice_id, text = voice_queue.pop()
            try:
                voice_real_work(voice_id, text)
            except Exception as e:
                print(f"语音处理错误: {str(e)}")
        else:
            # 队列为空时短暂休眠
            time.sleep(1)

# 启动后台工作线程
threading.Thread(target=voice_worker, daemon=True).start()

def generate_voice(voice_id, text):
    """添加语音任务到队列"""
    # 添加到队列，超过10个会自动移除最老的任务
    # voice_queue.append((voice_id, text))
    return True

def generate_voice_by_tongyi_tts(text):
    response = SpeechSynthesizer.call(
        model="qwen-tts-latest",
        text=text,
        voice="Dylan",
    )
    audio_url = response.output.audio["url"]
    uuid_filename = str(uuid.uuid4())
    save_path = f"D:/tmp/{uuid_filename}.wav"
    try:
        response = requests.get(audio_url)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"音频文件已保存至：{save_path}")
        return save_path
    except Exception as e:
        print(f"下载失败：{str(e)}")
        return None

if __name__ == "__main__":
    # create_voice('https://hxntest.oss-cn-beijing.aliyuncs.com/%E5%AD%99%E6%9D%832.mp3')
    # generate_voice('cosyvoice-v2-prefix-6fefd4b472ce4b2da7448f2df134a494',
    # "江东鼠辈，休走，吃我一记方天画戟！")
#     voice_content="""
# 美国AI三巨头战场对决！谁才是战略游戏的真·王者？马斯克Grok、谷歌Gemini、还是 微软O4-mini ？开战！
#     """
    voice_contents = [
'今天是神仙打架！决赛圈：榜首KIMI K2 VS 谷歌杀神Gemini-2.5！黑马o4-mini能否逆袭？',
'Gemini纽约起家，爆兵速度开挂！瞬间锁定战力榜TOP1！',
'o4-mini德州翻车！东西包抄，瞬间被抄家蒸发！',
'西部霸主KIMI K2强势崛起！坐拥半壁江山，虎视眈眈！ ',
'Gemini杀疯了！寸土不让，血腥绞杀！KIMI主力被斩尽杀绝... Gemini成为当之无愧的新王登基榜首！',
    ]
    for voice_content in voice_contents:
        file = generate_voice_by_tongyi_tts(voice_content)
    # voice_content='恭喜Gemini-2.5-flash获胜登顶！全程压制，统治战场！不到1小时终结比赛！留下一句：“Kimi K2？抱歉，你4个小时才啃下的局，我一杯咖啡的功夫就结束了。” '
    # generate_voice_by_tongyi_tts(voice_content)
    # play_voice_file(file)

