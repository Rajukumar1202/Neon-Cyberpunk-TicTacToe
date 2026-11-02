
import pygame
import math
from audio import SoundEffects

# ==================================================
# CONFIGURATION
# ==================================================

WIDTH, HEIGHT = 720, 820

BG = (6, 9, 22)
PANEL = (15, 23, 43)
PANEL_LIGHT = (23, 36, 62)
CELL_BG = (12, 20, 39)

CYAN = (0, 245, 220)
PURPLE = (177, 91, 255)
PINK = (255, 65, 175)
WHITE = (235, 245, 255)
MUTED = (130, 150, 180)
GREEN = (80, 255, 160)
GRID = (39, 57, 87)

# Compact centered board
BOARD_X, BOARD_Y = 187, 325
CELL = 115
BOARD_SIZE = CELL * 3

AI_MOVE_EVENT = pygame.USEREVENT + 1
AI_DELAY = 700

pygame.font.init()

TITLE_FONT = pygame.font.SysFont("arial", 43, bold=True)
SUB_FONT = pygame.font.SysFont("arial", 12, bold=True)
LABEL_FONT = pygame.font.SysFont("arial", 14, bold=True)
MARK_FONT = pygame.font.SysFont("arial", 76, bold=True)
PLAYER_MARK_FONT = pygame.font.SysFont("arial", 31, bold=True)
BUTTON_FONT = pygame.font.SysFont("arial", 12, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 11, bold=True)
SCORE_FONT = pygame.font.SysFont("arial", 25, bold=True)
BODY_FONT = pygame.font.SysFont("arial", 13)

sounds = None
active_panel = None
tournament_choice = 3


# ==================================================
# SOUND
# ==================================================

def get_sounds():
    global sounds

    if sounds is None:
        sounds = SoundEffects()

    return sounds


# ==================================================
# DRAW HELPERS
# ==================================================

def draw_text(surface, value, font, color, center):
    image = font.render(str(value), True, color)
    surface.blit(image, image.get_rect(center=center))


def panel(surface, rect, fill, border, radius=14, width=1):
    pygame.draw.rect(
        surface, fill, rect, border_radius=radius
    )
    pygame.draw.rect(
        surface, border, rect,
        width=width, border_radius=radius
    )


def glow_rect(surface, rect, color, radius=14):
    layer = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    for i in range(3, 0, -1):
        expanded = rect.inflate(i * 4, i * 4)

        pygame.draw.rect(
            layer,
            (*color, 9),
            expanded,
            width=2,
            border_radius=radius + i * 2
        )

    surface.blit(layer, (0, 0))


def neon_text(surface, value, font, color, center):
    glow = font.render(str(value), True, color)
    glow.set_alpha(40)

    surface.blit(
        glow,
        glow.get_rect(center=(center[0] + 1, center[1] + 1))
    )

    draw_text(surface, value, font, color, center)


def draw_button(surface, rect, label, color, mouse_pos,
                enabled=True):

    hovered = rect.collidepoint(mouse_pos) and enabled

    fill = PANEL_LIGHT if hovered else PANEL

    if hovered:
        glow_rect(surface, rect, color, 10)

    panel(
        surface,
        rect,
        fill if enabled else (15, 21, 37),
        color if enabled else GRID,
        10,
        2 if enabled else 1
    )

    draw_text(
        surface,
        label,
        BUTTON_FONT,
        WHITE if enabled else MUTED,
        rect.center
    )


# ==================================================
# BACKGROUND
# ==================================================

