import arcade

class Coin(arcade.Sprite):
    def __init__(self, sprite : str, scale: float, value: int):
        super().__init__()
        self.scale = scale
        self.value = value
        self.current_frame = 0
        self.frame_timer = 0
        self.FRAME_SPEED = 0.1

        self.textures_list = self.load_atlas('../sprites/Coin_tiles.png', frame_count=6)
        self.texture = self.textures_list[0]

    def load_atlas(self, path, frame_count):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        textures = []
        for i in range(frame_count):
            rect = arcade.LRBT(i * 16, i * 16 + 16, 0, 16)
            textures.append(sheet.get_texture(rect))
        return textures

    def update(self, delta_time: float = 1/60):
        self.frame_timer += delta_time
        if self.frame_timer >= self.FRAME_SPEED:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures_list)
            self.texture = self.textures_list[self.current_frame]