import pygame 
from .Visual_parser import get_visual_parser
from .Goo import 

class Visual: 
    args = get_visual_parser().parse_args()

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Initialize Game parameters from args
        self.width = self.args.w
        self.height = self.args.h
        self.fps = self.args.fps
        self.goos_limit = self.args.g
        self.bg_color = self.args.bg_color

        # Initialize Pygame screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The World of Goos")

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Coordinate transformation parameters
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Game state
        self.goos: list[Goo] = []
        self.new_goos: list[Goo] = []
        self.game_over = False
        self.game_won = False

        # Initialize platforms
        self.departure_platform = Platform(
            x=50,
            y=self.height - 100,

        )
        self.end_platform = Platform(
            x=self.width - 200,
            y=self.height - 100,

        )

        # Load images (with fallback to colored shapes)
        self.background_image = self._load_image("Assets/background_image.jpeg", (self.width, self.height))
        self.goo_image = self._load_image("Assets/goo_image.jpeg", (30, 30))

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Colors
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "gray": (128, 128, 128),
            "yellow": (255, 255, 0),
            "platform_start": (100, 200, 100),
            "platform_end": (200, 100, 100),
            "goo_color": (50, 150, 50),
            "line_color": (80, 80, 80),
        }

    def _load_image(self, path: str, size: tuple[int, int]) -> pygame.Surface | None:
        """Load an image from path with fallback to None."""
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
        except (pygame.error, FileNotFoundError):
            return None

    def draw_background(self):
        """Draw the background image or solid color."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            bg_color = self.colors.get(self.bg_color, self.colors["white"])
            self.screen.fill(bg_color)
        
    def draw_goos(self):
        """Draw all goos on the screen."""
        for goo in self.goos:
            screen_x, screen_y = self.maths_to_screen(goo.x, goo.y)

            if self.goo_image:
                # Center the image on the goo position
                image_rect = self.goo_image.get_rect(center=(screen_x, screen_y))
                self.screen.blit(self.goo_image, image_rect)
            else:
                return (pygame.error, FileNotFoundError)
        
    def draw_goo_counter(self):
        """Display the number of goos remaining."""
        goos_used = len(self.goos)
        goos_remaining = self.goos_limit - goos_used

        # Create counter text
        counter_text = f"Goos: {goos_used}/{self.goos_limit} (Remaining: {goos_remaining})"

        # Choose color based on remaining goos
        if goos_remaining <= 5:
            text_color = self.colors["red"]
        elif goos_remaining <= 15:
            text_color = self.colors["yellow"]
        else:
            text_color = self.colors["black"]

        # Render and display
        text_surface = self.font.render(counter_text, True, text_color)
        text_rect = text_surface.get_rect(topleft=(10, 10))

        # Draw background for better readability
        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(self.screen, (255, 255, 255, 180), bg_rect)
        pygame.draw.rect(self.screen, self.colors["black"], bg_rect, 1)

        self.screen.blit(text_surface, text_rect)
    
    
    
            

    def maths_to_screen(self, x: float, y: float) -> tuple[int, int]:
        """Convert mathematical coordinates to screen coordinates."""
        screen_x = int(x * self.scale + self.offset_x)
        screen_y = int(y * self.scale + self.offset_y)
        return (screen_x, screen_y)
    
    def screen_to_maths(self, screen_x: int, screen_y: int) -> tuple[float, float]:
        """Convert screen coordinates to mathematical coordinates."""
        x = (screen_x - self.offset_x) / self.scale
        y = (screen_y - self.offset_y) / self.scale
        return (x, y)
    
    def check_bridge_connected(self) -> bool:
        """Check if the bridge is connected between start and end platforms."""
        # actual connection check
        return False

    def check_win_condition(self) -> bool:
        """Check if the player has won (bridge connected)."""
        return self.check_bridge_connected()

    def check_lose_condition(self) -> bool:
        """Check if the player has lost (goo limit exceeded)."""
        return len(self.goos) >= self.goos_limit

        
    def update_events(self):


        # Handle Pygame events 
        for event in pygame.event.get():
            ## Exit the game 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            ## Mouse click -> create a goo 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                goos_limit_reached = len()
                if goos_limit_reached: 

                mouse_x, mouse_y = event.pos 
                math_x, math_y = self.screen_to_maths(mouse_x, mouse_y)
                
                new_goo = Goo(math_x, math_y)   #create a goo at (math_x, math_y) using a class Goo 
                display.new_goos.append(new_goo) #Add new_goo to the game goo list 

            ## End of the game (LOSE)


            ## End of the game (WIN)  

        pygame.display.flip()       
        
        pass


    
    def end_of_the_game(self):
        #Implement win condition
        ## if the two bridges are connected 
        ###Display end of the game messsage
         
        #Implement lose condition 
        ## if the number of goos exceed the limit 
        ###Display end of the game messsage

        pass