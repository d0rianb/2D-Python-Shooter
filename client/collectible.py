from render import RenderedObject

class Collectible:
    def __init__(self, id, x, y, type, env):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.env = env
        self.size = 25
        self.is_active = True

    def on_collect(self, player):
        print(f'{player.name} collected {self.type}')
        self.is_active = False

    def render(self):
        if not self.is_active: return
        self.env.rendering_stack.append(RenderedObject('oval', self.x, self.y, x2=self.x+self.size, y2=self.y+self.size, color='#A4CF8A', zIndex=4))


class Heal(Collectible):
    def __init__(self, id, x, y, env, amount=25):
        super().__init__(id, x, y, 'heal', env)
        self.amount = amount

    def on_collect(self, player):
        if self.is_active:
            player.health = min(player.health + self.amount, 100)
            self.is_active = False
