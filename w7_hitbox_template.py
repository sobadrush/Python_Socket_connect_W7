import pygame
import json
import socket
import sys

# === 初始化 ===
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Week 7 - 碰撞判定與血條爭奪戰")
clock = pygame.time.Clock()

my_x, my_y = 100, 300
enemy_x, enemy_y = 600, 300
my_hp = 10

bullets = [] # 儲存畫面上所有的子彈

# ==== 【TODO 1】網路 Socket 設定 ====
# 請在這裡建立 UDP Socket，綁定 5000 port 並設定為非阻塞 (Non-blocking)
# sock = ...
# sock.setblocking(False)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPv4, SOCK_DGRAM = UDP
sock.bind(('0.0.0.0', 5000)) # 綁定到本機的 5000 port
sock.setblocking(False)

TARGET_IP = "127.0.0.1" # 測試用

while True:
    screen.fill((30, 30, 50))

    # ==== 【TODO 2】接收對手網路封包 ====
    # try:
    #     data, addr = sock.recvfrom(1024)
    #     package = json.loads(data.decode())
    #     if package['type'] == 'pos':
    #          更新對方座標...
    #     elif package['type'] == 'shoot':
    #          把對方的子彈加進 bullets 陣列裡...
    #     elif package['type'] == 'hit':
    #          更新對方的血量數字...
    # except BlockingIOError: pass
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # 按下空白鍵發射子彈
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            new_bullet = {'x': my_x, 'y': my_y, 'dir': 10, 'owner': 'me'}
            bullets.append(new_bullet)
            
            # ==== 【TODO 3】通知對方我開槍了 ====
            # shoot_package = {'type': 'shoot', 'x': my_x, 'y': my_y}
            # 將這個 package 用 dumps 打包並送出

    # 控制移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: my_y -= 5
    if keys[pygame.K_s]: my_y += 5

    # 繪製自己與對手 (使用 Rect 作為碰撞箱)
    my_rect = pygame.Rect(my_x, my_y, 40, 40)
    pygame.draw.rect(screen, (59, 130, 246), my_rect)
    
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 40, 40)
    pygame.draw.rect(screen, (16, 185, 129), enemy_rect)

    # 處理並繪製每一顆子彈
    for b in bullets[:]:
        # 使子彈移動
        b['x'] += b['dir']
        
        # 繪製子彈
        bullet_color = (255, 200, 0) if b['owner'] == 'me' else (255, 50, 50)
        bullet_rect = pygame.Rect(b['x'], b['y'], 10, 10)
        pygame.draw.rect(screen, bullet_color, bullet_rect)

        # ==== 【TODO 4: P2P 碰撞判定】 ====
        # 若這是一顆「對方」射過來的子彈，且「打中我了」
        # if b['owner'] == 'enemy' and my_rect.colliderect(bullet_rect):
        #      1. my_hp -= 1
        #      2. bullets.remove(b)
        #      3. 傳送 {'type': 'hit', 'hp': my_hp} 告訴對方我受傷了
        
        # 飛出邊界則刪除
        if b['x'] < 0 or b['x'] > 800:
            if b in bullets:
                bullets.remove(b)

    pygame.display.flip()
    clock.tick(60)

    # ==== 【TODO 5】傳送座標 ====
    # 每回合結束，把自己的新座標透過封包 {'type': 'pos', 'x': xxx, 'y': xxx} 送過去
