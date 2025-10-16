import pygame
import numpy as np
import math
import random
from datetime import datetime

WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)

class SymmetryEngine:
    """Generate kaleidoscopic patterns with various symmetry modes"""
    
    def __init__(self, width, height, symmetry_order=6):
        self.width = width
        self.height = height
        self.symmetry_order = symmetry_order
        self.canvas = pygame.Surface((width, height))
        self.canvas.fill((10, 10, 10))
        self.gesture_history = []
        
    def transform_rotational(self, x, y, n_fold):
        """Apply n-fold rotational symmetry"""
        dx = x - CENTER[0]
        dy = y - CENTER[1]
        r = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        
        points = []
        for i in range(n_fold):
            a = angle + (2 * math.pi * i) / n_fold
            px = int(CENTER[0] + r * math.cos(a))
            py = int(CENTER[1] + r * math.sin(a))
            if 0 <= px < self.width and 0 <= py < self.height:
                points.append((px, py))
        return points
    
    def transform_reflection(self, x, y, axes=2):
        """Apply reflection symmetry across axes"""
        dx = x - CENTER[0]
        dy = y - CENTER[1]
        points = []
        
        for ax in range(axes):
            angle = (math.pi * ax) / axes
            # reflect across axis
            c, s = math.cos(2 * angle), math.sin(2 * angle)
            rx = c * dx + s * dy
            ry = s * dx - c * dy
            px = int(CENTER[0] + rx)
            py = int(CENTER[1] + ry)
            if 0 <= px < self.width and 0 <= py < self.height:
                points.append((px, py))
        return points
    
    def transform_spiral(self, x, y, spiral_param=0.05):
        """Apply spiral transformation"""
        dx = x - CENTER[0]
        dy = y - CENTER[1]
        r = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        
        # spiral out
        new_r = r * (1 + spiral_param)
        px = int(CENTER[0] + new_r * math.cos(angle))
        py = int(CENTER[1] + new_r * math.sin(angle))
        if 0 <= px < self.width and 0 <= py < self.height:
            return [(px, py)]
        return []
    
    def draw_line(self, x1, y1, x2, y2, color, symmetry_mode='rotational', n_fold=6):
        """Draw a line with applied symmetry"""
        # get symmetry-transformed points
        p1s = self.get_symmetry_points(x1, y1, symmetry_mode, n_fold)
        p2s = self.get_symmetry_points(x2, y2, symmetry_mode, n_fold)
        
        for (px1, py1), (px2, py2) in zip(p1s, p2s):
            pygame.draw.line(self.canvas, color, (px1, py1), (px2, py2), 2)
    
    def get_symmetry_points(self, x, y, mode='rotational', n_fold=6):
        """Get all symmetry-transformed points"""
        if mode == 'rotational':
            return self.transform_rotational(x, y, n_fold)
        elif mode == 'reflection':
            return self.transform_reflection(x, y, n_fold)
        elif mode == 'spiral':
            return self.transform_spiral(x, y)
        else:
            return [(x, y)]
    
    def add_gesture_point(self, x, y, speed):
        """Add a point to gesture history"""
        self.gesture_history.append((x, y, speed))
        if len(self.gesture_history) > 100:
            self.gesture_history.pop(0)
    
    def clear(self):
        """Clear canvas"""
        self.canvas.fill((10, 10, 10))
        self.gesture_history = []


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hypnotic Pattern Generator")
    clock = pygame.time.Clock()
    
    engine = SymmetryEngine(WIDTH, HEIGHT)
    
    # Pattern state
    symmetry_modes = ['rotational', 'reflection', 'spiral']
    current_mode_idx = 0
    n_fold = 6
    bg_color = (10, 10, 10)
    hue_offset = 0
    
    # Font for HUD
    try:
        font = pygame.font.SysFont("Arial", 14)
    except Exception:
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 14)
    
    running = True
    last_pos = None
    mouse_speed = 0
    
    # Create a surface from the numpy array
    def get_surface_from_array():
        return engine.canvas
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    engine.clear()
                elif event.key == pygame.K_SPACE:
                    current_mode_idx = (current_mode_idx + 1) % len(symmetry_modes)
                elif event.key == pygame.K_UP:
                    n_fold = min(16, n_fold + 1)
                elif event.key == pygame.K_DOWN:
                    n_fold = max(2, n_fold - 1)
                elif event.key == pygame.K_s:
                    fname = f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(screen, fname)
                    print(f"Saved {fname}")
                elif event.key == pygame.K_r:
                    hue_offset = random.randint(0, 360)
        
        # Mouse tracking
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mx, my = pygame.mouse.get_pos()
            if last_pos:
                dx = mx - last_pos[0]
                dy = my - last_pos[1]
                mouse_speed = min(20, math.hypot(dx, dy))
                
                # Color based on speed and hue
                r = int(128 + 127 * math.sin(hue_offset * math.pi / 180 + mouse_speed * 0.1))
                g = int(128 + 127 * math.sin(hue_offset * math.pi / 180 + mouse_speed * 0.1 + 2.0))
                b = int(128 + 127 * math.sin(hue_offset * math.pi / 180 + mouse_speed * 0.1 + 4.0))
                color = (r, g, b)
                
                # Draw with symmetry
                current_mode = symmetry_modes[current_mode_idx]
                engine.draw_line(last_pos[0], last_pos[1], mx, my, color, current_mode, n_fold)
                engine.add_gesture_point(mx, my, mouse_speed)
            
            last_pos = (mx, my)
        else:
            last_pos = None
            mouse_speed = 0
        
        # Render
        screen.fill(bg_color)
        
        # Blit canvas
        surf = get_surface_from_array()
        screen.blit(surf, (0, 0))
        
        # HUD
        mode_name = symmetry_modes[current_mode_idx].upper()
        hud_lines = [
            f"Mode (SPACE): {mode_name}",
            f"Symmetry (↑/↓): {n_fold}-fold",
            f"Speed: {mouse_speed:.1f}",
            "Clear (C), Save (S), Hue (R)"
        ]
        y0 = 8
        for line in hud_lines:
            txt = font.render(line, True, (200, 200, 200))
            screen.blit(txt, (8, y0))
            y0 += 18
        
        pygame.display.flip()
        clock.tick(120)
    
    pygame.quit()


if __name__ == '__main__':
    run()
