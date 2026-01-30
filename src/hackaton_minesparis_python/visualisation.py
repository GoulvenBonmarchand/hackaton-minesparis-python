import pygame
import numpy as np
from dataclasses import dataclass

from hackaton_minesparis_python.world import World
from hackaton_minesparis_python.goo import Goo
from hackaton_minesparis_python.math_goo import distance


@dataclass
class Platform:
    sommets: np.ndarray
    color: tuple[int, int, int]


class Visualisation:
    def __init__(self, width: int = 1000, height: int = 600, fps: int = 24):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("World of Goos")
        self.clock = pygame.time.Clock()

        self.world = World()
        self.platform_start, self.platform_end = self._create_platforms()
        self.world.new_platforms(self.platform_start)
        self.world.new_platforms(self.platform_end)

        self.bg_color = (18, 22, 30)
        self.goo_color = (84, 186, 120)
        self.link_color = (200, 220, 240)
        self.text_color = (235, 235, 235)
        self.panel_color = (30, 36, 46)

        self.link_distance = 60.0
        self.platform_attach_distance = 35.0
        self.min_spawn_distance = 14.0
        self.goo_radius = 8
        self.goo_limit = 40

        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.large_font = pygame.font.SysFont("Segoe UI Semibold", 42)

        self.game_over = False
        self.game_won = False
        self.click_cooldown_ms = 250
        self._last_click_ms = 0
        self._last_state = {}

    def _create_platforms(self) -> tuple[Platform, Platform]:
        h = self.height
        start = np.array(
            [
                [60, h - 140],
                [240, h - 140],
                [240, h - 80],
                [60, h - 80],
            ],
            dtype=float,
        )
        end = np.array(
            [
                [self.width - 240, h - 140],
                [self.width - 60, h - 140],
                [self.width - 60, h - 80],
                [self.width - 240, h - 80],
            ],
            dtype=float,
        )
        return (
            Platform(start, (120, 200, 120)),
            Platform(end, (200, 120, 120)),
        )

    def _distance_point_segment(self, p: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
        ab = b - a
        ap = p - a
        denom = float(ab @ ab)
        if denom == 0.0:
            return float(np.linalg.norm(ap))
        t = max(0.0, min(1.0, float((ap @ ab) / denom)))
        proj = a + t * ab
        return float(np.linalg.norm(p - proj))

    def _distance_point_platform(self, p: np.ndarray, platform: Platform) -> float:
        sommets = platform.sommets
        min_dist = float("inf")
        for i in range(len(sommets)):
            a = sommets[i]
            b = sommets[(i + 1) % len(sommets)]
            min_dist = min(min_dist, self._distance_point_segment(p, a, b))
        return min_dist

    def _connect_new_goo(self, new_goo: Goo) -> None:
        for other in self.world.goos:
            if other is new_goo:
                continue
            if distance(new_goo.pos, other.pos) <= self.link_distance:
                new_goo._voisins.append(other)
                other._voisins.append(new_goo)

    def _can_place(self, pos: tuple[int, int]) -> bool:
        if self.game_over:
            return False
        if len(self.world.goos) >= self.goo_limit:
            return False
        x, y = pos
        if x < self.goo_radius or x > self.width - self.goo_radius:
            return False
        if y < self.goo_radius or y > self.height - self.goo_radius:
            return False
        probe = np.array([x, y], dtype=float)
        for other in self.world.goos:
            if np.allclose(probe, other.pos, atol=1e-6):
                return False
            if distance(probe, other.pos) < self.min_spawn_distance:
                return False
        return True

    def _check_connected(self) -> bool:
        goos = list(self.world.goos)
        if not goos:
            return False
        start_nodes = [
            g
            for g in goos
            if self._distance_point_platform(g.pos, self.platform_start)
            <= self.platform_attach_distance
        ]
        end_nodes = {
            g
            for g in goos
            if self._distance_point_platform(g.pos, self.platform_end)
            <= self.platform_attach_distance
        }
        if not start_nodes or not end_nodes:
            return False
        queue = list(start_nodes)
        seen = set(start_nodes)
        while queue:
            g = queue.pop(0)
            if g in end_nodes:
                return True
            for v in g.voisins:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        return False

    def _reset(self) -> None:
        self.world = World()
        self.world.new_platforms(self.platform_start)
        self.world.new_platforms(self.platform_end)
        self.game_over = False
        self.game_won = False

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset()
                if event.key == pygame.K_q:
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                now_ms = pygame.time.get_ticks()
                if now_ms - self._last_click_ms < self.click_cooldown_ms:
                    continue
                self._last_click_ms = now_ms
                x, y = event.pos
                if not self._can_place((x, y)):
                    continue
                new_goo = Goo([x, y], self.world)
                self.world.new_goos(new_goo)
                self._connect_new_goo(new_goo)

    def _draw_platform(self, platform: Platform) -> None:
        pygame.draw.polygon(self.screen, platform.color, platform.sommets, width=0)
        pygame.draw.polygon(self.screen, (230, 230, 230), platform.sommets, width=2)

    def _draw_goos(self) -> None:
        for goo in self.world.goos:
            if not np.all(np.isfinite(goo.pos)):
                continue
            x, y = int(goo.pos[0]), int(goo.pos[1])
            pygame.draw.circle(self.screen, (10, 15, 20), (x + 2, y + 2), self.goo_radius + 1)
            pygame.draw.circle(self.screen, self.goo_color, (x, y), self.goo_radius)

    def _draw_links(self) -> None:
        for goo in self.world.goos:
            for v in goo.voisins:
                if goo.id >= v.id:
                    continue
                if not np.all(np.isfinite(goo.pos)) or not np.all(np.isfinite(v.pos)):
                    continue
                pygame.draw.line(
                    self.screen,
                    self.link_color,
                    (int(goo.pos[0]), int(goo.pos[1])),
                    (int(v.pos[0]), int(v.pos[1])),
                    2,
                )

    def _snapshot_state(self) -> None:
        self._last_state = {
            goo.id: (goo.pos.copy(), goo.vit.copy()) for goo in self.world.goos
        }

    def _restore_if_nan(self) -> None:
        for goo in self.world.goos:
            if not np.all(np.isfinite(goo.pos)) or not np.all(np.isfinite(goo.vit)):
                prev = self._last_state.get(goo.id)
                if prev is not None:
                    goo.pos = prev[0]
                    goo.vit = np.zeros_like(prev[1])

    def _draw_hud(self) -> None:
        panel = pygame.Surface((340, 70))
        panel.fill(self.panel_color)
        self.screen.blit(panel, (10, 10))
        text = self.font.render(f"Goos: {len(self.world.goos)} / {self.goo_limit}", True, self.text_color)
        self.screen.blit(text, (20, 18))
        hint = self.font.render("Click: place  |  R: reset  |  Q: quit", True, self.text_color)
        self.screen.blit(hint, (20, 42))

    def _draw_status(self) -> None:
        if self.game_over:
            msg = "Victoire !" if self.game_won else "Perdu !"
            text = self.large_font.render(msg, True, self.text_color)
            rect = text.get_rect(center=(self.width // 2, 40))
            self.screen.blit(text, rect)

    def _draw_placement_indicator(self) -> None:
        mx, my = pygame.mouse.get_pos()
        allowed = self._can_place((mx, my))
        color = (80, 220, 120) if allowed else (220, 80, 80)
        pygame.draw.circle(self.screen, color, (mx, my), self.goo_radius + 2, 2)

    def run(self) -> None:
        while True:
            self._handle_events()

            if len(self.world.goos) > 0:
                self._snapshot_state()
                self.world.step()
                self._restore_if_nan()

            if not self.game_over and self._check_connected():
                self.game_over = True
                self.game_won = True
            elif not self.game_over and len(self.world.goos) >= self.goo_limit:
                self.game_over = True
                self.game_won = False

            self.screen.fill(self.bg_color)
            self._draw_platform(self.platform_start)
            self._draw_platform(self.platform_end)
            self._draw_links()
            self._draw_goos()
            self._draw_placement_indicator()
            self._draw_hud()
            self._draw_status()

            pygame.display.flip()
            self.clock.tick(self.fps)
