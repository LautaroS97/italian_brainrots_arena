import pygame, re
from utils import get_responsive_rect
from game.skill import Skill


class BattleUI:
    LIFE_COLOR   = (235, 16, 33)
    ENERGY_COLOR = (20, 198, 9)

    def __init__(self, screen, player1, player2):
        self.screen   = screen
        self.player1  = player1
        self.player2  = player2

        self.font        = pygame.font.Font("assets/fonts/upheavtt.ttf", 32)
        self.font_labels = pygame.font.Font("assets/fonts/upheavtt.ttf", 32)
        self.font_status = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)

        self.frame_life  = pygame.image.load("assets/sprites/props/life_bar.png").convert_alpha()
        self.frame_power = pygame.image.load("assets/sprites/props/power_bar.png").convert_alpha()

        self.buttons = [
            {"skill_idx": 0, "rect": get_responsive_rect(11.55, 14.14, 5.13, 3.6, screen)},
            {"skill_idx": 1, "rect": get_responsive_rect(16.68, 14.14, 5.13, 3.6, screen)},
            {"skill_idx": 2, "rect": get_responsive_rect(21.84, 14.14, 5.13, 3.6, screen)},
            {"skill_idx": 3, "rect": get_responsive_rect(26.95, 14.14, 5.13, 3.6, screen)},
        ]

        self.button_imgs = {
            0: pygame.image.load("assets/sprites/props/button_simple_attack.png").convert_alpha(),
            1: pygame.image.load("assets/sprites/props/button_defense.png").convert_alpha(),
            2: pygame.image.load("assets/sprites/props/button_growth_attack.png").convert_alpha(),
            3: pygame.image.load("assets/sprites/props/button_special_power.png").convert_alpha(),
        }
        self.button_inactive = pygame.image.load("assets/sprites/props/button_inactive.png").convert_alpha()

        self.disp_hp1 = self.player1.hp
        self.disp_en1 = self.player1.energy
        self.disp_hp2 = self.player2.hp
        self.disp_en2 = self.player2.energy

        self.buttons_enabled = True

        self.status_icons = {
            "Radiación":       pygame.image.load("assets/sprites/status/status_radiacion.png").convert_alpha(),
            "Mojado":          pygame.image.load("assets/sprites/status/status_mojado.png").convert_alpha(),
            "Mareado":         pygame.image.load("assets/sprites/status/status_mareado.png").convert_alpha(),
            "Veneno":          pygame.image.load("assets/sprites/status/status_veneno.png").convert_alpha(),
            "Debilitado 20%":  pygame.image.load("assets/sprites/status/status_debilitado20.png").convert_alpha(),
            "Debilitado 50%":  pygame.image.load("assets/sprites/status/status_debilitado50.png").convert_alpha(),
            "Debilitado 75%":  pygame.image.load("assets/sprites/status/status_debilitado75.png").convert_alpha(),
            "PP +25%":         pygame.image.load("assets/sprites/status/status_energyup25.png").convert_alpha(),
            "Anulado":         pygame.image.load("assets/sprites/status/status_nullify.png").convert_alpha(),
        }

        self._rect_en1 = self._rect_en2 = None

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _blit_with_shadow(self, text, font, pos, fg=(255, 255, 255), offset=(2, 2)):
        x, y = pos
        shadow = font.render(text, True, (0, 0, 0))
        surf   = font.render(text, True, fg)
        self.screen.blit(shadow, (x + offset[0], y + offset[1]))
        self.screen.blit(surf,   (x, y))

    # ------------------------------------------------------------------ #
    # Barras de vida / energía
    # ------------------------------------------------------------------ #
    def _draw_static_bar(self, cm_x, cm_y, cm_w, cm_h, value, max_value, color):
        s = self.screen
        full_rect = get_responsive_rect(cm_x, cm_y, cm_w, cm_h, s)
        filled_width = int(full_rect.width * (value / max_value))
        filled_rect = pygame.Rect(full_rect.x, full_rect.y, filled_width, full_rect.height)
        pygame.draw.rect(s, color, filled_rect, border_radius=5)
        return full_rect

    def _draw_bar_value(self, value, full_rect):
        txt = str(int(value))
        x   = full_rect.x + 5
        y   = full_rect.y + (full_rect.height - self.font.get_height()) // 2
        self._blit_with_shadow(txt, self.font, (x, y))

    def _draw_bars(self):
        s = self.screen
        s.blit(pygame.transform.scale(self.frame_life,
             get_responsive_rect(0.39, 0.56, 6.85, 1.2, s).size),
             get_responsive_rect(0.39, 0.56, 0, 0, s).topleft)
        s.blit(pygame.transform.scale(self.frame_power,
             get_responsive_rect(0.39, 2.0, 6.85, 1.2, s).size),
             get_responsive_rect(0.39, 2.0, 0, 0, s).topleft)
        s.blit(pygame.transform.scale(self.frame_life,
             get_responsive_rect(26.63, 0.56, 6.85, 1.2, s).size),
             get_responsive_rect(26.63, 0.56, 0, 0, s).topleft)
        s.blit(pygame.transform.scale(self.frame_power,
             get_responsive_rect(26.63, 2.0, 6.85, 1.2, s).size),
             get_responsive_rect(26.63, 2.0, 0, 0, s).topleft)

        rect_hp1 = self._draw_static_bar(0.67, 0.8, 5.14, 0.7,
                                         self.disp_hp1, self.player1.max_hp, self.LIFE_COLOR)
        rect_hp2 = self._draw_static_bar(26.9, 0.8, 5.14, 0.7,
                                         self.disp_hp2, self.player2.max_hp, self.LIFE_COLOR)
        rect_en1 = self._draw_static_bar(0.67, 2.24, 5.14, 0.7,
                                         self.disp_en1, self.player1.max_energy, self.ENERGY_COLOR)
        rect_en2 = self._draw_static_bar(26.9, 2.24, 5.14, 0.7,
                                         self.disp_en2, self.player2.max_energy, self.ENERGY_COLOR)

        self._rect_en1, self._rect_en2 = rect_en1, rect_en2

        self._draw_bar_value(self.player1.hp,     rect_hp1)
        self._draw_bar_value(self.player2.hp,     rect_hp2)
        self._draw_bar_value(self.player1.energy, rect_en1)
        self._draw_bar_value(self.player2.energy, rect_en2)

    # ------------------------------------------------------------------ #
    # Iconos de estados
    # ------------------------------------------------------------------ #
    def _draw_status_icons(self, brainrot, bar_rect):
        active = [e for e in brainrot.status_effects if not getattr(e, "cured", False)]
        if not active:
            return
        icon_h = int(bar_rect.height * 1.2)
        icon_w = icon_h
        gap_px = 4
        x = bar_rect.x
        y = bar_rect.bottom + 5
        for eff in active:
            ico = self.status_icons.get(eff.name)
            if not ico:
                continue
            surf = pygame.transform.scale(ico, (icon_w, icon_h))
            self.screen.blit(surf, (x, y))
            x += icon_w + gap_px

    # ------------------------------------------------------------------ #
    # Texto de estado
    # ------------------------------------------------------------------ #
    def _draw_status(self, text_animator):
        if not text_animator:
            return
        s = self.screen
        text = text_animator.get_display_text()
        area = get_responsive_rect(1.82, 14.24, 9.24, 3.4, s)
        x0, y = area.topleft
        base_color = (0, 0, 0)

        words, line, lines = text.split(" "), "", []
        for word in words:
            test = line + word + " "
            if self.font_status.size(test)[0] < area.width:
                line = test
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        for line in lines:
            x = x0
            for part in re.split(r"(\d+)", line):
                if part.isdigit():
                    self._blit_with_shadow(part, self.font_status, (x, y), fg=self.LIFE_COLOR)
                    x += self.font_status.size(part)[0]
                else:
                    surf = self.font_status.render(part, True, base_color)
                    s.blit(surf, (x, y))
                    x += surf.get_width()
            y += self.font_status.get_height()

    # ------------------------------------------------------------------ #
    # Botones de skills
    # ------------------------------------------------------------------ #
    def _draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        for idx, btn in enumerate(self.buttons):
            rect = btn["rect"]
            skill_idx = btn["skill_idx"]
            skill = self.player1.skills[skill_idx] if skill_idx < len(self.player1.skills) else None

            img_src = self.button_imgs.get(idx, self.button_inactive)
            img = pygame.transform.scale(
                self.button_inactive if not self.buttons_enabled else img_src,
                rect.size
            )
            self.screen.blit(img, rect.topleft)

            label_text = skill.name.upper() if skill else "VACÍO"
            words, lines, current = label_text.split(" "), [], ""
            for word in words:
                test = current + word + " "
                if self.font_labels.size(test)[0] < rect.width:
                    current = test
                else:
                    lines.append(current.strip())
                    current = word + " "
            lines.append(current.strip())

            total_h = len(lines) * self.font_labels.get_height()
            y_start = rect.y + (rect.height - total_h) // 2
            for i, line in enumerate(lines):
                surf   = self.font_labels.render(line, True, (255, 255, 255))
                shadow = self.font_labels.render(line, True, (0, 0, 0))
                x_cen  = rect.centerx - surf.get_width() // 2
                y_lbl  = y_start + i * self.font_labels.get_height()
                self.screen.blit(shadow, (x_cen + 2, y_lbl + 2))
                self.screen.blit(surf,   (x_cen,     y_lbl))

            if self.buttons_enabled and rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)

    # ------------------------------------------------------------------ #
    # Animación números suavizados
    # ------------------------------------------------------------------ #
    def _smooth_values(self, speed=0.18):
        self.disp_hp1 += (self.player1.hp     - self.disp_hp1) * speed
        self.disp_en1 += (self.player1.energy - self.disp_en1) * speed
        self.disp_hp2 += (self.player2.hp     - self.disp_hp2) * speed
        self.disp_en2 += (self.player2.energy - self.disp_en2) * speed

    # ------------------------------------------------------------------ #
    # Punto de entrada público
    # ------------------------------------------------------------------ #
    def draw(self, text_animator=None):
        self._smooth_values()
        self._draw_bars()
        if self._rect_en1 and self._rect_en2:
            self._draw_status_icons(self.player1, self._rect_en1)
            self._draw_status_icons(self.player2, self._rect_en2)
        self._draw_status(text_animator)
        self._draw_buttons()

    def handle_click(self, pos):
        if not self.buttons_enabled:
            return None
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                idx = btn["skill_idx"]
                return self.player1.skills[idx] if idx < len(self.player1.skills) else None
        return None