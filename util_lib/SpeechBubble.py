from manim import *
from extra.color_schemes.gruvbox import *


class Bubble(SVGMobject):
    file_name: str = "assets/bubble.svg"

    def __init__(
        self,
        direction = LEFT,
        center_point = ORIGIN,
        content_scale_factor: float = 0.7,
        height: float = 4.0,
        width: float = 8.0,
        max_height: float | None = None,
        max_width: float | None = None,
        bubble_center_adjustment_factor: float = 0.125,
        fill_color = BG_FILL,
        fill_opacity: float = 1,
        stroke_color = FG,
        stroke_width: float = 3.0,
        **kwargs
    ):
        self.direction = direction
        self.bubble_center_adjustment_factor = bubble_center_adjustment_factor
        self.content_scale_factor = content_scale_factor

        super().__init__(
            file_name=self.file_name,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs
        )

        self.center()
        self.set_height(height)
        self.set_width(width)
        if max_height:
            self.set_max_height(max_height)
        if max_width:
            self.set_max_width(max_width)
        if direction[0] > 0:
            self.flip()

        self.content = VMobject()

    def get_tip(self):
        # TODO, find a better way
        return self.get_corner(DOWN + self.direction) - 0.6 * self.direction

    def get_bubble_center(self):
        factor = self.bubble_center_adjustment_factor
        return self.get_center() + factor * self.get_height() * UP

    def move_tip_to(self, point):
        mover = VGroup(self)
        if self.content is not None:
            mover.add(self.content)
        mover.shift(point - self.get_tip())
        return self

    def flip(self, axis=UP):
        super().flip(axis=axis)
        if abs(axis[1]) > 0:
            self.direction = -np.array(self.direction)
        return self

    def pin_to(self, mobject):
        mob_center = mobject.get_center()
        want_to_flip = np.sign(mob_center[0]) != np.sign(self.direction[0])
        if want_to_flip:
            self.flip()
        boundary_point = mobject.get_critical_point(UP - self.direction)
        vector_from_center = 1.0 * (boundary_point - mob_center)
        self.move_tip_to(mob_center + vector_from_center)
        return self

    def position_mobject_inside(self, mobject):
        width_scale = 0
        if (self.content_scale_factor * self.get_width()) > mobject.get_width():
            width_scale = 1
        else:
            width_scale = self.content_scale_factor * self.get_width() / mobject.get_width()
        height_scale = 0
        if (self.content_scale_factor * self.get_height()) > mobject.get_height():
            height_scale = 1
        else:
            height_scale = self.content_scale_factor * self.get_height() / (mobject.get_height() / 1.5)
        mobject.scale(width_scale)
        mobject.set_max_height(height_scale)
        mobject.shift(self.get_bubble_center() - mobject.get_center())
        return mobject

    def add_content(self, mobject):
        self.position_mobject_inside(mobject)
        self.content = mobject
        return self.content

    def write(self, *text):
        self.add_content(Tex(*text))
        return self

    def resize_to_content(self, buff=0.75):
        width = self.content.get_width()
        height = self.content.get_height()
        target_width = width + min(buff, height)
        target_height = 1.35 * (self.content.get_height() + buff)
        tip_point = self.get_tip()
        self.stretch_to_fit_width(target_width, about_point=tip_point)
        self.stretch_to_fit_height(target_height, about_point=tip_point)
        self.position_mobject_inside(self.content)

    def clear(self):
        self.add_content(VMobject())
        return self