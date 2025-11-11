"""
鼠标录制模块
负责监听和记录鼠标的所有操作
"""
import time
import json
from pynput import mouse
from threading import Thread


class MouseRecorder:
    """鼠标录制器"""
    
    def __init__(self):
        self.events = []  # 存储录制的事件
        self.is_recording = False
        self.start_time = None
        self.listener = None
        
    def start_recording(self):
        """开始录制"""
        self.events = []
        self.is_recording = True
        self.start_time = time.time()
        
        # 创建监听器
        self.listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self.listener.start()
        
    def stop_recording(self):
        """停止录制"""
        self.is_recording = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        return self.events
    
    def _get_timestamp(self):
        """获取相对时间戳（秒）"""
        return time.time() - self.start_time
    
    def _on_move(self, x, y):
        """鼠标移动事件"""
        if self.is_recording:
            self.events.append({
                'type': 'move',
                'x': x,
                'y': y,
                'timestamp': self._get_timestamp()
            })
    
    def _on_click(self, x, y, button, pressed):
        """鼠标点击事件"""
        if self.is_recording:
            self.events.append({
                'type': 'click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'timestamp': self._get_timestamp()
            })
    
    def _on_scroll(self, x, y, dx, dy):
        """鼠标滚轮事件"""
        if self.is_recording:
            self.events.append({
                'type': 'scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'timestamp': self._get_timestamp()
            })
    
    def save_to_file(self, filename):
        """保存录制内容到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filename):
        """从文件加载录制内容"""
        with open(filename, 'r', encoding='utf-8') as f:
            self.events = json.load(f)
        return self.events
    
    def get_event_count(self):
        """获取录制的事件数量"""
        return len(self.events)
    
    def get_duration(self):
        """获取录制时长（秒）"""
        if not self.events:
            return 0
        return self.events[-1]['timestamp']
