#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 00:14:53 2023

@author: wally
"""
import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import subprocess

pygame.init()

# 遊戲視窗尺寸
WINDOW_WIDTH = 670
WINDOW_HEIGHT = 670

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("遊戲首頁")

def game_screen():
    background_image = pygame.image.load("homepage.jpg").convert()

    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background_image, (0, 0))

    button_image = pygame.image.load("button.png").convert_alpha()

    button_image = pygame.transform.scale(button_image, (400, 150))

    button_rect = button_image.get_rect()

    button_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80)
    screen.blit(button_image, button_rect)
    pygame.display.update()

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                button_rect = pygame.Rect((WINDOW_WIDTH // 2) - 100, WINDOW_HEIGHT - 105, 200, 50)
                if button_rect.collidepoint(event.pos):
                    running = False

        game_screen()

    # 進入另一個五子棋遊戲
    subprocess.call(["python", "project.py"])  # 假設 "project.py" 是五子棋遊戲的程式碼檔案名稱

    # 結束遊戲的程式碼
    pygame.quit()
    sys.exit()

game_loop()