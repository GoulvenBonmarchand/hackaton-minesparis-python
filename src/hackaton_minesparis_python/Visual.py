import pygame 
from .Visual_parser import get_visual_parser
from .Goo import 

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



