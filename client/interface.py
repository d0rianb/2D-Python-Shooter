import tkinter.font as tkFont
from renderedObject import RenderedObject


class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.margin_x = 8
        self.margin_y = 20
        self.width = env.viewArea['width']
        self.height = env.viewArea['height']
        self.canvas = env.canvas # Soon useless
        self.refresh_rate = env.framerate
        self.padding = 20
        self.informations = {}
        self.fill = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')
        self.env.fen.bind('<Key-h>', self.display_help)

    def display_help(self, *args):
        text = '''Se déplacer : Z, Q, S, D (ou flèches directionnelles)\n Tirer : Clic Droit\n Dash : Majuscule gauche\n Recharger : R\ Restart Game: G\n Display Help : H '''
        self.env.rendering_queue.append(RenderedObject('text',self.env. width/2, 100, content=text, zIndex=10))

    def parse(self, position, x, y):
        infos = self.informations[position]
        for (index, info) in enumerate(infos):
            self.canvas.create_text(x, y + index*self.padding,
                text='{0}: {1}'.format(info, infos[info]),
                anchor='w',
                fill=self.fill,
                font=self.font)

    def update(self):
        self.informations = {
            'TopLeft': {
                'Player Name': self.player.name,
                'FrameRate': self.env.framerate
            },
            'TopRight': {
                'People Alive': len(list(filter(lambda player: player.alive, self.env.players)))
            },
            'BottomRight': {
                'Health': self.player.health,
                'Ammo': self.player.ammo if not self.player.is_reloading else 'Rechargement',
                'Dash': self.player.dash_left
            }
        }
        self.render()
        self.env.fen.after(1000//self.refresh_rate, self.update)

    def render(self):
        for position in self.informations:
            x, y = self.margin_x, self.margin_y
            if position == 'TopRight' or position == 'BottomRight': x = self.width - 120
            if position == 'BottomRight': y = self.height - 2.5*len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y)