def draw_background(screen, tick):

    screen.fill(BG)

    for x in range(0, WIDTH, 45):
        pygame.draw.line(
            screen, (13, 22, 40),
            (x, 0), (x, HEIGHT), 1
        )

    for y in range(0, HEIGHT, 45):
        pygame.draw.line(
            screen, (13, 22, 40),
            (0, y), (WIDTH, y), 1
        )

    light = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    pulse = int(7 + 5 * abs(math.sin(tick / 900)))

    pygame.draw.circle(
        light, (0, 220, 210, pulse),
        (65, 270), 190
    )

    pygame.draw.circle(
        light, (150, 65, 255, pulse),
        (660, 590), 200
    )

    screen.blit(light, (0, 0))

    for i in range(24):

        x = (i * 89 + 25) % WIDTH
        y = (i * 127 + int(tick * 0.018)) % HEIGHT

        brightness = int(
            75 + 90 * abs(math.sin(tick / 650 + i))
        )

        pygame.draw.circle(
            screen,
            (20, brightness, min(255, brightness + 35)),
            (x, int(y)),
            2
        )

    corner = (25, 90, 112)

    pygame.draw.line(screen, corner, (20, 25), (95, 25), 2)
    pygame.draw.line(screen, corner, (20, 25), (20, 62), 2)
    pygame.draw.line(screen, corner, (625, 25), (700, 25), 2)
    pygame.draw.line(screen, corner, (700, 25), (700, 62), 2)


# ==================================================
# HEADER
# ==================================================

