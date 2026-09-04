import math
import random
import sys
import pygame

WIDTH, HEIGHT = 1000, 800
FPS = 60

G = 1.0                    
M_CENTER = 50000.0         
PLUMMER_EPSILON = 25.0     
DARK_MATTER_HALO = 50.0    
NUM_STARS = 2000           
NUM_ARMS = 2                
ARM_DENSITY_STRENGTH = 0.3

R_DISK = 150.0             
B_SPIRAL = 0.3             

MOUSE_PULL_STRENGTH = 4000.0   
MOUSE_PULL_EPSILON = 15.0      

ZOOM_MIN = 0.2
ZOOM_MAX = 5.0
ZOOM_STEP = 1.1               

DISK_HEIGHT_SCALE = 8.0        
BULGE_HEIGHT_SCALE = 25.0      
BASE_FOCAL = 600.0             
CAMERA_DISTANCE = 500.0        
ROTATE_SENSITIVITY = 0.01      

class Star:
    def __init__(self, x, y, velocity_x, velocity_y, mass, radius,
                 brightness, temperature, color, age, height=0.0):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity_x, velocity_y)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.brightness = brightness
        self.temperature = temperature
        self.color = color
        self.age = age
        self.height = height

    def update_physics(self, dt, center, mouse_world_pos, mouse_pulling):
        rel = self.position - center
        r_sq = rel.x * rel.x + rel.y * rel.y
        r = math.sqrt(r_sq)

        if r == 0:
            r = 0.01
            r_sq = r * r

        softened_r3 = (r_sq + PLUMMER_EPSILON ** 2) ** 1.5
        acc_central = (G * M_CENTER) / softened_r3

        acc_dark_matter = (G * DARK_MATTER_HALO * r) / softened_r3

        acc_total = acc_central + acc_dark_matter
        acc = pygame.Vector2(-acc_total * rel.x, -acc_total * rel.y)

        angle = math.atan2(rel.y, rel.x)
        spiral_angle = (1.0 / B_SPIRAL) * math.log(max(r, 1.0) / R_DISK)
        perturbation = math.sin(NUM_ARMS * (angle - spiral_angle))

        acc.x += -rel.x / r * perturbation * ARM_DENSITY_STRENGTH
        acc.y += -rel.y / r * perturbation * ARM_DENSITY_STRENGTH

        if mouse_pulling:
            to_mouse = mouse_world_pos - self.position
            m_r_sq = to_mouse.length_squared()
            m_r = math.sqrt(m_r_sq) if m_r_sq > 0 else 0.01
            pull = MOUSE_PULL_STRENGTH / ((m_r_sq + MOUSE_PULL_EPSILON ** 2) ** 1.5)
            acc += to_mouse * pull * m_r  # scaled so nearby stars feel a strong, stable pull

        self.acceleration = acc
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def screen_color(self):
        return tuple(min(255, max(0, int(value * self.brightness))) for value in self.color)

def temperature_to_color(temperature):
    if temperature < 3500:
        return (255, 140, 90)
    elif temperature < 5000:
        return (255, 200, 140)
    elif temperature < 6000:
        return (255, 244, 214)
    elif temperature < 7500:
        return (255, 255, 255)
    elif temperature < 10000:
        return (200, 220, 255)
    else:
        return (155, 180, 255)

def project_2d(star, center, screen_center, camera_offset, zoom):
    rel = (star.position - center) * zoom
    screen_pos = screen_center + rel + camera_offset
    radius = max(1, round(star.radius * zoom))
    return screen_pos.x, screen_pos.y, radius, None

def unproject_2d(mouse_screen_pos, center, screen_center, camera_offset, zoom):
    rel = (mouse_screen_pos - screen_center - camera_offset) / zoom
    return center + rel

def project_3d(world_x, world_y, world_height, radius, center, screen_center, azimuth, elevation, zoom):
    x = world_x - center.x
    z = world_y - center.y   # galactic-plane 'depth' axis
    y = world_height         # vertical thickness axis
    x1 = x * math.cos(azimuth) - z * math.sin(azimuth)
    z1 = x * math.sin(azimuth) + z * math.cos(azimuth)
    y2 = y * math.cos(elevation) - z1 * math.sin(elevation)
    z2 = y * math.sin(elevation) + z1 * math.cos(elevation)
    z_cam = z2 + CAMERA_DISTANCE
    if z_cam < 10: 
        return None
    focal = BASE_FOCAL * zoom
    scale = focal / z_cam
    screen_x = screen_center.x + x1 * scale
    screen_y = screen_center.y - y2 * scale
    screen_radius = max(1, round(radius * scale))
    return screen_x, screen_y, screen_radius, z_cam

