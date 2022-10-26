import json
from pathlib import Path

import requests
import typer
from twitchio.ext import commands

from smirnybot9001.color_table import get_color_table
from smirnybot9001.config import create_config_and_inject_values, CONFIG_PATH_OPTION, CHANNEL_OPTION, ADDRESS_OPTION, \
    PORT_OPTION, DEFAULT_DURATION, MAX_DURATION
from smirnybot9001.util import is_identifier

SYMBOLIC_PART_NAMES = {'frog': '33320',
                       'banana': '33085',
                       'octopus': '6086pb01',
                       'whale': '6086pb01',
                       }


class BadCommandValue(ValueError):
    pass


class SmirnyBot9001ChatBot(commands.Bot):
    def __init__(self, token, channel, overlay_endpoint, default_duration, prefix='!', ):
        super().__init__(token=token, prefix=prefix, initial_channels=[channel, ])
        self.overlay_endpoint = overlay_endpoint
        self.default_duration = default_duration
        self.color_table = get_color_table()

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
        try:
            number, duration = parse_set_command(ctx.view.words, self.default_duration)
        except BadCommandValue as e:
            await ctx.send(f"{e} ☠Usage: !set SETNR [DURATION]")
            return

        await self.send_request('set/number', f"value={number}")
        await self.send_request('set/duration', f"value={duration}")

        json_info = await self.send_request("set/display")
        info = json.loads(json_info.content)
        await ctx.send(f"{info['description']} {info['bricklink_url']}")

    @commands.command()
    async def fig(self, ctx: commands.Context):
        try:
            number, duration = parse_fig_command(ctx.view.words, self.default_duration)
        except BadCommandValue as e:
            await ctx.send(f"{e} ☠Usage: !fig SETNR [DURATION]")
            return

        await self.send_request('fig/number', f"value={number}")
        await self.send_request('fig/duration', f"value={duration}")

        json_info = await self.send_request('fig/display')
        info = json.loads(json_info.content)
        await ctx.send(f"{info['description']} | Price new: {info['price_new']} Price used: {info['price_used']} | {info['bricklink_url']}")

    @commands.command()
    async def part(self, ctx: commands.Context):
        try:
            number, color_name, color_id, duration = parse_part_command(ctx.view.words, self.color_table, self.default_duration)
        except BadCommandValue as e:
            await ctx.send(f"{e} ☠ Usage: !part PARTNR [COLOR] [DURATION]")
            return

        await self.send_request('part/number', f"value={number}")
        await self.send_request('part/duration', f"value={duration}")
        await self.send_request('part/color', f"value={color_id}")

        json_info = await self.send_request('part/display')
        if json_info is None:
            await ctx.send(f"Unknown part: {number}")
        else:
            info = json.loads(json_info.content)
            await ctx.send(f"{info['description']} {info['bricklink_url']}")

        # await ctx.send(f"PART {number} Color {color_name} Duration {duration}")


def parse_set_command(words: dict, default_duration: int = DEFAULT_DURATION) -> (str, int):

    if len(words) == 0:
        raise BadCommandValue("No parameters given!")

    number = words[1]
    duration = default_duration
    if not is_identifier(number):
        raise BadCommandValue(f"Invalid identifier: {number}")

    if len(words) > 1:
        duration = extract_duration(words[2])

    return number, duration


# for now sets and fig commands have the same syntax
parse_fig_command = parse_set_command


def parse_part_command(words: dict, color_table: dict, default_duration: int = DEFAULT_DURATION) -> (str, str, int, int):

    if len(words) == 0:
        raise BadCommandValue("No parameters given!")

    number = words[1]
    color = -99
    duration = default_duration

    try:
        number = SYMBOLIC_PART_NAMES[number.lower()]
    except KeyError:
        pass  # not a symboli part name

    if not is_identifier(number):
        raise BadCommandValue(f"Invalid identifier: {number}")

    if len(words) > 1:
        color = words[2]
        if len(words) > 2:
            duration = extract_duration(words[3])

    try:
        color_id = int(color)
    except ValueError:
        color_name = color.lower()
        try:
            color_id = color_table[color_name]
        except KeyError:
            raise BadCommandValue(f"Unknown color name {color_name}")

    assert isinstance(color_id, int)

    if color_id not in get_color_table():
        raise BadCommandValue(f"Unknown color id: {color_id} ")

    color_name = color_table[color_id]

    return number, color_name, color_id, duration


def extract_duration(word):
    try:
        duration = int(word)
    except ValueError:
        raise BadCommandValue(f"Not an integer: {word}")

    if duration > MAX_DURATION:
        print(f"some trickster wanted to DOS with a large duration: {duration}")
        duration = MAX_DURATION

    return duration


def run_bot(config):
    bot = SmirnyBot9001ChatBot(config.token, config.channel, config.overlay_endpoint, config.default_duration)
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
