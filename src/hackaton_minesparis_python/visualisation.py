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

        self.background = (235, 235, 235)
        self.goo_color = (60, 140, 60)
        self.link_color = (80, 80, 80)
        self.text_color = (20, 20, 20)

        self.link_distance = 30.0
        self.platform_attach_distance = 35.0
        self.goo_radius = 8

        self.font = pygame.font.Font(None, 32)
        self.large_font = pygame.font.Font(None, 48)

        self.game_over = False
        self.game_won = False

    def _create_platforms(self) -> tuple[Platform, Platform]:
        h = self.height
        start = np.array(
            [
                [50, h - 140],
                [220, h - 140],
                [220, h - 80],
                [50, h - 80],
            ],
            dtype=float,
        )
        end = np.array(
            [
                [self.width - 220, h - 140],
                [self.width - 50, h - 140],
                [self.width - 50, h - 80],
                [self.width - 220, h - 80],
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

    def _update_neighbors(self) -> None:
        goos = list(self.world.goos)
        for goo in goos:
            goo._voisins = []
        for i, goo in enumerate(goos):
            for j in range(i + 1, len(goos)):
                other = goos[j]
                if distance(goo.pos, other.pos) <= self.link_distance:
                    goo._voisins.append(other)
                    other._voisins.append(goo)

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
                x, y = event.pos
                new_goo = Goo([x, y], self.world)
                self.world.new_goos(new_goo)

    def _reset(self) -> None:
        self.world = World()
        self.world.new_platforms(self.platform_start)
        self.world.new_platforms(self.platform_end)
        self.game_over = False
        self.game_won = False

    def _draw_platform(self, platform: Platform) -> None:
        pygame.draw.polygon(self.screen, platform.color, platform.sommets, width=0)
        pygame.draw.polygon(self.screen, (40, 40, 40), platform.sommets, width=2)

    def _draw_goos(self) -> None:
        for goo in self.world.goos:
            x, y = int(goo.pos[0]), int(goo.pos[1])
            pygame.draw.circle(self.screen, self.goo_color, (x, y), self.goo_radius)

    def _draw_links(self) -> None:
        for goo in self.world.goos:
            for v in goo.voisins:
                pygame.draw.line(
                    self.screen,
                    self.link_color,
                    (int(goo.pos[0]), int(goo.pos[1])),
                    (int(v.pos[0]), int(v.pos[1])),
                    2,
                )

    def _draw_status(self) -> None:
        if self.game_over:
            msg = "Victoire !" if self.game_won else "Perdu !"
            text = self.large_font.render(msg, True, self.text_color)
            rect = text.get_rect(center=(self.width // 2, 40))
            self.screen.blit(text, rect)

    def run(self) -> None:
        while True:
            self._handle_events()

            if len(self.world.goos) > 0:
                self._update_neighbors()
                self.world.step()

            if not self.game_over:
                if self._check_connected():
                    self.game_over = True
                    self.game_won = True

            self.screen.fill(self.background)
            self._draw_platform(self.platform_start)
            self._draw_platform(self.platform_end)
            self._draw_links()
            self._draw_goos()
            self._draw_status()

            pygame.display.flip()
            self.clock.tick(self.fps)
