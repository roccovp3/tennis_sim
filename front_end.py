import pygame
import sys
from tennis import Match
from player import Player
import dynamic_gameplay

# filepath: /Users/rocco/git/tennis_sim/front_end.py

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class TennisSimulatorUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tennis Simulator")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Create players
        self.player_one = Player("Nadal", forehand_skill=0.85, backhand_skill=0.8, serve_skill=0.89, return_skill=0.9)
        self.player_two = Player("Federer", forehand_skill=0.9, backhand_skill=0.7, serve_skill=0.99, return_skill=0.8)
        
        # Create match
        self.match = Match(self.player_one, self.player_two)
        self.running = True
        self.paused = False
        self.speed_multiplier = 1

    def draw_court(self):
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, WHITE, (100, 100, 1000, 600), 2)
        pygame.draw.line(self.screen, WHITE, (600, 100), (600, 700), 2)
        pygame.draw.line(self.screen, WHITE, (100, 400), (1100, 400), 2)

    def draw_scores(self):
        # Match score (sets)
        sets_text = f"Sets: {self.match.player_one_sets_won} - {self.match.player_two_sets_won}"
        sets_surf = self.font_medium.render(sets_text, True, BLACK)
        self.screen.blit(sets_surf, (SCREEN_WIDTH // 2 - sets_surf.get_width() // 2, 20))

        # Current game score
        game_score = self.match.current_game_state.name.replace("SCORE", "").replace("_", " - ")
        game_text = f"Game: {game_score}"
        game_surf = self.font_small.render(game_text, True, BLACK)
        self.screen.blit(game_surf, (SCREEN_WIDTH // 2 - game_surf.get_width() // 2, 80))

        # Set scores
        for i, set_obj in enumerate(self.match.sets):
            set_text = f"Set {i+1}: {set_obj.score[0]} - {set_obj.score[1]}"
            set_surf = self.font_tiny.render(set_text, True, BLACK)
            self.screen.blit(set_surf, (50, 720 + i * 25))

    def draw_player_info(self):
        # Player one (left)
        p1_name = self.font_small.render(self.player_one.name, True, BLACK)
        self.screen.blit(p1_name, (50, 150))

        # Player two (right)
        p2_name = self.font_small.render(self.player_two.name, True, BLACK)
        self.screen.blit(p2_name, (SCREEN_WIDTH - 250, 150))

        # Server indicator
        server_name = self.match.server.name
        server_text = f"Serving: {server_name}"
        server_surf = self.font_small.render(server_text, True, YELLOW)
        self.screen.blit(server_surf, (SCREEN_WIDTH // 2 - server_surf.get_width() // 2, 720))

    def draw_ui(self):
        # Pause/Resume button area
        pause_text = "PAUSED" if self.paused else "RUNNING"
        pause_surf = self.font_tiny.render(pause_text, True, BLACK)
        self.screen.blit(pause_surf, (50, 50))

        # Speed multiplier
        speed_text = f"Speed: {self.speed_multiplier}x"
        speed_surf = self.font_tiny.render(speed_text, True, BLACK)
        self.screen.blit(speed_surf, (SCREEN_WIDTH - 200, 50))

        # Instructions
        instructions = [
            "SPACE: Pause/Resume",
            "UP/DOWN: Speed",
            "Q: Quit",
            "R: Reset"
        ]
        for i, instruction in enumerate(instructions):
            inst_surf = self.font_tiny.render(instruction, True, GRAY)
            self.screen.blit(inst_surf, (SCREEN_WIDTH - 300, 500 + i * 25))

    def reset_match(self):
        """Create a completely fresh match with new player instances"""
        self.player_one = Player("Nadal", forehand_skill=0.85, backhand_skill=0.8, serve_skill=0.89, return_skill=0.9)
        self.player_two = Player("Federer", forehand_skill=0.9, backhand_skill=0.7, serve_skill=0.99, return_skill=0.8)
        self.match = Match(self.player_one, self.player_two)
        self.paused = False
        self.speed_multiplier = 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.speed_multiplier = min(5, self.speed_multiplier + 1)
                elif event.key == pygame.K_DOWN:
                    self.speed_multiplier = max(1, self.speed_multiplier - 1)
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_match()

    def update(self):
        if not self.paused and self.match.winner is None:
            for _ in range(self.speed_multiplier):
                self.match.add_point(dynamic_gameplay.play_point(self.match))

    def draw(self):
        self.draw_court()
        self.draw_scores()
        self.draw_player_info()
        self.draw_ui()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ui = TennisSimulatorUI()
    ui.run()