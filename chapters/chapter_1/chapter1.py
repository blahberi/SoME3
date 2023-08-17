from manim import *

from util_lib.rabbit_breeder import RabbitBreeder
from util_lib.SpeechBubble import Bubble
from extra.color_schemes.gruvbox import *


GOLDEN = 1.61803398875
INGOLDEN = 0.61803398875

WIDTH = 14
HEIGHT = 8


def introduction(scene):
    scene.remove(*scene.mobjects)

    title = Text("Chapter 1: Down the Rabbit Hole").center().move_to(0)
    scene.play(Write(title), run_time=5)
    scene.wait(2)
    scene.play(FadeOut(title), run_time=3)
    scene.wait(2)

    rabbit = SVGMobject("assets/rabbit.svg")

    pair = VGroup(rabbit.copy(), rabbit.copy().shift(RIGHT)).move_to(ORIGIN).shift(UP).scale(0.7)
    pair.z_index = 1
    scene.play(FadeIn(pair))

    rule1 = Text("1. A rabbit takes one month to mature", font_size=30)
    rule2 = Text("2. A pair of mature rabbits produce a new pair \neach month, one male one female", font_size=30)
    rule3 = Text("3. Rabbits never die", font_size=30)
    rules = VGroup(rule1, rule2, rule3).arrange(DOWN, buff=0.5, center=False, aligned_edge=LEFT).to_edge(LEFT).shift(0.5*RIGHT + UP)

    rules_text = Text("Rules", color=PRIMARY).next_to(rules, UP, buff=1)

    scene.play(pair.animate.shift(4.5*RIGHT), Write(rules_text))
    scene.play(Write(rule1))
    scene.play(pair.animate.scale(GOLDEN))
    scene.wait(2)

    new_pair = pair.copy()
    scene.play(Write(rule2))
    scene.play(new_pair.animate.shift(2.5*DOWN).scale(INGOLDEN))
    scene.wait(2)
    scene.play(Write(rule3))

    scene.play(FadeOut(new_pair, pair, rules_text, rule1, rule2, rule3), run_time=2)

    scene.wait(2)


    month_tracker = ValueTracker(0)
    month_text = Text("Month: ", color=SECONDARY).to_corner(UL).shift(0.5*DOWN + 0.5*RIGHT)
    month = Integer(0, color=SECONDARY).next_to(month_text, RIGHT).scale(1.5).add_updater(lambda m: m.set_value(month_tracker.get_value()))

    frame = FullScreenRectangle()
    rabbit_breeder = RabbitBreeder(0, 1, frame)

    scene.play(FadeIn(rabbit_breeder, month_text, month))
    scene.wait(2)
    month_tracker.set_value(1)
    rabbit_breeder.animate_pass_month(scene)
    scene.wait(2)
    month_tracker.set_value(2)
    rabbit_breeder.animate_pass_month(scene)
    scene.wait(2)
    month_tracker.set_value(3)
    rabbit_breeder.animate_pass_month(scene)
    scene.wait(1)
    month_tracker.set_value(4)
    rabbit_breeder.animate_pass_month(scene)
    scene.wait(1)

    text = Text("How many pairs after n months?", color=PRIMARY).move_to(ORIGIN).shift(2*UP)
    scene.play(rabbit_breeder.animate.shift(DOWN), FadeOut(month_text), FadeOut(month), run_time=2)
    scene.play(Write(text), run_time=2)
    scene.wait(2)


