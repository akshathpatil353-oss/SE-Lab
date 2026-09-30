import pygame
import io
import math
import struct
import wave

from .player import Player
from .platform import Platform
from .hazard import Hazard


# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # ---------------------------------------------------------
        # TASK 3: Difficulty settings
        # ---------------------------------------------------------

        self.difficulties = {
            "Easy": {
                "gravity": 0.45,
                "jump_strength": -11,
            },
            "Medium": {
                "gravity": 0.60,
                "jump_strength": -12,
            },
            "Hard": {
                "gravity": 0.85,
                "jump_strength": -13,
            },
        }

        # Start with the existing/default Medium difficulty.
        self.difficulty = "Medium"
        self.gravity = self.difficulties[self.difficulty]["gravity"]

        self.start_x, self.start_y = 40, height - 120

        self.player = Player(
            self.start_x,
            self.start_y
        )

        self.player.jump_strength = (
            self.difficulties[self.difficulty]["jump_strength"]
        )

        # ---------------------------------------------------------
        # Existing level
        # ---------------------------------------------------------

        ground_y = height - 40

        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]

        self.hazards = [
            Hazard(240, ground_y - 14, 100)
        ]

        self.goal_x = 740

        self.score = 0

        # ---------------------------------------------------------
        # Fonts
        # ---------------------------------------------------------

        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

        self.game_over_font = pygame.font.SysFont(
            "Arial",
            54,
            bold=True
        )

        self.game_over_score_font = pygame.font.SysFont(
            "Arial",
            36,
            bold=True
        )

        self.game_over_option_font = pygame.font.SysFont(
            "Arial",
            28
        )

        self.game_over_instruction_font = pygame.font.SysFont(
            "Arial",
            22
        )

        self.game_over = False

        # ---------------------------------------------------------
        # TASK 4: Sound initialization
        # ---------------------------------------------------------

        self._init_sounds()

    # =============================================================
    # TASK 4: SOUND SYSTEM
    # =============================================================

    def _init_sounds(self):
        """
        Initialize the Pygame mixer and create simple sound effects
        programmatically.

        No external sound files are required.
        """

        if not pygame.mixer.get_init():
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=1,
                buffer=512
            )

        # Jump: short high-pitched tone.
        self.jump_sound = self._make_tone(
            frequency=650,
            duration=0.08,
            volume=0.35
        )

        # Goal: slightly longer higher-pitched tone.
        self.goal_sound = self._make_tone(
            frequency=1000,
            duration=0.12,
            volume=0.35
        )

        # Death: lower-pitched tone.
        self.death_sound = self._make_tone(
            frequency=180,
            duration=0.25,
            volume=0.40
        )

    @staticmethod
    def _make_tone(frequency, duration, volume):
        """
        Generate a simple mono WAV tone in memory and convert it
        into a Pygame Sound object.
        """

        sample_rate = 44100

        sample_count = int(
            sample_rate * duration
        )

        samples = bytearray()

        for i in range(sample_count):
            sample = math.sin(
                2
                * math.pi
                * frequency
                * i
                / sample_rate
            )

            value = int(
                32767
                * volume
                * sample
            )

            samples.extend(
                struct.pack("<h", value)
            )

        wav_buffer = io.BytesIO()

        with wave.open(
            wav_buffer,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            wav_file.writeframes(samples)

        return pygame.mixer.Sound(
            buffer=wav_buffer.getvalue()
        )

    # =============================================================
    # INPUT / EVENTS
    # =============================================================

    def handle_event(self, event):

        # ---------------------------------------------------------
        # TASK 3: Replay / difficulty selection
        # ---------------------------------------------------------

        if self.game_over:

            if event.type == pygame.KEYDOWN:

                # Easy
                if event.key in (
                    pygame.K_e,
                    pygame.K_1
                ):
                    self.start_new_game("Easy")
                    return

                # Medium
                if event.key in (
                    pygame.K_m,
                    pygame.K_2
                ):
                    self.start_new_game("Medium")
                    return

                # Hard
                if event.key in (
                    pygame.K_h,
                    pygame.K_3
                ):
                    self.start_new_game("Hard")
                    return

                # Exit
                if event.key in (
                    pygame.K_x,
                    pygame.K_4,
                    pygame.K_ESCAPE
                ):
                    pygame.event.post(
                        pygame.event.Event(
                            pygame.QUIT
                        )
                    )
                    return

            return

        # ---------------------------------------------------------
        # Existing jump input + TASK 4 jump sound
        # ---------------------------------------------------------

        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w,
        ):

            # Only play the jump sound when an actual jump occurs.
            # This prevents repeated sounds while the player is
            # already in the air.
            if self.player.on_ground:
                self.player.jump()
                self.jump_sound.play()

    def handle_input(self):

        # Do not process movement after Game Over.
        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.player.vx = 0

        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        ):
            self.player.vx = -self.player.speed

        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):
            self.player.vx = self.player.speed

    # =============================================================
    # TASK 3: START NEW GAME
    # =============================================================

    def start_new_game(self, difficulty):
        """
        Reset the game using the selected difficulty.
        """

        self.difficulty = difficulty

        # Apply selected physics.
        self.gravity = (
            self.difficulties[difficulty]["gravity"]
        )

        self.player.jump_strength = (
            self.difficulties[difficulty]["jump_strength"]
        )

        # Reset player position.
        self.player.x = self.start_x
        self.player.y = self.start_y

        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False

        # Reset score.
        self.score = 0

        # Leave Game Over state.
        self.game_over = False

    # =============================================================
    # GAME UPDATE
    # =============================================================

    def update(self):

        if self.game_over:
            return

        self.player.vy += self.gravity

        self.player.x = max(
            0,
            self.player.x + self.player.vx
        )

        # ---------------------------------------------------------
        # TASK 1: Collision Detection
        # ---------------------------------------------------------
        #
        # IMPORTANT:
        # This is the Task 1 swept vertical collision logic.
        # Do not replace it with a simple post-movement
        # colliderect() check.
        # ---------------------------------------------------------

        previous_y = self.player.y

        # Move player.
        self.player.y += self.player.vy

        self.player.on_ground = False

        # Calculate player's bottom position before and after
        # movement.
        previous_bottom = (
            previous_y
            + self.player.height
        )

        current_bottom = (
            self.player.y
            + self.player.height
        )

        # Check whether the player's path crossed the top of
        # a platform during this frame.
        for platform in self.platforms:

            platform_rect = platform.rect()

            horizontal_overlap = (
                self.player.x
                < platform_rect.right
                and
                self.player.x
                + self.player.width
                > platform_rect.left
            )

            crossed_platform = (
                previous_bottom
                <= platform_rect.top
                and
                current_bottom
                >= platform_rect.top
            )

            if (
                self.player.vy >= 0
                and horizontal_overlap
                and crossed_platform
            ):

                self.player.y = (
                    platform.y
                    - self.player.height
                )

                self.player.vy = 0

                self.player.on_ground = True

                break

        # ---------------------------------------------------------
        # TASK 2 + TASK 4: Hazard / Death
        # ---------------------------------------------------------

        if any(
            self.player.rect().colliderect(
                hazard.rect()
            )
            for hazard in self.hazards
        ):

            self.game_over = True

            # TASK 4:
            # Play death sound exactly when Game Over is triggered.
            self.death_sound.play()

            return

        # ---------------------------------------------------------
        # TASK 2 + TASK 4: Falling off the screen
        # ---------------------------------------------------------

        if self.player.y > self.height:

            self.game_over = True

            # TASK 4:
            # Play death sound exactly when Game Over is triggered.
            self.death_sound.play()

            return

        # ---------------------------------------------------------
        # Existing goal/scoring behavior + TASK 4
        # ---------------------------------------------------------

        if self.player.x >= self.goal_x:

            self.score += 1

            # TASK 4:
            # Play goal sound only when the score actually increases.
            self.goal_sound.play()

            # Existing behavior: reset player after reaching goal.
            self.player.x = self.start_x
            self.player.y = self.start_y

            self.player.vy = 0

    # =============================================================
    # RENDER
    # =============================================================

    def render(self, screen):

        # ---------------------------------------------------------
        # Existing world rendering
        # ---------------------------------------------------------

        for platform in self.platforms:

            pygame.draw.rect(
                screen,
                BROWN,
                platform.rect()
            )

        for hazard in self.hazards:

            pygame.draw.rect(
                screen,
                RED,
                hazard.rect()
            )

        goal_rect = pygame.Rect(
            self.goal_x,
            0,
            6,
            self.height
        )

        pygame.draw.rect(
            screen,
            GREEN,
            goal_rect
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.player.rect()
        )

        # Score.
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # ---------------------------------------------------------
        # TASK 2 + TASK 3: Game Over / Replay screen
        # ---------------------------------------------------------

        if self.game_over:

            # Dark transparent overlay.
            overlay = pygame.Surface(
                (
                    self.width,
                    self.height
                )
            )

            overlay.set_alpha(180)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            # Game Over title.
            game_over_text = (
                self.game_over_font.render(
                    "GAME OVER",
                    True,
                    WHITE
                )
            )

            game_over_rect = (
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        75
                    )
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            # Final score.
            final_score_text = (
                self.game_over_score_font.render(
                    f"Final Score: {self.score}",
                    True,
                    WHITE
                )
            )

            final_score_rect = (
                final_score_text.get_rect(
                    center=(
                        self.width // 2,
                        140
                    )
                )
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            # -----------------------------------------------------
            # Task 3 replay options
            # -----------------------------------------------------

            easy_text = (
                self.game_over_option_font.render(
                    "E - Easy",
                    True,
                    WHITE
                )
            )

            medium_text = (
                self.game_over_option_font.render(
                    "M - Medium",
                    True,
                    WHITE
                )
            )

            hard_text = (
                self.game_over_option_font.render(
                    "H - Hard",
                    True,
                    WHITE
                )
            )

            exit_text = (
                self.game_over_option_font.render(
                    "X - Exit",
                    True,
                    WHITE
                )
            )

            screen.blit(
                easy_text,
                easy_text.get_rect(
                    center=(
                        self.width // 2,
                        220
                    )
                )
            )

            screen.blit(
                medium_text,
                medium_text.get_rect(
                    center=(
                        self.width // 2,
                        270
                    )
                )
            )

            screen.blit(
                hard_text,
                hard_text.get_rect(
                    center=(
                        self.width // 2,
                        320
                    )
                )
            )

            screen.blit(
                exit_text,
                exit_text.get_rect(
                    center=(
                        self.width // 2,
                        370
                    )
                )
            )

            # Instruction.
            instruction_text = (
                self.game_over_instruction_font.render(
                    "Choose a difficulty to play again, or exit.",
                    True,
                    WHITE
                )
            )

            instruction_rect = (
                instruction_text.get_rect(
                    center=(
                        self.width // 2,
                        435
                    )
                )
            )

            screen.blit(
                instruction_text,
                instruction_rect
            )