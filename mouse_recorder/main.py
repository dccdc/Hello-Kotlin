"""
鼠标录制回放工具 - 主界面
支持录制、回放、循环播放鼠标操作
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from recorder import MouseRecorder
from player import MousePlayer


class MouseRecorderApp:
    """鼠标录制器GUI应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("鼠标录制回放工具")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # 初始化录制器和播放器
        self.recorder = MouseRecorder()
        self.player = MousePlayer()
        
        # 状态变量
        self.is_recording = False
        self.is_playing = False
        
        # 创建界面
        self._create_widgets()
        
        # 启动状态更新
        self._update_status()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="🖱️ 鼠标录制回放工具",
            font=("Arial", 18, "bold"),
            pady=15
        )
        title_label.pack()
        
        # 信息显示区域
        info_frame = tk.LabelFrame(self.root, text="录制信息", padx=15, pady=15)
        info_frame.pack(padx=20, pady=10, fill="x")
        
        self.event_count_label = tk.Label(info_frame, text="事件数量: 0", font=("Arial", 11))
        self.event_count_label.pack(anchor="w", pady=3)
        
        self.duration_label = tk.Label(info_frame, text="录制时长: 0.0 秒", font=("Arial", 11))
        self.duration_label.pack(anchor="w", pady=3)
        
        self.status_label = tk.Label(info_frame, text="状态: 就绪", font=("Arial", 11), fg="green")
        self.status_label.pack(anchor="w", pady=3)
        
        # 录制控制区域
        record_frame = tk.LabelFrame(self.root, text="录制控制", padx=15, pady=15)
        record_frame.pack(padx=20, pady=10, fill="x")
        
        self.record_btn = tk.Button(
            record_frame,
            text="🔴 开始录制",
            command=self.toggle_recording,
            font=("Arial", 12, "bold"),
            bg="#FF6B6B",
            fg="white",
            width=20,
            height=2
        )
        self.record_btn.pack(pady=5)
        
        # 回放控制区域
        play_frame = tk.LabelFrame(self.root, text="回放控制", padx=15, pady=15)
        play_frame.pack(padx=20, pady=10, fill="x")
        
        # 循环选项
        loop_frame = tk.Frame(play_frame)
        loop_frame.pack(pady=5)
        
        self.loop_var = tk.BooleanVar(value=True)
        loop_check = tk.Checkbutton(
            loop_frame,
            text="循环播放",
            variable=self.loop_var,
            font=("Arial", 11)
        )
        loop_check.pack(side="left")
        
        # 速度选项
        speed_label = tk.Label(loop_frame, text="速度:", font=("Arial", 11))
        speed_label.pack(side="left", padx=(20, 5))
        
        self.speed_var = tk.StringVar(value="1.0")
        speed_combo = ttk.Combobox(
            loop_frame,
            textvariable=self.speed_var,
            values=["0.5", "0.75", "1.0", "1.5", "2.0"],
            width=6,
            state="readonly"
        )
        speed_combo.pack(side="left")
        
        self.play_btn = tk.Button(
            play_frame,
            text="▶️ 开始回放",
            command=self.toggle_playing,
            font=("Arial", 12, "bold"),
            bg="#4ECDC4",
            fg="white",
            width=20,
            height=2
        )
        self.play_btn.pack(pady=5)
        
        # 文件操作区域
        file_frame = tk.Frame(self.root)
        file_frame.pack(padx=20, pady=10, fill="x")
        
        save_btn = tk.Button(
            file_frame,
            text="💾 保存录制",
            command=self.save_recording,
            font=("Arial", 10),
            width=15
        )
        save_btn.pack(side="left", padx=5)
        
        load_btn = tk.Button(
            file_frame,
            text="📂 加载录制",
            command=self.load_recording,
            font=("Arial", 10),
            width=15
        )
        load_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(
            file_frame,
            text="🗑️ 清空",
            command=self.clear_recording,
            font=("Arial", 10),
            width=10
        )
        clear_btn.pack(side="left", padx=5)
    
    def toggle_recording(self):
        """切换录制状态"""
        if not self.is_recording:
            # 开始录制
            if self.is_playing:
                messagebox.showwarning("警告", "请先停止回放！")
                return
            
            self.recorder.start_recording()
            self.is_recording = True
            self.record_btn.config(text="⏹️ 停止录制", bg="#FFA500")
            self.status_label.config(text="状态: 正在录制...", fg="red")
        else:
            # 停止录制
            self.recorder.stop_recording()
            self.is_recording = False
            self.record_btn.config(text="🔴 开始录制", bg="#FF6B6B")
            self.status_label.config(text="状态: 录制完成", fg="green")
            self._update_info()
    
    def toggle_playing(self):
        """切换回放状态"""
        if not self.is_playing:
            # 开始回放
            if self.is_recording:
                messagebox.showwarning("警告", "请先停止录制！")
                return
            
            if self.recorder.get_event_count() == 0:
                messagebox.showwarning("警告", "没有可回放的内容！请先录制。")
                return
            
            loop = self.loop_var.get()
            speed = float(self.speed_var.get())
            
            success = self.player.play(self.recorder.events, loop=loop, speed=speed)
            if success:
                self.is_playing = True
                self.play_btn.config(text="⏹️ 停止回放", bg="#FF6B6B")
                status_text = "状态: 正在回放..." + ("(循环)" if loop else "")
                self.status_label.config(text=status_text, fg="blue")
        else:
            # 停止回放
            self.player.stop()
            self.is_playing = False
            self.play_btn.config(text="▶️ 开始回放", bg="#4ECDC4")
            self.status_label.config(text="状态: 回放已停止", fg="green")
    
    def save_recording(self):
        """保存录制到文件"""
        if self.recorder.get_event_count() == 0:
            messagebox.showwarning("警告", "没有可保存的内容！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="mouse_recording.json"
        )
        
        if filename:
            try:
                self.recorder.save_to_file(filename)
                messagebox.showinfo("成功", f"录制已保存到: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def load_recording(self):
        """从文件加载录制"""
        if self.is_recording or self.is_playing:
            messagebox.showwarning("警告", "请先停止当前操作！")
            return
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.recorder.load_from_file(filename)
                self._update_info()
                messagebox.showinfo("成功", "录制已加载！")
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def clear_recording(self):
        """清空当前录制"""
        if self.is_recording or self.is_playing:
            messagebox.showwarning("警告", "请先停止当前操作！")
            return
        
        if self.recorder.get_event_count() > 0:
            result = messagebox.askyesno("确认", "确定要清空当前录制吗？")
            if result:
                self.recorder.events = []
                self._update_info()
                self.status_label.config(text="状态: 已清空", fg="green")
    
    def _update_info(self):
        """更新信息显示"""
        count = self.recorder.get_event_count()
        duration = self.recorder.get_duration()
        
        self.event_count_label.config(text=f"事件数量: {count}")
        self.duration_label.config(text=f"录制时长: {duration:.2f} 秒")
    
    def _update_status(self):
        """定期更新状态"""
        # 更新录制信息
        if self.is_recording:
            self._update_info()
        
        # 检查回放是否结束
        if self.is_playing and not self.player.is_playing_now():
            self.is_playing = False
            self.play_btn.config(text="▶️ 开始回放", bg="#4ECDC4")
            self.status_label.config(text="状态: 回放完成", fg="green")
        
        # 每100ms更新一次
        self.root.after(100, self._update_status)
    
    def on_closing(self):
        """关闭窗口时的处理"""
        if self.is_recording:
            self.recorder.stop_recording()
        if self.is_playing:
            self.player.stop()
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    app = MouseRecorderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
