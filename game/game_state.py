import os, random, pygame
from game.battle import BattleManager
from game.scenarios import SCENARIOS
from ui.battle_ui import BattleUI
from utils import get_responsive_rect, REF_WIDTH_CM, REF_HEIGHT_CM
from game.brainrots.vaca_saturno_saturnita import get_brainrot as _vaca
from game.brainrots.lirili_larila import get_brainrot as _lirili
from game.brainrots.bombardino_crocodilo import get_brainrot as _bombardino
from game.brainrots.br_br_patapim import get_brainrot as _patapim
from game.brainrots.tralalero_tralala import get_brainrot as _tralalero
from game.brainrots.tung_tung_sahur import get_brainrot as _tung

MESSAGE_DELAY_MS = 2000

_tmp = [(_vaca(), _vaca), (_lirili(), _lirili), (_bombardino(), _bombardino),
        (_patapim(), _patapim), (_tralalero(), _tralalero), (_tung(), _tung)]
_BRAINROT_FACTORIES = {i.name: fn for i, fn in _tmp}
del _tmp

WIN_LOSE_CHANNEL_ID = 3
VICTORY_DONE_EVENT = pygame.USEREVENT + 1

player1 = player2 = battle = battle_ui = None
background_img = platform_img = interface_img = None
text_animator = sound_manager = None
battle_has_ended = end_menu_ready = False
_message_queue = []
_message_timer = 0
_current_message = ""
_intro_sequence_pending = False
_intro_sequence_frame_counter = 0

def get_battle():
    return battle
def get_sound_manager():
    return sound_manager

class TextAnimator:
    def __init__(self, full_text, speed=25):
        self.full_text, self.speed = full_text, speed
        self.current_index = self.timer = 0
    def update(self, dt):
        self.timer += dt
        while self.timer >= self.speed and self.current_index < len(self.full_text):
            self.current_index += 1
            self.timer -= self.speed
    def is_finished(self):
        return self.current_index >= len(self.full_text)
    def get_display_text(self):
        return self.full_text[:self.current_index]
    def set_text(self, txt):
        self.full_text, self.current_index, self.timer = txt, 0, 0

def init_battle(selected_data, sm=None, opponent_name=None, scenario_data=None):
    global player1, player2, battle, battle_ui
    global background_img, platform_img, interface_img
    global text_animator, sound_manager, _message_queue, _current_message
    global _intro_sequence_pending, _intro_sequence_frame_counter
    global battle_has_ended, end_menu_ready

    name = selected_data["name"] if isinstance(selected_data, dict) else selected_data
    player1 = _BRAINROT_FACTORIES[name]()
    if opponent_name and opponent_name in _BRAINROT_FACTORIES:
        player2 = _BRAINROT_FACTORIES[opponent_name]()
    else:
        opp = random.choice([n for n in _BRAINROT_FACTORIES if n != player1.name])
        player2 = _BRAINROT_FACTORIES[opp]()

    player1.load_assets()
    player2.load_assets()

    w_px, h_px = player1._frames_idle[0].get_size()
    w_cm = w_px * (REF_WIDTH_CM / 1920)
    h_cm = h_px * (REF_HEIGHT_CM / 1080)
    cx_l = 7 + w_cm / 2
    cx_r = REF_WIDTH_CM - 7 - w_cm / 2
    cy = 2.86 + h_cm
    player1.pos, player1.flipped = (cx_l, cy), False
    player2.pos, player2.flipped = (cx_r, cy), True

    sound_manager = sm
    scr = pygame.display.get_surface()
    sw, sh = scr.get_size()
    battle_has_ended = end_menu_ready = False

    scn = scenario_data if scenario_data is not None else random.choice(SCENARIOS)
    background_img = pygame.transform.scale(
        pygame.image.load(scn["background"]).convert(), (sw, sh))
    platform_img = pygame.transform.scale(
        pygame.image.load(scn["platform"]).convert_alpha(),
        get_responsive_rect(0, 0, 10.92, 6, scr).size)
    key = os.path.basename(scn["background"]).replace("_landscape.png", "")
    interface_img = pygame.transform.scale(
        pygame.image.load(f"assets/sprites/menu/{key}_menu.png").convert_alpha(),
        get_responsive_rect(0, 0, 33.85, 5.97, scr).size)

    battle = BattleManager(player1, player2, sound_manager)
    battle.scenario = scn
    battle_ui = BattleUI(scr, player1, player2)

    _message_queue.clear()
    _message_queue.extend(battle.get_status_messages())
    _current_message = _message_queue.pop(0)
    text_animator = TextAnimator(_current_message)

    _intro_sequence_pending = True
    _intro_sequence_frame_counter = 0
    pygame.mixer.set_num_channels(max(WIN_LOSE_CHANNEL_ID + 1, pygame.mixer.get_num_channels()))
    pygame.mixer.Channel(WIN_LOSE_CHANNEL_ID).set_endevent(VICTORY_DONE_EVENT)

