from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import platform
import cv2
import numpy as np
import os
import time
import math
from effects import Effects

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

class WahidVRKamera(App):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.is_running = False
        self.current_effect = None
        self.effects = Effects()
        self.time = 0
        self.capture_dir = os.path.join(os.path.expanduser('~'), 'WahidVR')
        os.makedirs(self.capture_dir, exist_ok=True)
    
    def build(self):
        self.title = 'WahidVR Kamera'
        Window.clearcolor = (0.04, 0.04, 0.1, 1)
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=0.08)
        header.add_widget(Label(
            text='WAHIDVR KAMERA',
            font_size=20,
            bold=True,
            color=(0, 0.83, 1, 1),
            size_hint_x=0.6
        ))
        header.add_widget(Label(
            text=f'{len(self.get_effect_data())} Efek',
            font_size=12,
            color=(0.4, 0.4, 0.4, 1),
            size_hint_x=0.4
        ))
        main_layout.add_widget(header)
        
        content = BoxLayout(orientation='horizontal', spacing=10)
        
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.35)
        
        effect_scroll = ScrollView()
        self.effect_grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.effect_grid.bind(minimum_height=self.effect_grid.setter('height'))
        
        categories = {}
        for key, data in self.get_effect_data().items():
            cat = data['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((key, data))
        
        for cat, effects in categories.items():
            cat_label = Label(
                text=f'[color=0088cc][b]{cat}[/b][/color]',
                markup=True,
                size_hint_y=None,
                height=35,
                font_size=12
            )
            self.effect_grid.add_widget(cat_label)
            
            for key, data in effects:
                btn = Button(
                    text=data['name'],
                    size_hint_y=None,
                    height=40,
                    background_color=(0.06, 0.06, 0.1, 1),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size=11
                )
                btn.bind(on_press=lambda x, k=key: self.select_effect(k))
                self.effect_grid.add_widget(btn)
        
        effect_scroll.add_widget(self.effect_grid)
        left_panel.add_widget(effect_scroll)
        
        content.add_widget(left_panel)
        
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.65)
        
        self.camera_display = Label(
            text='KAMERA\n\nTekan START',
            font_size=16,
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.7
        )
        right_panel.add_widget(self.camera_display)
        
        self.effect_info = Label(
            text='Pilih efek dari panel kiri',
            font_size=12,
            color=(0, 0.83, 1, 1),
            size_hint_y=0.05
        )
        right_panel.add_widget(self.effect_info)
        
        control = BoxLayout(size_hint_y=0.15, spacing=10)
        
        self.start_btn = Button(
            text='START',
            background_color=(0.15, 0.68, 0.38, 1),
            font_size=14,
            bold=True
        )
        self.start_btn.bind(on_press=self.toggle_camera)
        control.add_widget(self.start_btn)
        
        capture_btn = Button(
            text='FOTO',
            background_color=(0, 0.83, 1, 1),
            font_size=14,
            bold=True
        )
        capture_btn.bind(on_press=self.capture_photo)
        control.add_widget(capture_btn)
        
        clear_btn = Button(
            text='CLEAR',
            background_color=(0.91, 0.3, 0.24, 1),
            font_size=14,
            bold=True
        )
        clear_btn.bind(on_press=self.clear_effect)
        control.add_widget(clear_btn)
        
        right_panel.add_widget(control)
        
        gallery_btn = Button(
            text='GALERI',
            size_hint_y=0.1,
            background_color=(0.2, 0.6, 0.86, 1),
            font_size=12
        )
        gallery_btn.bind(on_press=self.show_gallery)
        right_panel.add_widget(gallery_btn)
        
        content.add_widget(right_panel)
        main_layout.add_widget(content)
        
        return main_layout
    
    def get_effect_data(self):
        return {
            'ai_mini_me': {'name': 'AI Mini Me', 'category': 'Transformasi AI'},
            'ai_giant': {'name': 'AI Giant', 'category': 'Transformasi AI'},
            'ghibli': {'name': 'Ghibli', 'category': 'Transformasi AI'},
            'pixar': {'name': 'Pixar', 'category': 'Transformasi AI'},
            'anime': {'name': 'Anime', 'category': 'Transformasi AI'},
            'cyberpunk': {'name': 'Cyberpunk', 'category': 'Transformasi AI'},
            'superhero': {'name': 'Superhero', 'category': 'Transformasi AI'},
            'robot': {'name': 'Robot', 'category': 'Transformasi AI'},
            'alien': {'name': 'Alien', 'category': 'Transformasi AI'},
            'face_scan': {'name': 'Face Scan', 'category': 'Face AI'},
            'avatar_anime': {'name': 'Avatar Anime', 'category': 'Face AI'},
            'avatar_cartoon': {'name': 'Avatar Cartoon', 'category': 'Face AI'},
            'beauty_ai': {'name': 'Beauty AI', 'category': 'Face AI'},
            'vr_portal': {'name': 'VR Portal', 'category': 'Portal'},
            'galaxy_portal': {'name': 'Galaxy Portal', 'category': 'Portal'},
            'portal_effect': {'name': 'Portal Effect', 'category': 'Portal'},
            'magic_door': {'name': 'Magic Door', 'category': 'Portal'},
            'teleport_portal': {'name': 'Teleport', 'category': 'Portal'},
            'neon': {'name': 'Neon', 'category': 'Klasik'},
            'glitch': {'name': 'Glitch', 'category': 'Klasik'},
            'vintage': {'name': 'Vintage', 'category': 'Klasik'},
            'thermal': {'name': 'Thermal', 'category': 'Klasik'},
            'sketch': {'name': 'Sketch', 'category': 'Klasik'},
            'cartoon': {'name': 'Cartoon', 'category': 'Klasik'},
            'pixelate': {'name': 'Pixelate', 'category': 'Klasik'},
            'heart_rain': {'name': 'Heart Rain', 'category': 'Klasik'},
            'star_rain': {'name': 'Star Rain', 'category': 'Klasik'},
            'sparkle': {'name': 'Sparkle', 'category': 'Klasik'},
            'cyberpunk_vr': {'name': 'Cyberpunk VR', 'category': 'VR Cinematic'},
            'matrix_world': {'name': 'Matrix World', 'category': 'VR Cinematic'},
            'hologram': {'name': 'Hologram', 'category': 'VR Cinematic'},
            'robot_vision': {'name': 'Robot Vision', 'category': 'VR Vision'},
            'night_vision': {'name': 'Night Vision', 'category': 'VR Vision'},
            'thermal_vision': {'name': 'Thermal Vision', 'category': 'VR Vision'},
            'clone_effect': {'name': 'Clone', 'category': 'VR Visual'},
            'mirror_clone': {'name': 'Mirror Clone', 'category': 'VR Visual'},
            'gravity_flip': {'name': 'Gravity Flip', 'category': 'VR Visual'},
            'little_planet': {'name': 'Little Planet', 'category': 'VR Camera'},
            'fisheye': {'name': 'Fisheye', 'category': 'VR Camera'},
            'infinite_zoom': {'name': 'Infinite Zoom', 'category': 'VR Camera'},
            '360_orbit': {'name': '360° Orbit', 'category': 'VR Camera'},
            'portal_teleport': {'name': 'Portal Teleport', 'category': 'VR Teleport'},
            'fire_aura': {'name': 'Fire Aura', 'category': 'VR Fantasy'},
            'ice_world': {'name': 'Ice World', 'category': 'VR Fantasy'},
            'ocean_vr': {'name': 'Ocean VR', 'category': 'VR Fantasy'},
            'magic_sparkle': {'name': 'Magic Sparkle', 'category': 'TikTok'},
            'galaxy_eyes': {'name': 'Galaxy Eyes', 'category': 'TikTok'},
            'royal_filter': {'name': 'Royal Filter', 'category': 'TikTok'},
            'weather_rain': {'name': 'Weather Rain', 'category': 'Weather'},
            'weather_fog': {'name': 'Weather Fog', 'category': 'Weather'},
            'future_vision': {'name': 'Future Vision', 'category': 'Special'},
            'time_machine': {'name': 'Time Machine', 'category': 'Special'},
            'hologram_studio': {'name': 'Hologram Studio', 'category': 'Special'},
        }
    
    def select_effect(self, effect_key):
        self.current_effect = effect_key
        data = self.get_effect_data().get(effect_key, {})
        self.effect_info.text = f'{data.get("name", effect_key)}'
    
    def clear_effect(self, *args):
        self.current_effect = None
        self.effect_info.text = 'Pilih efek dari panel kiri'
    
    def toggle_camera(self, *args):
        if self.is_running:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.effect_info.text = 'Error: Kamera tidak ditemukan!'
            return
        
        self.is_running = True
        self.start_btn.text = 'STOP'
        self.start_btn.background_color = (0.91, 0.3, 0.24, 1)
        
        Clock.schedule_interval(self.update_frame, 1.0/30.0)
    
    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_btn.text = 'START'
        self.start_btn.background_color = (0.15, 0.68, 0.38, 1)
        self.camera_display.text = 'KAMERA\n\nTekan START'
    
    def update_frame(self, dt):
        if not self.is_running or not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return
        
        frame = cv2.flip(frame, 1)
        self.effects.update()
        self.time += 1
        
        if self.current_effect:
            method = getattr(self.effects, f'apply_{self.current_effect}', None)
            if method:
                frame = method(frame)
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        h, w = frame_rgb.shape[:2]
        display_h = int(h * 0.6)
        display_w = int(w * 0.6)
        frame_small = cv2.resize(frame_rgb, (display_w, display_h))
        
        from PIL import Image as PILImage
        pil_img = PILImage.fromarray(frame_small)
        pil_img.save(os.path.join(self.capture_dir, 'temp_preview.jpg'), quality=50)
        
        self.camera_display.text = ''
    
    def capture_photo(self, *args):
        if not self.is_running or not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        
        if self.current_effect:
            method = getattr(self.effects, f'apply_{self.current_effect}', None)
            if method:
                frame = method(frame)
        
        filename = os.path.join(self.capture_dir, f"photo_{int(time.time())}.jpg")
        cv2.imwrite(filename, frame)
        
        popup = Popup(
            title='Tersimpan!',
            content=Label(text=f'Foto tersimpan:\n{filename}'),
            size_hint=(0.8, 0.3)
        )
        popup.open()
    
    def show_gallery(self, *args):
        files = [f for f in os.listdir(self.capture_dir) if f.endswith(('.jpg', '.png', '.mp4'))]
        
        content = BoxLayout(orientation='vertical', padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for f in sorted(files, reverse=True)[:20]:
            btn = Button(
                text=f[:15],
                size_hint_y=None,
                height=80,
                background_color=(0.1, 0.1, 0.2, 1)
            )
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        content.add_widget(scroll)
        
        close_btn = Button(text='Tutup', size_hint_y=0.15)
        content.add_widget(close_btn)
        
        popup = Popup(title='Galeri', content=content, size_hint=(0.95, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        pass

if __name__ == '__main__':
    WahidVRKamera().run()
