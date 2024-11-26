import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5),
         pg.K_DOWN:(0, 5),
         pg.K_LEFT:(-5, 0),
         pg.K_RIGHT:(5, 0)
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct : pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中過疎とかを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値:真理値タプル(横, 縦)/画面内:True, 画面外:False
    """

    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> tuple[int, int]:
    """
    gameover画面を表示する関数
    引数: screen
    戻り値: なし
    """
    bl = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bl, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    bl.set_alpha(200)
    go_fonto = pg.font.Font(None, 120)
    txt = go_fonto.render("GameOver", True, (255, 255, 255))
    go_kokaton = pg.image.load("fig/8.png")
    go_kokaton_rct = go_kokaton.get_rect()
    go_kokaton_rct2 = go_kokaton.get_rect()
    go_kokaton_rct.topleft = WIDTH  / 2 - 270, HEIGHT / 2
    go_kokaton_rct2.topleft = WIDTH / 2 + 290, HEIGHT / 2
    bl_rct = bl.get_rect()
    bl_rct.topleft = 0, 0
    screen.blit(bl, bl_rct)
    screen.blit(txt, [WIDTH / 2 - 190, HEIGHT / 2])
    screen.blit(go_kokaton, go_kokaton_rct)
    screen.blit(go_kokaton, go_kokaton_rct2)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    キャラクター画像を移動方向に応じて回転させる。
    引数:
        sum_mv: (x方向の移動量, y方向の移動量) のタプル
    戻り値:
        回転したこうかとん画像 (pg.Surface)
    """
    base_img = pg.image.load("fig/3.png")  # 基本のこうかとん画像を読み込む
    base_img_flip = pg.transform.flip(base_img, True, True)
    if sum_mv[0] == -5:
        img = base_img
    else:
        img = base_img_flip
    base_img = pg.transform.rotozoom(img, 0, 0.9)  # サイズ変更
    
    # 移動方向に応じた回転角度を辞書で定義
    direction_to_angle = {
        (-5, 0): 0,  
        (0, -5): 90,    
        (5, 0): 0,  
        (0, 5): -90,
    }
    
    # 辞書で角度を取得（該当なしは0度）
    angle = direction_to_angle(sum_mv)
    return pg.transform.rotozoom(img, angle, 0.9)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen) 
            pg.display.update()
            time.sleep(5)
            return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct = bb_img.get_rect(center= bb_rct.center)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
