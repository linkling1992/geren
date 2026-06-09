"""
2D肉鸽类游戏 - 主入口
"""
import pygame
import sys
from game.game_manager import GameManager


def main():
    pygame.init()
    
    # 游戏配置
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # 创建游戏管理器
    game = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    
    # 游戏循环
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # 更新逻辑
        game.update()
        
        # 渲染
        game.render()
        
        # 控制帧率
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
