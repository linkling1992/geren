"""
游戏管理器 - 控制游戏的核心逻辑
"""
import pygame
from game.player import Player
from game.weapon_manager import WeaponManager
from game.skill_manager import SkillManager
from game.enemy_manager import EnemyManager
from game.camera import Camera


class GameManager:
    def __init__(self, screen_width, screen_height, fps):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("2D肉鸽游戏")
        
        # 初始化游戏系统
        self.player = Player(screen_width // 2, screen_height // 2)
        self.weapon_manager = WeaponManager(self.player)
        self.skill_manager = SkillManager(self.player)
        self.enemy_manager = EnemyManager()
        self.camera = Camera(screen_width, screen_height)
        
        # 游戏状态
        self.running = True
        self.paused = False
        self.wave = 1
        self.time_elapsed = 0
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                # 武器切换
                weapon_index = event.key - pygame.K_1
                self.weapon_manager.switch_weapon(weapon_index)
            elif event.key in [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r]:
                # 技能释放
                skill_index = ord(event.unicode) - ord('q')
                self.skill_manager.cast_skill(skill_index)
    
    def update(self):
        """更新游戏逻辑"""
        if self.paused:
            return
        
        self.time_elapsed += 1 / self.fps
        
        # 更新玩家
        self.player.update()
        
        # 更新武器
        self.weapon_manager.update()
        
        # 更新技能
        self.skill_manager.update()
        
        # 更新敌人
        self.enemy_manager.update()
        
        # 更新摄像机
        self.camera.update(self.player.x, self.player.y)
        
        # 检查碰撞
        self._check_collisions()
        
        # 生成敌人
        if self.time_elapsed % 3 == 0:  # 每3秒生成一波
            self.enemy_manager.spawn_enemy(self.player.x, self.player.y)
    
    def _check_collisions(self):
        """检查碰撞"""
        # 检查玩家与敌人的碰撞
        for enemy in self.enemy_manager.enemies:
            if self.player.check_collision(enemy):
                self.player.take_damage(enemy.damage)
        
        # 检查武器与敌人的碰撞
        bullets = self.weapon_manager.get_active_bullets()
        for bullet in bullets:
            for enemy in self.enemy_manager.enemies:
                if bullet.check_collision(enemy):
                    enemy.take_damage(bullet.damage)
                    bullet.hit()
    
    def render(self):
        """渲染游戏"""
        self.screen.fill((20, 20, 20))
        
        # 获取摄像机偏移
        cam_x, cam_y = self.camera.get_offset()
        
        # 渲染敌人
        for enemy in self.enemy_manager.enemies:
            enemy.render(self.screen, cam_x, cam_y)
        
        # 渲染子弹
        bullets = self.weapon_manager.get_active_bullets()
        for bullet in bullets:
            bullet.render(self.screen, cam_x, cam_y)
        
        # 渲染技能效果
        self.skill_manager.render(self.screen, cam_x, cam_y)
        
        # 渲染玩家
        self.player.render(self.screen, cam_x, cam_y)
        
        # 渲染UI
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_ui(self):
        """渲染UI界面"""
        font = pygame.font.Font(None, 36)
        
        # 生命值
        hp_text = font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, (255, 0, 0))
        self.screen.blit(hp_text, (10, 10))
        
        # 当前武器
        weapon_name = self.weapon_manager.get_current_weapon_name()
        weapon_text = font.render(f"Weapon: {weapon_name}", True, (255, 255, 0))
        self.screen.blit(weapon_text, (10, 50))
        
        # 等级
        level_text = font.render(f"Level: {self.player.level}", True, (0, 255, 0))
        self.screen.blit(level_text, (10, 90))
        
        # 波数
        wave_text = font.render(f"Wave: {self.wave}", True, (255, 165, 0))
        self.screen.blit(wave_text, (self.screen_width - 300, 10))
