# --- Paramètres Généraux ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 30
TITLE = "CRYPTRIS - DUEL MODE"

# --- États du Jeu ---
STATE_SPLASH = "SPLASH"
STATE_MENU = "MENU"
STATE_TUTORIAL = "TUTORIAL"
STATE_GAME = "GAME"
STATE_END = "END"

# --- Difficultés ---
DIFFICULTES = {
    "DEBUTANT (8 blocs)": 8,
    "NORMAL (12 blocs)": 12,
    "EXPERT (16 blocs)": 16,
}

KEY_PEAK_VALUE = 5  # Valeur du pic dans la clé privée
MARGIN = 4  # Petit espace entre les colonnes
BASE_LINE_Y = SCREEN_HEIGHT - 100  # Ligne de base pour dessiner les polynômes

# --- Paramètres DUEL ---
X_PLAYER = 350
X_BOT = 1050
BOT_SPEED = 2  # Vitesse de jeu du bot (plus grand = plus lent)

# --- Paramètres Visuels (CORRECTION ICI) ---

BLOCK_SIZE = 18  # Taille d'un bloc (carré représentant un coefficient)

# --- Couleurs ---
COLOR_BG = (5, 10, 20)
COLOR_POS = (0, 255, 255)
COLOR_NEG = (255, 0, 80)
COLOR_BOT_POS = (255, 165, 0)
COLOR_BOT_NEG = (100, 0, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (0, 200, 255)
