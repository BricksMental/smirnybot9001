from pathlib import Path
import json

import typer
from twitchio.ext import commands
import requests

from smirnybot9001.config import create_config_and_inject_values, CONFIG_PATH_OPTION, CHANNEL_OPTION, ADDRESS_OPTION, PORT_OPTION
from smirnybot9001.util import is_valid_set_number, is_valid_fig_number


class SmirnyBot9001ChatBot(commands.Bot):
    def __init__(self, token, channel, address, port, default_duration, prefix='!', ):
        super().__init__(token=token, prefix=prefix, initial_channels=[channel, ])
        self.address = address
        self.port = port
        self.default_duration = default_duration
        self.overlay_endpoint = f"http://{address}:{port}/"

    async def send_request(self, path, query=None):
        url = f"{self.overlay_endpoint}{path}"
        if query is not None:
            url = f"{url}?{query}"
        print(url)
        try:
            return requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Error getting {url}: {e}")

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def colors(self, ctx: commands.Context):
        await ctx.send(f"Find all LEGO colors and their BrickLink names at https://www.bricklink.com/catalogColors.asp")

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
        if not len(ctx.view.words) > 0:
            await ctx.send(usage)
            return

        number = ctx.view.words[1]
        if not is_valid_set_number(number):
            await ctx.send('Invalid set number')
            return

        duration = await extract_integer(ctx, position=2, default=self.default_duration)

        await self.send_request('set/number', f"value={number}")
        await self.send_request('set/duration', f"value={duration}")

        json_info = await self.send_request("set/display")
        info = json.loads(json_info.content)
        if info['description'] is not None:
            await ctx.send(info['description'])
        await ctx.send(info['bricklink_url'])

    @commands.command()
    async def fig(self, ctx: commands.Context):
        usage = "☠☠ Usage: !fig SETNR [DURATION] ☠☠"
        if not len(ctx.view.words) > 0:
            await ctx.send(usage)
            return

        number = ctx.view.words[1]

        if not is_valid_fig_number(number):
            await ctx.send('Invalid fig number')
            return

        duration = await extract_integer(ctx, position=2, default=self.default_duration)

        await self.send_request('fig/number', f"value={number}")
        await self.send_request('fig/duration', f"value={duration}")

        json_info = await self.send_request('fig/display')
        info = json.loads(json_info.content)
        await ctx.send(info['description'])
        await ctx.send(info['bricklink_url'])

    @commands.command()
    async def part(self, ctx: commands.Context):
        num_words = len(ctx.view.words)
        usage = "☠☠ Usage: !part PARTNR [COLOR] [DURATION] ☠☠"
        if num_words == 0 or num_words > 3:
            await ctx.send(usage)
            return

        number = ctx.view.words[1]
        color = 'NOCOLOR'

        if num_words == 1:
            duration = self.default_duration
        else:
            duration = await extract_integer(ctx, position=num_words, default=self.default_duration)
            if num_words == 3:
                color = ctx.view.words[2]

        await self.send_request('part/number', f"value={number}")
        await self.send_request('part/duration', f"value={duration}")
        await self.send_request('part/color', f"value={color}")

        json_info = await self.send_request('part/display')
        if json_info is None:
            await ctx.send(f"Unknown part: {number}")
        else:
            info = json.loads(json_info.content)
            await ctx.send(info['description'])
            # await ctx.send(info['bricklink_url'])

        await ctx.send(f"PART {number} Color {color} Duration {duration}")


async def extract_integer(ctx, position, default):
    value = default
    if len(ctx.view.words) >= position:
        try:
            value = int(ctx.view.words[position])
        except ValueError:
            await ctx.send(f"Not an integer: {ctx.view.words[position]}. Ignoring bad value")
    return value


def run_bot(config):
    bot = SmirnyBot9001ChatBot(config.token, config.channel, config.address, config.port, config.default_duration)
    bot.run()


def main():
    app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True, pretty_exceptions_enable=False)

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
