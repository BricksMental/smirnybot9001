import abc
import re
import dataclasses
import json
import time
from dataclasses import dataclass
from pathlib import Path
import importlib.resources
from urllib.parse import urlparse, parse_qs

import remi
import requests
import typer
from bs4 import BeautifulSoup
from rich import print

from smirnybot9001.config import SmirnyBot9001Config, create_config_and_inject_values, CONFIG_PATH_OPTION, WIDTH_OPTION, \
    HEIGHT_OPTION, ADDRESS_OPTION, PORT_OPTION, START_BROWSER_OPTION, DEBUG_OPTION, MAX_DURATION
from smirnybot9001.util import get_with_user_agent
from smirnybot9001.color_table import get_color_table

APOCALYPSEBURG = 'https://img.bricklink.com/ItemImage/SN/0/70840-1.png'
HARLEY = 'https://img.bricklink.com/ItemImage/MN/0/tlm134.png'
DEFAULT_DISPLAY_WAV = 'happy-ending.wav'

TEXT_PLAIN_HEADERS = {'Content-type': 'text/plain; charset=utf-8', 'Content-encoding': 'utf-8'}
APPLICATION_JSON_HEADERS = {'Content-type': 'application/json; charset=utf-8', 'Content-encoding': 'utf-8'}

OK_HEADERS = ('OK', TEXT_PLAIN_HEADERS)


def extract_from_bricklink(some_number, color):
    try:
        return extract_from_bricklink_lego_element_id(some_number)
    except NotALEGOThingNumber:
        print(f"{some_number} is not a LEGO Element Number")
    try:
        return extract_from_bricklink_partnumber(some_number, color)
    except NotALEGOThingNumber:
        print(f"{some_number} also not BL part number. I give up")
        raise


def normalize_color(color):
    if color == '':
        return None
    else:
        return color


def extract_from_bricklink_partnumber(some_number, color=None):
    bricklink_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={some_number}#T=C"
    bl_color_id = normalize_color(color)
    bl_part_id = None
    # bl_part_number = some_number
    if bl_color_id is not None:
        bricklink_url += f"&C={bl_color_id}"
    print(f"trying {bricklink_url}")
    r = get_with_user_agent(bricklink_url)
    if 'notFound' in r.url:
        raise NotALEGOThingNumber
    assert r.status_code == 200
    name, bl_part_number, default_image_url = extract_bricklink_part_info(r.text)
    assert bl_part_number == some_number
    if bl_color_id is None:
        image_url = default_image_url
    else:
        image_url = f"https://img.bricklink.com/ItemImage/PN/{bl_color_id}/{bl_part_number}.png"

    return bl_color_id, bl_part_id, name, bl_part_number, r.url, image_url


def extract_from_bricklink_lego_element_id(lego_element_id):
    bricklink_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?ccName={lego_element_id}"
    r = get_with_user_agent(bricklink_url)
    if 'notFound' in r.url:
        raise NotALEGOThingNumber

    assert r.status_code == 200
    if r.url != bricklink_url:
        print(f"Got redirected from {bricklink_url} to: {r.url}")
    query_values = parse_qs(urlparse(r.url).query)
    assert query_values['ccName'][0] == lego_element_id
    bl_color_id = query_values['idColor'][0]
    bl_part_id = query_values['id'][0]
    name, bl_part_number, default_image_url = extract_bricklink_part_info(r.text)
    image_url = f"https://img.bricklink.com/ItemImage/PN/{bl_color_id}/{bl_part_number}.png"
    return bl_color_id, bl_part_id, name, bl_part_number, r.url, image_url


