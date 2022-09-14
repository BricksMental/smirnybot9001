from pathlib import Path

import typer
from twitchio.ext import commands
import requests

from smirnybot9001.config import CONFIG_PATH_OPTION, CHANNEL_OPTION, ADDRESS_OPTION, PORT_OPTION


class SmirnyBot9001ChatBot(commands.Bot):
    def __init__(self, token, channel, address, port, prefix='!', ):
        super().__init__(token=token, prefix=prefix, initial_channels=(channel, ))
        self.address = address
        self.port = port
        self.overlay_endpoint = f"http://{address}:{port}/"

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def greasy(self, ctx: commands.Context):
        await ctx.send('!so GreasyFro')

    @commands.command()
    async def vr(self, ctx: commands.Context):
        await ctx.send('!so vrgamer4life')

    @commands.command()
    async def chilli(self, ctx: commands.Context):
        await ctx.send('!so ChilliBrie')
        await ctx.send('Welcome the lovely ChilliBrie!')

    @commands.command()
    async def ll(self, ctx: commands.Context):
        await ctx.send('!so legolegend66')
        await ctx.send('Welcome the lovely LegoLegend66!')

    @commands.command()
    async def set(self, ctx: commands.Context):
        usage = "☠☠ Usage: !set SETNR [DURATION] ☠☠"
        print(ctx.view.words)
        if not len(ctx.view.words):
            await ctx.send(usage)
            return
        number = ctx.view.words[1]
        await ctx.send(f"☠Got set number {number}")
        url = self.overlay_endpoint + f"set/number?value={number}"
        print(url)
        requests.get(url)
        url = self.overlay_endpoint + f"set/display"
        print(url)
        requests.get(url)

    @commands.command()
    async def fig(self, ctx: commands.Context):
        usage = "☠☠ Usage: !fig SETNR [DURATION] ☠☠"
        print(ctx.view.words)
        if not len(ctx.view.words):
            await ctx.send(usage)
            return
        number = ctx.view.words[1]
        await ctx.send(f"☠Got minifig number {number}")
        url = self.overlay_endpoint + f"fig/number?value={number}"
        print(url)
        requests.get(url)
        url = self.overlay_endpoint + f"fig/display"
        print(url)
        requests.get(url)


def run_bot(token, channel, address, port):
    bot = SmirnyBot9001ChatBot(token, channel, address, port)
    bot.run()


def main():
    app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True, pretty_exceptions_show_locals=False)

    @app.command()
    def start(config_path: Path = CONFIG_PATH_OPTION,
              channel: str = CHANNEL_OPTION,
              address: str = ADDRESS_OPTION,
              port: int = PORT_OPTION,
              ):
        from smirnybot9001.config import parse_config
        config = parse_config(config_path)

        token = config['chatbot']['token']

        if not channel:
            channel = config['chatbot']['channel']

        run_bot(token, channel, address, port)

    app(help_option_names=('-h', '--help'))


if __name__ == '__main__':
    main()
