import argparse

GREETINGS = {"en": "Hello", "da": "Hej"}


def greet(name: str, shout: bool = False, lang: str = "en") -> str:
    message = f"{GREETINGS[lang]}, {name}!"
    return message.upper() if shout else message


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="world")
    parser.add_argument("--shout", action="store_true", help="upper-case the output")
    parser.add_argument(
        "--lang", choices=sorted(GREETINGS), default="en", help="greeting language"
    )
    args = parser.parse_args()
    print(greet(args.name, args.shout, args.lang))  # noqa: T201
