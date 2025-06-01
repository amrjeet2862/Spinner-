import pygame
import random
import math
import sys
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinner - Time Twister - Advanced Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Load assets
def load_assets():
    assets = {}
    try:
        # Load images
        assets['background'] = pygame.Surface((WIDTH, HEIGHT))
        assets['background'].fill((30, 30, 50))
        
        # Era icons
        era_icons = [
            'maurya', 'mughal', 'british', 'freedom', 'modern', 'mythology', 'time_warp'
        ]
        for i, icon in enumerate(era_icons):
            try:
                assets[icon] = pygame.Surface((64, 64))
                assets[icon].fill(COLORS[i])
            except:
                assets[icon] = pygame.Surface((64, 64))
                assets[icon].fill(COLORS[i])
        
        # Character images
        characters = ['chanakya', 'laxmibai', 'gandhi', 'bose', 'aryabhata']
        for char in characters:
            try:
                assets[char] = pygame.Surface((100, 150))
                assets[char].fill((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
            except:
                assets[char] = pygame.Surface((100, 150))
                assets[char].fill((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
        
        # Load sounds
        sounds = ['spin_start', 'spin_stop', 'mission_start', 'token_earned']
        for sound in sounds:
            try:
                assets[sound] = mixer.Sound(f'sounds/{sound}.wav')
            except:
                # Create silent sound if file not found
                silent_sound = mixer.Sound(buffer=bytearray(44))
                assets[sound] = silent_sound
        
        # Load music
        try:
            assets['bg_music'] = 'music/background.mp3'
            mixer.music.load(assets['bg_music'])
            mixer.music.set_volume(0.5)
        except:
            pass
            
    except Exception as e:
        print(f"Error loading assets: {e}")
    
    return assets

# Game constants
COLORS = [
    (139, 69, 19),    # Ancient India (brown)
    (210, 105, 30),   # Medieval Period (chocolate)
    (220, 20, 60),    # Colonial Era (crimson)
    (255, 215, 0),    # Freedom Struggle (gold)
    (70, 130, 180),   # Modern India (steel blue)
    (138, 43, 226),   # Mythological Bonus (purple)
    (50, 205, 50)     # Time Warp (lime green)
]

ERAS = [
    {"name": "Ancient India", "period": "Maurya/Gupta Empire", "icon": "maurya"},
    {"name": "Medieval Period", "period": "Delhi Sultanate/Mughal Era", "icon": "mughal"},
    {"name": "Colonial Era", "period": "East India Company/British Raj", "icon": "british"},
    {"name": "Freedom Struggle", "period": "1857, 1942, 1947", "icon": "freedom"},
    {"name": "Modern India", "period": "1990s - Present", "icon": "modern"},
    {"name": "Mythological India", "period": "Ramayana/Mahabharata", "icon": "mythology"},
    {"name": "TIME WARP", "period": "Special Mission!", "icon": "time_warp"}
]

CHARACTERS = {
    "Ancient India": [
        {"name": "Chanakya", "unlocked": False, "image": "chanakya", "cost": 5},
        {"name": "Aryabhata", "unlocked": False, "image": "aryabhata", "cost": 3}
    ],
    "Medieval Period": [
        {"name": "Akbar", "unlocked": True, "image": None, "cost": 0},
        {"name": "Shivaji", "unlocked": False, "image": None, "cost": 4}
    ],
    "Freedom Struggle": [
        {"name": "Rani Laxmibai", "unlocked": False, "image": "laxmibai", "cost": 7},
        {"name": "Mahatma Gandhi", "unlocked": False, "image": "gandhi", "cost": 5},
        {"name": "Subhas Bose", "unlocked": False, "image": "bose", "cost": 6}
    ]
}

MISSIONS = {
    "Ancient India": [
        "Strategy: Arrange army in Chakravyuh formation",
        "Economy: Manage Mauryan empire's treasury",
        "Diplomacy: Negotiate with Seleucus Nicator"
    ],
    "Medieval Period": [
        "Architecture: Help build Taj Mahal",
        "Battle: Defend against Mongol invasions",
        "Trade: Manage spice trade routes"
    ],
    "Colonial Era": [
        "Stealth: Deliver messages to revolutionaries",
        "Rebellion: Organize 1857 uprising",
        "Economy: Boycott British goods"
    ],
    "Freedom Struggle": [
        "Protest: Lead Dandi March",
        "Diplomacy: Negotiate with British",
        "Underground: Run secret Congress radio"
    ],
    "Modern India": [
        "Space: Launch ISRO satellite",
        "Economy: Manage 1991 reforms",
        "Technology: Develop Aadhaar system"
    ],
    "Mythological India": [
        "Epic Battle: Fight in Kurukshetra",
        "Wisdom: Solve Yaksha's questions",
        "Quest: Find Sita in Lanka"
    ],
    "TIME WARP": [
        "Mixed Mission: Mughal architecture meets ISRO tech",
        "Crossover: Chanakya advises freedom fighters",
        "Anomaly: British face Mauryan army"
    ]
}

# Game state
class GameState:
    def __init__(self):
        self.spinner_angle = 0
        self.spin_speed = 0
        self.spinning = False
        self.selected_era = None
        self.selected_mission = None
        self.time_tokens = 0
        self.history_coins = 10  # Starting coins
        self.time_gems = 0
        self.unlocked_characters = []
        self.current_character = None
        self.mission_completed = False
        self.player_level = 1
        self.xp = 0
        self.sound_enabled = True
        self.music_enabled = True
        self.guild_name = ""
        self.guild_members = []
        
        # Multiplayer
        self.multiplayer_mode = False
        self.opponent_era = None
        self.opponent_score = 0
        self.player_score = 0
        
        # Educational facts
        self.facts = [
            "Did you know? Chandragupta Maurya defeated Seleucus Nicator in 305 BCE",
            "Fact: The Taj Mahal took 22 years and 20,000 workers to complete",
            "Trivia: The 1857 revolt began in Meerut on May 10th",
            "FYI: India's first satellite Aryabhata was launched in 1975",
            "History: The Quit India Movement began on August 8, 1942"
        ]
        self.current_fact = 0

# Particle effect for spinner
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, math.pi*2)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        self.size = max(0, self.size - 0.05)
    
    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Load fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

# Create game state
game_state = GameState()
assets = load_assets()

# Create buttons
spin_button = Button(WIDTH-180, HEIGHT-80, 160, 60, "SPIN", (50, 150, 50), (70, 200, 70))
continue_button = Button(WIDTH//2-80, HEIGHT-70, 160, 50, "CONTINUE", (150, 50, 50), (200, 70, 70))
character_button = Button(50, HEIGHT-70, 200, 50, "CHARACTERS", (100, 50, 150), (150, 70, 200))
multiplayer_button = Button(WIDTH-250, 30, 220, 50, "MULTIPLAYER DUEL", (50, 100, 150), (70, 140, 200))
guild_button = Button(WIDTH-250, 100, 220, 50, "GUILD CHALLENGE", (150, 100, 50), (200, 140, 70))

# Particles
particles = []

def add_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def update_particles():
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)

def draw_particles(surface):
    for particle in particles:
        particle.draw(surface)

def draw_spinner():
    # Draw spinner segments
    for i, era in enumerate(ERAS):
        start_angle = math.radians(game_state.spinner_angle + i * (360/len(ERAS)))
        end_angle = math.radians(game_state.spinner_angle + (i+1) * (360/len(ERAS)))
        
        # Draw segment
        pygame.draw.arc(screen, COLORS[i], 
                       (WIDTH//2-spinner_radius, HEIGHT//2-spinner_radius, 
                        spinner_radius*2, spinner_radius*2),
                       start_angle, end_angle, spinner_radius)
        
        # Draw triangular segments
        points = [
            (WIDTH//2, HEIGHT//2),
            (WIDTH//2 + spinner_radius * math.cos(start_angle),
             HEIGHT//2 + spinner_radius * math.sin(start_angle)),
            (WIDTH//2 + spinner_radius * math.cos(end_angle),
             HEIGHT//2 + spinner_radius * math.sin(end_angle))
        ]
        pygame.draw.polygon(screen, COLORS[i], points)
        
        # Draw era icon
        mid_angle = start_angle + (end_angle - start_angle)/2
        icon_pos = (
            WIDTH//2 + (spinner_radius * 0.6) * math.cos(mid_angle),
            HEIGHT//2 + (spinner_radius * 0.6) * math.sin(mid_angle)
        )
        
        try:
            icon = assets[era["icon"]]
            icon_rect = icon.get_rect(center=icon_pos)
            screen.blit(icon, icon_rect)
        except:
            pass
        
        # Draw era name
        name_pos = (
            WIDTH//2 + (spinner_radius * 0.85) * math.cos(mid_angle),
            HEIGHT//2 + (spinner_radius * 0.85) * math.sin(mid_angle)
        )
        
        era_text = font_small.render(era["name"].split()[0], True, WHITE)
        text_rect = era_text.get_rect(center=name_pos)
        screen.blit(era_text, text_rect)
    
    # Draw spinner center with animation
    center_color = GOLD if game_state.spinning else SILVER
    pygame.draw.circle(screen, center_color, (WIDTH//2, HEIGHT//2), 30)
    pygame.draw.circle(screen, BLACK, (WIDTH//2, HEIGHT//2), 30, 3)
    
    # Draw pointer
    pointer_pos = (WIDTH//2, HEIGHT//2 - spinner_radius - 20)
    pygame.draw.polygon(screen, (220, 20, 60), [
        pointer_pos,
        (pointer_pos[0]-15, pointer_pos[1]+25),
        (pointer_pos[0]+15, pointer_pos[1]+25)
    ])

def draw_ui():
    # Draw player info
    pygame.draw.rect(screen, (50, 50, 70), (20, 20, 300, 120), border_radius=10)
    
    level_text = font_medium.render(f"Level: {game_state.player_level}", True, WHITE)
    screen.blit(level_text, (40, 30))
    
    xp_text = font_small.render(f"XP: {game_state.xp}/100", True, WHITE)
    screen.blit(xp_text, (40, 60))
    
    coins_text = font_small.render(f"Coins: {game_state.history_coins}", True, GOLD)
    screen.blit(coins_text, (40, 85))
    
    gems_text = font_small.render(f"Time Gems: {game_state.time_gems}", True, (100, 200, 255))
    screen.blit(gems_text, (40, 110))
    
    # Draw current character
    if game_state.current_character:
        char_text = font_small.render(f"Character: {game_state.current_character}", True, WHITE)
        screen.blit(char_text, (WIDTH-200, 170))
    
    # Draw buttons
    spin_button.draw(screen)
    character_button.draw(screen)
    multiplayer_button.draw(screen)
    guild_button.draw(screen)
    
    # Draw mission info if selected
    if game_state.selected_era is not None:
        era = ERAS[game_state.selected_era]
        
        # Mission panel
        pygame.draw.rect(screen, (50, 50, 80), (WIDTH//2-250, HEIGHT-200, 500, 180), border_radius=15)
        pygame.draw.rect(screen, (100, 100, 120), (WIDTH//2-250, HEIGHT-200, 500, 180), 3, border_radius=15)
        
        # Era title
        era_title = font_large.render(f"{era['name']} - {era['period']}", True, COLORS[game_state.selected_era])
        screen.blit(era_title, (WIDTH//2 - era_title.get_width()//2, HEIGHT-190))
        
        # Mission description
        if game_state.selected_mission is None:
            mission_options = MISSIONS[era["name"]]
            for i, mission in enumerate(mission_options[:3]):  # Show max 3 options
                mission_rect = pygame.Rect(WIDTH//2-230, HEIGHT-150 + i*40, 460, 35)
                pygame.draw.rect(screen, (70, 70, 90), mission_rect, border_radius=5)
                pygame.draw.rect(screen, (120, 120, 140), mission_rect, 1, border_radius=5)
                
                mission_text = font_small.render(mission, True, WHITE)
                screen.blit(mission_text, (mission_rect.x + 10, mission_rect.y + 8))
        else:
            mission_text = font_medium.render(game_state.selected_mission, True, WHITE)
            screen.blit(mission_text, (WIDTH//2 - mission_text.get_width()//2, HEIGHT-150))
            
            # Mission progress if in progress
            if not game_state.mission_completed:
                pygame.draw.rect(screen, (80, 80, 80), (WIDTH//2-100, HEIGHT-100, 200, 20))
                progress = min(100, (pygame.time.get_ticks() % 3000) / 30)  # Fake progress for demo
                pygame.draw.rect(screen, (100, 200, 100), (WIDTH//2-100, HEIGHT-100, progress*2, 20))
                
                progress_text = font_small.render(f"{int(progress)}%", True, WHITE)
                screen.blit(progress_text, (WIDTH//2 - progress_text.get_width()//2, HEIGHT-95))
            else:
                reward_text = font_medium.render("Mission Complete! +50 Coins", True, GOLD)
                screen.blit(reward_text, (WIDTH//2 - reward_text.get_width()//2, HEIGHT-100))
                
                fact_text = font_small.render(game_state.facts[game_state.current_fact], True, (200, 200, 100))
                screen.blit(fact_text, (WIDTH//2 - fact_text.get_width()//2, HEIGHT-70))
        
        # Continue button
        continue_button.draw(screen)
    
    # Draw multiplayer info if in multiplayer mode
    if game_state.multiplayer_mode and game_state.opponent_era:
        pygame.draw.rect(screen, (80, 50, 50), (WIDTH//2-300, 30, 600, 100), border_radius=10)
        
        player_text = font_medium.render(f"You: {ERAS[game_state.selected_era]['name']} - Score: {game_state.player_score}", 
                                       True, WHITE)
        screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, 40))
        
        opponent_text = font_medium.render(f"Opponent: {ERAS[game_state.opponent_era]['name']} - Score: {game_state.opponent_score}", 
                                         True, WHITE)
        screen.blit(opponent_text, (WIDTH//2 - opponent_text.get_width()//2, 80))

def spin():
    if not game_state.spinning:
        game_state.spin_speed = random.uniform(20, 30)
        game_state.spinning = True
        game_state.selected_era = None
        game_state.selected_mission = None
        game_state.mission_completed = False
        
        # Play sound
        if game_state.sound_enabled:
            assets['spin_start'].play()
        
        # Add particles
        add_particles(WIDTH//2, HEIGHT//2, GOLD, 20)

def update_spinner():
    if game_state.spinning:
        game_state.spinner_angle = (game_state.spinner_angle + game_state.spin_speed) % 360
        game_state.spin_speed = max(0, game_state.spin_speed - 0.15)
        
        # Add slowdown particles
        if random.random() < 0.2:
            add_particles(
                WIDTH//2 + spinner_radius * math.cos(math.radians(game_state.spinner_angle)),
                HEIGHT//2 + spinner_radius * math.sin(math.radians(game_state.spinner_angle)),
                COLORS[int(game_state.spinner_angle / (360/len(ERAS))) % len(COLORS)]
            )
        
        if game_state.spin_speed <= 0:
            game_state.spinning = False
            
            # Determine selected era
            segment = 360 / len(ERAS)
            normalized_angle = (360 - game_state.spinner_angle) % 360
            game_state.selected_era = int(normalized_angle // segment)
            
            # Check for special bonuses
            if game_state.selected_era == 5:  # Bonus section
                game_state.time_tokens += 1
                if game_state.sound_enabled:
                    assets['token_earned'].play()
            elif game_state.selected_era == 6:  # Time Warp
                pass  # Special logic can be added here
            
            if game_state.sound_enabled:
                assets['spin_stop'].play()
            
            # Add celebration particles
            add_particles(WIDTH//2, HEIGHT//2, COLORS[game_state.selected_era], 30)

def start_mission(mission_index):
    era = ERAS[game_state.selected_era]
    mission_options = MISSIONS[era["name"]]
    
    if mission_index < len(mission_options):
        game_state.selected_mission = mission_options[mission_index]
        
        # Play mission start sound
        if game_state.sound_enabled:
            assets['mission_start'].play()
        
        # In a real game, this would launch the actual mission minigame
        # For demo, we'll just simulate completion after a delay
        pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 seconds for demo

def complete_mission():
    game_state.mission_completed = True
    game_state.history_coins += 50
    game_state.xp += 10
    game_state.current_fact = random.randint(0, len(game_state.facts)-1)
    
    # Level up check
    if game_state.xp >= 100:
        game_state.player_level += 1
        game_state.xp = 0
        game_state.time_gems += 1

def start_multiplayer_duel():
    game_state.multiplayer_mode = True
    game_state.opponent_era = random.randint(0, len(ERAS)-2)  # Exclude Time Warp
    game_state.player_score = 0
    game_state.opponent_score = 0
    
    # Spin for player's era
    spin()

def update_multiplayer():
    if game_state.multiplayer_mode and not game_state.spinning and game_state.selected_era is not None:
        # Simulate opponent's progress
        if random.random() < 0.02:  # 2% chance per frame to score
            game_state.opponent_score += 1
        
        # Player can score by clicking
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and random.random() < 0.1:
            game_state.player_score += 1
        
        # Check for winner
        if game_state.player_score >= 20 or game_state.opponent_score >= 20:
            if game_state.player_score >= 20:
                reward = 100
                result_text = "You Won! +100 Coins"
            else:
                reward = 30
                result_text = "You Lost! +30 Coins"
            
            game_state.history_coins += reward
            game_state.multiplayer_mode = False
            
            # Show result
            pygame.draw.rect(screen, (50, 50, 80), (WIDTH//2-200, HEIGHT//2-50, 400, 100), border_radius=15)
            result_surf = font_medium.render(result_text, True, GOLD)
            screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, HEIGHT//2 - 20))

def show_character_menu():
    pygame.draw.rect(screen, (50, 50, 80), (WIDTH//2-300, HEIGHT//2-250, 600, 500), border_radius=15)
    
    title = font_large.render("CHARACTER SELECTION", True, GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2-230))
    
    # Show characters by era
    y_offset = HEIGHT//2 - 180
    for era, chars in CHARACTERS.items():
        era_text = font_medium.render(f"{era}:", True, WHITE)
        screen.blit(era_text, (WIDTH//2-280, y_offset))
        y_offset += 40
        
        for i, char in enumerate(chars):
            char_rect = pygame.Rect(WIDTH//2-280 + (i%2)*300, y_offset + (i//2)*180, 280, 160)
            pygame.draw.rect(screen, (70, 70, 90), char_rect, border_radius=10)
            
            # Character image
            if char["image"] and char["image"] in assets:
                screen.blit(assets[char["image"]], (char_rect.x + 90, char_rect.y + 20))
            
            # Character info
            name_text = font_medium.render(char["name"], True, WHITE)
            screen.blit(name_text, (char_rect.x + 10, char_rect.y + 10))
            
            if char["unlocked"]:
                status_text = font_small.render("UNLOCKED", True, (100, 255, 100))
                select_text = font_small.render("(Click to select)", True, (200, 200, 255))
                screen.blit(status_text, (char_rect.x + 10, char_rect.y + 120))
                screen.blit(select_text, (char_rect.x + 10, char_rect.y + 140))
            else:
                cost_text = font_small.render(f"Cost: {char['cost']} Time Gems", True, (255, 255, 100))
                unlock_text = font_small.render("(Click to unlock)", True, (200, 200, 255))
                screen.blit(cost_text, (char_rect.x + 10, char_rect.y + 120))
                screen.blit(unlock_text, (char_rect.x + 10, char_rect.y + 140))
    
    # Close button
    close_button = Button(WIDTH//2-80, HEIGHT//2+220, 160, 40, "CLOSE", (150, 50, 50), (200, 70, 70))
    close_button.draw(screen)
    
    return close_button

def handle_character_menu_click(pos, event):
    for era, chars in CHARACTERS.items():
        for i, char in enumerate(chars):
            char_rect = pygame.Rect(WIDTH//2-280 + (i%2)*300, HEIGHT//2-180 + (i//2)*180, 280, 160)
            
            if char_rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                if char["unlocked"]:
                    game_state.current_character = char["name"]
                elif game_state.time_gems >= char["cost"]:
                    game_state.time_gems -= char["cost"]
                    CHARACTERS[era][i]["unlocked"] = True
                    game_state.unlocked_characters.append(char["name"])

def show_guild_menu():
    pygame.draw.rect(screen, (50, 50, 80), (WIDTH//2-300, HEIGHT//2-200, 600, 400), border_radius=15)
    
    title = font_large.render("GUILD CHALLENGES", True, (100, 200, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2-180))
    
    # Guild info
    if not game_state.guild_name:
        name_text = font_medium.render("Create or Join a Guild", True, WHITE)
        screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, HEIGHT//2-130))
        
        # Create guild button
        create_button = Button(WIDTH//2-120, HEIGHT//2-80, 240, 50, "CREATE GUILD", (50, 150, 50), (70, 200, 70))
        create_button.draw(screen)
        
        # Join guild button
        join_button = Button(WIDTH//2-120, HEIGHT//2-20, 240, 50, "JOIN GUILD", (50, 100, 150), (70, 140, 200))
        join_button.draw(screen)
        
        return create_button, join_button
    else:
        guild_text = font_medium.render(f"Guild: {game_state.guild_name}", True, WHITE)
        screen.blit(guild_text, (WIDTH//2 - guild_text.get_width()//2, HEIGHT//2-130))
        
        # Guild challenges
        challenges = [
            "Re-enact Plassey Battle (Reward: 200 Coins)",
            "Organize Dandi March (Reward: 150 Coins)",
            "Build Taj Mahal (Reward: 100 Coins)"
        ]
        
        for i, challenge in enumerate(challenges):
            challenge_rect = pygame.Rect(WIDTH//2-250, HEIGHT//2-80 + i*60, 500, 50)
            pygame.draw.rect(screen, (70, 70, 90), challenge_rect, border_radius=10)
            
            challenge_text = font_medium.render(challenge, True, WHITE)
            screen.blit(challenge_text, (challenge_rect.x + 10, challenge_rect.y + 15))
    
    # Close button
    close_button = Button(WIDTH//2-80, HEIGHT//2+150, 160, 40, "CLOSE", (150, 50, 50), (200, 70, 70))
    close_button.draw(screen)
    
    return close_button

def main():
    global spinner_radius
    spinner_radius = 220
    
    # Start background music
    if game_state.music_enabled and 'bg_music' in assets:
        mixer.music.play(-1)
    
    clock = pygame.time.Clock()
    running = True
    show_characters = False
    show_guild = False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.USEREVENT:
                complete_mission()
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
            
            # Check button clicks
            if not show_characters and not show_guild:
                if spin_button.is_clicked(mouse_pos, event) and not game_state.spinning:
                    spin()
                
                if character_button.is_clicked(mouse_pos, event):
                    show_characters = True
                
                if multiplayer_button.is_clicked(mouse_pos, event) and not game_state.multiplayer_mode:
                    start_multiplayer_duel()
                
                if guild_button.is_clicked(mouse_pos, event):
                    show_guild = True
                
                if continue_button.is_clicked(mouse_pos, event) and game_state.selected_era is not None:
                    if game_state.mission_completed:
                        game_state.selected_era = None
                        game_state.selected_mission = None
                    elif game_state.selected_mission is None:
                        # Check mission selection
                        era = ERAS[game_state.selected_era]
                        mission_options = MISSIONS[era["name"]]
                        
                        for i in range(min(3, len(mission_options))):
                            mission_rect = pygame.Rect(WIDTH//2-230, HEIGHT-150 + i*40, 460, 35)
                            if mission_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                                start_mission(i)
            
            # Character menu
            elif show_characters:
                close_button = show_character_menu()
                if close_button.is_clicked(mouse_pos, event):
                    show_characters = False
                else:
                    handle_character_menu_click(mouse_pos, event)
            
            # Guild menu
            elif show_guild:
                if game_state.guild_name:
                    close_button = show_guild_menu()
                    if close_button.is_clicked(mouse_pos, event):
                        show_guild = False
                else:
                    create_button, join_button = show_guild_menu()
                    if create_button.is_clicked(mouse_pos, event):
                        game_state.guild_name = "Time Travelers"
                        game_state.guild_members = ["Player1", "Player2", "Player3"]  # Demo
                    elif join_button.is_clicked(mouse_pos, event):
                        game_state.guild_name = "History Buffs"
                        game_state.guild_members = ["PlayerA", "PlayerB", "You"]  # Demo
        
        # Update game state
        update_spinner()
        update_particles()
        
        if game_state.multiplayer_mode:
            update_multiplayer()
        
        # Check hover states
        if not show_characters and not show_guild:
            spin_button.check_hover(mouse_pos)
            character_button.check_hover(mouse_pos)
            multiplayer_button.check_hover(mouse_pos)
            guild_button.check_hover(mouse_pos)
            
            if game_state.selected_era is not None:
                continue_button.check_hover(mouse_pos)
        
        # Draw everything
        screen.blit(assets['background'], (0, 0))
        
        draw_spinner()
        draw_particles(screen)
        draw_ui()
        
        if show_characters:
            show_character_menu()
        
        if show_guild:
            show_guild_menu()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()