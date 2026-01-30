import argparse

def get_visual_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parameters for The World of Goos."
    )
    parser.add_argument(
        "--visual",
        action="store_true",
        help="Enable visual mode using Pygame.",
    )

    parser.add_argument(
        "--height", "-H", 
        type=int,
        default=600,  
        help="Height of the game window.",
    )

    parser.add_argument(
        "--width", "-w",
        type=int,
        default=800,  
        help="Width of the game window.",
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Frames per second for the game loop.",
    )

    parser.add_argument(
        "-g", "--goos",
        type=int,
        default=50,
        help="Limits of goos in the game.",
    )

    parser.add_argument(
        "--bg_color",
        type=str,
        default="white",
        help="Color of the Background.",
    )

    return parser