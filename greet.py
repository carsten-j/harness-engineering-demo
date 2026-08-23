import argparse


def greet(name: str, shout: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if shout else message


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="world")
    parser.add_argument("--shout", action="store_true", help="upper-case the output")
    args = parser.parse_args()
    print(greet(args.name, args.shout))  # noqa: T201
