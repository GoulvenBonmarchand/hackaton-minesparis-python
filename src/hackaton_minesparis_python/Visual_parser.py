import argparse 

def get_visual_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Visual parameters for The World of Goos."
    )
    parser.add_argument(
        "--visual",
        action="store_true",
        help="Enable visual mode using Pygame.",
    )

    parser.add_argument(
        "-h",
        type=int, 
        default=600
        help="Height of the game window.",
    )

    parser.add_argument(
        "-w",
        type=int, 
        default=800
        help="Width of the game window.",
    )

    parser.add_argument(
        "-fps",
        type=int, 
        default=30,
        help="Frames per second for the game loop.",
    )

    parser.add_argument(
        "-g",
        type=int, 
        default=50,
        help="Limits of goos in the game",
    )

    parser.add_argument(
        "-bg_color",
        type=str, 
        default="white",
        help="Color of the Background",
    )




    

    return parser