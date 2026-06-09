"""
游戏菜单系统
"""
import pygame
import sys


class Button:
    """按钮类"""
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
    
    def update(self, mouse_pos):
        """更新按钮状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
    
    def is_clicked(self, event):
        """检查是否被点击"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                return True
        return False
    
    def render(self, screen):
        """渲染按钮"""
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # 渲染文字
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Menu:
    """菜单基类"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
    
    def handle_event(self, event):
        """处理事件"""
        pass
    
    def update(self, mouse_pos):
        """更新菜单"""
        for button in self.buttons:
            button.update(mouse_pos)
    
    def render(self, screen):
        """渲染菜单"""
        pass


class MainMenu(Menu):
    """主菜单"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # 创建按钮
        button_width = 200
        button_height = 50
        center_x = screen_width // 2 - button_width // 2
        
        self.start_button = Button(center_x, 300, button_width, button_height, "开始游戏")
        self.settings_button = Button(center_x, 400, button_width, button_height, "设置")
        self.quit_button = Button(center_x, 500, button_width, button_height, "退出游戏")
        
        self.buttons = [self.start_button, self.settings_button, self.quit_button]
    
    def handle_event(self, event):
        """处理事件"""
        if self.start_button.is_clicked(event):
            return "start"
        elif self.settings_button.is_clicked(event):
            return "settings"
        elif self.quit_button.is_clicked(event):
            return "quit"
        return None
    
    def render(self, screen):
        """渲染主菜单"""
        screen.fill((20, 20, 20))
        
        # 标题
        font = pygame.font.Font(None, 72)
        title = font.render("2D 肉鸽游戏", True, (255, 100, 0))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        # 副标题
        font_small = pygame.font.Font(None, 36)
        subtitle = font_small.render("Roguelike Adventure", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 180))
        screen.blit(subtitle, subtitle_rect)
        
        # 按钮
        for button in self.buttons:
            button.render(screen)


