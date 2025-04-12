import fire


class Command:
    def init(self):
        """Initialize .pdk."""
        pass


def main():
    fire.Fire(Command)
