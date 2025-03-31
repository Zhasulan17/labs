import pygame
import sys
from typing import Tuple, Optional


class Brush:
    def __init__(self):
        self.color = (0, 0, 255)  
        self.size = 5
        self.drawing = False
        self.start_pos: Optional[Tuple[int, int]] = None
        self.mode = "brush" 

    def start_drawing(self, pos: Tuple[int, int]):
        self.drawing = True
        self.start_pos = pos

    def stop_drawing(self):
        self.drawing = False
        self.start_pos = None

    def change_size(self, change: int):
        self.size = max(1, self.size + change)

    def set_color(self, color: Tuple[int, int, int]):
        self.color = color

    def set_mode(self, mode: str):
        self.mode = mode

    def draw(self, surface: pygame.Surface, current_pos: Tuple[int, int]):
        if not self.drawing or not self.start_pos:
            return

        if self.mode == "brush":
            pygame.draw.line(surface, self.color, self.start_pos, current_pos, self.size)
            pygame.draw.circle(surface, self.color, current_pos, self.size // 2)
            self.start_pos = current_pos

        elif self.mode == "eraser":
            pygame.draw.line(surface, (255, 255, 255), self.start_pos, current_pos, self.size)
            pygame.draw.circle(surface, (255, 255, 255), current_pos, self.size // 2)
            self.start_pos = current_pos

    def draw_shape_preview(self, surface: pygame.Surface, current_pos: Tuple[int, int]):
        if not self.drawing or not self.start_pos:
            return

        x1, y1 = self.start_pos
        x2, y2 = current_pos
        width = x2 - x1
        height = y2 - y1

        if self.mode == "rect":
            pygame.draw.rect(surface, self.color, (x1, y1, width, height), 2)
        elif self.mode == "circle":
            radius = int(((width)**2 + (height)**2)**0.5 / 2)
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            pygame.draw.circle(surface, self.color, center, radius, 2)


class PaintApp:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Paint App for Students")
        self.canvas = pygame.Surface((width, height))  
        self.background_color = (255, 255, 255)
        self.canvas.fill(self.background_color)

        self.colors = {
            'r': (255, 0, 0),
            'g': (0, 255, 0),
            'b': (0, 0, 255),
            'k': (0, 0, 0),
            'w': (255, 255, 255)
        }

        self.brush = Brush()
        self.font = pygame.font.Font(None, 24)
        self.preview = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.brush.start_drawing(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.brush.mode in ["rect", "circle"] and self.brush.start_pos:
                        self.brush.draw_shape_preview(self.canvas, event.pos)
                    self.brush.stop_drawing()
            elif event.type == pygame.MOUSEMOTION:
                if self.brush.drawing:
                    if self.brush.mode in ["brush", "eraser"]:
                        self.brush.draw(self.canvas, event.pos)
                    else:
                        self.preview = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                self.brush.change_size(event.y)
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in self.colors:
                    self.brush.set_color(self.colors[key])
                elif event.key == pygame.K_c:
                    self.canvas.fill(self.background_color)
                elif event.key == pygame.K_e:
                    self.brush.set_mode("eraser")
                elif event.key == pygame.K_p:
                    self.brush.set_mode("brush")
                elif event.key == pygame.K_z:  
                    self.brush.set_mode("rect")
                elif event.key == pygame.K_o:
                    self.brush.set_mode("circle")
        return True

    def instructions(self):
        instructions = [
            "Z: RECT | O: CIRCLE | P: BRUSH | E: ERASER",
            "C: CLEAR SCREEN",
            "R: RED | G: GREEN | B: BLUE | K: BLACK | W: WHITE",
            "MOUSE WHEEL: CHANGE BRUSH SIZE",
            f"Current: size {self.brush.size}, mode {self.brush.mode}"
        ]
        for i, text in enumerate(instructions):
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (10, 10 + i * 25))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.screen.blit(self.canvas, (0, 0))

            if self.brush.drawing and self.brush.mode in ["rect", "circle"] and self.preview:
                self.brush.draw_shape_preview(self.screen, self.preview)

            self.instructions()
            pygame.display.flip()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = PaintApp()
    app.run()
