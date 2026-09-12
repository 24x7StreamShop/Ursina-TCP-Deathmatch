import ursina


class Enemy(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture="assets/DP.jpg", #"white_cube",
            color=ursina.color.hsv(0, 0, 1),
            scale=ursina.Vec3(1, 2, 1)
        )

        if hasattr(self, 'model_entity'):
            self.model_entity.uvs = [ursina.Vec2(1 - uv[0], uv[1]) for uv in self.model_entity.uvs]
            self.model_entity.generate()

        self.gun = ursina.Entity(
            parent=self,
            position=ursina.Vec3(0.55, 0.5, 0.6),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            model="cube",
            texture="white_cube",
            color=ursina.color.hsv(0, 0, 0.4)
        )

        self.name_tag = ursina.Text(
            parent=self,
            text=username,
            position=ursina.Vec3(0, 1.3, 0),
            scale=ursina.Vec2(5, 3),
            billboard=True,
            origin=ursina.Vec2(0, 0)
        )

        self.health = 100
        self.id = identifier
        self.username = username

    def update(self):
        if self.health <= 0:
            self.visible = False
            self.gun.visible = False
            self.name_tag.visible = False
            self.collider = None
        else:
            self.visible = True
            self.gun.visible = True
            self.name_tag.visible = True
            if not self.collider:
                self.collider = "box"

            try:
                color_saturation = max(0.0, min(1.0, 1.0 - self.health / 100.0))
            except (AttributeError, TypeError):
                self.health = 100
                color_saturation = 0.0

            self.color = ursina.color.hsv(0, color_saturation, 1)

    def respawn(self, position: ursina.Vec3, health: int = 100):
        self.world_position = position
        self.health = health
        self.visible = True
        self.gun.visible = True
        self.name_tag.visible = True
        self.collider = "box"
        self.color = ursina.color.hsv(0, 0, 1)

