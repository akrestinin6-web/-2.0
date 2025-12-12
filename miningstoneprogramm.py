from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Настройки
window.title = 'Python Minecraft'
window.borderless = False

# Текстуры (можно заменить на свои)
block_textures = {
    'grass': 'grass',
    'dirt': 'dirt',
    'stone': 'stone',
    'wood': 'wood',
    'leaf': 'leaf',
}

# Типы блоков
block_types = [
    {'name': 'Трава', 'texture': 'grass'},
    {'name': 'Земля', 'texture': 'dirt'},
    {'name': 'Камень', 'texture': 'stone'},
    {'name': 'Дерево', 'texture': 'wood'},
    {'name': 'Листва', 'texture': 'leaf'},
]

# Текущий выбранный блок
current_block = 0

class Block(Button):
    def __init__(self, position=(0,0,0), block_type=0):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=block_types[block_type]['texture'],
            origin_y=0.5,
            color=color.white,
            highlight_color=color.light_gray,
        )
        self.block_type = block_type

def input(key):
    global current_block
    
    # Выбор блока цифрами
    if key in '12345':
        current_block = int(key) - 1
        hand.texture = block_types[current_block]['texture']
    
    # ЛКМ - разрушить, ПКМ - поставить
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            destroy(hit_info.entity)
    
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Block(
                position=hit_info.entity.position + hit_info.normal,
                block_type=current_block
            )

# Генерация плоского мира
ground_size = 16
for x in range(-ground_size, ground_size):
    for z in range(-ground_size, ground_size):
        Block(position=(x, -1, z), block_type=1)  # Земля
        Block(position=(x, 0, z), block_type=0)   # Трава

# Случайные деревья
from random import randint
for _ in range(10):
    x = randint(-ground_size+2, ground_size-2)
    z = randint(-ground_size+2, ground_size-2)
    
    # Ствол
    for y in range(1, 4):
        Block(position=(x, y, z), block_type=3)
    
    # Листва
    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            for dy in [0, 1]:
                if not (dx == 0 and dz == 0 and dy == 0):
                    Block(position=(x+dx, 3+dy, z+dz), block_type=4)

# Игрок
player = FirstPersonController()
player.position = (0, 5, 0)

# Небо
Sky()

# Рука с текущим блоком
hand = Entity(
    parent=camera.ui,
    model='cube',
    texture=block_types[current_block]['texture'],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

# Панель выбора блоков
inventory_panel = Entity(
    parent=camera.ui,
    model='quad',
    texture='white_cube',
    scale=(0.5, 0.1),
    position=(0, -0.45),
    color=color.black66
)

for i, block in enumerate(block_types):
    btn = Button(
        parent=inventory_panel,
        model='cube',
        texture=block['texture'],
        scale=0.08,
        position=(-0.2 + i*0.1, 0),
        color=color.white if i != current_block else color.gold
    )
    btn.tooltip = Tooltip(block['name'])

app.run()