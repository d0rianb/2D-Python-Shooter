import math

from render import RenderedObject
from object.color import Color

BG_COLOR = Color((241, 231, 220))

class Collectible:
    def __init__(self, id, x, y, type, env):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = 'white'
        self.env = env
        self.size = 25
        self.is_active = True
        self.in_viewBox = 'undefined'
        self.cross_width = 4
        self.cross_height = 15

    def on_collect(self, player):
        print(f'{player.name} collected {self.type}')
        self.is_active = False

    def render(self):
        if not self.is_active: return
        self.env.rendering_stack.append(RenderedObject('rect', self.x + self.size/2 - self.cross_width/2, self.y + self.size/2 - self.cross_height/2, width=self.cross_width, height=self.cross_height, color='#fff',border=0, zIndex=6))
        self.env.rendering_stack.append(RenderedObject('rect', self.x + self.size/2 - self.cross_height/2, self.y + self.size/2 - self.cross_width/2, width=self.cross_height, height=self.cross_width, color='#fff',border=0, zIndex=6))
        self.env.rendering_stack.append(RenderedObject('oval', self.x, self.y, x2=self.x + self.size, y2=self.y + self.size, color=self.color, zIndex=4))


class Heal(Collectible):
    def __init__(self, id, x, y, env, amount=25):
        super().__init__(id, x, y, 'heal', env)
        self.amount = amount
        self.color = '#A4CF8A'

    def on_collect(self, player):
        if self.is_active:
            player.health = min(player.health + self.amount, 100)
            self.is_active = False


class LandMine(Collectible):
    def __init__(self, id, x, y, env, damage=25):
        super().__init__(id, x, y, 'LandMine', env)
        self.damage = damage
        self.initial_color = Color((153, 29, 62))
        self.color_speed = 1 / 60

    def on_collect(self, player):
        if self.is_active:
            player.health = max(player.health - self.damage, 0)
            player.message('warning', f'Hit by a land mine')
            if player.health == 0:
                player.dead()
            self.is_active = False

    def render(self):
        if not self.is_active: return
        alpha = 1 - 1 / 2 * abs(math.cos(self.env.tick * self.color_speed))
        self.color = Color.blend(self.initial_color, BG_COLOR, alpha).to_hex()
        self.env.rendering_stack.append(
            RenderedObject('oval', self.x, self.y, x2=self.x + self.size, y2=self.y + self.size, color=self.color,
                           zIndex=4))
