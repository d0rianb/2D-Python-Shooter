import tkinter.font as tkFont

class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.margin_x = 8
        self.margin_y = 20
        self.width = env.viewArea['width']
        self.height = env.viewArea['height']
        self.canvas = env.canvas
        self.refresh_rate = env.framerate
        self.padding = 20
        self.informations = {}
        self.fill = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')

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
                'Ammo': self.player.ammo if not self.player.is_reloading else 'Rechargement en cours',
                'Dash': self.player.dash_left
            }
        }
        self.render()
        self.env.fen.after(1000//self.refresh_rate, self.update)

    def parse(self, position, x, y):
        infos = self.informations[position]
        for (index, info) in enumerate(infos):
            self.canvas.create_text(x, y + index*self.padding,
                text='{0}: {1}'.format(info, infos[info]),
                anchor='w',
                fill=self.fill,
                font=self.font)

    def render(self):
        for position in self.informations:
            x, y = self.margin_x, self.margin_y
            if position == 'TopRight' or position == 'BottomRight': x = self.width - 120
            if position == 'BottomRight': y = self.height - 2.5*len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y)
