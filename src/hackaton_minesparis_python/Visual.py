import pygame 
from .Visual_parser import get_visual_parser

class Visual: 
    args = get_visual_parser().parse_args()

    def __init__(self):
        # Initizalize Game parameters from args
        self.width=self.args.w
        self.height=self.args.h 
        self.fps=self.args.fps 
        self.goos_limit=self.args.g

        # Initialize Pygame screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The World of Goos")

        # Coordinate transformation parameters
        self.scale = 1.0 
        self.offset_x = 0 
        self.offset_y = 0
    

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
    
    def update_events(self):
        # Handle Pygame events 

        ## Mouse click -> create a goo 

        ## Exit the game 

        ## End of the game (LOSE)

        ## End of the game (WIN) 
        pass


    
    def end_of_the_game(self):
        #Implement win condition 
        #Implement lose condition 

        pass



