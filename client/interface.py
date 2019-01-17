class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.margin_x = 8
        self.margin_y = 20
        self.width = env.width
        self.height = env.height
        self.canvas = env.canvas
        self.refresh_rate = env.framerate
        self.padding = 18
        self.informations = {}
        self.fill = '#92959b'

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
                'Ammo': self.player.ammo,
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
                fill=self.fill)

    def render(self):
        for position in self.informations:
            x, y = self.margin_x, self.margin_y
            if position == 'TopRight' or position == 'BottomRight': x = self.width - 120
            if position == 'BottomRight': y = self.height - len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y)
