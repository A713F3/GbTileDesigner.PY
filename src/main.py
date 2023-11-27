import pygame
from sys import platform
import subprocess

def clip_win(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def clip_mac(txt):
    cmd='echo '+txt.strip()+'|pbcopy'
    return subprocess.check_call(cmd, shell=True)

copy_to_clip = clip_win
if platform == "darwin":
    copy_to_clip = clip_mac


def cells_to_2bpp(cells):
    bpp = ""

    for row in cells:
        left, right = "", ""

        for col in row:
            h, l = '{0:02b}'.format(col)

            left += l
            right += h

        bpp += '{0:02x}'.format(int(left, 2)) + " "
        bpp += '{0:02x}'.format(int(right, 2)) + " "

    return bpp


pygame.init()

screen = pygame.display.set_mode([400, 500])
pygame.display.set_caption("2BPP Designer")

palette = {0:(23, 62, 12), 1:(65, 113, 45), 2:(151, 190, 60), 3:(170, 206, 66)}

cell_space = 1
cell_size = 40
palette_size = 50
palette_space = 10

cell_offset = (screen.get_width() - (cell_size * 8)) // 2

palette_offset_y = (screen.get_height() - (cell_size*8 + cell_offset)) // 2
palette_offset_x = len(palette) * palette_size + (len(palette)-1) * palette_space

palette_x = (screen.get_width() - palette_offset_x) // 2
palette_y = (cell_size*8 + cell_offset) + palette_offset_y - palette_size // 2

cells = [[0 for j in range(8)] for i in range(8)]

cell_rects = []
for yi in range(8):
    row = []
    for xi in range(8):
        cell = cells[yi][xi]

        x = cell_offset + xi*cell_size+cell_space
        y = cell_offset + yi*cell_size+cell_space

        row.append(pygame.Rect(x, y, cell_size-cell_space*2, cell_size-cell_space*2)) 

    cell_rects.append(row)

palette_rects = []
for c in palette:
    r = pygame.Rect(palette_x + c * (palette_size + palette_space), palette_y, palette_size, palette_size)
    palette_rects.append(r)

selected_color = 0
selected_rect = palette_rects[0].copy()

selected_rect.inflate_ip(4, 4)

copy_clip_rect = pygame.Rect(screen.get_width() // 2 - 20, screen.get_height() - 30, 40, 20)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            for i in range(len(palette_rects)):
                if palette_rects[i].collidepoint(pos):
                    selected_color = i
                    selected_rect = palette_rects[i].copy()

                    selected_rect.inflate_ip(4, 4)

            for yi in range(8):
                for xi in range(8): 
                    if cell_rects[yi][xi].collidepoint(pos):
                        cells[yi][xi] = selected_color

            if copy_clip_rect.collidepoint(pos):
                b = cells_to_2bpp(cells)
                print("2BPP: ", b)
                copy_to_clip(b)

    screen.fill((51, 51, 51))

    pygame.draw.rect(screen, (200, 200, 200), selected_rect)

    pygame.draw.rect(screen, (200, 200, 200), copy_clip_rect)

    for yi in range(8):
        for xi in range(8):
            cell_color = palette[cells[yi][xi]]
            pygame.draw.rect(screen, cell_color, cell_rects[yi][xi])


    for c in palette:
        palette_color = palette[c]
        pygame.draw.rect(screen, palette_color, palette_rects[c])

    
    pygame.display.flip()

pygame.quit()