def solution(scene):
    scene.remove(*scene.mobjects)
    frame = Rectangle(width=WIDTH/2, height=HEIGHT/2 + 2, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(RIGHT)
    scene.add(frame)

    rabbit_breeder = RabbitBreeder(2, 1, frame, buff=0.1)
    scene.add(rabbit_breeder)

    scene.wait(2)
    formula = MathTex("P_n = P_{n-1} + P_{n-2}").scale(1.5).to_edge(LEFT)

    formula[0][0:2].set_color(PRIMARY)
    formula[0][3:7].set_color(SECONDARY)
    formula[0][8:].set_color(CYAN)

    t0 = formula[0][0:3]
    t1 = formula[0][3:7]
    t2 = formula[0][7:]
    scene.play(Write(t0))
    scene.wait(1)
    scene.play(Write(t1))
    scene.wait(1)
    rabbit_breeder.animate_pass_month(scene, focus_breeding=True)
    scene.wait(0.5)
    group = rabbit_breeder.grownRabbits[:2]
    scene.play(group.animate.set_opacity(1))
    highlight_rect = SurroundingRectangle(group, color=EMPHASIZED)
    scene.play(Create(highlight_rect))
    text = Text("At least 2 months old!", color=EMPHASIZED).move_to(frame).shift(2*UP)
    scene.play(Write(text))
    scene.play(Write(t2))
    scene.wait(2)

    scene.play(FadeOut(text), FadeOut(highlight_rect), run_time=2)
    scene.play(frame.animate.shift(10*RIGHT), rabbit_breeder.animate.shift(10*RIGHT), formula.animate.move_to(ORIGIN), run_time=2)

    scene.play(formula.animate.shift(2*UP))
    fib_sequence = Tex("1, 1, 2, 3, 5, 8, 13, 21, ...")
    scene.play(Write(fib_sequence))
    scene.wait(2)
    formula2 = MathTex("F_n = F_{n-1} + F_{n-2}").scale(1.5).to_edge(LEFT).move_to(formula.get_center())
    formula2[0][0:2].set_color(PRIMARY)
    formula2[0][3:7].set_color(SECONDARY)
    formula2[0][8:].set_color(CYAN)
    scene.wait(2)
    scene.play(TransformMatchingTex(formula, formula2), run_time=0.5)
    scene.wait(2)


def motivation(scene):
    scene.remove(*scene.mobjects)

    rabbit_breeder = RabbitBreeder(8, 5, FullScreenRectangle().scale(0.8), y_padding=1, buff=0.1)
    scene.add(rabbit_breeder)

    rabbit1 = rabbit_breeder.grownRabbits[3]
    rabbit2 = rabbit_breeder.babyRabbits[3]
    rabbit3 = rabbit_breeder.grownRabbits[1]
    rabbit4 = rabbit_breeder.babyRabbits[0]
    bubble1 = Bubble().scale(0.3).pin_to(rabbit1)
    bubble1.write(r"How many pairs \\ after 1000 months?")
    bubble1.content.scale(1.2)
    scene.play(DrawBorderThenFill(bubble1), Write(bubble1.content))
    scene.wait(1)

    bubble2 = Bubble().scale(0.3).rotate(PI).pin_to(rabbit2).shift(2.6*DOWN + 2*RIGHT)
    bubble2.add_content(MathTex("F_{1000} = F_{999} + F_{998}"))
    bubble2.content.shift(0.5*DOWN).scale(1.2)
    scene.play(DrawBorderThenFill(bubble2), Write(bubble2.content))
    scene.wait(1)

    bubble3 = Bubble().scale(0.3).rotate(PI).pin_to(rabbit3).shift(3*DOWN + 2.5*LEFT)
    bubble3.add_content(Tex(r"But we are \\ still stuck!"))
    bubble3.content.shift(0.5*DOWN).scale(0.8)
    scene.play(DrawBorderThenFill(bubble3), Write(bubble3.content))
    scene.wait(2)
    scene.play(
        FadeOut(bubble1), FadeOut(bubble2), FadeOut(bubble3),
        FadeOut(bubble1.content), FadeOut(bubble2.content), FadeOut(bubble3.content))
    bubble4 = Bubble().scale(0.3).flip(LEFT).pin_to(rabbit4).shift(2.5*DOWN)
    tex = MathTex(r"F_{n} = \text{?!?!}")
    tex[0][0:2].set_color(PRIMARY)
    tex[0][3:].set_color(DANGER)
    bubble4.add_content(tex)
    bubble4.content.shift(0.5*DOWN)
    scene.play(DrawBorderThenFill(bubble4), Write(bubble4.content))
    scene.wait(2)
    scene.play(FadeOut(bubble4, rabbit_breeder))
    scene.remove(rabbit_breeder)
    scene.wait(0.5)
    scene.play(tex.animate.move_to(ORIGIN).scale(2), run_time=2)
    scene.wait(2)
    scene.play(FadeOut(tex), run_time=2)
    scene.wait(2)


class Chapter1(Scene):
    def construct(self):
        introduction(self)
        solution(self)
        motivation(self)


#TODO: add more snazz, maybe remake everything to be more snazzy