def draw_battle_placeholder(screen):
    screen.blit(background_img, (0, 0))
    screen.blit(platform_img, get_responsive_rect(6.15, 6.95, 0, 0, screen).topleft)
    screen.blit(platform_img, get_responsive_rect(16.79, 6.95, 0, 0, screen).topleft)

    front = None
    if player1._state == "skill" and not (player1._current_skill and player1._current_skill.render_behind_rival):
        front = player1
    elif player2._state == "skill" and not (player2._current_skill and player2._current_skill.render_behind_rival):
        front = player2

    if front is player1:
        player2.draw(screen)
        player1.draw(screen)
    elif front is player2:
        player1.draw(screen)
        player2.draw(screen)
    else:
        player1.draw(screen)
        player2.draw(screen)

    screen.blit(interface_img, get_responsive_rect(0.02, 13.05, 0, 0, screen).topleft)
    if battle_ui:
        battle_ui.draw(text_animator)

def handle_battle_event(event):
    global _message_queue, _current_message
    if text_animator and not text_animator.is_finished():
        return
    if event.type == pygame.KEYDOWN:
        key_to_idx = {pygame.K_a: 0, pygame.K_s: 1, pygame.K_d: 2, pygame.K_f: 3}
        if event.key in key_to_idx and battle.get_active_player() == player1:
            idx = key_to_idx[event.key]
            if idx < len(player1.skills):
                battle_ui.buttons_enabled = False
                battle.apply_action(player1.skills[idx])
                _message_queue = battle.get_status_messages()
                _current_message = _message_queue.pop(0)
                text_animator.set_text(_current_message)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and battle_ui:
        if battle.get_active_player() == player1:
            skill = battle_ui.handle_click(event.pos)
            if skill:
                battle_ui.buttons_enabled = False
                battle.apply_action(skill)
                _message_queue = battle.get_status_messages()
                _current_message = _message_queue.pop(0)
                text_animator.set_text(_current_message)

def update_battle_logic(dt):
    global _message_timer, _message_queue, _current_message
    global _intro_sequence_pending, _intro_sequence_frame_counter

    if battle:
        player1.update(dt)
        player2.update(dt)

    if _intro_sequence_pending:
        _intro_sequence_frame_counter += 1
        if _intro_sequence_frame_counter >= 2:
            _intro_sequence_pending = False
            if sound_manager:
                sound_manager.play_intro_sequence(player1.name, player2.name)

    if text_animator:
        text_animator.update(dt)
        if text_animator.is_finished():
            if _message_queue:
                _message_timer += dt
                if _message_timer >= MESSAGE_DELAY_MS:
                    _message_timer = 0
                    _current_message = _message_queue.pop(0)
                    text_animator.set_text(_current_message)
            else:
                _handle_end_of_battle()
                if not battle.is_game_over():
                    if battle.get_active_player() == player1:
                        battle_ui.buttons_enabled = True
                    else:
                        _handle_cpu_turn()

def _handle_end_of_battle():
    global battle_has_ended
    if not battle or not battle.is_game_over():
        return
    if not battle_has_ended:
        battle_has_ended = True
        if sound_manager:
            sound_manager.stop("fx_combat_curtain")
            battle.play_victory_sound()
            snd = "fx_win" if battle.winner == player1.name else "fx_lose"
            pygame.mixer.Channel(WIN_LOSE_CHANNEL_ID).play(sound_manager._get(snd))

def _handle_cpu_turn():
    global _message_queue, _current_message
    if battle.get_active_player() != player2 or battle.is_game_over():
        return
    pygame.time.delay(400)
    skill = random.choice(player2.skills)
    battle.apply_action(skill)
    _message_queue = battle.get_status_messages()
    if _message_queue:
        _current_message = _message_queue.pop(0)
        text_animator.set_text(_current_message)