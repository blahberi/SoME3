from manim import *

from util_lib.rabbit_breeder import RabbitBreeder
from extra import color_schemes
from extra.color_schemes import gruvbox
from extra import fonts
from chapters.chapter_1.chapter1 import Chapter1
from chapters.chapter_2.chapter2 import Chapter2
from chapters.chapter_3.chapter3 import Chapter3
from chapters.chapter_4.chapter4 import Chapter4
from chapters.finish import Finish
from util_lib.utils import *


class C1(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        Chapter1.construct(self)


class C2(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        Chapter2.construct(self)


class C3(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        Chapter3.construct(self)


class C4(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        Chapter4.construct(self)


class Finish(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        Finish.construct(self)


class Test(Scene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()
        line = MathTex(
            vector_to_tex(["x + y", "x"]) + " = x" + vector_to_tex([1, 1]) + " + y" +
            vector_to_tex([1, 0]) + " = " + matrix_to_tex([[1, 1], [1, 0]]) + vector_to_tex(["x", "y"])
        )
        line[0][1].set_color(gruvbox.GREEN)
        line[0][3].set_color(gruvbox.RED)
        line[0][4].set_color(gruvbox.GREEN)
        line[0][7].set_color(gruvbox.GREEN)
        line[0][13].set_color(gruvbox.RED)
        line[0][19:25].set_color(EMPHASIZED)
        line[0][26].set_color(gruvbox.GREEN)
        line[0][27].set_color(gruvbox.RED)

        #self.add(line)
        #self.add(get_tex_debug(line))

        scene = self

        scene.play(Write(line[0][:7]))
        scene.wait(2)
        scene.play(Write(line[0][7:19]), run_time=1.5)
        scene.wait(2)
        scene.play(
            TransformFromCopy(line[0][7], line[0][26]),
            TransformFromCopy(line[0][13], line[0][27]),
            TransformFromCopy(line[0][9:11], VGroup(line[0][20], line[0][22])),
            TransformFromCopy(line[0][15:17], VGroup(line[0][21], line[0][23])),
            Write(line[0][19]), Write(line[0][24]), Write(line[0][25]), Write(line[0][28]),
            run_time=1.5
        )
        scene.wait(2)