def draw_header(screen):

    neon_text(
        screen, "TIC-TAC-TOE",
        TITLE_FONT, CYAN,
        (WIDTH // 2, 53)
    )

    draw_text(
        screen,
        "CYBER ARENA  /  NEON EDITION 3.1",
        SUB_FONT, MUTED,
        (WIDTH // 2, 96)
    )

    pygame.draw.circle(screen, GREEN, (125, 96), 3)

    draw_text(
        screen, "ONLINE",
        SMALL_FONT, MUTED,
        (160, 96)
    )

    pygame.draw.line(
        screen, (39, 59, 87),
        (65, 120), (655, 120), 1
    )


# ==================================================
# PLAYER CARDS
# ==================================================

def draw_player_card(screen, x, title, name, mark,
                     score, color, active):

    rect = pygame.Rect(x, 138, 190, 72)

    if active:
        glow_rect(screen, rect, color)

    panel(
        screen, rect, PANEL,
        color if active else GRID,
        13, 2 if active else 1
    )

    icon_rect = pygame.Rect(x + 12, 153, 40, 40)

    panel(
        screen, icon_rect,
        PANEL_LIGHT, color, 10, 1
    )

    # FIX: Small X/O icon in player card
    neon_text(
        screen, mark, PLAYER_MARK_FONT,
        color, icon_rect.center
    )

    draw_text(
        screen, title, SMALL_FONT,
        MUTED, (x + 111, 153)
    )

    draw_text(
        screen, name, LABEL_FONT,
        color, (x + 111, 177)
    )

    draw_text(
        screen, str(score), LABEL_FONT,
        WHITE, (x + 170, 165)
    )


def draw_scoreboard(screen, game):

    x_active = (
        game.current_player == "X"
        and not game.game_over
    )

    o_active = (
        game.current_player == "O"
        and not game.game_over
    )

    player1 = "YOU" if game.mode == "AI" else "PLAYER 1"
    player2 = "AI" if game.mode == "AI" else "PLAYER 2"

    draw_player_card(
        screen, 45, "PLAYER 01", player1,
        "X", game.score["X"], CYAN, x_active
    )

    draw_player_card(
        screen, 485, "PLAYER 02", player2,
        "O", game.score["O"], PURPLE, o_active
    )

    rect = pygame.Rect(263, 145, 194, 58)

    panel(screen, rect, PANEL, PINK, 12, 1)

    draw_text(
        screen, "DRAW MATCHES",
        SMALL_FONT, MUTED, (360, 161)
    )

    neon_text(
        screen, str(game.score["Draw"]),
        SCORE_FONT, PINK, (360, 184)
    )


# ==================================================
# SETTINGS
# ==================================================

def draw_settings(screen, game, mouse_pos):

    draw_button(
        screen,
        pygame.Rect(45, 225, 195, 43),
        "MODE / " + (
            "VS AI" if game.mode == "AI"
            else "2 PLAYERS"
        ),
        CYAN, mouse_pos
    )

    draw_button(
        screen,
        pygame.Rect(262, 225, 195, 43),
        "LEVEL / " + game.difficulty.upper(),
        PURPLE, mouse_pos,
        game.mode == "AI"
    )

    draw_button(
        screen,
        pygame.Rect(480, 225, 195, 43),
        "SOUND / " + (
            "ON" if game.sound_on else "OFF"
        ),
        PINK, mouse_pos
    )


# ==================================================
# STATUS AND AI PERSONALITY
# ==================================================

def draw_status(screen, game, tick):

    if game.game_over:

        if game.winner == "Draw":
            message = "MATCH DRAW"
            color = PINK

        elif game.winner == "X":
            message = (
                "PLAYER 1 WINS!"
                if game.mode == "TWO_PLAYER"
                else "YOU WIN!"
            )
            color = GREEN

        else:
            message = (
                "PLAYER 2 WINS!"
                if game.mode == "TWO_PLAYER"
                else "AI WINS!"
            )
            color = PURPLE

    elif game.current_player == "X":

        message = (
            "PLAYER 1 TURN / X"
            if game.mode == "TWO_PLAYER"
            else "YOUR TURN / PLACE X"
        )

        color = CYAN

    else:

        message = (
            "PLAYER 2 TURN / O"
            if game.mode == "TWO_PLAYER"
            else "AI THINKING / O"
        )

        color = PURPLE

    neon_text(
        screen, message,
        LABEL_FONT, color,
        (WIDTH // 2, 280)
    )

    # FIX: AI dialogue has its own visible space
    if game.mode == "AI":

        message = game.get_ai_message()

        if len(message) > 65:
            message = message[:62] + "..."

        draw_text(
            screen,
            message,
            SMALL_FONT,
            MUTED,
            (WIDTH // 2, 301)
        )


# ==================================================
# GAME BOARD
# ==================================================

def draw_board(screen, game, mouse_pos):

    outer = pygame.Rect(
        BOARD_X - 13,
        BOARD_Y - 13,
        BOARD_SIZE + 26,
        BOARD_SIZE + 26
    )

    glow_rect(screen, outer, CYAN, 20)

    panel(
        screen, outer, PANEL,
        (48, 74, 110), 20, 2
    )

    for row in range(3):
        for col in range(3):

            index = row * 3 + col

            cell_rect = pygame.Rect(
                BOARD_X + col * CELL + 5,
                BOARD_Y + row * CELL + 5,
                CELL - 10,
                CELL - 10
            )

            mark = game.board[index]

            can_click = (
                not mark
                and not game.game_over
                and (
                    game.mode != "AI"
                    or game.current_player == "X"
                )
            )

            hovered = (
                cell_rect.collidepoint(mouse_pos)
                and can_click
            )

            fill = PANEL_LIGHT if hovered else CELL_BG

            border = CYAN if hovered else GRID

            if mark == "X":
                border = (0, 115, 112)

            elif mark == "O":
                border = (101, 55, 145)

            if hovered:
                glow_rect(screen, cell_rect, CYAN, 12)

            panel(
                screen, cell_rect,
                fill, border, 13,
                2 if hovered else 1
            )

            if mark:

                color = CYAN if mark == "X" else PURPLE

                neon_text(
                    screen, mark,
                    MARK_FONT, color,
                    cell_rect.center
                )


# ==================================================
# FEATURE NAVIGATION
# ==================================================

def draw_feature_navigation(screen, mouse_pos):

    buttons = [
        (pygame.Rect(35, 720, 155, 34), "BADGES", CYAN),
        (pygame.Rect(200, 720, 155, 34), "REPLAY", PURPLE),
        (pygame.Rect(365, 720, 155, 34), "AI CHAT", PINK),
        (pygame.Rect(530, 720, 155, 34), "TOURNAMENT", GREEN)
    ]

    for rect, label, color in buttons:
        draw_button(
            screen, rect, label, color, mouse_pos
        )


def draw_footer(screen, mouse_pos):

    pygame.draw.line(
        screen, GRID,
        (100, 764), (620, 764), 1
    )

    draw_button(
        screen,
        pygame.Rect(145, 775, 195, 38),
        "NEW ROUND  [ R ]",
        CYAN, mouse_pos
    )

    draw_button(
        screen,
        pygame.Rect(380, 775, 195, 38),
        "RESET SCORES",
        PINK, mouse_pos
    )


# ==================================================
# MODAL BACKGROUND
# ==================================================

def draw_modal(screen, title, accent):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 195))
    screen.blit(overlay, (0, 0))

    rect = pygame.Rect(55, 265, 610, 340)

    glow_rect(screen, rect, accent, 20)

    panel(
        screen, rect, PANEL,
        accent, 20, 2
    )

    neon_text(
        screen, title,
        TITLE_FONT, accent,
        (WIDTH // 2, 305)
    )

    return rect


def draw_close_button(screen, mouse_pos):

    rect = pygame.Rect(580, 278, 65, 34)

    draw_button(
        screen, rect, "CLOSE",
        PINK, mouse_pos
    )


# ==================================================
# ACHIEVEMENT CENTER
# ==================================================

def draw_achievements(screen, game, mouse_pos):

    draw_modal(screen, "ACHIEVEMENTS", CYAN)
    draw_close_button(screen, mouse_pos)

    achievements = game.get_achievements()

    for i, item in enumerate(achievements):

        y = 350 + i * 43

        rect = pygame.Rect(90, y, 540, 36)

        color = GREEN if item["unlocked"] else GRID

        panel(
            screen, rect,
            PANEL_LIGHT if item["unlocked"] else CELL_BG,
            color, 8, 1
        )

        icon = "UNLOCKED" if item["unlocked"] else "LOCKED"

        draw_text(
            screen,
            item["name"],
            LABEL_FONT,
            WHITE if item["unlocked"] else MUTED,
            (220, y + 18)
        )

        draw_text(
            screen,
            icon,
            SMALL_FONT,
            color,
            (545, y + 18)
        )


# ==================================================
# REPLAY CONSOLE
# ==================================================

def draw_replay_board(screen, board):

    start_x = 245
    start_y = 355
    cell = 75

    for row in range(3):
        for col in range(3):

            index = row * 3 + col

            rect = pygame.Rect(
                start_x + col * cell,
                start_y + row * cell,
                cell - 5,
                cell - 5
            )

            mark = board[index]

            color = (
                CYAN if mark == "X"
                else PURPLE if mark == "O"
                else GRID
            )

            panel(
                screen, rect,
                CELL_BG, color, 8, 1
            )

            if mark:
                draw_text(
                    screen, mark,
                    MARK_FONT, color,
                    rect.center
                )


def draw_replay(screen, game, mouse_pos):

    draw_modal(screen, "REPLAY CONSOLE", PURPLE)
    draw_close_button(screen, mouse_pos)

    if not game.last_replay:

        draw_text(
            screen,
            "NO REPLAY AVAILABLE",
            LABEL_FONT,
            MUTED,
            (360, 460)
        )

        return

    replay = game.last_replay

    draw_text(
        screen,
        f"WINNER: {replay['winner']}",
        LABEL_FONT,
        GREEN if replay["winner"] == "X" else PURPLE,
        (360, 340)
    )

    draw_replay_board(
        screen, game.replay_board
    )

    total = len(replay["moves"])

    draw_text(
        screen,
        f"MOVE {game.replay_index} / {total}",
        LABEL_FONT,
        WHITE,
        (360, 590)
    )

    buttons = [
        (pygame.Rect(100, 625, 110, 35), "FIRST"),
        (pygame.Rect(220, 625, 110, 35), "PREVIOUS"),
        (pygame.Rect(390, 625, 110, 35), "NEXT"),
        (pygame.Rect(510, 625, 110, 35), "LAST")
    ]

    for rect, label in buttons:
        draw_button(
            screen, rect, label,
            PURPLE, mouse_pos
        )


# ==================================================
# AI PERSONALITY PANEL
# ==================================================

def draw_ai_panel(screen, game, mouse_pos):

    draw_modal(screen, "AI PERSONALITY", PINK)
    draw_close_button(screen, mouse_pos)

    draw_text(
        screen,
        "YOUR CYBER OPPONENT",
        LABEL_FONT,
        MUTED,
        (360, 365)
    )

    avatar = pygame.Rect(300, 390, 120, 85)

    panel(
        screen, avatar,
        PANEL_LIGHT, PURPLE, 18, 2
    )

    pygame.draw.circle(
        screen, CYAN, (330, 420), 8
    )

    pygame.draw.circle(
        screen, CYAN, (390, 420), 8
    )

    pygame.draw.line(
        screen, PINK,
        (340, 450), (380, 450), 3
    )

    message = game.get_ai_message()

    if len(message) > 65:
        message = message[:62] + "..."

    draw_text(
        screen,
        message,
        BODY_FONT,
        WHITE,
        (360, 510)
    )

    draw_text(
        screen,
        "DIFFICULTY: " + game.difficulty.upper(),
        SMALL_FONT,
        CYAN,
        (360, 550)
    )


# ==================================================
# TOURNAMENT ARENA
# ==================================================

def draw_tournament(screen, game, mouse_pos):

    draw_modal(screen, "TOURNAMENT ARENA", GREEN)
    draw_close_button(screen, mouse_pos)

    status = game.get_tournament_status()

    draw_text(
        screen,
        "SELECT TOURNAMENT FORMAT",
        LABEL_FONT,
        MUTED,
        (360, 355)
    )

    draw_button(
        screen,
        pygame.Rect(180, 375, 145, 42),
        "BEST OF 3",
        CYAN,
        mouse_pos,
        tournament_choice == 3
    )

    draw_button(
        screen,
        pygame.Rect(395, 375, 145, 42),
        "BEST OF 5",
        PURPLE,
        mouse_pos,
        tournament_choice == 5
    )

    if status["active"]:

        draw_text(
            screen,
            "TOURNAMENT IN PROGRESS",
            LABEL_FONT,
            GREEN,
            (360, 445)
        )

    elif status["champion"]:

        draw_text(
            screen,
            "CHAMPION: " + status["champion"],
            LABEL_FONT,
            GREEN,
            (360, 445)
        )

    else:

        draw_text(
            screen,
            "READY TO START",
            LABEL_FONT,
            MUTED,
            (360, 445)
        )

    draw_text(
        screen,
        f"X WINS: {status['wins']['X']}     "
        f"O WINS: {status['wins']['O']}     "
        f"DRAWS: {status['draws']}",
        LABEL_FONT,
        WHITE,
        (360, 485)
    )

    draw_text(
        screen,
        f"ROUNDS PLAYED: {status['rounds']}",
        SMALL_FONT,
        MUTED,
        (360, 515)
    )

    if status["active"]:

        draw_button(
            screen,
            pygame.Rect(245, 545, 230, 40),
            "END TOURNAMENT",
            PINK,
            mouse_pos
        )

    else:

        draw_button(
            screen,
            pygame.Rect(245, 545, 230, 40),
            "START TOURNAMENT",
            GREEN,
            mouse_pos
        )


# ==================================================
# MAIN DRAW FUNCTION
# ==================================================

def draw_game(screen, game):

    tick = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    draw_background(screen, tick)
    draw_header(screen)
    draw_scoreboard(screen, game)
    draw_settings(screen, game, mouse_pos)
    draw_status(screen, game, tick)
    draw_board(screen, game, mouse_pos)

    draw_feature_navigation(screen, mouse_pos)
    draw_footer(screen, mouse_pos)

    if active_panel == "ACHIEVEMENTS":
        draw_achievements(screen, game, mouse_pos)

    elif active_panel == "REPLAY":
        draw_replay(screen, game, mouse_pos)

    elif active_panel == "AI":
        draw_ai_panel(screen, game, mouse_pos)

    elif active_panel == "TOURNAMENT":
        draw_tournament(screen, game, mouse_pos)


# ==================================================
# FEATURE PANEL CLICK HANDLER
# ==================================================

def handle_panel_click(pos, game):

    global active_panel
    global tournament_choice

    close_rect = pygame.Rect(580, 278, 65, 34)

    if close_rect.collidepoint(pos):

        if active_panel == "REPLAY":
            game.stop_replay()

        active_panel = None
        return True

    if active_panel == "ACHIEVEMENTS":
        return True

    if active_panel == "REPLAY":

        if not game.last_replay:
            return True

        if pygame.Rect(100, 625, 110, 35).collidepoint(pos):
            game.replay_first()

        elif pygame.Rect(220, 625, 110, 35).collidepoint(pos):
            game.replay_previous()

        elif pygame.Rect(390, 625, 110, 35).collidepoint(pos):
            game.replay_next()

        elif pygame.Rect(510, 625, 110, 35).collidepoint(pos):
            game.replay_last()

        return True

    if active_panel == "AI":
        return True

    if active_panel == "TOURNAMENT":

        if pygame.Rect(180, 375, 145, 42).collidepoint(pos):
            tournament_choice = 3
            return True

        if pygame.Rect(395, 375, 145, 42).collidepoint(pos):
            tournament_choice = 5
            return True

        start_rect = pygame.Rect(245, 545, 230, 40)

        if start_rect.collidepoint(pos):

            status = game.get_tournament_status()

            if status["active"]:
                game.stop_tournament()

            else:
                game.start_tournament(tournament_choice)

            return True

        return True

    return False


# ==================================================
# MAIN CLICK HANDLER
# ==================================================

def handle_click(pos, game):

    global active_panel

    sound = get_sounds()

    if active_panel is not None:
        handle_panel_click(pos, game)
        return

    features = [
        (pygame.Rect(35, 720, 155, 34), "ACHIEVEMENTS"),
        (pygame.Rect(200, 720, 155, 34), "REPLAY"),
        (pygame.Rect(365, 720, 155, 34), "AI"),
        (pygame.Rect(530, 720, 155, 34), "TOURNAMENT")
    ]

    for rect, name in features:

        if rect.collidepoint(pos):

            if name == "REPLAY":

                if game.start_replay():
                    active_panel = "REPLAY"

                else:
                    game.set_ai_message(
                        "Play a complete match first!"
                    )

            else:
                active_panel = name

            if game.sound_on:
                sound.play("click")

            return

    mode_rect = pygame.Rect(45, 225, 195, 43)
    difficulty_rect = pygame.Rect(262, 225, 195, 43)
    sound_rect = pygame.Rect(480, 225, 195, 43)

    new_round_rect = pygame.Rect(145, 775, 195, 38)
    reset_rect = pygame.Rect(380, 775, 195, 38)

    # Mode
    if mode_rect.collidepoint(pos):

        pygame.time.set_timer(AI_MOVE_EVENT, 0)

        new_mode = (
            "TWO_PLAYER"
            if game.mode == "AI"
            else "AI"
        )

        game.set_mode(new_mode)

        if game.sound_on:
            sound.play("click")

        return

    # Difficulty
    if difficulty_rect.collidepoint(pos):

        if game.mode == "AI":

            game.cycle_difficulty()

            if game.sound_on:
                sound.play("click")

        return

    # Sound
    if sound_rect.collidepoint(pos):

        enabled = game.toggle_sound()
        sound.set_enabled(enabled)

        if enabled:
            sound.play("click")

        return

    # New round
    if new_round_rect.collidepoint(pos):

        pygame.time.set_timer(AI_MOVE_EVENT, 0)
        game.new_round()

        if game.sound_on:
            sound.play("click")

        return

    # Reset scores
    if reset_rect.collidepoint(pos):

        pygame.time.set_timer(AI_MOVE_EVENT, 0)
        game.reset_scores()

        if game.sound_on:
            sound.play("click")

        return

    if game.game_over:
        return

    if game.mode == "AI" and game.current_player != "X":
        return

    # Board click
    x, y = pos

    if (
        BOARD_X <= x < BOARD_X + BOARD_SIZE
        and BOARD_Y <= y < BOARD_Y + BOARD_SIZE
    ):

        col = (x - BOARD_X) // CELL
        row = (y - BOARD_Y) // CELL

        index = row * 3 + col

        if not game.play(index):
            return

        if game.sound_on:
            sound.play("move")

        if game.game_over:

            if game.sound_on:
                sound.play(
                    "draw" if game.winner == "Draw"
                    else "win" if game.winner == "X"
                    else "lose"
                )

            return

        if game.mode == "AI":

            pygame.time.set_timer(
                AI_MOVE_EVENT,
                AI_DELAY,
                loops=1
            )


# ==================================================
# AI MOVE HANDLER
# ==================================================

def handle_ai_move(game):

    pygame.time.set_timer(AI_MOVE_EVENT, 0)

    if (
        game.mode != "AI"
        or game.current_player != "O"
        or game.game_over
    ):
        return

    game.computer_move()

    if game.sound_on:

        sound = get_sounds()

        if game.game_over:
            sound.play(
                "draw" if game.winner == "Draw"
                else "lose"
            )
        else:
            sound.play("move")
