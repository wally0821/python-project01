import sys
import pygame
from pygame.locals import QUIT, KEYDOWN
import numpy as np
pygame.init()


pygame.display.set_caption("五子棋")
screen = pygame.display.set_mode((670, 700))

screen_color = [205, 133, 65]  #背景色
line_color = [0, 0, 0]  #線的顏色
white_color = [255, 255, 255]  # 白棋
black_color = [0, 0, 0]  # 黑棋

# 滑鼠位置對應棋盤座標
def find_pos(x, y):
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            L1 = i - 22
            L2 = i + 22
            R1 = j - 22
            R2 = j + 22
            if L1 <= x <= L2 and R1 <= y <= R2:
                return i, j
    return x, y

# 檢查有沒有重複下棋
def check_over_pos(x, y, over_pos):
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    return True

# 檢查連成五顆星了沒
def check_win(over_pos):
    mp = np.zeros([15, 15], dtype=int)

    # 畫棋盤
    for i in range(27, 670, 44):
        if i == 27 or i == 670 - 27:
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 8)
        else:
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 2)

        if i == 27 or i == 670 - 27:
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 8)
        else:
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 2)

        center_x = 27 + (670 - 2 * 27) // 2
        center_y = 27 + (670 - 2 * 27) // 2
        pygame.draw.circle(screen, line_color, [center_x, center_y], 8, 0)

    star_points = [(3, 3), (3, 11), (11, 3), (11, 11)]
    for point in star_points:
        x = 27 + point[0] * 44
        y = 27 + point[1] * 44
        pygame.draw.circle(screen, line_color, (x, y), 6)

    # 取得滑鼠位置
    x, y = pygame.mouse.get_pos()
    x, y = find_pos(x, y)

    # 下棋
    for val in over_pos:
        x_pos, y_pos = val[0]
        if x == x_pos and y == y_pos:
            continue
        pygame.draw.circle(screen, val[1], val[0], 20, 0)

    for val in over_pos:
        x, y = (val[0][0] - 27) // 44, (val[0][1] - 27) // 44
        mp[x][y] = 2 if val[1] == white_color else 1

    # 連線方向
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    # 檢查連線了沒
    for i in range(15):
        for j in range(15):
            if mp[i][j] == 0:
                continue

            for dx, dy in directions:
                count = 1
                nx, ny = i + dx, j + dy

                while 0 <= nx < 15 and 0 <= ny < 15 and mp[nx][ny] == mp[i][j]:
                    count += 1
                    nx += dx
                    ny += dy

                    if count == 5:
                        # 返回連線的顏色和座標
                        return [mp[i][j], [[i, j]] + [[i + k * dx, j + k * dy]
                                                      for k in range(1, 5)]]

    return [0, []]

flag = False
time = 0
over_pos = []

# 遊戲主迴圈
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                over_pos = []
                flag = False
                time = 0

    # 填充背景色
    screen.fill(screen_color)

    # 取得滑鼠座標
    x, y = pygame.mouse.get_pos()
    x, y = find_pos(x, y)

    # 在滑鼠位置繪製方框
    if check_over_pos(x, y, over_pos):
        pygame.draw.rect(screen, [0, 0, 238], [x - 22, y - 22, 40, 40], 2, 1)
    else:
        pygame.draw.rect(screen, [0, 238, 0], [x - 22, y - 22, 40, 40], 2, 1)

    # 按下滑鼠左鍵放下旗子
    keys_pressed = pygame.mouse.get_pressed()
    if keys_pressed[0] and time == 0:
        flag = True
        if check_over_pos(x, y, over_pos):
            if len(over_pos) % 2 == 0:
                over_pos.append([[x, y], black_color])
            else:
                over_pos.append([[x, y], white_color])

    # 檢查是否有五子連線
    res = check_win(over_pos)
    if res[0] != 0:
        if res[0] == 1:
            text = "BLACK WIN"
            text_color = [0, 255, 0]
        elif res[0] == 2:
            text = "WHITE WIN"
            text_color = [0, 255, 0]
        else:
            text = "Draw"
            text_color = [230, 0, 92]

        # 顯示遊戲結果
        font = pygame.font.Font(None, 100)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 
                                                  screen.get_height() // 2))
        screen.blit(text_surface, text_rect)

    # 顯示重新開始提示
    font = pygame.font.Font(None, 36)
    text = font.render("press ESC to restart", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
    screen.blit(text, text_rect)

    # 更新顯示
    pygame.display.update()