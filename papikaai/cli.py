import click

from papikaai.bots import PapikaAIBot


@click.command()
def main():
    bot = PapikaAIBot()
    bot.run()

if __name__ == "__main__":
    main()