class PauseMenu(Menu):
    """暂停菜单"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # 创建按钮
        button_width = 200
        button_height = 50
        center_x = screen_width // 2 - button_width // 2
        
        self.resume_button = Button(center_x, 300, button_width, button_height, "继续游戏")
        self.settings_button = Button(center_x, 400, button_width, button_height, "设置")
        self.quit_button = Button(center_x, 500, button_width, button_height, "返回菜单")
        
        self.buttons = [self.resume_button, self.settings_button, self.quit_button]
    
    def handle_event(self, event):
        """处理事件"""
        if self.resume_button.is_clicked(event):
            return "resume"
        elif self.settings_button.is_clicked(event):
            return "settings"
        elif self.quit_button.is_clicked(event):
            return "main_menu"
        return None
    
    def render(self, screen):
        """渲染暂停菜单"""
        # 绘制半透明覆盖层
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 标题
        font = pygame.font.Font(None, 72)
        title = font.render("暂停", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        # 按钮
        for button in self.buttons:
            button.render(screen)


class SettingsMenu(Menu):
    """设置菜单"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # 创建按钮
        button_width = 200
        button_height = 50
        center_x = screen_width // 2 - button_width // 2
        
        self.back_button = Button(center_x, 500, button_width, button_height, "返回")
        self.buttons = [self.back_button]
        
        # 设置选项
        self.sound_enabled = True
        self.music_enabled = True
        self.sound_volume = 70
        self.music_volume = 50
    
    def handle_event(self, event):
        """处理事件"""
        if self.back_button.is_clicked(event):
            return "back"
        
        # 处理按键
        if event.type == pygame.KEYDOWN:
            # 音量控制
            if event.key == pygame.K_UP:
                self.sound_volume = min(100, self.sound_volume + 5)
            elif event.key == pygame.K_DOWN:
                self.sound_volume = max(0, self.sound_volume - 5)
            elif event.key == pygame.K_LEFT:
                self.music_volume = max(0, self.music_volume - 5)
            elif event.key == pygame.K_RIGHT:
                self.music_volume = min(100, self.music_volume + 5)
            elif event.key == pygame.K_s:
                self.sound_enabled = not self.sound_enabled
            elif event.key == pygame.K_m:
                self.music_enabled = not self.music_enabled
        
        return None
    
    def render(self, screen):
        """渲染设置菜单"""
        screen.fill((20, 20, 20))
        
        # 标题
        font = pygame.font.Font(None, 72)
        title = font.render("设置", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title, title_rect)
        
        # 设置选项
        font_small = pygame.font.Font(None, 36)
        
        # 音效
        y_offset = 150
        sound_text = "音效: " + ("开启" if self.sound_enabled else "关闭")
        sound_surface = font_small.render(sound_text, True, (200, 200, 200))
        screen.blit(sound_surface, (100, y_offset))
        
        # 音效音量条
        volume_bar_width = 300
        volume_bar_height = 20
        pygame.draw.rect(screen, (100, 100, 100), (100, y_offset + 50, volume_bar_width, volume_bar_height))
        pygame.draw.rect(screen, (100, 200, 100), (100, y_offset + 50, volume_bar_width * self.sound_volume // 100, volume_bar_height))
        volume_text = font_small.render(f"{self.sound_volume}%", True, (200, 200, 200))
        screen.blit(volume_text, (420, y_offset + 50))
        
        # 音乐
        y_offset = 250
        music_text = "音乐: " + ("开启" if self.music_enabled else "关闭")
        music_surface = font_small.render(music_text, True, (200, 200, 200))
        screen.blit(music_surface, (100, y_offset))
        
        # 音乐音量条
        pygame.draw.rect(screen, (100, 100, 100), (100, y_offset + 50, volume_bar_width, volume_bar_height))
        pygame.draw.rect(screen, (100, 150, 200), (100, y_offset + 50, volume_bar_width * self.music_volume // 100, volume_bar_height))
        volume_text = font_small.render(f"{self.music_volume}%", True, (200, 200, 200))
        screen.blit(volume_text, (420, y_offset + 50))
        
        # 操作说明
        y_offset = 400
        help_font = pygame.font.Font(None, 24)
        help_texts = [
            "↑/↓ - 调整音效音量",
            "←/→ - 调整音乐音量",
            "S - 切换音效开关",
            "M - 切换音乐开关"
        ]
        for i, text in enumerate(help_texts):
            help_surface = help_font.render(text, True, (150, 150, 150))
            screen.blit(help_surface, (100, y_offset + i * 30))
        
        # 返回按钮
        self.back_button.render(screen)


class GameOverMenu(Menu):
    """游戏结束菜单"""
    def __init__(self, screen_width, screen_height, score=0, level=1):
        super().__init__(screen_width, screen_height)
        self.score = score
        self.level = level
        
        # 创建按钮
        button_width = 200
        button_height = 50
        center_x = screen_width // 2 - button_width // 2
        
        self.restart_button = Button(center_x, 400, button_width, button_height, "重新开始")
        self.menu_button = Button(center_x, 500, button_width, button_height, "返回菜单")
        
        self.buttons = [self.restart_button, self.menu_button]
    
    def handle_event(self, event):
        """处理事件"""
        if self.restart_button.is_clicked(event):
            return "restart"
        elif self.menu_button.is_clicked(event):
            return "main_menu"
        return None
    
    def render(self, screen):
        """渲染游戏结束菜单"""
        screen.fill((20, 20, 20))
        
        # 标题
        font = pygame.font.Font(None, 72)
        title = font.render("游戏结束", True, (255, 100, 0))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        # 统计信息
        font_small = pygame.font.Font(None, 48)
        score_text = font_small.render(f"最终等级: {self.level}", True, (200, 200, 200))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(score_text, score_rect)
        
        enemy_text = font_small.render(f"击杀敌人: {self.score}", True, (200, 200, 200))
        enemy_rect = enemy_text.get_rect(center=(self.screen_width // 2, 280))
        screen.blit(enemy_text, enemy_rect)
        
        # 按钮
        for button in self.buttons:
            button.render(screen)


class MenuManager:
    """菜单管理器"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_menu = MainMenu(screen_width, screen_height)
        self.menu_stack = []
    
    def push_menu(self, menu):
        """压入菜单"""
        self.menu_stack.append(self.current_menu)
        self.current_menu = menu
    
    def pop_menu(self):
        """弹出菜单"""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
    
    def handle_event(self, event):
        """处理事件"""
        result = self.current_menu.handle_event(event)
        
        if result == "start":
            return "start_game"
        elif result == "settings":
            self.push_menu(SettingsMenu(self.screen_width, self.screen_height))
            return "in_menu"
        elif result == "quit":
            return "quit"
        elif result == "resume":
            return "resume_game"
        elif result == "main_menu":
            return "main_menu"
        elif result == "back":
            self.pop_menu()
            return "in_menu"
        elif result == "restart":
            return "restart_game"
        
        return "in_menu"
    
    def update(self):
        """更新菜单"""
        mouse_pos = pygame.mouse.get_pos()
        self.current_menu.update(mouse_pos)
    
    def render(self, screen):
        """渲染菜单"""
        self.current_menu.render(screen)
