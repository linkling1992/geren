"""
音效管理系统
"""
import pygame
import os


class SoundManager:
    """音效管理器"""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None
        self.sound_enabled = True
        self.music_enabled = True
        self.sound_volume = 0.7
        self.music_volume = 0.5
        
        # 加载所有音效
        self._load_sounds()
    
    def _load_sounds(self):
        """加载所有音效文件"""
        # 定义音效列表
        sound_files = {
            'weapon_pistol': 'assets/sounds/weapon_pistol.wav',
            'weapon_shotgun': 'assets/sounds/weapon_shotgun.wav',
            'weapon_rifle': 'assets/sounds/weapon_rifle.wav',
            'weapon_laser': 'assets/sounds/weapon_laser.wav',
            'skill_explosion': 'assets/sounds/skill_explosion.wav',
            'skill_shield': 'assets/sounds/skill_shield.wav',
            'skill_frost': 'assets/sounds/skill_frost.wav',
            'skill_teleport': 'assets/sounds/skill_teleport.wav',
            'enemy_hit': 'assets/sounds/enemy_hit.wav',
            'player_hit': 'assets/sounds/player_hit.wav',
            'level_up': 'assets/sounds/level_up.wav',
            'enemy_death': 'assets/sounds/enemy_death.wav',
            'ui_click': 'assets/sounds/ui_click.wav',
            'ui_hover': 'assets/sounds/ui_hover.wav',
        }
        
        # 尝试加载音效（文件不存在时使用占位符）
        for key, filepath in sound_files.items():
            try:
                if os.path.exists(filepath):
                    self.sounds[key] = pygame.mixer.Sound(filepath)
                    self.sounds[key].set_volume(self.sound_volume)
                else:
                    self.sounds[key] = None
            except Exception as e:
                print(f"Failed to load sound {key}: {e}")
                self.sounds[key] = None
    
    def load_background_music(self, filepath):
        """加载背景音乐"""
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume)
                self.music = filepath
            else:
                print(f"Music file not found: {filepath}")
        except Exception as e:
            print(f"Failed to load music: {e}")
    
    def play_sound(self, sound_key):
        """播放音效"""
        if not self.sound_enabled or sound_key not in self.sounds:
            return
        
        sound = self.sounds[sound_key]
        if sound is not None:
            try:
                sound.play()
            except Exception as e:
                print(f"Failed to play sound {sound_key}: {e}")
    
    def play_music(self, loops=-1):
        """播放背景音乐"""
        if not self.music_enabled or self.music is None:
            return
        
        try:
            pygame.mixer.music.play(loops)
        except Exception as e:
            print(f"Failed to play music: {e}")
    
    def stop_music(self):
        """停止背景音乐"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Failed to stop music: {e}")
    
    def set_sound_volume(self, volume):
        """设置音效音量（0-1）"""
        self.sound_volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """设置音乐音量（0-1）"""
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
    
    def toggle_music(self):
        """切换音乐开关"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
    
    def is_sound_enabled(self):
        """检查音效是否启用"""
        return self.sound_enabled
    
    def is_music_enabled(self):
        """检查音乐是否启用"""
        return self.music_enabled


# 全局音效管理器实例
_sound_manager = None


def get_sound_manager():
    """获取全局音效管理器"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
