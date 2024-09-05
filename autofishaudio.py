import pyaudiowpatch as pyaudio
import audioop
import pyautogui
import time
import random

# 声音分析参数
THRESHOLD = 1000  # 阈值，需要自己调试
FISHING_KEY = ','  # 钓鱼键，按照游戏设置
CATCH_KEY = '.'    # 收杆键，按照游戏设置
LEFT_WALK_KEY = 'a' #向左平移按键，按照游戏设置
RIGHT_WALK_KEY = 'd' #向右平移按键，按照游戏设置
WALK_AMPLITUDE = 1 #左右平移幅度，需要自己调试
FISHING_TIME_IN_HOUR_MIN = 2  # 钓鱼时间，小时
FISHING_TIME_IN_HOUR_MAX = 3.5  # 钓鱼时间，小时

MAX_FISHING_TIME_ONE_TIME = 22  # 最大钓鱼时间，秒
CHUNK_SIZE = 512

p = pyaudio.PyAudio()
wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
default_speakers = p.get_device_info_by_index(
    wasapi_info["defaultOutputDevice"])

if not default_speakers["isLoopbackDevice"]:
    for loopback in p.get_loopback_device_info_generator():
        """
        Try to find loopback device with same name(and [Loopback suffix]).
        Unfortunately, this is the most adequate way at the moment.
        """
        if default_speakers["name"] in loopback["name"]:
            default_speakers = loopback
            break


def random_press(key):
    press_time = random.uniform(0.1, 0.2)
    pyautogui.keyDown(key)
    time.sleep(press_time)
    pyautogui.keyUp(key)


def print_decibel_bar(decibel):
    # 每50分贝打印一个方块
    num_blocks = decibel // 50
    bar = '=' * num_blocks  # 使用方块字符
    print(f"Decibel: {decibel} [{bar}]")


stream = p.open(format=pyaudio.paInt16,
                channels=default_speakers["maxInputChannels"],
                rate=int(default_speakers["defaultSampleRate"]),
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                input_device_index=default_speakers["index"])


def detect_sound():
    # 读取声音数据
    data = stream.read(1024)
    # 获取声音的分贝值
    decibel = audioop.rms(data, 2)
    print_decibel_bar(decibel)
    return decibel > THRESHOLD


def move_around():
    key1 = random.choice([LEFT_WALK_KEY, RIGHT_WALK_KEY])
    pyautogui.keyDown(key1)

    wait = random.uniform(0, 0.1)*WALK_AMPLITUDE
    wait2 = random.uniform(0, 0.1)*WALK_AMPLITUDE+wait
    time.sleep(random.uniform(wait, wait2))

    wait = random.uniform(0, 0.1)*WALK_AMPLITUDE
    key2 = random.choice([LEFT_WALK_KEY, RIGHT_WALK_KEY])
    pyautogui.keyDown(key2)
    time.sleep(wait)
    pyautogui.keyUp(key1)

    wait = random.uniform(0, 0.01)*WALK_AMPLITUDE
    wait2 = random.uniform(0, 0.1)*WALK_AMPLITUDE+wait
    time.sleep(random.uniform(wait, wait2))

    wait = random.uniform(0, 0.1)*WALK_AMPLITUDE
    key3 = random.choice([LEFT_WALK_KEY, RIGHT_WALK_KEY])
    pyautogui.keyDown(key3)
    time.sleep(wait)
    pyautogui.keyUp(key2)

    wait = random.uniform(0, 0.1)*WALK_AMPLITUDE
    wait2 = random.uniform(0, 0.1)*WALK_AMPLITUDE+wait
    time.sleep(random.uniform(wait, wait2))
    pyautogui.keyUp(key3)


def fish():
    # 模拟按下钓鱼键
    random_press(FISHING_KEY)
    print('Start fishing...')
    start_time = time.time()

    while time.time() - start_time < MAX_FISHING_TIME_ONE_TIME:
        if detect_sound():
            if time.time() - start_time > 2:
                time.sleep(random.uniform(0.12321, 0.19773)),
                random_press(CATCH_KEY)
                print('Catch!')
                break
        time.sleep(0.0333),

    # 等待随机时间后再次钓鱼
    print('Wait for next fishing...')

    behaviour = random.uniform(0., 10.)
    if behaviour < 0.5:
        move_around()

    time.sleep(random.uniform(1.434, 2.918))


# 主循环.
print('Start in 5 Sec!')
time.sleep(5)
overall_start_time = time.time()
random_fish_time = random.uniform(
    FISHING_TIME_IN_HOUR_MIN, FISHING_TIME_IN_HOUR_MAX)
while time.time() - overall_start_time < random_fish_time*3600:
    fish()

print('End')
