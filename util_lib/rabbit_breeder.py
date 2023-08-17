from manim import *
import numpy as np
from math import *
from util_lib.utils import *


def setup_rabbits(frame, num_baby, num_grown, min_width, rabbit, x_padding=0.25, y_padding=0.25, buff=0):
    B = num_baby
    G = num_grown
    phi = GOLDEN
    x = frame.get_width() - x_padding
    y = frame.get_height() - y_padding
    r = rabbit.get_height() / rabbit.get_width()
    alpha = ceil(r*(G/x + B/(phi*phi*x)))
    beta = ceil(r)
    gamma = -y

    #width = sqrt((phi * phi * x * y) / (r * (phi * phi * G + B + phi*phi*4)))
    width = (-beta + sqrt(beta*beta - 4*alpha*gamma)) / (2*alpha)

    if width > min_width:
        width = min_width
    g_per_row = floor(x / width)
    b_per_row = floor(phi * x / width)
    Rg = ceil(G / g_per_row)
    Rb = ceil(B / b_per_row)

    pair = VGroup(rabbit.copy(), rabbit.copy().shift(RIGHT)).set_width(width*(1-buff))
    babyPair = pair.copy().scale(INGOLDEN).shift(RIGHT)
    if G == 0:
        grownRabbits = VGroup()
    else:
        grownRabbits = VGroup(*[pair.copy() for _ in range(G)]).arrange_in_grid(
            Rg, g_per_row,
            row_heights=[width * r] * Rg,
            col_widths=[width] * g_per_row,
            buff=0.001
        )
        grownRabbits[(Rg - 1) * g_per_row:].shift(
            (grownRabbits.get_center()[0] - grownRabbits[(Rg - 1) * g_per_row:].get_center()[0]) * RIGHT
        )
    if B == 0:
        babyRabbits = VGroup()
    else:
        babyRabbits = VGroup(*[babyPair.copy() for _ in range(B)]).arrange_in_grid(Rb, b_per_row, row_heights=[
            width * INGOLDEN * r] * Rb,
            col_widths=[width * INGOLDEN] * b_per_row,
            buff=0.001
        )
        babyRabbits[(Rb - 1) * b_per_row:].shift(
            (babyRabbits.get_center()[0] - babyRabbits[(Rb - 1) * b_per_row:].get_center()[0]) * RIGHT
        )

    VGroup(grownRabbits, babyRabbits).arrange(DOWN, buff=0.5*width).move_to(frame.get_center())
    return babyRabbits, grownRabbits

class RabbitBreeder(VGroup):
    def __init__(
            self,
            num_grown,
            num_baby,
            frame,
            x_padding=0.25,
            y_padding=0,
            buff=0
    ):
        self.frame = frame
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.num_baby = num_baby
        self.num_grown = num_grown
        self.min_width = 2
        self.rabbit = SVGMobject("assets/rabbit.svg")
        self.buff = buff

        self.babyRabbits, self.grownRabbits = self.setup()

        super().__init__(self.babyRabbits, self.grownRabbits)

    def setup(self):
        return setup_rabbits(self.frame, self.num_baby, self.num_grown, self.min_width, self.rabbit, self.x_padding, self.y_padding, self.buff)

    def animate_pass_month(self, scene, extra_animations=[], run_time=1, focus_breeding=False):
        if focus_breeding:
            scene.play(self.babyRabbits.animate.set_opacity(0.5))
            scene.wait(0.5)

        next_num_baby = self.num_grown
        next_num_grown = self.num_grown + self.num_baby

        next_babyRabbits, next_grownRabbits = setup_rabbits(self.frame, next_num_baby, next_num_grown, self.min_width, self.rabbit, self.x_padding, self.y_padding, self.buff)

        animations = []
        babies_to_remove = []

        # grow rabbits
        for i in range(self.num_grown):
            if focus_breeding: next_grownRabbits[i].set_opacity(0.5)
            animations.append(
                Transform(self.grownRabbits[i], next_grownRabbits[i])
            )
        for i in range(self.num_baby):
            if focus_breeding: next_grownRabbits[i+self.num_grown].set_opacity(0.5)
            animations.append(
                Transform(self.babyRabbits[i], next_grownRabbits[i+self.num_grown])
            )
            self.grownRabbits.add(self.babyRabbits[i])
            babies_to_remove.append(self.babyRabbits[i])

        # breed rabbits
        for i in range(self.num_grown):
            baby = self.grownRabbits[i].copy()
            if focus_breeding: self.grownRabbits[i].set_opacity(0.5)
            animations.append(
                Transform(baby, next_babyRabbits[i])
            )
            self.babyRabbits.add(baby)

        # remove babies
        for baby in babies_to_remove:
            self.babyRabbits.remove(baby)

        self.num_baby = next_num_baby
        self.num_grown = next_num_grown

        scene.play(AnimationGroup(*animations), *extra_animations, run_time=run_time)

        scene.remove(*self.babyRabbits, *self.grownRabbits)
        self.remove(self.babyRabbits, self.grownRabbits)
        self.babyRabbits = next_babyRabbits
        self.grownRabbits = next_grownRabbits
        scene.add(*self.babyRabbits, *self.grownRabbits)
        self.add(self.babyRabbits, self.grownRabbits)