from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import os
import time
import random
import math

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])

class WahidVRApp(App):
    def build(self):
        self.title = 'WahidVR Kamera'
        Window.clearcolor = (0.04, 0.04, 0.1, 1)
        self.current_effect = None
        self.time = 0
        self.capture_dir = os.path.join(os.path.expanduser('~'), 'WahidVR')
        os.makedirs(self.capture_dir, exist_ok=True)
        
        main = BoxLayout(orientation='vertical', padding=8, spacing=8)
        
        header = BoxLayout(size_hint_y=0.06)
        header.add_widget(Label(text='WAHIDVR KAMERA', font_size=18, bold=True, color=(0,0.83,1,1)))
        header.add_widget(Label(text='50+ Efek', font_size=11, color=(0.4,0.4,0.4,1)))
        main.add_widget(header)
        
        content = BoxLayout(orientation='horizontal', spacing=8)
        
        left = BoxLayout(orientation='vertical', size_hint_x=0.38)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=4)
        grid.bind(minimum_height=grid.setter('height'))
        
        effects = {
            'Transformasi AI': ['ai_mini_me','ai_giant','ghibli','pixar','anime','cyberpunk','superhero','robot','alien'],
            'Face AI': ['face_scan','avatar_anime','beauty_ai','emotion_happy','emotion_sad'],
            'Portal': ['vr_portal','galaxy_portal','portal_effect','magic_door','teleport_portal'],
            'VR Cinematic': ['cyberpunk_vr','matrix_world','hologram','neon_cyberpunk','digital_glitch'],
            'VR Visual': ['clone_effect','mirror_clone','gravity_flip','floating_object','particle_body'],
            'VR Camera': ['little_planet','fisheye_ultra','360_equirectangular','infinite_zoom','360_orbit'],
            'VR Fantasy': ['fire_aura','ice_world','ocean_vr','lightning_power','galaxy_eyes'],
            'Klasik': ['neon','glitch','vintage','thermal','sketch','cartoon','pixelate','heart_rain','sparkle'],
            'Weather': ['weather_rain','weather_fog','snow_world','fireworks','aurora_sky'],
            'Special': ['future_vision','time_machine','hologram_studio','magic_portal'],
        }
        
        for cat, keys in effects.items():
            grid.add_widget(Label(text=f'[color=0088cc][b]{cat}[/b][/color]', markup=True, size_hint_y=None, height=30, font_size=11))
            for key in keys:
                btn = Button(text=key.replace('_',' ').title(), size_hint_y=None, height=38,
                           background_color=(0.06,0.06,0.1,1), color=(0.8,0.8,0.8,1), font_size=10)
                btn.bind(on_press=lambda x, k=key: self.select_effect(k))
                grid.add_widget(btn)
        
        scroll.add_widget(grid)
        left.add_widget(scroll)
        content.add_widget(left)
        
        right = BoxLayout(orientation='vertical', size_hint_x=0.62)
        
        self.preview = Label(text='KAMERA\n\nTekan START', font_size=14, color=(0.2,0.2,0.2,1), size_hint_y=0.65)
        right.add_widget(self.preview)
        
        self.info = Label(text='Pilih efek dari panel kiri', font_size=11, color=(0,0.83,1,1), size_hint_y=0.08)
        right.add_widget(self.info)
        
        ctrl = BoxLayout(size_hint_y=0.15, spacing=8)
        self.start_btn = Button(text='START', background_color=(0.15,0.68,0.38,1), font_size=13, bold=True)
        self.start_btn.bind(on_press=self.toggle)
        ctrl.add_widget(self.start_btn)
        ctrl.add_widget(Button(text='FOTO', background_color=(0,0.83,1,1), font_size=13, bold=True, on_press=self.capture))
        ctrl.add_widget(Button(text='CLEAR', background_color=(0.91,0.3,0.24,1), font_size=13, bold=True, on_press=self.clear))
        right.add_widget(ctrl)
        
        right.add_widget(Button(text='GALERI', size_hint_y=0.1, background_color=(0.2,0.6,0.86,1), font_size=11, on_press=self.gallery))
        
        content.add_widget(right)
        main.add_widget(content)
        return main
    
    def select_effect(self, key):
        self.current_effect = key
        self.info.text = key.replace('_',' ').title()
    
    def clear(self, *a):
        self.current_effect = None
        self.info.text = 'Pilih efek dari panel kiri'
    
    def toggle(self, *a):
        if self.current_effect:
            self.info.text = f'Efek aktif: {self.current_effect.replace("_"," ").title()}'
        else:
            self.info.text = 'Pilih efek dulu!'
    
    def capture(self, *a):
        f = os.path.join(self.capture_dir, f"photo_{int(time.time())}.txt")
        with open(f, 'w') as file:
            file.write(f"Effect: {self.current_effect}\nTime: {time.ctime()}")
        Popup(title='Tersimpan!', content=Label(text=f'File tersimpan:\n{f}'), size_hint=(0.8,0.3)).open()
    
    def gallery(self, *a):
        content = BoxLayout(orientation='vertical', padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for i in range(10):
            grid.add_widget(Button(text=f'Foto {i+1}', size_hint_y=None, height=60, background_color=(0.1,0.1,0.2,1)))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        close = Button(text='Tutup', size_hint_y=0.12)
        content.add_widget(close)
        p = Popup(title='Galeri', content=content, size_hint=(0.95,0.9))
        close.bind(on_press=p.dismiss)
        p.open()

if __name__ == '__main__':
    WahidVRApp().run()
