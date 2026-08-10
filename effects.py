import cv2
import numpy as np
import math
import random
import os
import time

class Particle:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -1)
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.size = random.randint(10, 25)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        self.angle += 0.1

    def is_alive(self):
        return self.life > 0


class Effects:
    def __init__(self):
        self.particles = []
        self.time = 0
        self.bulge_strength = 30

    def update(self):
        self.time += 1
        self.particles = [p for p in self.particles if p.is_alive()]
        for p in self.particles:
            p.update()

    def draw_heart(self, frame, x, y, size, color, alpha=1.0):
        overlay = frame.copy()
        pts = []
        for t in np.linspace(0, 2 * math.pi, 100):
            hx = size * 16 * math.sin(t) ** 3
            hy = -size * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            pts.append([int(x + hx), int(y + hy)])
        pts = np.array(pts, np.int32)
        cv2.fillPoly(overlay, [pts], color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    def draw_star(self, frame, x, y, size, color, alpha=1.0):
        overlay = frame.copy()
        pts = []
        for i in range(5):
            angle = math.pi / 2 + i * 2 * math.pi / 5
            pts.append([int(x + size * math.cos(angle)), int(y - size * math.sin(angle))])
            angle += math.pi / 5
            pts.append([int(x + size * 0.4 * math.cos(angle)), int(y - size * 0.4 * math.sin(angle))])
        pts = np.array(pts, np.int32)
        cv2.fillPoly(overlay, [pts], color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    def draw_sparkle(self, frame, x, y, size, color):
        cv2.circle(frame, (int(x), int(y)), size, color, -1)
        cv2.circle(frame, (int(x), int(y)), size + 2, (255, 255, 255), 1)

    def draw_butterfly(self, frame, x, y, size, color, angle=0):
        overlay = frame.copy()
        wing_pts1 = np.array([
            [int(x), int(y)],
            [int(x - size * math.cos(angle)), int(y - size * math.sin(angle))],
            [int(x - size * 0.5 * math.cos(angle + 0.5)), int(y - size * 0.5 * math.sin(angle + 0.5))]
        ], np.int32)
        wing_pts2 = np.array([
            [int(x), int(y)],
            [int(x + size * math.cos(angle)), int(y - size * math.sin(angle))],
            [int(x + size * 0.5 * math.cos(angle + 0.5)), int(y - size * 0.5 * math.sin(angle + 0.5))]
        ], np.int32)
        cv2.fillPoly(overlay, [wing_pts1], color)
        cv2.fillPoly(overlay, [wing_pts2], color)
        cv2.line(overlay, (int(x), int(y)), (int(x), int(y - size)), (50, 50, 50), 2)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    def apply_heart_rain(self, frame):
        if random.random() < 0.3:
            x = random.randint(0, frame.shape[1])
            self.particles.append(Particle(x, 0, 'heart'))
        for p in self.particles:
            if p.effect_type == 'heart':
                color = (0, 0, 255)
                self.draw_heart(frame, int(p.x), int(p.y), p.size * (p.life / p.max_life), color, p.life / p.max_life)
        return frame

    def apply_star_rain(self, frame):
        if random.random() < 0.3:
            x = random.randint(0, frame.shape[1])
            self.particles.append(Particle(x, 0, 'star'))
        for p in self.particles:
            if p.effect_type == 'star':
                color = (0, 255, 255)
                self.draw_star(frame, int(p.x), int(p.y), p.size * (p.life / p.max_life), color, p.life / p.max_life)
        return frame

    def apply_sparkle(self, frame):
        if random.random() < 0.5:
            x = random.randint(0, frame.shape[1])
            y = random.randint(0, frame.shape[0])
            self.particles.append(Particle(x, y, 'sparkle'))
        for p in self.particles:
            if p.effect_type == 'sparkle':
                color = (255, 255, 255)
                self.draw_sparkle(frame, int(p.x), int(p.y), p.size // 4, color)
        return frame

    def apply_butterfly(self, frame):
        if random.random() < 0.1 and len([p for p in self.particles if p.effect_type == 'butterfly']) < 5:
            x = random.randint(0, frame.shape[1])
            y = random.randint(0, frame.shape[0] // 2)
            self.particles.append(Particle(x, y, 'butterfly'))
        for p in self.particles:
            if p.effect_type == 'butterfly':
                color = (255, 150, 0)
                self.draw_butterfly(frame, int(p.x), int(p.y), p.size, color, p.angle)
                p.vy = math.sin(p.angle) * 2
        return frame

    def apply_vintage(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 255)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frame[:, :, 0] = np.clip(frame[:, :, 0] + 20, 0, 255)
        frame[:, :, 2] = np.clip(frame[:, :, 2] + 10, 0, 255)
        return frame

    def apply_neon(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        neon_colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        color = neon_colors[self.time % len(neon_colors)]
        mask = edges > 0
        frame[mask] = color
        return frame

    def apply_glitch(self, frame):
        output = frame.copy()
        num_slices = random.randint(3, 8)
        for _ in range(num_slices):
            y = random.randint(0, frame.shape[0] - 20)
            h_slice = random.randint(5, 20)
            shift = random.randint(-30, 30)
            output[y:y+h_slice] = np.roll(frame[y:y+h_slice], shift, axis=1)
        if random.random() < 0.3:
            b, g, r = cv2.split(output)
            shift = random.randint(-10, 10)
            b = np.roll(b, shift, axis=1)
            output = cv2.merge([b, g, r])
        return output

    def apply_thermal(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    def apply_emboss(self, frame):
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        return cv2.filter2D(frame, -1, kernel)

    def apply_sketch(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    def apply_wave(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        for i in range(h):
            offset = int(20 * math.sin(i / 30 + self.time / 10))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return output

    def apply_cartoon(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)

    def apply_mirror(self, frame):
        return cv2.flip(frame, 1)

    def apply_color_shift(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + self.time * 2) % 180
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_sepia(self, frame):
        kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    def apply_invert(self, frame):
        return cv2.bitwise_not(frame)

    def apply_pixelate(self, frame, block_size=10):
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // block_size, h // block_size), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_edge_detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def apply_ai_mini_me(self, frame):
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 3, h // 3))
        output = frame.copy()
        output[0:h//3, 0:w//3] = small
        cv2.rectangle(output, (0, 0), (w//3, h//3), (0, 255, 255), 3)
        return output

    def apply_ai_giant(self, frame):
        h, w = frame.shape[:2]
        face_region = frame[h//4:3*h//4, w//4:3*w//4]
        return cv2.resize(face_region, (w, h), interpolation=cv2.INTER_LANCZOS4)

    def apply_ghibli(self, frame):
        output = cv2.bilateralFilter(frame, 9, 75, 75)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        output = cv2.filter2D(output, -1, kernel)
        warm = np.zeros_like(output)
        warm[:, :, 2] = 15
        return cv2.add(output, warm)

    def apply_pixar(self, frame):
        output = cv2.bilateralFilter(frame, 15, 100, 100)
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        output = cv2.bitwise_and(output, edges)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_anime(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        output = cv2.bitwise_and(color, edges)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_cyberpunk(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + 90) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        neon = np.zeros_like(output)
        neon[:, :, 0] = 255
        neon[:, :, 2] = 255
        output[edges > 0] = neon[edges > 0]
        scanlines = np.zeros_like(output)
        for i in range(0, output.shape[0], 4):
            scanlines[i, :] = 30
        return cv2.add(output, scanlines)

    def apply_superhero(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        output = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        rows, cols = output.shape[:2]
        X = cv2.getGaussianKernel(cols, cols / 2)
        Y = cv2.getGaussianKernel(rows, rows / 2)
        vignette = Y * X.T
        vignette = vignette / vignette.max()
        return (output * vignette[:, :, np.newaxis]).astype(np.uint8)

    def apply_robot(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        metallic = cv2.convertScaleAbs(frame, alpha=1.2, beta=-20)
        hsv = cv2.cvtColor(metallic, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 0
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.5, 0, 255)
        metallic = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return cv2.addWeighted(metallic, 0.7, edges, 0.3, 0)

    def apply_alien(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 60
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        glow = cv2.GaussianBlur(output, (21, 21), 0)
        return cv2.addWeighted(output, 0.7, glow, 0.3, 0)

    def apply_old_to_young(self, frame):
        output = cv2.bilateralFilter(frame, 15, 100, 100)
        output = cv2.bilateralFilter(output, 15, 100, 100)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.1, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_face_tracking(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(3):
            radius = 80 + i * 40
            cv2.circle(overlay, (cx, cy), radius, (0, 255, 0), 2)
        crosshair_size = 30
        cv2.line(overlay, (cx - crosshair_size, cy), (cx + crosshair_size, cy), (0, 255, 0), 2)
        cv2.line(overlay, (cx, cy - crosshair_size), (cx, cy + crosshair_size), (0, 255, 0), 2)
        return cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    def apply_head_tracking(self, frame):
        h, w = frame.shape[:2]
        offset_x = int(10 * math.sin(self.time / 20))
        offset_y = int(10 * math.cos(self.time / 15))
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_eye_glow(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        left_eye = (w // 3, h // 3)
        right_eye = (2 * w // 3, h // 3)
        glow_intensity = int(128 + 127 * math.sin(self.time / 5))
        glow_color = (0, glow_intensity, 255)
        for radius in range(40, 0, -5):
            cv2.circle(overlay, left_eye, radius, glow_color, -1)
            cv2.circle(overlay, right_eye, radius, glow_color, -1)
        return cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    def apply_laser_eyes(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        left_eye = (w // 3, h // 3)
        right_eye = (2 * w // 3, h // 3)
        laser_length = 300
        angle = self.time * 0.1
        left_end = (int(left_eye[0] + laser_length * math.cos(angle)), int(left_eye[1] + laser_length * math.sin(angle)))
        right_end = (int(right_eye[0] + laser_length * math.cos(angle)), int(right_eye[1] + laser_length * math.sin(angle)))
        cv2.line(overlay, left_eye, left_end, (0, 0, 255), 5)
        cv2.line(overlay, right_eye, right_end, (0, 0, 255), 5)
        cv2.circle(overlay, left_eye, 15, (0, 0, 255), -1)
        cv2.circle(overlay, right_eye, 15, (0, 0, 255), -1)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        return cv2.addWeighted(overlay, 0.7, glow, 0.3, 0)

    def apply_floating_head(self, frame):
        h, w = frame.shape[:2]
        head_region = frame[h//4:3*h//4, w//4:3*w//4]
        output = np.zeros_like(frame)
        y_offset = int(20 * math.sin(self.time / 10))
        x_center = w // 2
        y_center = h // 2 + y_offset
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (x_center, y_center), (w//4, h//4), 0, 0, 360, 255, -1)
        head_resized = cv2.resize(head_region, (w//2, h//2))
        x1 = x_center - w//4
        y1 = y_center - h//4
        x2 = x_center + w//4
        y2 = y_center + h//4
        output[max(0,y1):min(h,y2), max(0,x1):min(w,x2)] = head_resized[:min(h,y2)-max(0,y1), :min(w,x2)-max(0,x1)]
        return output

    def apply_clone_effect(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        clone_regions = [(0, 0), (w//2, 0), (0, h//2), (w//2, h//2)]
        small = cv2.resize(frame, (w//3, h//3))
        for cx, cy in clone_regions:
            x1 = min(cx, w - w//3)
            y1 = min(cy, h - h//3)
            output[y1:y1+h//3, x1:x1+w//3] = small
        return output

    def apply_invisible_body(self, frame):
        h, w = frame.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (w//2, h//3), (w//5, h//4), 0, 0, 360, 255, -1)
        bg = cv2.GaussianBlur(frame, (51, 51), 0)
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        return (frame * (1 - mask_3ch) + bg * mask_3ch).astype(np.uint8)

    def apply_body_freeze(self, frame):
        if not hasattr(self, 'frozen_frame') or self.frozen_frame is None:
            self.frozen_frame = frame.copy()
            self.freeze_counter = 0
        self.freeze_counter += 1
        if self.freeze_counter % 60 == 0:
            self.frozen_frame = frame.copy()
        return self.frozen_frame

    def apply_morph_face(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        center = (w // 2, h // 2)
        radius = min(w, h) // 3
        strength = 0.3 + 0.2 * math.sin(self.time / 10)
        for y in range(max(0, center[1] - radius), min(h, center[1] + radius)):
            for x in range(max(0, center[0] - radius), min(w, center[0] + radius)):
                dx = x - center[0]
                dy = y - center[1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < radius:
                    factor = 1.0 + strength * (1 - dist / radius)
                    src_x = int(center[0] + dx * factor)
                    src_y = int(center[1] + dy * factor)
                    if 0 <= src_x < w and 0 <= src_y < h:
                        output[y, x] = frame[src_y, src_x]
        return output

    def apply_smile_enhancement(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_vr_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cx, cy = w // 2, h // 2
        for r in range(min(w, h) // 2, 0, -20):
            hue = (r + self.time * 5) % 180
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(overlay, (cx, cy), r, color_bgr.tolist(), 3)
        return cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    def apply_teleport_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cx, cy = w // 2, h // 2
        for i in range(50):
            angle = (2 * math.pi * i / 50) + self.time * 0.1
            radius = 100 + 50 * math.sin(self.time * 0.2 + i)
            px = int(cx + radius * math.cos(angle))
            py = int(cy + radius * math.sin(angle))
            size = int(5 + 5 * math.sin(self.time * 0.3 + i))
            cv2.circle(overlay, (px, py), size, (255, 200, 0), -1)
        cv2.circle(overlay, (cx, cy), 80, (255, 255, 255), 2)
        return cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    def apply_mirror_dimension(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(frame[:, w//2:], 1)
        output = np.zeros_like(frame)
        output[:, :w//2] = left
        output[:, w//2:] = right
        cv2.line(output, (w//2, 0), (w//2, h), (0, 255, 255), 2)
        return output

    def apply_multiverse_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(4):
            angle = (2 * math.pi * i / 4) + self.time * 0.05
            scale = 0.3 + 0.1 * math.sin(self.time * 0.1 + i)
            small = cv2.resize(frame, None, fx=scale, fy=scale)
            sh, sw = small.shape[:2]
            px = int(w // 2 + 150 * math.cos(angle) - sw // 2)
            py = int(h // 2 + 150 * math.sin(angle) - sh // 2)
            px = max(0, min(w - sw, px))
            py = max(0, min(h - sh, py))
            output[py:py+sh, px:px+sw] = small
        return output

    def apply_wormhole_jump(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h // 2
        for r in range(min(w, h) // 2, 0, -5):
            distortion = int(10 * math.sin(r / 20 + self.time / 5))
            y_start = max(0, cy - r)
            y_end = min(h, cy + r)
            strip_h = min(3, y_end - y_start)
            if strip_h > 0:
                output[y_start:y_start+strip_h, :] = np.roll(output[y_start:y_start+strip_h, :], distortion, axis=1)
        return output

    def apply_quantum_tunnel(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h // 2
        for i in range(5):
            radius = 100 - i * 15
            offset = int(50 * math.sin(self.time / 10 + i))
            pts = []
            for angle in np.linspace(0, 2 * math.pi, 100):
                x = int(cx + (radius + offset) * math.cos(angle))
                y = int(cy + (radius + offset) * 0.6 * math.sin(angle))
                pts.append([x, y])
            pts = np.array(pts, np.int32)
            cv2.polylines(output, [pts], True, (255, 255, 0), 2)
        return output

    def apply_time_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h // 2
        for i in range(8):
            angle = (2 * math.pi * i / 8) + self.time * 0.05
            radius = 150
            px = int(cx + radius * math.cos(angle))
            py = int(cy + radius * math.sin(angle))
            cv2.circle(output, (px, py), 30, (255, 255, 255), 2)
            hand_angle = self.time * 0.2 + i
            hx = int(px + 20 * math.cos(hand_angle))
            hy = int(py + 20 * math.sin(hand_angle))
            cv2.line(output, (px, py), (hx, hy), (0, 0, 255), 2)
        return output

    def apply_black_hole_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h // 2
        for r in range(min(w, h) // 2, 0, -3):
            darkness = r / (min(w, h) // 2)
            output[max(0,cy-r):min(h,cy+r), max(0,cx-r):min(w,cx+r)] = (output[max(0,cy-r):min(h,cy+r), max(0,cx-r):min(w,cx+r)] * darkness).astype(np.uint8)
        for angle in np.linspace(0, 2 * math.pi, 20):
            r = 150
            x = int(cx + r * math.cos(angle + self.time * 0.1))
            y = int(cy + r * math.sin(angle + self.time * 0.1))
            cv2.circle(output, (x, y), 3, (255, 200, 0), -1)
        return output

    def apply_door_another_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        door_w = w // 3
        door_h = 2 * h // 3
        door_x = (w - door_w) // 2
        door_y = (h - door_h) // 2
        cv2.rectangle(output, (door_x - 10, door_y - 10), (door_x + door_w + 10, door_y + door_h + 10), (139, 69, 19), 10)
        portal_color = int(128 + 127 * math.sin(self.time / 10))
        cv2.rectangle(output, (door_x, door_y), (door_x + door_w, door_y + door_h), (portal_color, 100, 255), -1)
        return output

    def apply_infinite_room(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(5):
            scale = 1.0 - i * 0.15
            small = cv2.resize(frame, None, fx=scale, fy=scale)
            sh, sw = small.shape[:2]
            x1 = (w - sw) // 2
            y1 = (h - sh) // 2
            x2 = x1 + sw
            y2 = y1 + sh
            brightness = 255 - i * 40
            cv2.rectangle(output, (x1 - 2, y1 - 2), (x2 + 2, y2 + 2), (brightness, brightness, brightness), 2)
            output[y1:y2, x1:x2] = small
        return output

    def apply_floating_objects(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for i in range(8):
            x = int((100 + i * 100 + self.time * 2) % w)
            y = int(h // 2 + 50 * math.sin(self.time / 20 + i))
            size = int(20 + 10 * math.sin(self.time / 15 + i))
            color = [(0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0)][i % 4]
            cv2.circle(overlay, (x, y), size, color, -1)
        return cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    def apply_gravity_flip(self, frame):
        return cv2.flip(frame, 0)

    def apply_zero_gravity(self, frame):
        h, w = frame.shape[:2]
        offset_x = int(15 * math.sin(self.time / 30))
        offset_y = int(15 * math.cos(self.time / 25))
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_earthquake(self, frame):
        h, w = frame.shape[:2]
        shake_x = int(20 * math.sin(self.time * 2))
        shake_y = int(10 * math.cos(self.time * 3))
        M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_meteor_shower(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        if random.random() < 0.3:
            x = random.randint(0, w)
            self.particles.append(Particle(x, 0, 'meteor'))
        for p in self.particles:
            if p.effect_type == 'meteor':
                p.vy = 8
                p.vx = -2
                end_x = int(p.x + 50)
                end_y = int(p.y + 50)
                cv2.line(overlay, (int(p.x), int(p.y)), (end_x, end_y), (0, 150, 255), 3)
                cv2.circle(overlay, (int(p.x), int(p.y)), 5, (0, 200, 255), -1)
        return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    def apply_aurora_sky(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(h // 4):
            y = i * 4
            hue = int((120 + 40 * math.sin(y / 50 + self.time / 20)) % 180)
            color_hsv = np.uint8([[[hue, 255, 200]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.line(output, (0, y), (w, y), color_bgr.tolist(), 2)
        return cv2.addWeighted(output, 0.7, frame, 0.3, 0)

    def apply_fireworks(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        if random.random() < 0.2:
            cx = random.randint(w // 4, 3 * w // 4)
            cy = random.randint(h // 4, h // 2)
            for _ in range(30):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.randint(20, 80)
                x = int(cx + dist * math.cos(angle))
                y = int(cy + dist * math.sin(angle))
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv2.circle(overlay, (x, y), 3, color, -1)
        return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    def apply_lightning_storm(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        if random.random() < 0.1:
            x = random.randint(w // 4, 3 * w // 4)
            points = [(x, 0)]
            current_x = x
            for y in range(0, h, 20):
                current_x += random.randint(-30, 30)
                points.append((current_x, y))
            for i in range(len(points) - 1):
                cv2.line(overlay, points[i], points[i + 1], (255, 255, 255), 3)
        return cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

    def apply_snow_world(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        if random.random() < 0.5:
            x = random.randint(0, w)
            self.particles.append(Particle(x, 0, 'snow'))
        for p in self.particles:
            if p.effect_type == 'snow':
                p.vy = 2
                p.vx = math.sin(p.angle) * 0.5
                size = random.randint(3, 8)
                cv2.circle(overlay, (int(p.x), int(p.y)), size, (255, 255, 255), -1)
        return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    def apply_sandstorm(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(100):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(1, 4)
            color = (random.randint(150, 200), random.randint(180, 220), random.randint(200, 240))
            cv2.circle(overlay, (x, y), size, color, -1)
        hsv = cv2.cvtColor(overlay, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 20
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.8, 0, 255)
        overlay = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    def apply_ai_melt(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(h - 1, h // 2, -1):
            offset = int(30 * math.sin(y / 20 + self.time / 10) * (h - y) / h)
            output[y, :] = np.roll(frame[y, :], offset, axis=0)
        return output

    def apply_ai_squish(self, frame):
        h, w = frame.shape[:2]
        squish = 0.8 + 0.2 * math.sin(self.time / 10)
        new_h = int(h * squish)
        squished = cv2.resize(frame, (w, new_h))
        output = np.zeros_like(frame)
        y_offset = (h - new_h) // 2
        output[y_offset:y_offset + new_h, :] = squished
        return output

    def apply_cakeify(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 10
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.5, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        h, w = frame.shape[:2]
        for y in range(0, h, 30):
            cv2.line(output, (0, y), (w, y), (200, 150, 200), 2)
        return output

    def apply_glass_break(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(15):
            start_x = random.randint(0, w)
            start_y = random.randint(0, h)
            points = [(start_x, start_y)]
            for _ in range(5):
                new_x = points[-1][0] + random.randint(-50, 50)
                new_y = points[-1][1] + random.randint(-50, 50)
                points.append((new_x, new_y))
            for i in range(len(points) - 1):
                cv2.line(output, points[i], points[i + 1], (255, 255, 255), 1)
        return output

    def apply_ice_freeze(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 120
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        overlay = output.copy()
        for _ in range(50):
            x = random.randint(0, frame.shape[1])
            y = random.randint(0, frame.shape[0])
            size = random.randint(5, 20)
            pts = []
            for i in range(6):
                angle = math.pi / 3 * i
                px = int(x + size * math.cos(angle))
                py = int(y + size * math.sin(angle))
                pts.append([px, py])
            pts = np.array(pts, np.int32)
            cv2.polylines(overlay, [pts], True, (200, 230, 255), 1)
        return cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)

    def apply_liquid_metal(self, frame):
        output = frame.copy()
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 0
        hsv[:, :, 1] = 20
        hsv[:, :, 2] = gray
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        return cv2.filter2D(output, -1, kernel)

    def apply_crystal(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        for i in range(10):
            pts = []
            cx = random.randint(0, w)
            cy = random.randint(0, h)
            num_sides = random.randint(4, 8)
            radius = random.randint(30, 80)
            for j in range(num_sides):
                angle = 2 * math.pi * j / num_sides
                px = int(cx + radius * math.cos(angle))
                py = int(cy + radius * math.sin(angle))
                pts.append([px, py])
            pts = np.array(pts, np.int32)
            color = (random.randint(150, 255), random.randint(150, 255), random.randint(200, 255))
            overlay = output.copy()
            cv2.fillPoly(overlay, [pts], color)
            cv2.addWeighted(overlay, 0.2, output, 0.8, 0, output)
            cv2.polylines(output, [pts], True, (255, 255, 255), 1)
        return output

    def apply_gold(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 25
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(output, -1, kernel)

    def apply_smoke_dissolve(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(20, 60)
            alpha = random.uniform(0.1, 0.4)
            overlay = output.copy()
            cv2.circle(overlay, (x, y), size, (100, 100, 100), -1)
            overlay = cv2.GaussianBlur(overlay, (21, 21), 0)
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
        return output

    def apply_pixel_disintegration(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        block_size = 10
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                if random.random() < 0.1:
                    offset_x = random.randint(-20, 20)
                    offset_y = random.randint(-20, 20)
                    src_y = min(max(0, y), h - block_size)
                    src_x = min(max(0, x), w - block_size)
                    dst_y = min(max(0, y + offset_y), h - block_size)
                    dst_x = min(max(0, x + offset_x), w - block_size)
                    output[dst_y:dst_y+block_size, dst_x:dst_x+block_size] = frame[src_y:src_y+block_size, src_x:src_x+block_size]
        return output

    def apply_hologram(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 120
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.5, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        scanline_intensity = 0.3 + 0.1 * math.sin(self.time / 5)
        for y in range(0, h, 3):
            output[y, :] = (output[y, :] * scanline_intensity).astype(np.uint8)
        glow = cv2.GaussianBlur(output, (15, 15), 0)
        return cv2.addWeighted(output, 0.7, glow, 0.3, 0)

    def apply_neon_cyberpunk(self, frame):
        output = frame.copy()
        edges = cv2.Canny(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY), 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        neon_colors = [(255, 0, 255), (0, 255, 255), (255, 0, 0)]
        color = neon_colors[self.time % len(neon_colors)]
        output[edges > 0] = color
        glow = cv2.GaussianBlur(output, (15, 15), 0)
        return cv2.addWeighted(output, 0.7, glow, 0.3, 0)

    def apply_digital_glitch(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(5):
            y = random.randint(0, h - 10)
            slice_h = random.randint(5, 20)
            shift = random.randint(-50, 50)
            output[y:y+slice_h] = np.roll(frame[y:y+slice_h], shift, axis=1)
        b, g, r = cv2.split(output)
        shift = random.randint(-5, 5)
        b = np.roll(b, shift, axis=1)
        return cv2.merge([b, g, r])

    def apply_rgb_split(self, frame):
        b, g, r = cv2.split(frame)
        offset = int(10 * math.sin(self.time / 10))
        b = np.roll(b, offset, axis=1)
        r = np.roll(r, -offset, axis=1)
        return cv2.merge([b, g, r])

    def apply_vhs_retro(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        noise = np.random.normal(0, 15, (h, w, 3)).astype(np.uint8)
        output = cv2.add(output, noise)
        for y in range(0, h, 2):
            if random.random() < 0.1:
                output[y, :] = np.roll(output[y, :], random.randint(-10, 10), axis=0)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.putText(output, "REC", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return output

    def apply_matrix_rain(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        chars = "0123456789ABCDEF"
        if not hasattr(self, 'matrix_columns'):
            self.matrix_columns = [random.randint(0, h) for _ in range(w // 20)]
        for i, col_y in enumerate(self.matrix_columns):
            x = i * 20
            if x < w:
                char = chars[random.randint(0, len(chars) - 1)]
                cv2.putText(overlay, char, (x, col_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                self.matrix_columns[i] = col_y + 20 if col_y < h else 0
        return cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    def apply_energy_aura(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(5):
            radius = 100 + i * 30 + 10 * math.sin(self.time / 10 + i)
            hue = (self.time * 5 + i * 30) % 180
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(overlay, (cx, cy), int(radius), color_bgr.tolist(), 3)
        glow = cv2.GaussianBlur(overlay, (21, 21), 0)
        return cv2.addWeighted(glow, 0.3, frame, 0.7, 0)

    def apply_magic_spell(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(50):
            angle = (2 * math.pi * i / 50) + self.time * 0.1
            radius = 120 + 30 * math.sin(self.time * 0.2 + i * 0.5)
            px = int(cx + radius * math.cos(angle))
            py = int(cy + radius * math.sin(angle))
            color = (random.randint(150, 255), random.randint(100, 200), random.randint(200, 255))
            cv2.circle(overlay, (px, py), 4, color, -1)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        return cv2.addWeighted(glow, 0.4, frame, 0.6, 0)

    def apply_dragon_fire(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        mouth_x = w // 2
        mouth_y = h // 2
        for _ in range(20):
            angle = random.uniform(-0.5, 0.5)
            dist = random.randint(50, 150)
            x = int(mouth_x + dist * math.cos(angle))
            y = int(mouth_y + dist * math.sin(angle))
            size = random.randint(10, 30)
            color = (0, random.randint(100, 200), random.randint(200, 255))
            cv2.circle(overlay, (x, y), size, color, -1)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        return cv2.addWeighted(glow, 0.5, frame, 0.5, 0)

    def apply_electric_shock(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(5):
            start_x = random.randint(0, w)
            start_y = random.randint(0, h)
            points = [(start_x, start_y)]
            for _ in range(10):
                new_x = points[-1][0] + random.randint(-30, 30)
                new_y = points[-1][1] + random.randint(-30, 30)
                points.append((new_x, new_y))
            for i in range(len(points) - 1):
                cv2.line(overlay, points[i], points[i + 1], (255, 255, 0), 2)
        glow = cv2.GaussianBlur(overlay, (7, 7), 0)
        return cv2.addWeighted(glow, 0.5, frame, 0.5, 0)

    def apply_magic_circle(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        radius = 150
        cv2.circle(overlay, (cx, cy), radius, (255, 255, 0), 2)
        for i in range(8):
            angle = (2 * math.pi * i / 8) + self.time * 0.05
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            cv2.circle(overlay, (x, y), 10, (0, 255, 255), 2)
        return cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    def apply_particle_explosion(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        if random.random() < 0.3:
            cx = random.randint(w // 4, 3 * w // 4)
            cy = random.randint(h // 4, 3 * h // 4)
            for _ in range(50):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.randint(10, 100)
                x = int(cx + dist * math.cos(angle))
                y = int(cy + dist * math.sin(angle))
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv2.circle(overlay, (x, y), 3, color, -1)
        return cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    def apply_rainbow_energy(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        for i, color in enumerate(rainbow_colors):
            radius = 100 + i * 15 + 5 * math.sin(self.time / 10)
            cv2.circle(overlay, (cx, cy), int(radius), color, 3)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        return cv2.addWeighted(glow, 0.4, frame, 0.6, 0)

    def apply_phoenix_wings(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        wing_span = 200
        wing_height = 150
        left_pts = np.array([
            [w // 4, h // 2],
            [w // 4 - wing_span // 2, h // 2 - wing_height],
            [w // 4 - wing_span // 4, h // 2],
            [w // 4 - wing_span // 2, h // 2 + wing_height // 2]
        ], np.int32)
        right_pts = np.array([
            [3 * w // 4, h // 2],
            [3 * w // 4 + wing_span // 2, h // 2 - wing_height],
            [3 * w // 4 + wing_span // 4, h // 2],
            [3 * w // 4 + wing_span // 2, h // 2 + wing_height // 2]
        ], np.int32)
        cv2.fillPoly(overlay, [left_pts], (0, 150, 255))
        cv2.fillPoly(overlay, [right_pts], (0, 150, 255))
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        return cv2.addWeighted(glow, 0.4, frame, 0.6, 0)

    def apply_angel_wings(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        wing_span = 180
        wing_height = 130
        left_pts = np.array([
            [w // 4, h // 2],
            [w // 4 - wing_span // 2, h // 2 - wing_height],
            [w // 4 - wing_span // 3, h // 2],
            [w // 4 - wing_span // 2, h // 2 + wing_height // 3]
        ], np.int32)
        right_pts = np.array([
            [3 * w // 4, h // 2],
            [3 * w // 4 + wing_span // 2, h // 2 - wing_height],
            [3 * w // 4 + wing_span // 3, h // 2],
            [3 * w // 4 + wing_span // 2, h // 2 + wing_height // 3]
        ], np.int32)
        cv2.fillPoly(overlay, [left_pts], (255, 255, 255))
        cv2.fillPoly(overlay, [right_pts], (255, 255, 255))
        glow = cv2.GaussianBlur(overlay, (11, 11), 0)
        return cv2.addWeighted(glow, 0.4, frame, 0.6, 0)

    def apply_devil_wings(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        wing_span = 200
        wing_height = 150
        left_pts = np.array([
            [w // 4, h // 2],
            [w // 4 - wing_span // 2, h // 2 - wing_height],
            [w // 4 - wing_span // 3, h // 2 - wing_height // 2],
            [w // 4 - wing_span // 2, h // 2]
        ], np.int32)
        right_pts = np.array([
            [3 * w // 4, h // 2],
            [3 * w // 4 + wing_span // 2, h // 2 - wing_height],
            [3 * w // 4 + wing_span // 3, h // 2 - wing_height // 2],
            [3 * w // 4 + wing_span // 2, h // 2]
        ], np.int32)
        cv2.fillPoly(overlay, [left_pts], (0, 0, 150))
        cv2.fillPoly(overlay, [right_pts], (0, 0, 150))
        glow = cv2.GaussianBlur(overlay, (11, 11), 0)
        return cv2.addWeighted(glow, 0.4, frame, 0.6, 0)

    def apply_floating_text(self, frame):
        h, w = frame.shape[:2]
        texts = ["TikTok", "VIRAL", "FYP", "TRENDING"]
        for i, text in enumerate(texts):
            x = int(100 + i * 150 + 10 * math.sin(self.time / 10 + i))
            y = int(h // 2 + 30 * math.cos(self.time / 15 + i))
            cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        return frame

    def apply_orbiting_planets(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        cv2.circle(overlay, (cx, cy), 40, (0, 200, 200), -1)
        for i in range(3):
            angle = (2 * math.pi * i / 3) + self.time * 0.05
            orbit_radius = 100 + i * 40
            px = int(cx + orbit_radius * math.cos(angle))
            py = int(cy + orbit_radius * math.sin(angle))
            planet_size = 10 + i * 5
            color = [(255, 100, 0), (0, 255, 100), (100, 0, 255)][i]
            cv2.circle(overlay, (px, py), planet_size, color, -1)
            cv2.circle(overlay, (cx, cy), orbit_radius, (100, 100, 100), 1)
        return cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    def apply_mini_planet(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        cx, cy = w // 2, h // 2
        max_r = min(w, h) // 3
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                dx = x - cx
                dy = y - cy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < max_r:
                    angle = math.atan2(dy, dx)
                    src_x = int((angle + math.pi) / (2 * math.pi) * w) % w
                    src_y = int(dist / max_r * h) % h
                    output[y:y+2, x:x+2] = frame[src_y:src_y+2, src_x:src_x+2]
        return output

    def apply_cinematic_zoom(self, frame):
        h, w = frame.shape[:2]
        zoom_factor = 1.0 + 0.1 * math.sin(self.time / 20)
        new_w = int(w * zoom_factor)
        new_h = int(h * zoom_factor)
        zoomed = cv2.resize(frame, (new_w, new_h))
        x1 = (new_w - w) // 2
        y1 = (new_h - h) // 2
        return zoomed[y1:y1+h, x1:x1+w]

    def apply_young_to_old(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        noise = np.random.normal(0, 10, gray.shape).astype(np.uint8)
        noisy = cv2.add(gray, noise)
        output = cv2.cvtColor(noisy, cv2.COLOR_GRAY2BGR)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        output = cv2.filter2D(output, -1, kernel)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.6, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # ==================== FACE AI EFFECTS ====================
    def apply_face_scan(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        scan_line = int((self.time * 5) % h)
        cv2.line(overlay, (0, scan_line), (w, scan_line), (0, 255, 0), 2)
        cv2.putText(overlay, "SCANNING...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(overlay, f"Resolution: {w}x{h}", (10, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(overlay, "Face Detection: ON", (10, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(overlay, "Age Estimation: Active", (10, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        return frame

    def apply_avatar_anime(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        output = cv2.bitwise_and(color, edges)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_avatar_cartoon(self, frame):
        output = cv2.bilateralFilter(frame, 15, 100, 100)
        output = cv2.bilateralFilter(output, 15, 100, 100)
        output = cv2.bilateralFilter(output, 15, 100, 100)
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        output = cv2.bitwise_and(output, edges)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_beauty_ai(self, frame):
        output = cv2.bilateralFilter(frame, 15, 100, 100)
        output = cv2.bilateralFilter(output, 15, 100, 100)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.1, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        glow = cv2.GaussianBlur(output, (15, 15), 0)
        return cv2.addWeighted(output, 0.8, glow, 0.2, 0)

    def apply_emotion_happy(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(5):
            angle = math.radians(i * 72 + self.time * 2)
            x = int(cx + 100 * math.cos(angle))
            y = int(cy + 100 * math.sin(angle))
            cv2.circle(overlay, (x, y), 15, (0, 255, 255), -1)
        cv2.putText(overlay, "HAPPY", (cx - 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_emotion_sad(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(3):
            y = int(50 + i * 30 + 10 * math.sin(self.time / 5))
            cv2.line(overlay, (cx - 10, y), (cx + 10, y + 20), (255, 100, 100), 3)
        cv2.putText(overlay, "SAD", (cx - 30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_emotion_surprised(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        pulse = int(20 + 10 * math.sin(self.time / 3))
        cv2.circle(overlay, (cx, cy), pulse, (255, 255, 0), 3)
        cv2.putText(overlay, "WOW!", (cx - 40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_emotion_angry(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            x1 = int(cx + 80 * math.cos(angle))
            y1 = int(cy + 80 * math.sin(angle))
            x2 = int(cx + 120 * math.cos(angle))
            y2 = int(cy + 120 * math.sin(angle))
            cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(overlay, "ANGRY", (cx - 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    # ==================== VR FANTASY EFFECTS ====================
    def apply_galaxy_portal(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(50):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(50, 200)
            x = int(cx + dist * math.cos(angle + self.time * 0.05))
            y = int(cy + dist * math.sin(angle + self.time * 0.05))
            size = random.randint(1, 4)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(overlay, (x, y), size, color, -1)
        for r in range(50, 150, 20):
            hue = (r + self.time * 3) % 180
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(overlay, (cx, cy), r, color_bgr.tolist(), 2)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_fire_aura(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for i in range(30):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(100, 200)
            x = int(cx + dist * math.cos(angle))
            y = int(cy + dist * math.sin(angle) * 0.5)
            size = random.randint(10, 30)
            color = (0, random.randint(100, 200), random.randint(200, 255))
            cv2.circle(overlay, (x, y), size, color, -1)
        glow = cv2.GaussianBlur(overlay, (21, 21), 0)
        frame = cv2.addWeighted(glow, 0.3, frame, 0.7, 0)
        return frame

    def apply_lightning_power(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(5):
            start_x = random.randint(0, w)
            start_y = random.randint(0, h // 2)
            points = [(start_x, start_y)]
            for _ in range(8):
                new_x = points[-1][0] + random.randint(-40, 40)
                new_y = points[-1][1] + random.randint(20, 50)
                points.append((new_x, new_y))
            for i in range(len(points) - 1):
                cv2.line(overlay, points[i], points[i + 1], (255, 255, 200), 3)
        glow = cv2.GaussianBlur(overlay, (7, 7), 0)
        frame = cv2.addWeighted(glow, 0.5, frame, 0.5, 0)
        return frame

    def apply_ice_world(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 120
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        overlay = output.copy()
        for _ in range(100):
            x = random.randint(0, frame.shape[1])
            y = random.randint(0, frame.shape[0])
            size = random.randint(1, 5)
            cv2.circle(overlay, (x, y), size, (255, 255, 255), -1)
        cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)
        return output

    def apply_ocean_vr(self, frame):
        output = frame.copy()
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 100
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        overlay = output.copy()
        for i in range(20):
            x = int((self.time * 3 + i * 50) % frame.shape[1])
            y = int(frame.shape[0] // 2 + 50 * math.sin(self.time / 20 + i))
            pts = []
            for t in np.linspace(0, 2 * math.pi, 20):
                px = int(x + 15 * math.cos(t))
                py = int(y + 8 * math.sin(t))
                pts.append([px, py])
            pts = np.array(pts, np.int32)
            cv2.fillPoly(overlay, [pts], (255, 200, 100))
        cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)
        return output

    # ==================== AR CAMERA EFFECTS ====================
    def apply_object_detection(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        objects = [
            {"name": "Person", "conf": 95, "x": w//4, "y": h//4, "w": w//3, "h": h//2},
            {"name": "Object", "conf": 87, "x": w//2, "y": h//3, "w": w//4, "h": h//3},
        ]
        for obj in objects:
            x, y, ow, oh = obj["x"], obj["y"], obj["w"], obj["h"]
            cv2.rectangle(overlay, (x, y), (x + ow, y + oh), (0, 255, 0), 2)
            cv2.putText(overlay, f'{obj["name"]} {obj["conf"]}%', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(overlay, "AI OBJECT DETECTION", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        return frame

    def apply_human_scanner(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        scan_line = int((self.time * 3) % h)
        cv2.line(overlay, (0, scan_line), (w, scan_line), (0, 255, 255), 2)
        cv2.putText(overlay, "HUMAN SCANNER", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(overlay, "Person Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(overlay, "Pose: Active", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(overlay, "Tracking: ON", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        return frame

    # ==================== VIRAL TIKTOK EFFECTS ====================
    def apply_magic_sparkle(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(2, 8)
            alpha = random.uniform(0.5, 1.0)
            color = (255, 255, 255)
            cv2.circle(overlay, (x, y), size, color, -1)
            cv2.line(overlay, (x - size * 2, y), (x + size * 2, y), color, 1)
            cv2.line(overlay, (x, y - size * 2), (x, y + size * 2), color, 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_galaxy_eyes(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        left_eye = (w // 3, h // 3)
        right_eye = (2 * w // 3, h // 3)
        for eye in [left_eye, right_eye]:
            for r in range(30, 0, -3):
                hue = (r * 10 + self.time * 5) % 180
                color_hsv = np.uint8([[[hue, 255, 255]]])
                color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
                cv2.circle(overlay, eye, r, color_bgr.tolist(), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        return frame

    def apply_royal_filter(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 4
        crown_pts = np.array([
            [cx - 60, cy + 30], [cx - 50, cy - 20], [cx - 20, cy],
            [cx, cy - 40], [cx + 20, cy], [cx + 50, cy - 20], [cx + 60, cy + 30]
        ], np.int32)
        cv2.fillPoly(overlay, [crown_pts], (0, 215, 255))
        for i in range(3):
            gem_x = cx + (-40 + i * 40)
            gem_y = cy - 10 + (i % 2) * 10
            cv2.circle(overlay, (gem_x, gem_y), 5, (0, 0, 255), -1)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        frame = cv2.addWeighted(glow, 0.3, frame, 0.7, 0)
        return frame

    def apply_cyberpunk_hud(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cv2.putText(overlay, "SYSTEM ONLINE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(overlay, "FACE DETECTED", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(overlay, "OBJECT SCAN", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(overlay, "TARGET LOCK", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
        cv2.rectangle(overlay, (w - 150, 10), (w - 10, 110), (0, 255, 255), 2)
        cv2.putText(overlay, "AI POWER", (w - 140, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        power_bar = int(80 + 10 * math.sin(self.time / 10))
        cv2.rectangle(overlay, (w - 140, 45), (w - 140 + power_bar, 55), (0, 255, 0), -1)
        for i in range(5):
            y = 150 + i * 20
            cv2.line(overlay, (10, y), (w - 10, y), (0, 255, 255), 1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_robot_vision(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cv2.putText(overlay, "ROBOT VISION", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.putText(overlay, "SCAN COMPLETE", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        grid_size = 50
        for x in range(0, w, grid_size):
            cv2.line(overlay, (x, 0), (x, h), (255, 0, 0), 1)
        for y in range(0, h, grid_size):
            cv2.line(overlay, (0, y), (w, y), (255, 0, 0), 1)
        cv2.circle(overlay, (w // 2, h // 2), 100, (0, 255, 0), 2)
        cv2.line(overlay, (w // 2 - 120, h // 2), (w // 2 + 120, h // 2), (0, 255, 0), 1)
        cv2.line(overlay, (w // 2, h // 2 - 120), (w // 2, h // 2 + 120), (0, 255, 0), 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    # ==================== PROFESSIONAL CAMERA EFFECTS ====================
    def apply_cinematic_ai(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        output = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        rows, cols = output.shape[:2]
        X = cv2.getGaussianKernel(cols, cols / 2)
        Y = cv2.getGaussianKernel(rows, rows / 2)
        vignette = Y * X.T
        vignette = vignette / vignette.max()
        output = (output * vignette[:, :, np.newaxis]).astype(np.uint8)
        return output

    def apply_sunset_ai(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 10
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        warm = np.zeros_like(output)
        warm[:, :, 2] = 30
        output = cv2.add(output, warm)
        return output

    def apply_weather_rain(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        for _ in range(100):
            x = random.randint(0, w)
            y = random.randint(0, h)
            length = random.randint(10, 30)
            cv2.line(overlay, (x, y), (x - 5, y + length), (200, 200, 255), 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_weather_fog(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        fog = np.ones_like(overlay) * 200
        alpha = 0.3 + 0.1 * math.sin(self.time / 20)
        output = cv2.addWeighted(overlay, 1 - alpha, fog, alpha, 0)
        return output

    # ==================== SPECIAL MODES ====================
    def apply_future_vision(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cv2.putText(overlay, "WAHID AI VISION", (w // 2 - 120, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(overlay, "FACE DETECTED", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(overlay, "OBJECT DETECTED", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(overlay, "ENVIRONMENT SCAN", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        power = int(90 + 9 * math.sin(self.time / 10))
        cv2.putText(overlay, f"AI POWER {power}%", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.rectangle(overlay, (20, 180), (20 + power * 2, 195), (0, 255, 0), -1)
        cv2.rectangle(overlay, (20, 180), (220, 195), (0, 255, 0), 2)
        for i in range(10):
            y = 220 + i * 15
            bar_width = int(50 + 30 * math.sin(self.time / 10 + i))
            cv2.rectangle(overlay, (20, y), (20 + bar_width, y + 10), (0, 255, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_time_machine(self, frame):
        year = 1920 + int((self.time / 10) % 130)
        if year < 2000:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            output[:, :, 0] = np.clip(output[:, :, 0] + 20, 0, 255)
            output[:, :, 2] = np.clip(output[:, :, 2] + 10, 0, 255)
        elif year < 2050:
            output = frame.copy()
            hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
            output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        else:
            output = frame.copy()
            hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
            hsv[:, :, 0] = (hsv[:, :, 0] + 90) % 180
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
            output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.putText(output, f"YEAR: {year}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return output

    def apply_hologram_studio(self, frame):
        output = frame.copy()
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 120
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.5, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        for y in range(0, h, 3):
            output[y, :] = (output[y, :] * 0.7).astype(np.uint8)
        glow = cv2.GaussianBlur(output, (15, 15), 0)
        output = cv2.addWeighted(output, 0.7, glow, 0.3, 0)
        cv2.putText(output, "HOLOGRAM MODE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        return output

    def apply_magic_portal(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        for r in range(20, 150, 10):
            hue = (r * 3 + self.time * 5) % 180
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            angle = self.time * 0.1 + r * 0.1
            offset_x = int(10 * math.sin(angle))
            offset_y = int(10 * math.cos(angle))
            cv2.circle(overlay, (cx + offset_x, cy + offset_y), r, color_bgr.tolist(), 2)
        glow = cv2.GaussianBlur(overlay, (15, 15), 0)
        frame = cv2.addWeighted(glow, 0.4, frame, 0.6, 0)
        return frame


# ============================================================
# 100+ EFEK VR UNTUK KAMERA & VIDEO
# ============================================================

# --- A. Camera & Lens ---

    def apply_360_equirectangular(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                theta = (j / w) * 2 * math.pi
                phi = (i / h) * math.pi
                map_x[i, j] = cx + 0.5 * w * math.sin(phi) * math.cos(theta)
                map_y[i, j] = cy + 0.5 * h * math.cos(phi)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)

    def apply_little_planet(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        cx, cy = w // 2, h // 2
        radius = min(w, h) * 0.35
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < radius:
                    angle = math.atan2(dy, dx)
                    r = (dist / radius) * h * 0.8
                    sx = int((math.cos(angle) * r + w / 2) % w)
                    sy = int((math.sin(angle) * r + h / 2) % h)
                    output[i, j] = frame[sy, sx]
                else:
                    blue_shift = int(255 * (1 - (dist - radius) / (max(w, h) * 0.3)))
                    output[i, j] = [max(0, blue_shift), max(0, blue_shift // 2), min(255, blue_shift)]
        return output

    def apply_tiny_planet_spin(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        cx, cy = w // 2, h // 2
        radius = min(w, h) * 0.35
        angle_offset = self.time * 0.05
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < radius:
                    angle = math.atan2(dy, dx) + angle_offset
                    r = (dist / radius) * h * 0.8
                    sx = int((math.cos(angle) * r + w / 2) % w)
                    sy = int((math.sin(angle) * r + h / 2) % h)
                    output[i, j] = frame[sy, sx]
                else:
                    output[i, j] = [30, 15, 10]
        return output

    def apply_fisheye_ultra(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k = 0.5
        for i in range(h):
            for j in range(w):
                r2 = ((j - cx)**2 + (i - cy)**2) / (cx**2 + cy**2)
                r2 = min(r2, 1.0)
                map_x[i, j] = cx + (j - cx) * (1 + k * r2)
                map_y[i, j] = cy + (i - cy) * (1 + k * r2)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_super_fisheye(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k = 1.0
        for i in range(h):
            for j in range(w):
                r2 = ((j - cx)**2 + (i - cy)**2) / (cx**2 + cy**2)
                r2 = min(r2, 1.0)
                map_x[i, j] = cx + (j - cx) * (1 + k * r2)
                map_y[i, j] = cy + (i - cy) * (1 + k * r2)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_barrel_distortion(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k1, k2 = 0.3, 0.1
        for i in range(h):
            for j in range(w):
                x = (j - cx) / cx
                y = (i - cy) / cy
                r2 = x*x + y*y
                r4 = r2 * r2
                x_new = x * (1 + k1*r2 + k2*r4)
                y_new = y * (1 + k1*r2 + k2*r4)
                map_x[i, j] = x_new * cx + cx
                map_y[i, j] = y_new * cy + cy
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_ultra_wide(self, frame):
        h, w = frame.shape[:2]
        scale = 0.5
        new_w = int(w * scale)
        new_h = int(h * scale)
        small = cv2.resize(frame, (new_w, new_h))
        result = cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)
        return result

    def apply_macro_vr(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        roi_size = min(w, h) // 3
        x1 = max(0, cx - roi_size)
        y1 = max(0, cy - roi_size)
        x2 = min(w, cx + roi_size)
        y2 = min(h, cy + roi_size)
        roi = frame[y1:y2, x1:x2]
        roi = cv2.resize(roi, (w, h))
        overlay = roi.copy()
        cv2.circle(overlay, (cx, cy), roi_size, (0, 0, 0), -1)
        mask = np.zeros((h, w, 3), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                dist = math.sqrt((j - cx)**2 + (i - cy)**2)
                if dist < roi_size:
                    mask[i, j] = [1.0, 1.0, 1.0]
                else:
                    fade = max(0, 1 - (dist - roi_size) / (roi_size * 0.5))
                    mask[i, j] = [fade, fade, fade]
        result = (frame * (1 - mask) + roi * mask).astype(np.uint8)
        vignette = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                dist = math.sqrt((j - cx)**2 + (i - cy)**2) / (max(w, h) * 0.5)
                vignette[i, j] = max(0, 1 - dist * 1.5)
        result = (result * vignette[:, :, np.newaxis]).astype(np.uint8)
        return result

    def apply_telephoto_compression(self, frame):
        h, w = frame.shape[:2]
        center_crop = frame[h//4:3*h//4, w//4:3*w//4]
        return cv2.resize(center_crop, (w, h))

    def apply_panoramic_stitch(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//3]
        center = frame[:, w//3:2*w//3]
        right = frame[:, 2*w//3:]
        blended1 = cv2.addWeighted(left, 0.5, center, 0.5, 0)
        blended2 = cv2.addWeighted(center, 0.5, right, 0.5, 0)
        return cv2.hconcat([blended1, frame[:, w//3:2*w//3], blended2])

    def apply_spherical_lens(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k = 0.8
        for i in range(h):
            for j in range(w):
                r2 = ((j - cx)**2 + (i - cy)**2) / (cx**2 + cy**2)
                r2 = min(r2, 1.0)
                map_x[i, j] = cx + (j - cx) * math.sqrt(1 + k * r2)
                map_y[i, j] = cy + (i - cy) * math.sqrt(1 + k * r2)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_dome_lens(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        output = np.zeros_like(frame)
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                dist = math.sqrt(dx*dx + dy*dy)
                max_dist = math.sqrt(cx*cx + cy*cy)
                if dist < max_dist:
                    theta = math.atan2(dy, dx)
                    r = (dist / max_dist) ** 0.7
                    sx = int((cx + r * cx * math.cos(theta)) % w)
                    sy = int((cy + r * cy * math.sin(theta)) % h)
                    output[i, j] = frame[sy, sx]
        return output

    def apply_curved_lens(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w / 2, h / 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k = 0.4
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                r2 = (dx*dx + dy*dy) / (cx*cx + cy*cy)
                map_x[i, j] = cx + dx * (1 - k * r2)
                map_y[i, j] = cy + dy * (1 - k * r2)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_anamorphic_vr(self, frame):
        h, w = frame.shape[:2]
        stretched = cv2.resize(frame, (int(w * 1.5), h))
        x_off = (stretched.shape[1] - w) // 2
        return stretched[:, x_off:x_off + w]

    def apply_tilt_shift_vr(self, frame):
        h, w = frame.shape[:2]
        center_y = h // 2
        blur_radius = 21
        output = frame.copy()
        for i in range(h):
            dist = abs(i - center_y) / (h / 2)
            if dist > 0.3:
                k_size = int(blur_radius * min(dist * 2, 1))
                if k_size % 2 == 0:
                    k_size += 1
                row = frame[max(0, i-2):min(h, i+3), :]
                blurred_row = cv2.GaussianBlur(row, (k_size, k_size), 0)
                output[i, :] = blurred_row[len(row)//2]
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_lens_flare_vr(self, frame):
        overlay = frame.copy()
        h, w = frame.shape[:2]
        cx = w // 2 + int(100 * math.sin(self.time * 0.02))
        cy = h // 3
        for r in range(80, 10, -5):
            alpha = 0.1 * (r / 80)
            color = (0, int(255 * (r / 80)), int(255 * (r / 80)))
            cv2.circle(overlay, (cx, cy), r, color, -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        for i in range(5):
            x = int(cx + 150 * math.cos(i * 0.8 + self.time * 0.01))
            y = int(cy + 100 * math.sin(i * 0.8 + self.time * 0.01))
            cv2.circle(frame, (x, y), 5, (0, 200, 255), -1)
        return frame

    def apply_prism_lens(self, frame):
        h, w = frame.shape[:2]
        third = w // 3
        part1 = frame[:, :third]
        part2 = frame[:, third:2*third]
        part3 = frame[:, 2*third:]
        output = np.zeros_like(frame)
        output[:, :third] = part3
        output[:, third:2*third] = part1
        output[:, 2*third:] = part2
        return output

    def apply_kaleidoscope_lens(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        size = min(w, h) // 2
        roi = frame[cy-size:cy+size, cx-size:cx+size]
        if roi.shape[0] == 0 or roi.shape[1] == 0:
            return frame
        mirror1 = cv2.flip(roi, 1)
        mirror2 = cv2.flip(roi, 0)
        mirror3 = cv2.flip(roi, -1)
        combined = np.zeros_like(frame)
        half = size
        combined[cy-half:cy+half, cx-half:cx+half] = roi
        combined[cy-half:cy+half, cx-half:cx] = mirror1[:, :half]
        combined[cy-half:cy, cx-half:cx+half] = mirror2[:half, :]
        combined[cy:cy+half, cx:cx+half] = mirror3
        return combined

    def apply_crystal_lens(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        edges = cv2.Canny(frame, 50, 150)
        edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=2)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
        if lines is not None:
            for line in lines[:20]:
                x1, y1, x2, y2 = line[0]
                cv2.line(overlay, (x1, y1), (x2, y2), (255, 200, 100), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_glass_refraction(self, frame):
        h, w = frame.shape[:2]
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                map_x[i, j] = j + 10 * math.sin(i / 20 + self.time * 0.05)
                map_y[i, j] = i + 10 * math.cos(j / 20 + self.time * 0.05)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)


# --- B. Immersive / 360° ---

    def apply_360_street_view(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        gradient = np.linspace(0, 1, w).reshape(1, w)
        gradient = np.tile(gradient, (h, 1))
        overlay = np.zeros_like(frame, dtype=np.float32)
        overlay[:, :, 0] = gradient * 50
        overlay[:, :, 1] = gradient * 30
        overlay[:, :, 2] = 20
        return cv2.addWeighted(frame.astype(np.float32), 0.85, overlay, 0.15, 0).astype(np.uint8)

    def apply_360_drone_view(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for angle in range(0, 360, 30):
            rad = math.radians(angle + self.time)
            x = int(cx + 200 * math.cos(rad))
            y = int(cy + 100 * math.sin(rad))
            cv2.arrowedLine(output, (cx, cy), (x, y), (0, 255, 255), 2)
        cv2.circle(output, (cx, cy), 5, (0, 255, 0), -1)
        return output

    def apply_360_rooftop_view(self, frame):
        h, w = frame.shape[:2]
        sky = np.zeros_like(frame)
        sky[:h//3] = [180, 120, 60]
        sky[h//3:2*h//3] = [200, 160, 100]
        sky[2*h//3:] = [100, 80, 60]
        return cv2.addWeighted(frame, 0.7, sky, 0.3, 0)

    def apply_360_stadium_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for y in range(0, h, 40):
            cv2.line(overlay, (0, y), (w, y), (255, 255, 255), 1)
        for x in range(0, w, 40):
            cv2.line(overlay, (x, 0), (x, h), (255, 255, 255), 1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        cv2.putText(frame, "STADIUM 360", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        return frame

    def apply_360_concert_view(self, frame):
        h, w = frame.shape[:2]
        for _ in range(5):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.randint(20, 80)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.circle(frame, (x, y), r, color, 2)
        return frame

    def apply_360_classroom_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, h-100), (w-50, h-50), (100, 60, 20), 3)
        cv2.rectangle(overlay, (100, 50), (w-100, h-150), (50, 50, 50), 2)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_360_museum_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(3):
            x = 100 + i * (w - 200) // 2
            cv2.rectangle(overlay, (x, 50), (x + 150, h - 100), (80, 80, 80), 3)
            cv2.rectangle(overlay, (x + 20, 70), (x + 130, h - 120), (120, 100, 60), 2)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_360_city_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(10):
            x = i * w // 10
            bh = random.randint(h // 4, h // 2)
            bw = w // 15
            cv2.rectangle(overlay, (x, h - bh), (x + bw, h), (60, 60, 80), -1)
            cv2.rectangle(overlay, (x, h - bh), (x + bw, h), (80, 80, 100), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_360_forest_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(8):
            x = i * w // 8 + random.randint(-20, 20)
            tree_h = random.randint(h // 3, h // 2)
            cv2.line(overlay, (x, h), (x, h - tree_h), (40, 80, 20), 8)
            cv2.circle(overlay, (x, h - tree_h), 40, (30, 120, 30), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_360_beach_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h - h // 4), (w, h), (60, 180, 220), -1)
        cv2.rectangle(overlay, (0, h - h // 3), (w, h - h // 4), (194, 178, 128), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_360_mountain_view(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        pts = np.array([[0, h], [w//3, h//3], [2*w//3, h//2], [w, h]], np.int32)
        cv2.fillPoly(overlay, [pts], (100, 100, 120))
        pts2 = np.array([[w//4, h], [w//2, h//4], [3*w//4, h]], np.int32)
        cv2.fillPoly(overlay, [pts2], (80, 90, 100))
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_360_space_view(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        output[:] = [10, 5, 20]
        for _ in range(200):
            x = random.randint(0, w)
            y = random.randint(0, h)
            brightness = random.randint(150, 255)
            cv2.circle(output, (x, y), random.randint(1, 2), (brightness, brightness, brightness), -1)
        return output

    def apply_360_underwater_view(self, frame):
        h, w = frame.shape[:2]
        overlay = np.zeros_like(frame, dtype=np.float32)
        for i in range(h):
            blue = int(150 + 50 * (i / h))
            green = int(100 + 30 * (i / h))
            overlay[i, :] = [min(255, blue), min(255, green), 50]
        result = cv2.addWeighted(frame.astype(np.float32), 0.6, overlay, 0.4, 0).astype(np.uint8)
        for _ in range(10):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(result, (x, y), random.randint(20, 50), (255, 200, 100), 1)
        return result

    def apply_360_night_view(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = (hsv[:, :, 2] * 0.3).astype(np.uint8)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        h, w = frame.shape[:2]
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h // 2)
            cv2.circle(frame, (x, y), random.randint(1, 2), (200, 200, 255), -1)
        return frame

    def apply_360_time_freeze(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.putText(overlay, "TIME FROZEN", (w//4, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        for i in range(0, w, 30):
            cv2.line(frame, (i, 0), (i, h), (100, 200, 255), 1)
        return frame

    def apply_360_mirror_world(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(left, 1)
        return np.hstack([left, right])

    def apply_360_infinite_room(self, frame):
        h, w = frame.shape[:2]
        scale = 0.7
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        x_off = (w - small.shape[1]) // 2
        y_off = (h - small.shape[0]) // 2
        output = frame.copy()
        output[y_off:y_off + small.shape[0], x_off:x_off + small.shape[1]] = small
        cv2.rectangle(output, (x_off, y_off), (x_off + small.shape[1], y_off + small.shape[0]), (255, 255, 255), 2)
        return output

    def apply_360_portal_room(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        for r in range(150, 10, -5):
            color = (int(255 * (r / 150)), 0, int(255 * (1 - r / 150)))
            cv2.circle(overlay, (cx, cy), r, color, 2)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_360_floating_island(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        pts = np.array([[w//4, h//2], [w//3, h//3], [2*w//3, h//3], [3*w//4, h//2], [2*w//3, h//2+50], [w//3, h//2+50]], np.int32)
        cv2.fillPoly(overlay, [pts], (100, 80, 60))
        cv2.circle(overlay, (w//2, h//3 - 30), 40, (50, 150, 50), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_360_miniature_world(self, frame):
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 3, h // 3))
        small = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        overlay = small.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (100, 80, 60), 10)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        return small


# --- C. Dunia Fantasi ---

    def apply_portal_effect(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        for r in range(120, 10, -3):
            hue = (r * 2 + self.time * 5) % 180
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(overlay, (cx, cy), r, color_bgr.tolist(), 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_magic_door(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        door_w = w // 3
        door_h = int(h * 0.7)
        x1 = (w - door_w) // 2
        y1 = h - door_h
        cv2.rectangle(overlay, (x1, y1), (x1 + door_w, h), (80, 50, 20), -1)
        cv2.rectangle(overlay, (x1 + 10, y1 + 10), (x1 + door_w - 10, h - 10), (120, 80, 40), -1)
        cv2.circle(overlay, (x1 + door_w - 30, y1 + door_h // 2), 8, (200, 180, 0), -1)
        glow = np.zeros_like(frame, dtype=np.float32)
        glow[y1:y1+door_h, x1:x1+door_w] = [0, 100, 200]
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        cv2.addWeighted(frame.astype(np.float32), 0.8, glow, 0.2, 0, frame)
        return frame

    def apply_mirror_portal(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = frame[:, w//2:]
        right_mirror = cv2.flip(right, 1)
        output = np.hstack([left, right_mirror])
        overlay = output.copy()
        cv2.line(overlay, (w//2, 0), (w//2, h), (200, 200, 255), 3)
        cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)
        return output

    def apply_galaxy_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for _ in range(300):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(20, min(w, h) // 2 - 20)
            x = int(cx + dist * math.cos(angle))
            y = int(cy + dist * math.sin(angle))
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        for r in range(100, 10, -5):
            alpha = 0.3 * (r / 100)
            cv2.circle(output, (cx, cy), r, (80, 20, 120), 2)
        return output

    def apply_time_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        for i in range(12):
            angle = (i * 30 + self.time * 2) * math.pi / 180
            x = int(cx + 100 * math.cos(angle))
            y = int(cy + 100 * math.sin(angle))
            cv2.circle(overlay, (x, y), 15, (255, 200, 0), -1)
            cv2.putText(overlay, str(i + 1), (x - 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_dimension_rift(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(5):
            y = (h // 6) * (i + 1)
            shift = int(20 * math.sin(self.time * 0.1 + i))
            overlay[y-2:y+2, :] = np.roll(frame[y-2:y+2, :], shift, axis=1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        return frame

    def apply_black_hole(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for r in range(min(w, h) // 2, 10, -2):
            angle = self.time * 0.05 + r * 0.1
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            color_val = int(50 + 100 * (r / (min(w, h) // 2)))
            cv2.circle(output, (x, y), 3, (color_val, color_val // 2, 0), -1)
        cv2.circle(output, (cx, cy), 20, (0, 0, 0), -1)
        cv2.circle(output, (cx, cy), 22, (0, 0, 255), 2)
        return output

    def apply_wormhole(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for r in range(5, min(w, h) // 2, 8):
            angle = self.time * 0.1 + r * 0.05
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            size = max(1, 5 - r // 50)
            cv2.circle(output, (x, y), size, (255, 255, 0), -1)
        return output

    def apply_cyber_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        for r in range(80, 10, -2):
            color = (0, int(255 * (1 - r / 80)), int(255 * (r / 80)))
            cv2.rectangle(overlay, (cx - r, cy - r), (cx + r, cy + r), color, 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_neon_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0)]
        for i, r in enumerate(range(100, 10, -15)):
            color = colors[i % len(colors)]
            cv2.circle(overlay, (cx, cy), r, color, 3)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_fire_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(50):
            x = random.randint(w//3, 2*w//3)
            y = random.randint(h//3, h)
            size = random.randint(5, 20)
            cv2.circle(overlay, (x, y), size, (0, 100, 255), -1)
            cv2.circle(overlay, (x, y - 5), size - 3, (0, 150, 255), -1)
            cv2.circle(overlay, (x, y - 10), size - 6, (0, 200, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_ice_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(10, 40)
            cv2.circle(overlay, (x, y), size, (255, 200, 150), 2)
            for j in range(6):
                angle = j * 60 * math.pi / 180
                x2 = int(x + size * math.cos(angle))
                y2 = int(y + size * math.sin(angle))
                cv2.line(overlay, (x, y), (x2, y2), (200, 230, 255), 1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_water_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = np.zeros_like(frame, dtype=np.float32)
        for i in range(h):
            wave = int(10 * math.sin(i / 20 + self.time * 0.1))
            overlay[i, :] = [200, 150, 50]
        result = cv2.addWeighted(frame.astype(np.float32), 0.6, overlay, 0.4, 0).astype(np.uint8)
        return result

    def apply_lightning_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(3):
            x = random.randint(w//3, 2*w//3)
            points = [(x, 0)]
            y = 0
            while y < h:
                y += random.randint(10, 30)
                x += random.randint(-20, 20)
                points.append((x, min(y, h)))
            pts = np.array(points, np.int32)
            cv2.polylines(overlay, [pts], False, (255, 255, 0), 2)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_cloud_portal(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(15):
            x = random.randint(0, w)
            y = random.randint(0, h // 2)
            axes = (random.randint(40, 100), random.randint(20, 50))
            cv2.ellipse(overlay, (x, y), axes, 0, 0, 360, (200, 200, 220), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_crystal_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        for i in range(6):
            angle = i * 60 * math.pi / 180 + self.time * 0.02
            pts = []
            for t in range(3):
                a = angle + t * 2 * math.pi / 3
                pts.append([int(cx + 60 * math.cos(a)), int(cy + 60 * math.sin(a))])
            cv2.fillPoly(overlay, [np.array(pts, np.int32)], (200, 150, 255))
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_ancient_portal(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        cv2.circle(overlay, (cx, cy), 100, (100, 80, 50), 8)
        cv2.circle(overlay, (cx, cy), 90, (80, 60, 30), 3)
        for i in range(8):
            angle = i * 45 * math.pi / 180
            x = int(cx + 85 * math.cos(angle))
            y = int(cy + 85 * math.sin(angle))
            cv2.circle(overlay, (x, y), 8, (120, 100, 60), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_fantasy_gate(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        overlay = frame.copy()
        pts = np.array([[cx - 80, cy + 100], [cx - 60, cy - 80], [cx + 60, cy - 80], [cx + 80, cy + 100]], np.int32)
        cv2.fillPoly(overlay, [pts], (60, 40, 100))
        inner = np.array([[cx - 60, cy + 80], [cx - 45, cy - 60], [cx + 45, cy - 60], [cx + 60, cy + 80]], np.int32)
        cv2.fillPoly(overlay, [inner], (100, 50, 150))
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def apply_floating_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(5):
            x = random.randint(50, w - 50)
            y = random.randint(50, h - 50)
            size = random.randint(20, 60)
            offset_y = int(10 * math.sin(self.time * 0.05 + x))
            cv2.circle(output, (x, y + offset_y), size, (100, 200, 100), -1)
            cv2.circle(output, (x, y + offset_y), size, (150, 255, 150), 2)
        return output

    def apply_parallel_universe(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2].copy()
        right = frame[:, w//2:].copy()
        left_hsv = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)
        left_hsv[:, :, 0] = (left_hsv[:, :, 0] + 40) % 180
        left = cv2.cvtColor(left_hsv, cv2.COLOR_HSV2BGR)
        return np.hstack([left, right])


# --- D. Visual Viral ---

    def apply_clone_viral(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(3):
            x_offset = (i - 1) * w // 4
            roi = frame[:, max(0, w//4 + x_offset):min(w, 3*w//4 + x_offset)]
            if roi.shape[1] > 0:
                scale = 0.4
                small = cv2.resize(roi, (int(roi.shape[1] * scale), int(roi.shape[0] * scale)))
                x_pos = w // 4 + x_offset
                y_pos = h // 4
                if x_pos >= 0 and x_pos + small.shape[1] <= w and y_pos + small.shape[0] <= h:
                    output[y_pos:y_pos + small.shape[0], x_pos:x_pos + small.shape[1]] = small
        return output

    def apply_multiple_self(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        positions = [(0, 0), (w//3, 0), (2*w//3, 0), (0, h//3), (w//3, h//3), (2*w//3, h//3)]
        for px, py in positions:
            small = cv2.resize(frame, (w//3, h//3))
            output[py:py + h//3, px:px + w//3] = small
        return output

    def apply_giant_person(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        center_crop = frame[h//4:3*h//4, w//4:3*w//4]
        giant = cv2.resize(center_crop, (w, h))
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w//2, h//2), min(w, h) // 3, 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        mask_3ch = cv2.merge([mask, mask, mask]).astype(np.float32) / 255.0
        output = (giant * mask_3ch + frame * (1 - mask_3ch)).astype(np.uint8)
        return output

    def apply_mini_person(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        mini = cv2.resize(frame, (w // 4, h // 4))
        x, y = w // 2 - w // 8, h // 2 - h // 8
        output[y:y + h//4, x:x + w//4] = mini
        cv2.rectangle(output, (x - 2, y - 2), (x + w//4 + 2, y + h//4 + 2), (255, 255, 255), 2)
        return output

    def apply_giant_room(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scale = 2
        big = cv2.resize(frame, (w * scale, h * scale))
        x = (big.shape[1] - w) // 2
        y = (big.shape[0] - h) // 2
        output = big[y:y+h, x:x+w]
        return output

    def apply_tiny_room(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scale = 0.3
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        x = (w - small.shape[1]) // 2
        y = (h - small.shape[0]) // 2
        output[:] = (30, 30, 40)
        output[y:y+small.shape[0], x:x+small.shape[1]] = small
        cv2.rectangle(output, (x - 5, y - 5), (x + small.shape[1] + 5, y + small.shape[0] + 5), (100, 100, 150), 2)
        return output

    def apply_gravity_flip_viral(self, frame):
        return cv2.flip(frame, 0)

    def apply_upside_down_world(self, frame):
        flipped = cv2.flip(frame, 0)
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        output[:h//2] = frame[:h//2]
        output[h//2:] = flipped[h//2:]
        return output

    def apply_infinite_mirror_viral(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(5):
            scale = 1 - i * 0.15
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
            cv2.rectangle(output, (x, y), (x + small.shape[1], y + small.shape[0]), (150, 150, 200), 1)
        return output

    def apply_mirror_clone_viral(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(left, 1)
        return np.hstack([left, right])

    def apply_reflection_world(self, frame):
        h, w = frame.shape[:2]
        top = frame[:h//2, :]
        bottom = cv2.flip(top, 0)
        output = np.vstack([top, bottom])
        return output

    def apply_invisible_wall(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.line(overlay, (w//2, 0), (w//2, h), (200, 200, 255), 5)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_invisible_person(self, frame):
        h, w = frame.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        cx, cy = w // 2, h // 2
        cv2.ellipse(mask, (cx, cy - 30), (50, 80), 0, 0, 360, 255, -1)
        cv2.ellipse(mask, (cx, cy + 80), (70, 100), 0, 0, 360, 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        bg = np.zeros_like(frame)
        bg[:] = (30, 30, 40)
        mask_3ch = cv2.merge([mask, mask, mask]).astype(np.float32) / 255.0
        output = (frame * mask_3ch + bg * (1 - mask_3ch)).astype(np.uint8)
        return output

    def apply_floating_object(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(5):
            x = random.randint(50, w - 50)
            y = random.randint(50, h - 50)
            offset_y = int(15 * math.sin(self.time * 0.08 + x * 0.01))
            cv2.circle(output, (x, y + offset_y), 15, (100, 200, 255), -1)
            cv2.circle(output, (x, y + offset_y + 20), 5, (0, 0, 0), -1)
        return output

    def apply_levitation(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        center = frame[h//4:3*h//4, w//4:3*w//4]
        small = cv2.resize(center, (w//2, h//2))
        y_offset = int(20 * math.sin(self.time * 0.05))
        y_pos = h//4 + y_offset
        if y_pos >= 0 and y_pos + small.shape[0] <= h:
            output[y_pos:y_pos + small.shape[0], w//4:w//4 + small.shape[1]] = small
        return output

    def apply_object_explosion(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(20):
            x = random.randint(w//3, 2*w//3)
            y = random.randint(h//3, 2*h//3)
            vx = random.randint(-10, 10)
            vy = random.randint(-10, 10)
            size = random.randint(5, 15)
            cv2.circle(output, (x + vx * 5, y + vy * 5), size, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), -1)
        return output

    def apply_object_disintegration(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(0, h, 3):
            for j in range(0, w, 3):
                if random.random() < 0.1:
                    output[i:i+3, j:j+3] = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
        return output

    def apply_particle_body(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(100):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, 3*h//4)
            size = random.randint(2, 6)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.circle(output, (x, y), size, color, -1)
        return output

    def apply_hologram_body(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 3):
            alpha = 0.7 + 0.3 * math.sin(y / 10 + self.time * 0.1)
            output[y:y+1, :] = (frame[y:y+1, :] * alpha).astype(np.uint8)
        return output

    def apply_transparent_body(self, frame):
        h, w = frame.shape[:2]
        bg = np.zeros_like(frame)
        bg[:] = (40, 40, 50)
        alpha = 0.3
        return cv2.addWeighted(frame, alpha, bg, 1 - alpha, 0)


# --- E. Cinematic / Stylized ---

    def apply_cyberpunk_vr(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + 20) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        h, w = frame.shape[:2]
        for y in range(0, h, 4):
            if random.random() < 0.3:
                x = random.randint(0, w)
                length = random.randint(20, 80)
                cv2.line(frame, (x, y), (x + length, y), (255, 0, 100), 1)
        return frame

    def apply_futuristic_city(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(15):
            x = i * w // 15
            bh = random.randint(h // 3, h // 2)
            bw = w // 20
            cv2.rectangle(overlay, (x, h - bh), (x + bw, h), (30, 30, 60), -1)
            for j in range(3):
                wx = x + random.randint(5, bw - 10)
                wy = h - bh + random.randint(10, bh - 20)
                cv2.rectangle(overlay, (wx, wy), (wx + 5, wy + 5), (0, 200, 255), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_neon_night(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = (hsv[:, :, 2] * 0.4).astype(np.uint8)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        h, w = frame.shape[:2]
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = (random.randint(150, 255), random.randint(0, 100), random.randint(150, 255))
            cv2.circle(frame, (x, y), random.randint(3, 10), color, -1)
        return frame

    def apply_matrix_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        output[:] = [10, 20, 5]
        for x in range(0, w, 15):
            for y in range(0, h, 20):
                char = chr(random.randint(33, 126))
                cv2.putText(output, char, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        alpha = 0.7
        output = cv2.addWeighted(output, 1 - alpha, frame, alpha, 0)
        return output

    def apply_scifi_laboratory(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (w-20, h-20), (50, 50, 80), 2)
        for i in range(5):
            y = 50 + i * (h - 100) // 5
            cv2.line(overlay, (30, y), (w-30, y), (0, 100, 150), 1)
            cv2.rectangle(overlay, (30, y-5), (100, y+5), (0, 200, 255), -1)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_digital_grid(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for x in range(0, w, 40):
            cv2.line(overlay, (x, 0), (x, h), (0, 255, 255), 1)
        for y in range(0, h, 40):
            cv2.line(overlay, (0, y), (w, y), (0, 255, 255), 1)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_holographic_city(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(10):
            x = i * w // 10
            bh = random.randint(h // 4, h // 2)
            pts = np.array([[x, h], [x + 20, h - bh], [x + 40, h]], np.int32)
            cv2.fillPoly(overlay, [pts], (100, 150, 200))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_vr_room(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, 50), (w-50, h-50), (40, 40, 60), 3)
        for i in range(4):
            x = 50 + i * (w-100) // 4
            cv2.line(overlay, (x, 50), (x, h-50), (60, 60, 80), 1)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_metaverse_world(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(10):
            x = random.randint(50, w-50)
            y = random.randint(50, h-50)
            size = random.randint(20, 50)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.circle(overlay, (x, y), size, color, 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_dream_world(self, frame):
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_surreal_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(5):
            y = h // 6 * (i + 1)
            shift = int(30 * math.sin(self.time * 0.05 + i))
            output[y-2:y+2, :] = np.roll(frame[y-2:y+2, :], shift, axis=1)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + 30) % 180
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_anime_vr(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
        colorful = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return cv2.bitwise_and(colorful, edges)

    def apply_cartoon_vr(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)

    def apply_game_world(self, frame):
        small = cv2.resize(frame, (frame.shape[1] // 4, frame.shape[0] // 4), interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    def apply_pixel_world(self, frame):
        pixel_size = 8
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_lowpoly_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        triangle_size = 30
        for y in range(0, h - triangle_size, triangle_size):
            for x in range(0, w - triangle_size, triangle_size):
                color = frame[y + triangle_size // 2, x + triangle_size // 2].tolist()
                pts = np.array([
                    [x, y],
                    [x + triangle_size, y],
                    [x + triangle_size // 2, y + triangle_size]
                ], np.int32)
                cv2.fillPoly(output, [pts], color)
        return output

    def apply_glass_world(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        edges = cv2.Canny(frame, 30, 100)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        mask = edges > 0
        overlay[mask] = (200, 220, 255)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_liquid_world(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(15 * math.sin(i / 15 + self.time * 0.08))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return output

    def apply_cloud_world(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for _ in range(20):
            x = random.randint(0, w)
            y = random.randint(0, h)
            axes = (random.randint(30, 80), random.randint(15, 40))
            cv2.ellipse(overlay, (x, y), axes, 0, 0, 360, (220, 220, 240), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_ultimate_immersive_vr(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for r in range(min(w, h) // 2, 10, -3):
            angle = self.time * 0.05 + r * 0.02
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            color = (int(128 + 127 * math.sin(angle)), int(128 + 127 * math.cos(angle)), int(128 + 127 * math.sin(angle + 1)))
            cv2.circle(output, (x, y), 3, color, -1)
        return output


# --- Camera Movement (untuk video) ---

    def apply_360_orbit(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        angle = self.time * 0.03
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                r = math.sqrt(dx*dx + dy*dy)
                theta = math.atan2(dy, dx) + angle
                map_x[i, j] = cx + r * math.cos(theta)
                map_y[i, j] = cy + r * math.sin(theta)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)

    def apply_360_spin(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        angle = self.time * 0.1
        M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_drone_flyover(self, frame):
        h, w = frame.shape[:2]
        scale = 1.0 + 0.3 * math.sin(self.time * 0.02)
        M = np.float32([[scale, 0, w*(1-scale)/2], [0, scale, h*(1-scale)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_fpv_fly_through(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.5 * (1 - math.cos(self.time * 0.03)) / 2
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_one_take_orbit(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        angle = self.time * 0.02
        offset_x = int(50 * math.cos(angle))
        offset_y = int(50 * math.sin(angle))
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_camera_dive(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.5 * (self.time % 100) / 100
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, 0]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_camera_rise(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.3 * (self.time % 100) / 100
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_camera_drop(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.3 * (self.time % 100) / 100
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, 0]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_camera_roll(self, frame):
        h, w = frame.shape[:2]
        angle = self.time * 0.5
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_camera_barrel_roll(self, frame):
        h, w = frame.shape[:2]
        angle = (self.time * 2) % 360
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_hyper_zoom(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 2.0 * (1 - math.cos(self.time * 0.05)) / 2
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_crash_zoom(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 3.0 * max(0, math.sin(self.time * 0.1))
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        result = cv2.warpAffine(frame, M, (w, h))
        return result

    def apply_slow_push_in(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.1 * math.sin(self.time * 0.01)
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_fast_push_in(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.5 * math.sin(self.time * 0.05)
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_pull_out_reveal(self, frame):
        h, w = frame.shape[:2]
        zoom = 2.0 - 1.0 * min(1, (self.time % 200) / 200)
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_whip_pan(self, frame):
        h, w = frame.shape[:2]
        shift = int(100 * math.sin(self.time * 0.2))
        output = np.roll(frame, shift, axis=1)
        return output

    def apply_dutch_angle(self, frame):
        h, w = frame.shape[:2]
        angle = 15 * math.sin(self.time * 0.02)
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_spiral_camera(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        angle = self.time * 0.05
        radius = 30 * math.sin(self.time * 0.02)
        offset_x = int(radius * math.cos(angle))
        offset_y = int(radius * math.sin(angle))
        M = cv2.getRotationMatrix2D((cx + offset_x, cy + offset_y), self.time * 0.3, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_circular_dolly(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        angle = self.time * 0.03
        offset_x = int(80 * math.cos(angle))
        offset_y = int(40 * math.sin(angle))
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                map_x[i, j] = j - offset_x * (i / h)
                map_y[i, j] = i - offset_y * (j / w)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_infinite_zoom(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0
        output = frame.copy()
        for _ in range(5):
            zoom *= 1.3
            small = cv2.resize(output, (int(w / zoom), int(h / zoom)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
        return output


# --- Teleport & Transition ---

    def apply_portal_teleport(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        progress = (self.time % 100) / 100
        radius = int(min(w, h) * progress)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (cx, cy), radius, 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        glow = np.zeros_like(frame, dtype=np.float32)
        glow[:] = [200, 100, 0]
        mask_f = mask.astype(np.float32) / 255.0
        output = (frame * (1 - mask_f[:, :, np.newaxis]) + glow * mask_f[:, :, np.newaxis]).astype(np.uint8)
        return output

    def apply_door_teleport(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        door_w = int(w * 0.4 * min(1, (self.time % 100) / 50))
        door_h = int(h * 0.7)
        x1 = (w - door_w) // 2
        y1 = (h - door_h) // 2
        cv2.rectangle(output, (x1, y1), (x1 + door_w, y1 + door_h), (0, 150, 255), -1)
        cv2.rectangle(output, (x1, y1), (x1 + door_w, y1 + door_h), (0, 200, 255), 3)
        return output

    def apply_mirror_teleport(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        split = int(w * progress)
        output = frame.copy()
        output[:, split:w] = cv2.flip(frame[:, split:w], 1)
        cv2.line(output, (split, 0), (split, h), (200, 200, 255), 3)
        return output

    def apply_wall_teleport(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        wall_x = int(w * progress)
        cv2.line(output, (wall_x, 0), (wall_x, h), (100, 200, 255), 5)
        for y in range(0, h, 20):
            offset = int(20 * math.sin(y / 20 + self.time * 0.1))
            if wall_x + offset < w and wall_x + offset >= 0:
                cv2.line(output, (wall_x, y), (wall_x + offset, y), (150, 200, 255), 2)
        return output

    def apply_ground_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h - 50
        progress = min(1, (self.time % 100) / 100)
        for r in range(int(100 * progress), 0, -5):
            color = (int(100 + 155 * (r / 100)), 0, int(200 * (1 - r / 100)))
            cv2.ellipse(output, (cx, cy), (r, r // 3), 0, 0, 360, color, 2)
        return output

    def apply_sky_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, 50
        progress = min(1, (self.time % 100) / 100)
        for r in range(int(120 * progress), 0, -5):
            color = (int(200 * (r / 120)), int(100 * (r / 120)), 255)
            cv2.circle(output, (cx, cy), r, color, 2)
        return output

    def apply_galaxy_portal_v(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for _ in range(int(200 * min(1, (self.time % 100) / 100))):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(10, 100)
            x = int(cx + dist * math.cos(angle))
            y = int(cy + dist * math.sin(angle))
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_time_portal_v(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        for i in range(int(12 * progress)):
            angle = (i * 30 + self.time * 3) * math.pi / 180
            x = int(cx + 80 * math.cos(angle))
            y = int(cy + 80 * math.sin(angle))
            cv2.circle(output, (x, y), 10, (255, 200, 0), -1)
        return output

    def apply_dimension_jump(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 60) / 60)
        shift = int(100 * math.sin(progress * math.pi))
        output = np.roll(frame, shift, axis=1)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + int(30 * progress)) % 180
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_reality_glitch_v(self, frame):
        output = frame.copy()
        num_slices = random.randint(3, 8)
        for _ in range(num_slices):
            y = random.randint(0, frame.shape[0] - 20)
            h_slice = random.randint(5, 20)
            shift = random.randint(-30, 30)
            output[y:y+h_slice] = np.roll(frame[y:y+h_slice], shift, axis=1)
        if random.random() < 0.3:
            b, g, r = cv2.split(output)
            shift = random.randint(-10, 10)
            b = np.roll(b, shift, axis=1)
            output = cv2.merge([b, g, r])
        return output

    def apply_blink_transition(self, frame):
        h, w = frame.shape[:2]
        progress = (self.time % 60) / 60
        if progress < 0.5:
            brightness = 1.0 - progress * 2
        else:
            brightness = (progress - 0.5) * 2
        return (frame * brightness).astype(np.uint8)

    def apply_flash_transition(self, frame):
        h, w = frame.shape[:2]
        progress = (self.time % 40) / 40
        white = np.ones_like(frame, dtype=np.float32) * 255
        alpha = max(0, 1 - progress * 3)
        return cv2.addWeighted(frame.astype(np.float32), 1 - alpha, white, alpha, 0).astype(np.uint8)

    def apply_smoke_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        for _ in range(int(50 * progress)):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(20, 60)
            cv2.circle(output, (x, y), size, (100, 100, 100), -1)
        return output

    def apply_fire_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 60) / 60)
        flame_h = int(h * progress)
        for y in range(h - flame_h, h):
            for x in range(0, w, 5):
                offset = int(10 * math.sin(x / 10 + self.time * 0.2))
                color = (0, int(100 + 155 * ((y - (h - flame_h)) / flame_h)), int(200 * ((y - (h - flame_h)) / flame_h)))
                cv2.circle(output, (x + offset, y), 3, color, -1)
        return output

    def apply_water_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        water_level = int(h * progress)
        overlay = output[:water_level, :].copy()
        hsv = cv2.cvtColor(overlay, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 100
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        output[:water_level] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return output

    def apply_lightning_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        if random.random() < 0.1:
            output[:] = (255, 255, 255)
        return output

    def apply_glass_shatter_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 60) / 60)
        num_cracks = int(20 * progress)
        for _ in range(num_cracks):
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            x2 = x1 + random.randint(-100, 100)
            y2 = y1 + random.randint(-100, 100)
            cv2.line(output, (x1, y1), (x2, y2), (200, 220, 255), 2)
        return output

    def apply_pixel_transition(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 80) / 80)
        pixel_size = max(1, int(30 * (1 - progress)))
        small = cv2.resize(frame, (w // pixel_size, h // pixel_size))
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_digital_scan_transition(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scan_y = int(h * ((self.time % 100) / 100))
        cv2.line(output, (0, scan_y), (w, scan_y), (0, 255, 0), 3)
        for y in range(max(0, scan_y - 50), scan_y):
            alpha = (y - (scan_y - 50)) / 50
            output[y, :] = (frame[y, :] * (1 - alpha) + np.array([0, 255, 0]) * alpha).astype(np.uint8)
        return output

    def apply_black_hole_transition(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        max_r = int(min(w, h) * 0.4 * progress)
        cv2.circle(output, (cx, cy), max_r, (0, 0, 0), -1)
        cv2.circle(output, (cx, cy), max_r + 5, (0, 0, 255), 3)
        return output


# --- Reality-Bending ---

    def apply_gravity_reverse(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(10 * math.sin(i / 30 + self.time * 0.05))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return cv2.flip(output, 0)

    def apply_gravity_zero(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            for j in range(w):
                new_i = int(i + 5 * math.sin(j / 20 + self.time * 0.05))
                new_j = int(j + 5 * math.cos(i / 20 + self.time * 0.05))
                if 0 <= new_i < h and 0 <= new_j < w:
                    output[i, j] = frame[new_i, new_j]
        return output

    def apply_world_rotation(self, frame):
        h, w = frame.shape[:2]
        angle = self.time * 0.3
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    def apply_time_freeze_v(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(0, h, 5):
            cv2.line(output, (0, i), (w, i), (200, 200, 255), 1)
        cv2.putText(output, "FROZEN", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        return output

    def apply_time_reverse(self, frame):
        return cv2.flip(frame, 1)

    def apply_time_warp(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(30 * math.sin(i / 20 + self.time * 0.1))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return output

    def apply_speed_ramp(self, frame):
        h, w = frame.shape[:2]
        progress = (self.time % 100) / 100
        zoom = 1.0 + 0.5 * math.sin(progress * math.pi)
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_slow_motion(self, frame):
        h, w = frame.shape[:2]
        blur_size = 5 + int(10 * abs(math.sin(self.time * 0.02)))
        if blur_size % 2 == 0:
            blur_size += 1
        return cv2.GaussianBlur(frame, (blur_size, blur_size), 0)

    def apply_hyperlapse(self, frame):
        h, w = frame.shape[:2]
        zoom = 1.0 + 0.3 * (self.time % 50) / 50
        M = np.float32([[zoom, 0, w*(1-zoom)/2], [0, zoom, h*(1-zoom)/2]])
        return cv2.warpAffine(frame, M, (w, h))

    def apply_infinite_loop(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scale = 0.8
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        x = (w - small.shape[1]) // 2
        y = (h - small.shape[0]) // 2
        output[y:y+small.shape[0], x:x+small.shape[1]] = small
        return output

    def apply_endless_corridor(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(5):
            scale = 1 - i * 0.15
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            cv2.rectangle(output, (x, y), (x + small.shape[1], y + small.shape[0]), (150, 150, 200), 1)
        return output

    def apply_infinite_staircase(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(8):
            y = int(h * 0.1 + i * h * 0.1)
            x = int(w * 0.1 + i * w * 0.05)
            step_w = int(w * (0.8 - i * 0.08))
            step_h = int(h * 0.08)
            cv2.rectangle(output, (x, y), (x + step_w, y + step_h), (100 + i*10, 80 + i*10, 60), -1)
        return output

    def apply_infinite_room_v(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(4):
            scale = 1 - i * 0.2
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
            cv2.rectangle(output, (x, y), (x + small.shape[1], y + small.shape[0]), (100, 100, 150), 1)
        return output

    def apply_infinite_city(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(3):
            scale = 1 - i * 0.25
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
        return output

    def apply_mirror_dimension_v(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(frame[:, w//2:], 1)
        return np.hstack([left, right])

    def apply_parallel_universe_v(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2].copy()
        right = frame[:, w//2:].copy()
        left_hsv = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)
        left_hsv[:, :, 0] = (left_hsv[:, :, 0] + 60) % 180
        left = cv2.cvtColor(left_hsv, cv2.COLOR_HSV2BGR)
        return np.hstack([left, right])

    def apply_world_folding(self, frame):
        h, w = frame.shape[:2]
        top = frame[:h//2, :]
        bottom = cv2.flip(frame[h//2:, :], 0)
        return np.vstack([top, bottom])

    def apply_reality_melting(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(20 * math.sin(i / 15 + self.time * 0.08))
            new_i = min(h - 1, max(0, i + int(10 * math.sin(i / 30))))
            output[i, :] = np.roll(frame[new_i, :], offset, axis=0)
        return output

    def apply_space_bending(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        k = 0.3 * math.sin(self.time * 0.03)
        for i in range(h):
            for j in range(w):
                dx, dy = j - cx, i - cy
                r2 = (dx*dx + dy*dy) / (cx*cx + cy*cy)
                map_x[i, j] = cx + dx * (1 + k * r2)
                map_y[i, j] = cy + dy * (1 + k * r2)
        return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    def apply_perspective_shift(self, frame):
        h, w = frame.shape[:2]
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        shift = int(20 * math.sin(self.time * 0.03))
        pts2 = np.float32([[shift, 0], [w-shift, 0], [0, h], [w, h]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(frame, M, (w, h))


# --- Character Effects ---

    def apply_clone_army(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        positions = [(0, 0), (w//3, 0), (2*w//3, 0), (0, h//3), (w//3, h//3), (2*w//3, h//3), (0, 2*h//3), (w//3, 2*h//3), (2*w//3, 2*h//3)]
        for px, py in positions:
            small = cv2.resize(frame, (w//3, h//3))
            output[py:py + h//3, px:px + w//3] = small
        return output

    def apply_giant_character(self, frame):
        h, w = frame.shape[:2]
        center = frame[h//4:3*h//4, w//4:3*w//4]
        return cv2.resize(center, (w, h))

    def apply_tiny_character(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        mini = cv2.resize(frame, (w // 5, h // 5))
        x, y = w // 2 - w // 10, h // 2 - h // 10
        output[y:y + h//5, x:x + w//5] = mini
        return output

    def apply_character_levitation(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        y_offset = int(30 * math.sin(self.time * 0.05))
        center = frame[h//4:3*h//4, w//4:3*w//4]
        small = cv2.resize(center, (w//2, h//2))
        y_pos = h//4 + y_offset
        if y_pos >= 0 and y_pos + small.shape[0] <= h:
            output[y_pos:y_pos + small.shape[0], w//4:w//4 + small.shape[1]] = small
        return output

    def apply_character_teleport(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = (self.time % 60) / 60
        num_particles = int(100 * progress)
        for _ in range(num_particles):
            x = random.randint(w//3, 2*w//3)
            y = random.randint(h//3, 2*h//3)
            cv2.circle(output, (x, y), random.randint(2, 5), (0, 200, 255), -1)
        return output

    def apply_character_disappear(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        mask = np.zeros((h, w), dtype=np.uint8)
        cx, cy = w // 2, h // 2
        radius = int(min(w, h) * 0.4 * (1 - progress))
        cv2.circle(mask, (cx, cy), radius, 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        bg = np.zeros_like(frame)
        bg[:] = (20, 20, 30)
        mask_f = mask.astype(np.float32) / 255.0
        return (frame * mask_f[:, :, np.newaxis] + bg * (1 - mask_f[:, :, np.newaxis])).astype(np.uint8)

    def apply_character_reappear(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        mask = np.zeros((h, w), dtype=np.uint8)
        cx, cy = w // 2, h // 2
        radius = int(min(w, h) * 0.4 * progress)
        cv2.circle(mask, (cx, cy), radius, 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        bg = np.zeros_like(frame)
        bg[:] = (20, 20, 30)
        mask_f = mask.astype(np.float32) / 255.0
        return (frame * mask_f[:, :, np.newaxis] + bg * (1 - mask_f[:, :, np.newaxis])).astype(np.uint8)

    def apply_character_hologram(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 2):
            alpha = 0.5 + 0.5 * math.sin(y / 10 + self.time * 0.15)
            output[y:y+1, :] = (frame[y:y+1, :] * alpha).astype(np.uint8)
        return output

    def apply_character_glitch(self, frame):
        output = frame.copy()
        for _ in range(5):
            y = random.randint(0, frame.shape[0] - 10)
            h_slice = random.randint(3, 15)
            shift = random.randint(-20, 20)
            output[y:y+h_slice] = np.roll(frame[y:y+h_slice], shift, axis=1)
        return output

    def apply_character_pixelate(self, frame):
        pixel_size = max(2, int(10 + 5 * math.sin(self.time * 0.05)))
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // pixel_size, h // pixel_size))
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_character_turn_to_stone(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stone = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        stone[:, :, 0] = np.clip(stone[:, :, 0] * 0.8, 0, 255)
        stone[:, :, 1] = np.clip(stone[:, :, 1] * 0.7, 0, 255)
        stone[:, :, 2] = np.clip(stone[:, :, 2] * 0.6, 0, 255)
        return stone

    def apply_character_turn_to_glass(self, frame):
        overlay = frame.copy()
        edges = cv2.Canny(frame, 30, 100)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        mask = edges > 0
        overlay[mask] = (200, 220, 255)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_character_turn_to_crystal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 20):
            for x in range(0, w, 20):
                color = frame[min(y+10, h-1), min(x+10, w-1)].tolist()
                pts = np.array([[x, y], [x+10, y+5], [x+20, y], [x+15, y+15], [x+5, y+15]], np.int32)
                cv2.fillPoly(output, [pts], color)
        return output

    def apply_character_turn_to_smoke(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(50):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, 3*h//4)
            size = random.randint(15, 40)
            alpha = random.uniform(0.2, 0.5)
            cv2.circle(output, (x, y), size, (80, 80, 80), -1)
        return output

    def apply_character_turn_to_fire(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(30):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, h)
            size = random.randint(10, 25)
            cv2.circle(output, (x, y), size, (0, 100, 255), -1)
            cv2.circle(output, (x, y-5), size-5, (0, 150, 255), -1)
        return output

    def apply_character_turn_to_water(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(10 * math.sin(i / 15 + self.time * 0.08))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 100
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_character_turn_to_lightning(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(5):
            x = random.randint(w//3, 2*w//3)
            points = [(x, h//4)]
            y = h // 4
            while y < 3*h//4:
                y += random.randint(10, 30)
                x += random.randint(-20, 20)
                points.append((x, min(y, 3*h//4)))
            pts = np.array(points, np.int32)
            cv2.polylines(output, [pts], False, (255, 255, 0), 2)
        return output

    def apply_character_turn_to_particles(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for _ in range(200):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = frame[min(y, h-1), min(x, w-1)].tolist()
            cv2.circle(output, (x, y), random.randint(2, 5), color, -1)
        return output

    def apply_character_digital_scan(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scan_y = int(h * ((self.time % 100) / 100))
        cv2.line(output, (0, scan_y), (w, scan_y), (0, 255, 0), 3)
        for y in range(max(0, scan_y - 30), scan_y):
            alpha = (y - (scan_y - 30)) / 30
            output[y, :] = (frame[y, :] * (1 - alpha) + np.array([0, 255, 0]) * alpha).astype(np.uint8)
        return output

    def apply_character_shadow_clone(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(3):
            x_offset = (i - 1) * 30
            y_offset = (i - 1) * 20
            clone = frame.copy()
            shadow = np.zeros_like(clone)
            shadow[:] = (20, 20, 30)
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.ellipse(mask, (w//2 + x_offset, h//2 + y_offset), (80, 120), 0, 0, 360, 255, -1)
            mask = cv2.GaussianBlur(mask, (31, 31), 0)
            mask_f = mask.astype(np.float32) / 255.0
            blended = (clone * mask_f[:, :, np.newaxis] + shadow * (1 - mask_f[:, :, np.newaxis])).astype(np.uint8)
            output = cv2.addWeighted(output, 0.7, blended, 0.3, 0)
        return output


# --- Environment ---

    def apply_city_transform(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        num_buildings = int(15 * progress)
        for i in range(num_buildings):
            x = i * w // 15
            bh = random.randint(h // 4, h // 2)
            bw = w // 20
            cv2.rectangle(overlay, (x, h - bh), (x + bw, h), (40, 40, 60), -1)
        cv2.addWeighted(overlay, 0.3 * progress, frame, 1 - 0.3 * progress, 0, frame)
        return frame

    def apply_room_transform(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, 50), (w-50, h-50), (60, 60, 80), 3)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_day_to_night(self, frame):
        progress = min(1, (self.time % 100) / 100)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = (hsv[:, :, 2] * (1 - 0.7 * progress)).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_night_to_day(self, frame):
        progress = min(1, (self.time % 100) / 100)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2].astype(np.float32) * (1 + 0.7 * progress), 0, 255).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_earth_to_space(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        output = frame.copy()
        output[:] = (10, 5, 20)
        for _ in range(int(200 * progress)):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(output, (x, y), 1, (255, 255, 255), -1)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w//2, h//2), int(min(w, h) * 0.3 * (1 - progress)), 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        mask_f = mask.astype(np.float32) / 255.0
        return (output * (1 - mask_f[:, :, np.newaxis]) + frame * mask_f[:, :, np.newaxis]).astype(np.uint8)

    def apply_street_to_cyberpunk(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + 20) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        h, w = frame.shape[:2]
        for _ in range(10):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(frame, (x, y), random.randint(3, 8), (255, 0, 100), -1)
        return frame

    def apply_real_to_anime(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
        colorful = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return cv2.bitwise_and(colorful, edges)

    def apply_real_to_game(self, frame):
        small = cv2.resize(frame, (frame.shape[1] // 4, frame.shape[0] // 4), interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    def apply_real_to_fantasy(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(20):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(10, 30)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.circle(output, (x, y), size, color, -1)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_real_to_metaverse(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for x in range(0, w, 40):
            cv2.line(overlay, (x, 0), (x, h), (0, 255, 255), 1)
        for y in range(0, h, 40):
            cv2.line(overlay, (0, y), (w, y), (0, 255, 255), 1)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_ocean_appears(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        output = frame.copy()
        water_level = int(h * (1 - progress))
        for y in range(water_level, h):
            wave = int(5 * math.sin(y / 10 + self.time * 0.1))
            blue = int(150 + 50 * ((y - water_level) / (h - water_level)))
            output[y, :] = [min(255, blue), 100, 50]
        return output

    def apply_forest_appears(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        overlay = frame.copy()
        num_trees = int(10 * progress)
        for i in range(num_trees):
            x = i * w // 10 + random.randint(-20, 20)
            tree_h = random.randint(h // 4, h // 2)
            cv2.line(overlay, (x, h), (x, h - tree_h), (40, 80, 20), 6)
            cv2.circle(overlay, (x, h - tree_h), 30, (30, 120, 30), -1)
        cv2.addWeighted(overlay, 0.4 * progress, frame, 1 - 0.4 * progress, 0, frame)
        return frame


# ============================================================
# 100+ EFEK VR TAMBAHAN — CAMPURAN
# ============================================================

# --- Portal Lens ---

    def apply_portal_lens(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for r in range(100, 10, -3):
            angle = self.time * 0.05 + r * 0.1
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            hue = int((r * 3 + self.time * 10) % 180)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(output, (x, y), 3, color_bgr.tolist(), -1)
        return output

    def apply_reality_warp(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            for j in range(w):
                new_i = int(i + 15 * math.sin(j / 30 + self.time * 0.05))
                new_j = int(j + 15 * math.cos(i / 30 + self.time * 0.05))
                if 0 <= new_i < h and 0 <= new_j < w:
                    output[i, j] = frame[new_i, new_j]
        return output

    def apply_360_tunnel(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        for r in range(min(w, h) // 2, 10, -5):
            angle = self.time * 0.05 + r * 0.05
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            color_val = int(100 + 155 * (r / (min(w, h) // 2)))
            cv2.circle(output, (x, y), 4, (color_val, color_val // 2, 255 - color_val), -1)
        return output

    def apply_infinite_tunnel(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(8):
            scale = 1 - i * 0.1
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
            cv2.rectangle(output, (x, y), (x + small.shape[1], y + small.shape[0]), (100, 100, 200), 1)
        return output

    def apply_galaxy_eye(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(300):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_cosmic_reflection(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = frame[:, w//2:]
        right_cosmic = right.copy()
        hsv = cv2.cvtColor(right_cosmic, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0] + 60) % 180
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        right_cosmic = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return np.hstack([left, right_cosmic])

    def apply_neon_vision(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        neon_colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
        color = neon_colors[self.time % len(neon_colors)]
        mask = edges > 0
        frame[mask] = color
        return frame

    def apply_cyber_eye(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.putText(overlay, "CYBER", (w//4, h//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
        cv2.putText(overlay, "SCANNING...", (w//4, h//2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 200), 2)
        for i in range(0, h, 30):
            cv2.line(overlay, (0, i), (w, i), (0, 100, 100), 1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_robot_vision(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 3):
            cv2.line(output, (0, y), (w, y), (0, 255, 0), 1)
        cv2.putText(output, "ROBOT MODE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(output, f"FRAME: {self.time}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 1)
        return output

    def apply_hologram_vision(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 2):
            alpha = 0.5 + 0.5 * math.sin(y / 8 + self.time * 0.15)
            output[y:y+1, :] = (frame[y:y+1, :] * alpha).astype(np.uint8)
        return output

    def apply_thermal_vision(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    def apply_night_vision(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 60
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.3, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_xray_world(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    def apply_infrared_world(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 0
        hsv[:, :, 1] = 255
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_digital_vision(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for x in range(0, w, 40):
            cv2.line(output, (x, 0), (x, h), (0, 255, 255), 1)
        for y in range(0, h, 40):
            cv2.line(output, (0, y), (w, y), (0, 255, 255), 1)
        return output

    def apply_matrix_vision(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for x in range(0, w, 15):
            char = chr(random.randint(33, 126))
            y = random.randint(20, h - 20)
            cv2.putText(output, char, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        return output

    def apply_glitch_vision(self, frame):
        output = frame.copy()
        for _ in range(5):
            y = random.randint(0, frame.shape[0] - 10)
            h_slice = random.randint(3, 15)
            shift = random.randint(-20, 20)
            output[y:y+h_slice] = np.roll(frame[y:y+h_slice], shift, axis=1)
        return output

    def apply_dream_vision(self, frame):
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_future_vision(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.putText(overlay, "2050", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
        for i in range(5):
            y = h // 6 * (i + 1)
            cv2.line(overlay, (0, y), (w, y), (0, 150, 150), 1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_quantum_vision(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            for j in range(w):
                new_i = int(i + 10 * math.sin(j / 25 + self.time * 0.05))
                new_j = int(j + 10 * math.cos(i / 25 + self.time * 0.05))
                if 0 <= new_i < h and 0 <= new_j < w:
                    output[i, j] = frame[new_i, new_j]
        return output


# --- Mirror Effects ---

    def apply_mirror_portal_v(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(frame[:, w//2:], 1)
        output = np.hstack([left, right])
        overlay = output.copy()
        cv2.line(overlay, (w//2, 0), (w//2, h), (200, 200, 255), 3)
        cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)
        return output

    def apply_mirror_clone_v(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = cv2.flip(left, 1)
        return np.hstack([left, right])

    def apply_mirror_explosion(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(20):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(5, 15)
            cv2.circle(output, (x, y), size, (200, 200, 255), 2)
        return output

    def apply_mirror_maze(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(4):
            scale = 1 - i * 0.2
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
            cv2.rectangle(output, (x, y), (x + small.shape[1], y + small.shape[0]), (150, 150, 200), 1)
        return output

    def apply_infinite_reflection(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(6):
            scale = 1 - i * 0.15
            small = cv2.resize(frame, (int(w * scale), int(h * scale)))
            x = (w - small.shape[1]) // 2
            y = (h - small.shape[0]) // 2
            if x >= 0 and y >= 0 and x + small.shape[1] <= w and y + small.shape[0] <= h:
                output[y:y+small.shape[0], x:x+small.shape[1]] = small
        return output

    def apply_reverse_reflection(self, frame):
        return cv2.flip(frame, 1)

    def apply_broken_mirror_world(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        block_size = 30
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                if random.random() < 0.3:
                    shift_x = random.randint(-10, 10)
                    shift_y = random.randint(-10, 10)
                    src_y = max(0, min(h - block_size, y + shift_y))
                    src_x = max(0, min(w - block_size, x + shift_x))
                    output[y:y+block_size, x:x+block_size] = frame[src_y:src_y+block_size, src_x:src_x+block_size]
        return output

    def apply_liquid_mirror(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(15 * math.sin(i / 15 + self.time * 0.08))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return output

    def apply_galaxy_mirror(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(200):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        left = output[:, :w//2]
        right = cv2.flip(left, 1)
        return np.hstack([left, right])

    def apply_cyber_mirror(self, frame):
        h, w = frame.shape[:2]
        left = frame[:, :w//2]
        right = frame[:, w//2:]
        right_hsv = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)
        right_hsv[:, :, 0] = (right_hsv[:, :, 0] + 40) % 180
        right = cv2.cvtColor(right_hsv, cv2.COLOR_HSV2BGR)
        return np.hstack([left, right])


# --- Teleport Through ---

    def apply_teleport_behind_camera(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 80) / 80)
        output = frame.copy()
        num_particles = int(100 * progress)
        for _ in range(num_particles):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(output, (x, y), random.randint(2, 5), (0, 200, 255), -1)
        return output

    def apply_teleport_through_phone(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        phone_w = w // 3
        phone_h = h // 2
        x1 = (w - phone_w) // 2
        y1 = (h - phone_h) // 2
        cv2.rectangle(output, (x1, y1), (x1 + phone_w, y1 + phone_h), (50, 50, 50), 3)
        progress = min(1, (self.time % 80) / 80)
        if progress > 0.5:
            cv2.putText(output, "TELEPORT", (x1 + 20, y1 + phone_h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        return output

    def apply_teleport_through_screen(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        scan_x = int(w * progress)
        cv2.line(output, (scan_x, 0), (scan_x, h), (0, 255, 0), 3)
        return output

    def apply_teleport_through_glass(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        for r in range(int(80 * progress), 0, -3):
            cv2.circle(output, (w//2, h//2), r, (200, 220, 255), 2)
        return output

    def apply_teleport_through_shadow(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        shadow_alpha = progress
        shadow = np.zeros_like(frame)
        shadow[:] = (20, 20, 30)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (w//2, h//2 + 50), (100, 50), 0, 0, 360, 255, -1)
        mask = cv2.GaussianBlur(mask, (31, 31), 0)
        mask_f = mask.astype(np.float32) / 255.0 * shadow_alpha
        return (output * (1 - mask_f[:, :, np.newaxis]) + shadow * mask_f[:, :, np.newaxis]).astype(np.uint8)

    def apply_teleport_through_water(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        water_level = int(h * progress)
        for y in range(max(0, water_level - 20), min(h, water_level + 20)):
            wave = int(10 * math.sin(y / 10 + self.time * 0.1))
            if 0 <= y < h:
                output[y, :] = np.roll(frame[y, :], wave, axis=0)
        return output

    def apply_teleport_through_fire(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        num_flames = int(50 * progress)
        for _ in range(num_flames):
            x = random.randint(w//3, 2*w//3)
            y = random.randint(h//3, 2*h//3)
            size = random.randint(10, 25)
            cv2.circle(output, (x, y), size, (0, 100, 255), -1)
            cv2.circle(output, (x, y-5), size-5, (0, 150, 255), -1)
        return output

    def apply_teleport_through_lightning(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        num_bolts = int(5 * progress)
        for _ in range(num_bolts):
            x = random.randint(w//3, 2*w//3)
            points = [(x, h//4)]
            y = h // 4
            while y < 3*h//4:
                y += random.randint(10, 30)
                x += random.randint(-20, 20)
                points.append((x, min(y, 3*h//4)))
            pts = np.array(points, np.int32)
            cv2.polylines(output, [pts], False, (255, 255, 0), 2)
        return output

    def apply_teleport_through_clouds(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 80) / 80)
        num_clouds = int(15 * progress)
        for _ in range(num_clouds):
            x = random.randint(0, w)
            y = random.randint(0, h)
            axes = (random.randint(40, 80), random.randint(20, 40))
            cv2.ellipse(output, (x, y), axes, 0, 0, 360, (220, 220, 240), -1)
        return output

    def apply_teleport_into_space(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        output[:] = (10, 5, 20)
        for _ in range(int(300 * progress)):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(output, (x, y), 1, (255, 255, 255), -1)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w//2, h//2), int(min(w, h) * 0.3 * (1 - progress)), 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        mask_f = mask.astype(np.float32) / 255.0
        return (output * (1 - mask_f[:, :, np.newaxis]) + frame * mask_f[:, :, np.newaxis]).astype(np.uint8)


# --- Object Comes Alive ---

    def apply_object_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(10):
            x = random.randint(50, w - 50)
            y = random.randint(50, h - 50)
            offset_y = int(10 * math.sin(self.time * 0.08 + x * 0.01))
            cv2.circle(output, (x, y + offset_y), 10, (100, 255, 100), -1)
            cv2.circle(output, (x, y + offset_y), 12, (200, 255, 200), 2)
        return output

    def apply_photo_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        border = 20
        cv2.rectangle(output, (border, border), (w - border, h - border), (100, 80, 60), 5)
        offset_y = int(5 * math.sin(self.time * 0.05))
        center = frame[border+10:h-border-10, border+10:w-border-10]
        if center.shape[0] > 0 and center.shape[1] > 0:
            output[border+5+offset_y:h-border-5+offset_y, border+5:w-border-5] = cv2.resize(center, (w - 2*border - 10, h - 2*border - 10 - offset_y))
        return output

    def apply_painting_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cv2.rectangle(output, (30, 30), (w-30, h-30), (80, 60, 40), 8)
        cv2.rectangle(output, (40, 40), (w-40, h-40), (120, 100, 60), 3)
        offset_x = int(5 * math.sin(self.time * 0.05))
        cv2.putText(output, "ALIVE", (w//3 + offset_x, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return output

    def apply_statue_comes_alive(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stone = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        stone[:, :, 0] = np.clip(stone[:, :, 0] * 0.9, 0, 255)
        stone[:, :, 1] = np.clip(stone[:, :, 1] * 0.85, 0, 255)
        stone[:, :, 2] = np.clip(stone[:, :, 2] * 0.8, 0, 255)
        h, w = frame.shape[:2]
        cv2.putText(stone, "ALIVE", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        return stone

    def apply_poster_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cv2.rectangle(output, (50, 50), (w-50, h-50), (50, 50, 80), 3)
        progress = min(1, (self.time % 100) / 100)
        cv2.putText(output, "POSTER", (w//4, h//3), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
        if progress > 0.5:
            cv2.putText(output, "ALIVE!", (w//4, 2*h//3), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 255), 2)
        return output

    def apply_logo_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h // 2
        angle = self.time * 0.05
        size = 50
        pts = []
        for i in range(6):
            a = angle + i * math.pi / 3
            pts.append([int(cx + size * math.cos(a)), int(cy + size * math.sin(a))])
        cv2.polylines(output, [np.array(pts, np.int32)], True, (0, 255, 255), 3)
        return output

    def apply_text_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        offset_y = int(10 * math.sin(self.time * 0.08))
        cv2.putText(output, "TEXT", (w//3, h//2 + offset_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)
        return output

    def apply_drawing_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(5):
            x1 = random.randint(50, w-50)
            y1 = random.randint(50, h-50)
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(-50, 50)
            cv2.line(output, (x1, y1), (x2, y2), (255, 200, 100), 2)
        return output

    def apply_shadow_comes_alive(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        shadow_x = int(w//2 + 30 * math.sin(self.time * 0.05))
        cv2.ellipse(output, (shadow_x, h - 30), (60, 20), 0, 0, 360, (30, 30, 40), -1)
        return output

    def apply_reflection_comes_alive(self, frame):
        h, w = frame.shape[:2]
        top = frame[:h//2, :]
        bottom = cv2.flip(top, 0)
        offset = int(5 * math.sin(self.time * 0.05))
        bottom = np.roll(bottom, offset, axis=1)
        return np.vstack([top, bottom])


# --- Body Becomes ---

    def apply_body_becomes_smoke(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(50):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, 3*h//4)
            size = random.randint(15, 40)
            cv2.circle(output, (x, y), size, (80, 80, 80), -1)
        return output

    def apply_body_becomes_water(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(10 * math.sin(i / 15 + self.time * 0.08))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 100
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_body_becomes_fire(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(30):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, h)
            size = random.randint(10, 25)
            cv2.circle(output, (x, y), size, (0, 100, 255), -1)
            cv2.circle(output, (x, y-5), size-5, (0, 150, 255), -1)
        return output

    def apply_body_becomes_ice(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(20):
            x = random.randint(w//4, 3*w//4)
            y = random.randint(h//4, 3*h//4)
            size = random.randint(15, 35)
            cv2.circle(output, (x, y), size, (255, 200, 150), 2)
            for j in range(6):
                angle = j * 60 * math.pi / 180
                x2 = int(x + size * math.cos(angle))
                y2 = int(y + size * math.sin(angle))
                cv2.line(output, (x, y), (x2, y2), (200, 230, 255), 1)
        return output

    def apply_body_becomes_glass(self, frame):
        overlay = frame.copy()
        edges = cv2.Canny(frame, 30, 100)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        mask = edges > 0
        overlay[mask] = (200, 220, 255)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame

    def apply_body_becomes_crystal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 20):
            for x in range(0, w, 20):
                color = frame[min(y+10, h-1), min(x+10, w-1)].tolist()
                pts = np.array([[x, y], [x+10, y+5], [x+20, y], [x+15, y+15], [x+5, y+15]], np.int32)
                cv2.fillPoly(output, [pts], color)
        return output

    def apply_body_becomes_metal(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        metal = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        metal[:, :, 0] = np.clip(metal[:, :, 0] * 1.2, 0, 255)
        metal[:, :, 1] = np.clip(metal[:, :, 1] * 1.1, 0, 255)
        metal[:, :, 2] = np.clip(metal[:, :, 2] * 1.0, 0, 255)
        return metal

    def apply_body_becomes_gold(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gold = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        gold[:, :, 0] = np.clip(gold[:, :, 0] * 0.5, 0, 255)
        gold[:, :, 1] = np.clip(gold[:, :, 1] * 0.8, 0, 255)
        gold[:, :, 2] = np.clip(gold[:, :, 2] * 1.5, 0, 255)
        return gold

    def apply_body_becomes_stone(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stone = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        stone[:, :, 0] = np.clip(stone[:, :, 0] * 0.8, 0, 255)
        stone[:, :, 1] = np.clip(stone[:, :, 1] * 0.7, 0, 255)
        stone[:, :, 2] = np.clip(stone[:, :, 2] * 0.6, 0, 255)
        return stone

    def apply_body_becomes_sand(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 20
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.8, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


# --- Face Effects ---

    def apply_face_morph(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for i in range(5):
            y = h // 6 * (i + 1)
            shift = int(20 * math.sin(self.time * 0.05 + i))
            output[y-2:y+2, :] = np.roll(frame[y-2:y+2, :], shift, axis=1)
        return output

    def apply_face_pixel_morph(self, frame):
        h, w = frame.shape[:2]
        pixel_size = max(2, int(10 + 5 * math.sin(self.time * 0.05)))
        small = cv2.resize(frame, (w // pixel_size, h // pixel_size))
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_face_hologram(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 2):
            alpha = 0.5 + 0.5 * math.sin(y / 8 + self.time * 0.15)
            output[y:y+1, :] = (frame[y:y+1, :] * alpha).astype(np.uint8)
        return output

    def apply_face_crystal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 15):
            for x in range(0, w, 15):
                color = frame[min(y+7, h-1), min(x+7, w-1)].tolist()
                pts = np.array([[x, y], [x+7, y+3], [x+15, y], [x+12, y+12], [x+3, y+12]], np.int32)
                cv2.fillPoly(output, [pts], color)
        return output

    def apply_face_galaxy(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(200):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_face_liquid(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for i in range(h):
            offset = int(10 * math.sin(i / 15 + self.time * 0.08))
            output[i, :] = np.roll(frame[i, :], offset, axis=0)
        return output

    def apply_face_robot(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for y in range(0, h, 3):
            cv2.line(output, (0, y), (w, y), (0, 100, 0), 1)
        return output

    def apply_face_anime_v(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
        colorful = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return cv2.bitwise_and(colorful, edges)

    def apply_face_digital_scan(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        scan_y = int(h * ((self.time % 100) / 100))
        cv2.line(output, (0, scan_y), (w, scan_y), (0, 255, 0), 3)
        return output

    def apply_face_particle_explosion(self, frame):
        h, w = frame.shape[:2]
        output = np.zeros_like(frame)
        for _ in range(200):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = frame[min(y, h-1), min(x, w-1)].tolist()
            cv2.circle(output, (x, y), random.randint(2, 5), color, -1)
        return output


# --- Environment Transforms ---

    def apply_street_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(10):
            x = i * w // 10
            bh = random.randint(h // 4, h // 2)
            cv2.rectangle(overlay, (x, h - bh), (x + w // 15, h), (50, 50, 70), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_house_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cx, cy = w // 2, h // 2
        cv2.rectangle(overlay, (cx - 80, cy), (cx + 80, h), (80, 60, 40), -1)
        pts = np.array([[cx - 100, cy], [cx, cy - 60], [cx + 100, cy]], np.int32)
        cv2.fillPoly(overlay, [pts], (100, 50, 30))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_building_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(8):
            x = i * w // 8
            bh = random.randint(h // 3, h // 2)
            cv2.rectangle(overlay, (x, h - bh), (x + w // 12, h), (40, 40, 60), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_school_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//4, h//3), (3*w//4, h), (100, 80, 60), -1)
        cv2.putText(overlay, "SCHOOL", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_mall_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//6, h//4), (5*w//6, h), (60, 60, 80), -1)
        cv2.putText(overlay, "MALL", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 255), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_office_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//4, h//4), (3*w//4, h), (50, 50, 70), -1)
        cv2.putText(overlay, "OFFICE", (w//3, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_room_transforms_v(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, 50), (w-50, h-50), (60, 60, 80), 3)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        return frame

    def apply_car_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//4, h//2), (3*w//4, 3*h//4), (80, 80, 100), -1)
        cv2.circle(overlay, (w//3, 3*h//4), 20, (30, 30, 30), -1)
        cv2.circle(overlay, (2*w//3, 3*h//4), 20, (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_landscape_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        pts = np.array([[0, h], [w//3, h//3], [2*w//3, h//2], [w, h]], np.int32)
        cv2.fillPoly(overlay, [pts], (50, 120, 50))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def apply_entire_city_transforms(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        for i in range(15):
            x = i * w // 15
            bh = random.randint(h // 4, h // 2)
            cv2.rectangle(overlay, (x, h - bh), (x + w // 20, h), (40, 40, 60), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        return frame


# --- Sky Effects ---

    def apply_sky_opens(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        opening_size = int(min(w, h) * 0.3 * progress)
        cv2.circle(output, (w//2, h//4), opening_size, (0, 150, 255), -1)
        cv2.circle(output, (w//2, h//4), opening_size + 5, (0, 200, 255), 3)
        return output

    def apply_sky_portal_v(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        for r in range(int(100 * progress), 0, -5):
            hue = int((r * 2 + self.time * 5) % 180)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(output, (w//2, h//4), r, color_bgr.tolist(), 2)
        return output

    def apply_moon_falls(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        moon_y = int(h // 4 + h // 2 * progress)
        cv2.circle(output, (w//2, moon_y), 40, (200, 200, 220), -1)
        cv2.circle(output, (w//2, moon_y), 42, (220, 220, 240), 2)
        return output

    def apply_planet_appears(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        radius = int(60 * progress)
        cv2.circle(output, (w//2, h//3), radius, (150, 100, 80), -1)
        cv2.circle(output, (w//2, h//3), radius + 3, (180, 130, 100), 2)
        return output

    def apply_galaxy_descends(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        num_stars = int(200 * progress)
        for _ in range(num_stars):
            x = random.randint(0, w)
            y = random.randint(0, int(h * progress))
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_meteor_shower_v(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(10):
            x1 = random.randint(0, w)
            y1 = random.randint(0, h // 2)
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(50, 150)
            cv2.line(output, (x1, y1), (x2, y2), (0, 200, 255), 2)
            cv2.circle(output, (x2, y2), 3, (0, 255, 255), -1)
        return output

    def apply_aurora_world(self, frame):
        h, w = frame.shape[:2]
        overlay = np.zeros_like(frame, dtype=np.float32)
        for y in range(h // 4, h // 2):
            hue = int(120 + 30 * math.sin(y / 30 + self.time * 0.02))
            color_hsv = np.uint8([[[hue, 255, 200]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            overlay[y, :] = color_bgr
        result = cv2.addWeighted(frame.astype(np.float32), 0.7, overlay, 0.3, 0).astype(np.uint8)
        return result

    def apply_rainbow_tunnel(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for r in range(min(w, h) // 2, 10, -5):
            hue = int((r * 3 + self.time * 10) % 180)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(output, (w//2, h//2), r, color_bgr.tolist(), 2)
        return output

    def apply_cloud_ocean(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(h//2, h)
            axes = (random.randint(40, 80), random.randint(15, 30))
            cv2.ellipse(output, (x, y), axes, 0, 0, 360, (200, 200, 220), -1)
        return output

    def apply_floating_clouds(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(15):
            x = random.randint(0, w)
            y = random.randint(0, h//2)
            offset_x = int(5 * math.sin(self.time * 0.02 + x * 0.01))
            axes = (random.randint(30, 60), random.randint(15, 25))
            cv2.ellipse(output, (x + offset_x, y), axes, 0, 0, 360, (220, 220, 240), -1)
        return output


# --- Ground Effects ---

    def apply_ground_becomes_water(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        water_level = h // 2
        for y in range(water_level, h):
            wave = int(5 * math.sin(y / 10 + self.time * 0.1))
            blue = int(150 + 50 * ((y - water_level) / (h - water_level)))
            output[y, :] = [min(255, blue), 100, 50]
        return output

    def apply_ground_becomes_lava(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        lava_level = h // 2
        for y in range(lava_level, h):
            wave = int(5 * math.sin(y / 10 + self.time * 0.1))
            intensity = (y - lava_level) / (h - lava_level)
            output[y, :] = [0, int(100 * intensity), int(200 * intensity)]
        return output

    def apply_ground_becomes_glass(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        glass_level = h // 2
        overlay = output[glass_level:, :].copy()
        edges = cv2.Canny(overlay, 30, 100)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        mask = edges > 0
        overlay[mask] = (200, 220, 255)
        output[glass_level:] = overlay
        return output

    def apply_ground_becomes_galaxy(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        galaxy_level = h // 2
        for _ in range(100):
            x = random.randint(0, w)
            y = random.randint(galaxy_level, h)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_ground_opens_portal(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        cx, cy = w // 2, h - 50
        progress = min(1, (self.time % 100) / 100)
        for r in range(int(80 * progress), 0, -3):
            hue = int((r * 3 + self.time * 5) % 180)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.ellipse(output, (cx, cy), (r, r // 3), 0, 0, 360, color_bgr.tolist(), 2)
        return output


# --- Weather Effects ---

    def apply_ocean_rises(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        water_level = int(h * (1 - progress * 0.5))
        for y in range(water_level, h):
            wave = int(5 * math.sin(y / 10 + self.time * 0.1))
            blue = int(150 + 50 * ((y - water_level) / (h - water_level)))
            output[y, :] = [min(255, blue), 100, 50]
        return output

    def apply_water_floats(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(20):
            x = random.randint(0, w)
            y = random.randint(0, h)
            offset_y = int(10 * math.sin(self.time * 0.05 + x * 0.01))
            cv2.circle(output, (x, y + offset_y), 8, (200, 150, 50), -1)
        return output

    def apply_rain_reverses_upward(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h)
            length = random.randint(10, 30)
            cv2.line(output, (x, y), (x, y - length), (200, 200, 255), 1)
        return output

    def apply_snow_freezes_mid_air(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h)
            cv2.circle(output, (x, y), random.randint(2, 5), (255, 255, 255), -1)
        return output

    def apply_reality_breaks_apart(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        block_size = 30
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                if random.random() < 0.2:
                    shift_x = random.randint(-15, 15)
                    shift_y = random.randint(-15, 15)
                    src_y = max(0, min(h - block_size, y + shift_y))
                    src_x = max(0, min(w - block_size, x + shift_x))
                    output[y:y+block_size, x:x+block_size] = frame[src_y:src_y+block_size, src_x:src_x+block_size]
        return output


    def apply_galaxy_appears(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        output = frame.copy()
        for _ in range(int(300 * progress)):
            x = random.randint(0, w)
            y = random.randint(0, h)
            color = (random.randint(100, 255), random.randint(50, 200), random.randint(150, 255))
            cv2.circle(output, (x, y), random.randint(1, 3), color, -1)
        return output

    def apply_giant_planet_appears(self, frame):
        h, w = frame.shape[:2]
        progress = min(1, (self.time % 100) / 100)
        output = frame.copy()
        radius = int(min(w, h) * 0.3 * progress)
        cv2.circle(output, (w//2, h//2), radius, (100, 80, 60), -1)
        cv2.circle(output, (w//2, h//2), radius, (150, 120, 80), 3)
        return output

    def apply_floating_island_v(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        y_offset = int(20 * math.sin(self.time * 0.03))
        pts = np.array([[w//4, h//3 + y_offset], [w//3, h//4 + y_offset], [2*w//3, h//4 + y_offset], [3*w//4, h//3 + y_offset], [2*w//3, h//3+30 + y_offset], [w//3, h//3+30 + y_offset]], np.int32)
        cv2.fillPoly(output, [pts], (100, 80, 60))
        cv2.circle(output, (w//2, h//4 - 20 + y_offset), 30, (50, 150, 50), -1)
        return output

    def apply_city_floating(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        y_offset = int(15 * math.sin(self.time * 0.02))
        for i in range(8):
            x = i * w // 8
            bh = random.randint(h // 6, h // 3)
            bw = w // 12
            cv2.rectangle(output, (x, h//3 + y_offset - bh), (x + bw, h//3 + y_offset), (50, 50, 70), -1)
        return output

    def apply_building_collapse_rebuild(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = (self.time % 100) / 100
        if progress < 0.5:
            collapse = progress * 2
            for i in range(8):
                x = i * w // 8
                bh = int((h // 3) * (1 - collapse * 0.5))
                bw = w // 12
                cv2.rectangle(output, (x, h - bh), (x + bw, h), (60, 60, 80), -1)
        else:
            rebuild = (progress - 0.5) * 2
            for i in range(8):
                x = i * w // 8
                bh = int((h // 3) * (0.5 + rebuild * 0.5))
                bw = w // 12
                cv2.rectangle(output, (x, h - bh), (x + bw, h), (60, 60, 80), -1)
        return output

    def apply_world_explosion(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 60) / 60)
        cx, cy = w // 2, h // 2
        for _ in range(int(200 * progress)):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(0, int(min(w, h) * 0.5 * progress))
            x = int(cx + dist * math.cos(angle))
            y = int(cy + dist * math.sin(angle))
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.circle(output, (x, y), random.randint(3, 8), color, -1)
        return output

    def apply_world_reconstruct(self, frame):
        h, w = frame.shape[:2]
        output = frame.copy()
        progress = min(1, (self.time % 100) / 100)
        num_pieces = int(100 * (1 - progress))
        for _ in range(num_pieces):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(5, 15)
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            cv2.rectangle(output, (x, y), (x + size, y + size), color, -1)
        return output

    def apply_ultimate_vr_reality_transformation(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        output = frame.copy()
        progress = min(1, (self.time % 200) / 200)
        for r in range(int(min(w, h) * 0.4), 0, -3):
            angle = self.time * 0.05 + r * 0.02
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            hue = int((r * 5 + self.time * 10) % 180)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            cv2.circle(output, (x, y), 3, color_bgr.tolist(), -1)
        return output