def extract_bricklink_part_info(bricklink_html):
    soup = BeautifulSoup(bricklink_html, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'}).get('content')
    span_name = soup.find('span', id='item-name-title').text
    match = re.match(r'^ItemName: (?P<name>.*), ItemType:.* ItemNo: (?P<bl_number>.*), Buy and sell', description)
    if match:
        name = match.group('name')
        bl_number = match.group('bl_number')

    # bricklink has  a bug in their code missing a ", i have to pick the wrong data apart here...
    borked_image_url = soup.find('div', attrs={'data-color': '-99'}).get('data-imgurl')
    default_image_url = borked_image_url.split(' ')[0]

    return span_name, bl_number, default_image_url


class NotALEGOThingNumber(Exception):
    pass


@dataclass
class LEGOThing(metaclass=abc.ABCMeta):
    number: str
    name: str = None
    description: str = None
    color: str = None
    image_url: str = None
    bricklink_url: str = None
    rebrickable_url: str = None
    brickset_url: str = None

    def __post_init__(self):
        self.scrape_info()

    @staticmethod
    @abc.abstractmethod
    def irc_command():
        raise NotImplementedError

    @abc.abstractmethod
    def scrape_info(self):
        raise NotImplementedError


class LEGOSet(LEGOThing):
    def __init__(self, number, *args, **kwargs):
        super().__init__(number, *args, **kwargs)

    @staticmethod
    def irc_command():
        return 'set'

    def scrape_info(self):
        self.brickset_url = f"https://brickset.com/sets/{self.number}"
        self.bricklink_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?S={self.number}"
        self.name = f"{self.irc_command()} {self.number}"
        self.description = self.get_description()
        self.image_url = self.get_image_url()

    def get_description(self):

        page = requests.get(self.brickset_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('meta', {"property": "og:title"}).get('content')
        description = soup.find(property='og:description').get('content')
        if title == '' and description == '':
            return ''
        else:
            return f"☠{title}: {description}☠"

    def get_image_url(self):
        if '-' not in self.number:
            img = self.number + '-1'
        else:
            img = self.number
        return f"https://img.bricklink.com/ItemImage/SN/0/{img}.png"


class LEGOMiniFig(LEGOThing):
    def __init__(self, number, *args, **kwargs):
        super().__init__(number, *args, **kwargs)

    @staticmethod
    def irc_command():
        return 'fig'

    def scrape_info(self):
        self.brickset_url = f"https://brickset.com/minifigs/{self.number}"
        self.bricklink_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?M={self.number}"
        self.name = f"FIG {self.number}"
        self.description = self.get_description()
        self.image_url = f"https://img.bricklink.com/ItemImage/MN/0/{self.number}.png"

    def get_description(self):
        page = requests.get(self.brickset_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        description = soup.find('meta', {"property": "og:title"}).get('content')
        return description


class LEGOPart(LEGOThing):

    def __init__(self, number, color):
        super().__init__(number, color=color)

    @staticmethod
    def irc_command():
        return 'part'

    def scrape_info(self):
        self.name = f"{self.irc_command()} {self.number} Color: {self.color}"
        self.description = self.name
        self.image_url = APOCALYPSEBURG
        bl_color_id, bl_part_id, name, bl_part_number, bricklink_url, image_url = extract_from_bricklink(self.number, self.color)
        print(bl_color_id, bl_part_id, name, bl_part_number, bricklink_url, image_url)
        self.name = bl_part_number
        self.description = name
        try:
            color_name = get_color_table()[bl_color_id]
            self.description += f" color: {color_name}"
        except KeyError:
            pass
        self.image_url = image_url
        self.bricklink_url = bricklink_url
        self.bricklink_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?ccName={self.number}"

class InputButtonHBox(remi.gui.HBox):
    def __init__(self, overlay, command, default_value='', show_controls=True, default_duration=10, *args, **kwargs):
        super().__init__(attributes={'id': command}, *args, **kwargs)
        display_style = 'initial' if show_controls else 'none'
        self.overlay = overlay
        self.command = command
        self.default_duration = int(default_duration)
        self.id_label = remi.gui.Label(f"{command} id", style={'display': display_style})
        self.id_input = remi.gui.Input(style={'display': display_style})
        self.id_input.set_value(default_value)
        self.color_label = remi.gui.Label(f"{command} color", style={'display': display_style})
        self.color_input = remi.gui.Input(style={'display': display_style})
        # self.color_input.set_value(default_value)
        self.duration_label = remi.gui.Label(f"{command} duration (s)", style={'display': display_style})
        self.duration_input = remi.gui.Input(style={'display': display_style})
        self.duration_input.set_value(default_duration)
        self.button = remi.gui.Button(text=f"Show {command}", style={'display': display_style})

        self.button.onclick.do(self.on_button_click)

        self.append((self.id_label, self.id_input, self.color_label, self.color_input, self.duration_label, self.duration_input, self.button))

    def number(self, value):
        self.id_input.set_value(value)
        return OK_HEADERS

    def color(self, value):
        if value == 'NOCOLOR':
            value = ''
        self.color_input.set_value(value)
        return OK_HEADERS

    def duration(self, value):
        try:
            duration = int(value)
            if duration > MAX_DURATION:
                print(f"Some trickster wants to go above max duration: {duration}")
                duration = self.default_duration
            self.duration_input.set_value(duration)
            return OK_HEADERS
        except ValueError:
            print(f"[red] Ignoring bad duration {value}")
            return f"Bad value {value}", TEXT_PLAIN_HEADERS

    def on_button_click(self, _button):
        self.display()

    def display(self):
        try:
            duration = int(self.duration_input.get_value())
        except ValueError:
            duration = self.default_duration
            self.duration_input.set_value(self.default_duration)

        thing = self.overlay.display(self.command, self.id_input.get_value(), self.color_input.get_value(), duration)
        json_thing = json.dumps(dataclasses.asdict(thing), )
        return json_thing, APPLICATION_JSON_HEADERS


class SmirnyBot9001Overlay(remi.App):

    def __init__(self, *args):
        super().__init__(*args)
        self._commands = {c.irc_command(): c for c in LEGOThing.__subclasses__()}
        self._lego_thing_cache = {}

    def idle(self):

        if hasattr(self, '_hide_image_after'):  # check if already initialized, idle() might be called before __init__
            if self._hide_image_after and time.time() > self._hide_image_after:
                self._hide_image_after = None
                self.hide_image()

    def main(self, config: SmirnyBot9001Config):
        if config.display_wav_abs_path and config.display_wav_abs_path.exists():
            self._on_display_wav = remi.gui.load_resource(config.display_wav_abs_path)
        else:
            dwav = importlib.resources.files('smirnybot9001.data') / DEFAULT_DISPLAY_WAV
            self._on_display_wav = remi.gui.load_resource(dwav)
        width = config.width
        height = config.height
        debug = config.debug
        bgcolor = 'red' if debug else 'transparent'
        label_bgcolor = 'green' if debug else 'white'
        # only show controls when debug is enabled
        show_controls = debug
        self.root_vbox = remi.gui.VBox(height=height, width=width,
                                       style={'display': 'block', 'overflow': 'visible', 'text-align': 'center',
                                              'background': bgcolor})
        self.image_vbox = remi.gui.VBox(height='95%', width='99%',
                                        style={'display': 'block', 'overflow': 'visible', 'text-align': 'center',
                                               'background': bgcolor})
        self.inputs_vbox = remi.gui.VBox(height=height / 10, width=width,
                                         style={'display': 'block', 'overflow': 'auto', 'text-align': 'center',
                                                'background': bgcolor})

        self.image = remi.gui.Image(APOCALYPSEBURG, height='85%', margin='10px')
        self.image_description_label = remi.gui.Label(width='100%', height='15%',
                                                      style={'display': 'block', 'overflow': 'visible',
                                                             'text-align': 'center', 'background': 'rgba(0,0,0,.6)',
                                                             'color': 'white', 'font-family': 'cursive',
                                                             'font-size': '40px', })
        self.set_description_text('🐸🐸🐸🐸 HELLO CHILLIBRIE 🐸🐸🐸🐸 ' * 2)

        for command, default in (('set', '10228'), ('fig', 'col128'), ('part', '6337632')):
            input_button_hbox = InputButtonHBox(overlay=self, command=command, default_value=default,
                                                show_controls=show_controls, default_duration=config.default_duration)
            self.inputs_vbox.append(input_button_hbox)

        self.image_vbox.append((self.image, self.image_description_label))
        self.root_vbox.append((self.image_vbox, self.inputs_vbox))
        return self.root_vbox

    def get_lego_thing(self, command, number, color):
        key = (command, number, color)
        if key not in self._lego_thing_cache:
            lego_thing = self._commands[command](number, color=color)
            self._lego_thing_cache[key] = lego_thing
        return self._lego_thing_cache[key]

    def display(self, command, number, color, duration):
        thing = self.get_lego_thing(command, number, color)
        self.set_image_url(thing.image_url)
        self.set_description_text(thing.description)
        self.show_image(duration)
        self.execute_javascript(f"(new Audio('{self._on_display_wav}')).play();")
        return thing

    def set_description_text(self, description):
        self.image_description_label.set_text(description)

    def set_image_url(self, url):
        self.image.set_image(url)

    def show_image(self, duration):
        self.image_vbox.css_visibility = 'visible'
        self._hide_image_after = time.time() + duration

    def hide_image(self):
        self.image_vbox.css_visibility = 'hidden'


def start_overlay(config: SmirnyBot9001Config):
    remi.start(SmirnyBot9001Overlay, debug=config.debug, address=config.address, port=config.port,
               start_browser=config.start_browser,
               multiple_instance=False,
               userdata=(config,))


def main():
    app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=False,
                      pretty_exceptions_enable=False)

    @app.callback()
    def start(config_path: Path = CONFIG_PATH_OPTION,
              width: int = WIDTH_OPTION,
              height: int = HEIGHT_OPTION,
              address: str = ADDRESS_OPTION,
              port: int = PORT_OPTION,
              start_browser: bool = START_BROWSER_OPTION,
              debug: bool = DEBUG_OPTION,
              ):
        config = create_config_and_inject_values(config_path, locals())
        start_overlay(config)

    app(help_option_names=('-h', '--help'))


if __name__ == '__main__':
    main()
