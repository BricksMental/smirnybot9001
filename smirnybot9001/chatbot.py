from pathlib import Path
import json

import typer
from twitchio.ext import commands
import requests

from smirnybot9001.config import create_config_and_inject_values, CONFIG_PATH_OPTION, CHANNEL_OPTION, ADDRESS_OPTION, PORT_OPTION


class SmirnyBot9001ChatBot(commands.Bot):
    def __init__(self, token, channel, address, port, prefix='!', ):
        super().__init__(token=token, prefix=prefix, initial_channels=[channel, ])
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
        if not len(ctx.view.words) > 0:
            await ctx.send(usage)
            return
        number = ctx.view.words[1]
        # await ctx.send(f"☠Got set number {number}")
        url = self.overlay_endpoint + f"set/number?value={number}"
        print(url)
        requests.get(url, timeout=5)
        try:
            duration = ctx.view.words[2]
            url = self.overlay_endpoint + f"set/duration?value={number}"
            print(url)
            requests.get(url, timeout=5)
        except KeyError:
            pass
        url = self.overlay_endpoint + f"set/display"
        print(url)
        json_info = requests.get(url, timeout=5).content
        info = json.loads(json_info)
        print(info)
        await ctx.send(info['description'])
        blu = info['bricklink_url']
        if blu is not None:
            await ctx.send(blu)
        #bsu = info['brickset_url']
        #if bsu is not None:
        #    await ctx.send(bsu)

    @commands.command()
    async def fig(self, ctx: commands.Context):
        usage = "☠☠ Usage: !fig SETNR [DURATION] ☠☠"
        print(ctx.view.words)
        if not len(ctx.view.words) > 0:
            await ctx.send(usage)
            return
        number = ctx.view.words[1]
        await ctx.send(f"☠Got minifig number {number}")
        url = self.overlay_endpoint + f"fig/number?value={number}"
        print(url)
        requests.get(url, timeout=5)
        url = self.overlay_endpoint + f"fig/display"
        print(url)
        json_info = requests.get(url, timeout=5).content
        info = json.loads(json_info)
        await ctx.send(info['description'])
        await ctx.send(info['bricklink_url'])


def run_bot(config):
    bot = SmirnyBot9001ChatBot(config.token, config.channel, config.address, config.port)
    bot.run()


def main():
    app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True, pretty_exceptions_show_locals=False)

    @app.command()
    def start(config_path: Path = CONFIG_PATH_OPTION,
              channel: str = CHANNEL_OPTION,
              address: str = ADDRESS_OPTION,
              port: int = PORT_OPTION,
              ):
        config = create_config_and_inject_values(config_path, locals())
        run_bot(config)

    app(help_option_names=('-h', '--help'))


if __name__ == '__main__':
    main()