def create_galaxy(center_x, center_y):
    stars = []

    for _ in range(NUM_STARS):
        u = random.random()
        r = -R_DISK * math.log(1.0 - u + 1e-6) + 10  # avoid exact center
        arm_offset = (2 * math.pi / NUM_ARMS) * random.randint(0, NUM_ARMS - 1)
        base_angle = (1.0 / B_SPIRAL) * math.log(r / R_DISK) + arm_offset
        scatter = random.gauss(0, 0.25)
        angle = base_angle + scatter
        rel_x = r * math.cos(angle)
        rel_y = r * math.sin(angle)
        x = center_x + rel_x
        y = center_y + rel_y
        v_mag = math.sqrt(
            (G * M_CENTER + G * DARK_MATTER_HALO * r) / math.sqrt(r ** 2 + PLUMMER_EPSILON ** 2)
        )
        tan_x = -rel_y / r
        tan_y = rel_x / r
        vx = tan_x * v_mag
        vy = tan_y * v_mag

        if r < 40:
            temperature = random.uniform(6000, 9000)
            brightness = random.uniform(0.8, 1.0)
            age = random.uniform(1e9, 1e10)
        else:
            temperature = random.uniform(3000, 12000)
            brightness = random.uniform(0.5, 1.0)
            age = random.uniform(1e7, 1e10)

        color = temperature_to_color(temperature)
        mass = random.uniform(0.3, 3.0)
        radius = 1 if r > 40 else random.choice([1, 1, 2])

        height_scale = BULGE_HEIGHT_SCALE if r < 40 else DISK_HEIGHT_SCALE
        height = random.gauss(0, height_scale)
        stars.append(Star(x, y, vx, vy, mass, radius, brightness, temperature, color, age, height))
    return stars

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galaxy Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    center = pygame.Vector2(center_x, center_y)
    stars = create_galaxy(center_x, center_y)
    screen_center = pygame.Vector2(center_x, center_y)
    camera_offset = pygame.Vector2(0, 0)
    azimuth = 0.0
    elevation = 0.4  
    dragging = False
    drag_anchor_mouse = pygame.Vector2(0, 0)
    drag_anchor_offset = pygame.Vector2(0, 0)
    drag_anchor_azimuth = 0.0
    drag_anchor_elevation = 0.0
    zoom = 1.0
    view_mode = "2D"  
    mouse_pulling = False
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.1)  
        mouse_screen_pos = pygame.Vector2(pygame.mouse.get_pos())
        if view_mode == "2D":
            mouse_world_pos = unproject_2d(mouse_screen_pos, center, screen_center, camera_offset, zoom)
        else:
            mouse_world_pos = center  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_v:
                    view_mode = "3D" if view_mode == "2D" else "2D"
                    mouse_pulling = False  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    dragging = True
                    drag_anchor_mouse = mouse_screen_pos
                    drag_anchor_offset = camera_offset.copy()
                    drag_anchor_azimuth = azimuth
                    drag_anchor_elevation = elevation
                elif event.button == 3 and view_mode == "2D":  
                    mouse_pulling = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 3:
                    mouse_pulling = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    delta = mouse_screen_pos - drag_anchor_mouse
                    if view_mode == "2D":
                        camera_offset = drag_anchor_offset + delta
                    else:
                        azimuth = drag_anchor_azimuth + delta.x * ROTATE_SENSITIVITY
                        elevation = drag_anchor_elevation - delta.y * ROTATE_SENSITIVITY
                        elevation = max(-1.4, min(1.4, elevation)) 
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom = min(ZOOM_MAX, zoom * ZOOM_STEP)
                elif event.y < 0:
                    zoom = max(ZOOM_MIN, zoom / ZOOM_STEP)
        for star in stars:
            star.update_physics(dt, center, mouse_world_pos, mouse_pulling)
        screen.fill((5, 5, 12))
        if view_mode == "2D":
            for star in stars:
                sx, sy, sr, _ = project_2d(star, center, screen_center, camera_offset, zoom)
                pygame.draw.circle(screen, star.screen_color(), (int(sx), int(sy)), sr)
            bh_pos = screen_center + camera_offset
            pygame.draw.circle(screen, (255, 255, 220), (int(bh_pos.x), int(bh_pos.y)), 3)
            if mouse_pulling:
                pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 40, width=1)
        else:
            projected = []
            for star in stars:
                result = project_3d(
                    star.position.x, star.position.y, star.height, star.radius,
                    center, screen_center, azimuth, elevation, zoom,
                )
                if result is not None:
                    projected.append((result[3], result, star))
            projected.sort(key=lambda item: item[0], reverse=True)

            for _, (sx, sy, sr, _), star in projected:
                pygame.draw.circle(screen, star.screen_color(), (int(sx), int(sy)), sr)

            bh_result = project_3d(
                center.x, center.y, 0.0, 3,
                center, screen_center, azimuth, elevation, zoom,
            )
            if bh_result is not None:
                bx, by, br, _ = bh_result
                pygame.draw.circle(screen, (255, 255, 220), (int(bx), int(by)), max(3, br))

        controls = (
            "Drag LMB to pan | Hold RMB to pull stars"
            if view_mode == "2D"
            else "Drag LMB to orbit | Scroll to zoom"
        )
        info_text = font.render(
            f"FPS: {int(clock.get_fps())} | Stars: {len(stars)} | View: {view_mode} "
            f"(press V) | Zoom: {zoom:.2f}x | {controls}",
            True, (200, 200, 200),
        )
        screen.blit(info_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()