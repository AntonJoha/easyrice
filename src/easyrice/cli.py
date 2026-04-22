import argparse

from easyrice.Makeimage import make_image


def main() -> None:
    parser = argparse.ArgumentParser(description="Easy rice")
    parser.add_argument("-con", "--config", dest="config", type=str, help="Path to configuration file")
    parser.add_argument("-com", "--commands", dest="command", type=str, help="Path to command file")
    parser.add_argument("-d", "--dest", required=True, dest="dest", type=str, help="Path to save file")
    parser.add_argument("-s", "--src", dest="src", type=str, help="Path to source image")
    parser.add_argument(
        "-b",
        "--black",
        action="store_true",
        help="Render on a black background instead of an image",
    )
    args = parser.parse_args()

    source_image = None if args.black else args.src
    make_image(args.config, args.command, args.dest, source_image)

