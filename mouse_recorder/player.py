"""
鼠标回放模块
负责回放录制的鼠标操作
"""
import time
from pynput.mouse import Button, Controller
from threading import Thread


class MousePlayer:
    """鼠标回放器"""
    
    def __init__(self):
        self.mouse = Controller()
        self.is_playing = False
        self.should_stop = False
        self.play_thread = None
        self.loop = False
        self.speed = 1.0  # 播放速度倍数
        
    def play(self, events, loop=False, speed=1.0):
        """
        开始回放
        :param events: 事件列表
        :param loop: 是否循环播放
        :param speed: 播放速度（1.0为正常速度）
        """
        if self.is_playing:
            return False
        
        self.loop = loop
        self.speed = speed
        self.should_stop = False
        
        # 在新线程中播放，避免阻塞GUI
        self.play_thread = Thread(target=self._play_events, args=(events,))
        self.play_thread.daemon = True
        self.play_thread.start()
        
        return True
    
    def stop(self):
        """停止回放"""
        self.should_stop = True
        self.is_playing = False
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=1)
    
    def _play_events(self, events):
        """播放事件的内部方法"""
        if not events:
            return
        
        self.is_playing = True
        
        while not self.should_stop:
            last_timestamp = 0
            
            for event in events:
                if self.should_stop:
                    break
                
                # 等待到正确的时间点
                timestamp = event['timestamp']
                delay = (timestamp - last_timestamp) / self.speed
                if delay > 0:
                    time.sleep(delay)
                last_timestamp = timestamp
                
                # 执行事件
                self._execute_event(event)
            
            # 如果不循环，播放一次后退出
            if not self.loop:
                break
        
        self.is_playing = False
    
    def _execute_event(self, event):
        """执行单个事件"""
        event_type = event['type']
        
        try:
            if event_type == 'move':
                # 鼠标移动
                self.mouse.position = (event['x'], event['y'])
                
            elif event_type == 'click':
                # 鼠标点击
                x, y = event['x'], event['y']
                self.mouse.position = (x, y)
                
                # 解析按钮
                button_str = event['button']
                if 'left' in button_str.lower():
                    button = Button.left
                elif 'right' in button_str.lower():
                    button = Button.right
                elif 'middle' in button_str.lower():
                    button = Button.middle
                else:
                    button = Button.left
                
                # 按下或释放
                if event['pressed']:
                    self.mouse.press(button)
                else:
                    self.mouse.release(button)
                    
            elif event_type == 'scroll':
                # 鼠标滚轮
                x, y = event['x'], event['y']
                self.mouse.position = (x, y)
                self.mouse.scroll(event['dx'], event['dy'])
                
        except Exception as e:
            print(f"执行事件时出错: {e}")
    
    def is_playing_now(self):
        """检查是否正在播放"""
        return self.is_playing
