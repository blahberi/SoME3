from manim import *
from extra.color_schemes.gruvbox import *
from extra.color_schemes import gruvbox
from util_lib.utils import *
from util_lib.SpeechBubble import Bubble
from util_lib.rabbit_breeder import RabbitBreeder


def extra(scene):
    scene.remove(*scene.mobjects)
    text = Text("Other types of Fibonacci sequences", color=EMPHASIZED).to_edge(UP)
    scene.play(Write(text))
    scene.wait(2)
    sequence = MathTex(r"F = 1, 1, 2, 3, 5, 8, 13, 21, \cdots").next_to(text, DOWN, buff=1)
    scene.play(Write(sequence))
    scene.wait(1)

    vector = MathTex(vector_to_tex([1, 1]), color=SECONDARY).next_to(sequence, DOWN, buff=0.75)

    scene.play(
        sequence[0][2].animate.set_color(PRIMARY),
        sequence[0][4].animate.set_color(PRIMARY),
        Write(vector)
    )
    scene.wait(2)

    next_sequence = MathTex(r"F = 0, 1, 1, 2, 3, 5, 8, 13, \cdots").next_to(text, DOWN, buff=1)
    next_sequence[0][2].set_color(PRIMARY)
    next_sequence[0][4].set_color(PRIMARY)
    scene.play(
        sequence.animate.become(next_sequence),
        vector.animate.become(
            MathTex(vector_to_tex([1, 0]), color=SECONDARY).next_to(sequence, DOWN, buff=0.75)
        ),
    )
    scene.wait(1)

    next_sequence = MathTex(r"F = -1, 4, 3, 7, 10, 17, 27, 44, \cdots").next_to(text, DOWN, buff=1)
    next_sequence[0][2:4].set_color(PRIMARY)
    next_sequence[0][5].set_color(PRIMARY)
    scene.play(
        sequence.animate.become(next_sequence),
        vector.animate.become(
            MathTex(vector_to_tex([4, -1]), color=SECONDARY).next_to(sequence, DOWN, buff=0.75)
        ),
    )
    scene.wait(1)

    scene.play(vector.animate.become(
        MathTex(vector_to_tex(["F_1", "F_0"]), color=SECONDARY).next_to(sequence, DOWN, buff=0.75)
    ))
    scene.wait(1)

    tex = MathTex(
        r"F_n = \frac{\varphi^{n-1}(\varphi F_1 + F_0) - \psi^{n-1}(\psi F_1 + F_0)}{\sqrt{5}}",
        color=EMPHASIZED
    ).next_to(vector, DOWN, buff=1)
    scene.play(Write(tex))
    scene.wait(2)


def challenge(scene):
    scene.remove(*scene.mobjects)
    text = Text("Challenge", color=PRIMARY).scale(1.25)
    scene.play(Write(text))
    scene.wait(1)

    tex = MathTex(r"F_n = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}")
    surrounding_rect = SurroundingRectangle(tex, color=DANGER)
    surrounding_text = Text("Not optimal!", color=DANGER).next_to(surrounding_rect, UP)
    scene.play(Write(tex), text.animate.shift(3*UP))
    scene.wait(1)
    scene.play(Create(surrounding_rect), Write(surrounding_text))
    scene.wait(2)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.move_to(8 * LEFT + 2.7 * DOWN)
    scene.play(rabbit.animate.shift(2 * RIGHT))
    bubble = Bubble(content_scale_factor=0.8).scale(0.4).pin_to(rabbit).shift(
        0.5 * DOWN + 0.25 * LEFT)
    tex = Tex(r"Why isn't it optimal?").set_z_index(1)
    bubble.add_content(tex)
    scene.play(DrawBorderThenFill(bubble), Write(tex))
    scene.wait(2)

    rabbit2 = rabbit.copy().shift(12*RIGHT)
    scene.play(FadeIn(rabbit2))
    bubble2 = Bubble(content_scale_factor=0.8).scale(0.4).pin_to(rabbit2).shift(
        0.5 * DOWN + 0.25 * LEFT)
    tex = Tex(r"How can we \\ make it optimal").set_z_index(1)
    bubble2.add_content(tex)
    scene.play(DrawBorderThenFill(bubble2), Write(tex))
    scene.wait(2)


def thanks_for_watching_rabbits(scene):
    scene.remove(*scene.mobjects)
    frame = FullScreenRectangle()
    rabbit_breeder = RabbitBreeder(0, 1, frame, 0.5, 0.5)
    scene.add(rabbit_breeder)
    scene.wait(2)
    for i in range(16):
        rabbit_breeder.animate_pass_month(scene)
        scene.wait(2)


class Finish(Scene):
    def construct(self):
        pass
        #extra(self)
        #challenge(self)
        #thanks_for_watching_rabbits(self)