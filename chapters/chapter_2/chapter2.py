from manim import *
from extra.color_schemes.gruvbox import *
from extra.color_schemes import gruvbox
from util_lib.rabbit_breeder import RabbitBreeder
from util_lib.SpeechBubble import Bubble
from util_lib import utils
from util_lib.utils import *
import numpy as np


WIDTH = 14
HEIGHT = 8
GOLDEN = 1.61803398875
INGOLDEN = 0.61803398875


def introduction(scene):
    scene.remove(*scene.mobjects)

    title = Text("Chapter 2: Curiouser and Curiouser")
    scene.play(Write(title), run_time=5)
    scene.wait(2)
    scene.play(FadeOut(title), run_time=3)
    scene.wait(2)


def learning_time_vectors(scene):
    scene.remove(*scene.mobjects)
    title = Text("Vectors", color=PRIMARY).scale(1.5).to_edge(UP)
    scene.play(Write(title))
    scene.wait(1)

    title1 = Text("Algebraic", color=gruvbox.SECONDARY).to_edge(LEFT).shift(1.5*UP + 1*RIGHT)
    scene.play(Write(title1))
    scene.wait(1)
    pair = MathTex(r"\begin{bmatrix} 2 \\ 1 \end{bmatrix}").scale(1.5).next_to(title1, DOWN).shift(DOWN)
    scene.play(Write(pair))
    scene.wait(2)

    title2 = Text("Geometric", color=gruvbox.SECONDARY).to_edge(RIGHT).shift(1.5*UP + 1*LEFT)
    scene.play(Write(title2))
    scene.wait(1)
    frame = Rectangle(height=4.75, width=4.75, color=FG, fill_color=BG_FILL, fill_opacity=1).next_to(title2, DOWN)
    plane = utils.scale_plane_to_fit_frame(utils.EpicPlane((-5, 5, 1)).move_to(frame), frame)
    scene.play(FadeIn(frame, plane))
    scene.wait(1)
    arrow = utils.plot_vector((2, 1), plane, color=PRIMARY)
    scene.play(GrowArrow(arrow))
    scene.wait(2)

    coords = pair.copy().move_to(arrow).set_color(PRIMARY).scale(0.5).shift(0.75*RIGHT + 0.25*UP)
    scene.play(TransformFromCopy(pair, coords), run_time=2)
    scene.wait(2)

    addition_tex = MathTex(r"\begin{bmatrix} 1 \\ -1 \end{bmatrix} + \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}").scale(1.5).next_to(title1, DOWN).shift(DOWN + 0.5*RIGHT)
    addition_tex[0][0:5].set_color(gruvbox.GREEN)
    addition_tex[0][6:10].set_color(gruvbox.RED)
    addition_tex[0][11:15].set_color(PRIMARY)
    scene.play(pair.animate.move_to(addition_tex[0][11:15]).set_color(PRIMARY), Write(addition_tex[0][:11]), run_time=2)
    scene.wait(2)

    green_arrow = utils.plot_vector((1, -1), plane, color=gruvbox.GREEN)
    red_arrow = utils.plot_vector((1, 2), plane, color=gruvbox.RED)
    red_arrow.shift(green_arrow.get_end() - red_arrow.get_start())
    scene.play(GrowArrow(green_arrow))
    scene.wait(0.5)
    scene.play(GrowArrow(red_arrow))
    scene.wait(2)

    connection = MathTex(r"\longleftrightarrow").scale(2.25).move_to(ORIGIN).shift(frame.get_center()[1]*UP + 0.5*RIGHT + 0.25*UP)
    scene.play(Write(connection))
    scene.wait(2)

    scalar_mult_tex = MathTex(r"2 \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}").scale(1.5).next_to(title1, DOWN).shift(DOWN)
    scalar_mult_tex[0][0].set_color(gruvbox.GREEN)
    scalar_mult_tex[0][1:5].set_color(gruvbox.RED)
    scalar_mult_tex[0][6:10].set_color(PRIMARY)

    scene.play(
        pair.animate.move_to(scalar_mult_tex[0][1:5]).set_color(gruvbox.RED),
        Write(scalar_mult_tex[0][0]),
        Write(scalar_mult_tex[0][5:10]), FadeOut(addition_tex[0][:11]),
        FadeOut(green_arrow), FadeOut(red_arrow), FadeOut(connection),
        run_time=2
    )
    scene.wait(2)

    new_arrow = utils.plot_vector((4, 2), plane, color=PRIMARY)
    scene.play(arrow.animate.become(new_arrow), FadeOut(coords), run_time=1.5)
    scene.remove(coords)
    scene.wait(1)

    coords = scalar_mult_tex[0][6:10].copy()
    scene.play(
        coords.animate.move_to(arrow.get_end() + 0.75*DOWN).scale(0.5).set_color(PRIMARY),
        run_time=2
    )
    scene.wait(2)

    # next_tex = MathTex(
    #     r"\frac{1}{2} \begin{bmatrix} 4 \\ 2 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}"
    # ).scale(1.5).next_to(title1, DOWN).shift(DOWN)
    # next_tex[0][0:3].set_color(gruvbox.GREEN)
    # next_tex[0][3:7].set_color(gruvbox.RED)
    # next_tex[0][8:12].set_color(PRIMARY)
    #
    # scene.remove(*scalar_mult_tex[0], pair)
    # scene.add(scalar_mult_tex)
    # scene.play(
    #     Transform(scalar_mult_tex[0][0], next_tex[0][0:3]),
    #     scalar_mult_tex[0][1:5].animate.move_to(next_tex[0][8:12]).set_color(PRIMARY),
    #     Transform(scalar_mult_tex[0][5], next_tex[0][7]),
    #     scalar_mult_tex[0][6:10].animate.move_to(next_tex[0][3:7]).set_color(gruvbox.RED),
    #     scalar_mult_tex[0][5].animate.move_to(next_tex[0][7]),
    #     arrow.animate.become(utils.plot_vector((2, 1), plane, color=PRIMARY)),
    #     run_time=2
    # )
    # scene.play(
    #     coords.animate.become(
    #         next_tex[0][8:12].copy().move_to(arrow).set_color(PRIMARY).scale(0.5).shift(0.75*RIGHT + 0.25 * UP)
    #     )
    # )
    # print(plane.p2c(2, 1))
    #
    # scene.wait(2)

    scene.play(FadeOut(*scene.mobjects), run_time=1.5)
    scene.wait(1)


def learning_time_matrices(scene):
    scene.remove(*scene.mobjects)
    title = Text("Matrices", color=PRIMARY).scale(1.5).to_edge(UP)
    scene.play(Write(title))
    scene.wait(1)
    matrix = MathTex(matrix_to_tex([[1, 2], [3, 4]])).move_to(ORIGIN).scale(1.25)
    scene.play(Write(matrix))
    scene.wait(2)
    green_matrix_tex = matrix_to_tex([["a", "b"], ["c", "d"]])
    red_matrix_tex = matrix_to_tex([["e", "f"], ["g", "h"]])
    addition_tex = MathTex(green_matrix_tex + " + " + red_matrix_tex + " = " + matrix_to_tex([["a+e", "b+f"], ["c+g", "d+h"]])).scale(1.25).move_to(ORIGIN)
    addition_tex[0][:6].set_color(gruvbox.GREEN)
    addition_tex[0][7:13].set_color(gruvbox.RED)
    green_indices = [15, 18, 21, 24]
    red_indices = [17, 20, 23, 26]
    for i in range(len(addition_tex[0])):
        if i in green_indices:
            addition_tex[0][i].set_color(gruvbox.GREEN)
        elif i in red_indices:
            addition_tex[0][i].set_color(gruvbox.RED)

    subtitle = Text("Addition", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5*UP)
    scene.play(Transform(matrix, addition_tex[0][:6]), Write(addition_tex[0][6:]), Write(subtitle), run_time=2)
    scene.remove(matrix, *addition_tex[0])
    scene.add(addition_tex)
    scene.wait(2)

    red_matrix_tex = matrix_to_tex([["a", "b"], ["c", "d"]])
    scalar_mult_tex = MathTex(r"\delta " + red_matrix_tex + " = " + matrix_to_tex([[r"\delta a", r"\delta b"], [r"\delta c", r"\delta d"]])).scale(1.25).move_to(ORIGIN)
    scalar_mult_tex[0][0].set_color(gruvbox.GREEN)
    scalar_mult_tex[0][1:7].set_color(gruvbox.RED)

    green_indices = [9, 11, 13, 15]
    red_indices = [10, 12, 14, 16]
    for i in range(len(scalar_mult_tex[0])):
        if i in green_indices:
            scalar_mult_tex[0][i].set_color(gruvbox.GREEN)
        elif i in red_indices:
            scalar_mult_tex[0][i].set_color(gruvbox.RED)

    scene.play(
        addition_tex[0][:6].animate.move_to(scalar_mult_tex[0][1:7]).set_color(RED),
        Write(scalar_mult_tex[0][0]),
        Write(scalar_mult_tex[0][7:]),
        FadeOut(addition_tex[0][6:]),
        subtitle.animate.become(
            Text("Scalar multiplication", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5 * UP)
        ),
        run_time=1.5
    )
    scene.remove(*addition_tex[0], *scalar_mult_tex[0])
    scene.add(scalar_mult_tex)
    scene.wait(2)
    new_matrix = matrix_to_tex([["a", "b"], ["c", "d"]])
    vector = r"\begin{bmatrix} x \\ y \end{bmatrix}"
    expansion = r"x\begin{bmatrix} a \\ c \end{bmatrix} + y\begin{bmatrix} b \\ d \end{bmatrix}"
    result = r"\begin{bmatrix} ax + by \\ cx + dy \end{bmatrix}"
    vector_mult_tex = MathTex(new_matrix + " " + vector + " = " + expansion + " = " + result).scale(1.25).move_to(ORIGIN)
    vector_mult_tex[0][:6].set_color(gruvbox.GREEN)
    vector_mult_tex[0][6:10].set_color(gruvbox.RED)
    vector_mult_tex[0][11].set_color(gruvbox.RED)
    vector_mult_tex[0][12:16].set_color(gruvbox.GREEN)
    vector_mult_tex[0][17].set_color(gruvbox.RED)
    vector_mult_tex[0][18:22].set_color(gruvbox.GREEN)

    green_indices = [24, 27, 29, 32]
    red_indices = [25, 28, 30, 33]
    for i in range(len(vector_mult_tex[0])):
        if i in green_indices:
            vector_mult_tex[0][i].set_color(gruvbox.GREEN)
        elif i in red_indices:
            vector_mult_tex[0][i].set_color(gruvbox.RED)

    line0 = vector_mult_tex[0][:11].copy().move_to(ORIGIN)
    line1 = vector_mult_tex[0][:22].copy().move_to(ORIGIN)
    line2 = vector_mult_tex[0].copy().move_to(ORIGIN)

    scene.play(
        scalar_mult_tex[0][1:7].animate.move_to(line0[:6]).set_color(gruvbox.GREEN),
        Write(line0[6:]),
        FadeOut(*scalar_mult_tex[0][0], *scalar_mult_tex[0][7:]),
        subtitle.animate.become(
            Text("Matrix-vector multiplication", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5 * UP)
        ),
        run_time=1.5
    )
    scene.wait(0.5)
    scene.remove(*scalar_mult_tex[0], *line0)
    scene.add(line0)
    scene.wait(1)

    scene.play(
        line0.animate.move_to(line1[:11]),
        run_time=1.5
    )
    scene.wait(0.5)
    copies = [
        VGroup(line0[1], line0[3]).copy(),
        VGroup(line0[2], line0[4]).copy(),
        line0[7].copy(),
        line0[8].copy()
    ]
    scene.play(
        LaggedStart(
            AnimationGroup(
                copies[0].animate.move_to(line1[13:15]),
                copies[1].animate.move_to(line1[19:21]),
                copies[2].animate.move_to(line1[11]),
                copies[3].animate.move_to(line1[17]),
                Write(line1[16])
            ),
            FadeIn(line1[12], line1[15], line1[18], line1[21]),
            lag_ratio=0.25
        ),
        run_time=1.5
    )
    scene.remove(*line0, *line1, *copies)
    scene.add(line1)
    scene.wait(1)

    scene.play(line1.animate.move_to(line2[:22]), run_time=1.5)
    copies = [
        line1[13:15].copy(),
        line1[19:21].copy(),
        line1[11].copy(),
        line1[11].copy(),
        line1[17].copy(),
        line1[17].copy(),
    ]
    scene.play(
        LaggedStart(
            AnimationGroup(
                copies[0].animate.move_to(VGroup(line2[24], line2[29])),
                copies[1].animate.move_to(VGroup(line2[27], line2[32])),
                copies[2].animate.move_to(line2[25]),
                copies[3].animate.move_to(line2[30]),
                copies[4].animate.move_to(line2[28]),
                copies[5].animate.move_to(line2[33]),
            ),
            AnimationGroup(
                Write(line2[22]),
                Write(line2[23]),
                Write(line2[26]),
                Write(line2[31]),
                Write(line2[34]),
            ),
            lag_ratio=0.25
        ),
        run_time=1.5
    )
    scene.remove(*line1, *line2, *copies)
    scene.add(line2)
    scene.wait(2)
    previous_line = line2

    line0 = MathTex(
        matrix_to_tex([["a", "b"], ["c", "d"]]) + matrix_to_tex([["e", "f"], ["g", "h"]]) + " = "
    ).scale(1.25)
    line11 = MathTex(
        matrix_to_tex([["a", "b"], ["c", "d"]]) + r"\begin{bmatrix} e \\ g \end{bmatrix} = " +
        r"\begin{bmatrix} ae + bg \\ ce + dg \end{bmatrix}"
    )
    line12 = MathTex(
        matrix_to_tex([["a", "b"], ["c", "d"]]) + r"\begin{bmatrix} f \\ h \end{bmatrix} = " +
        r"\begin{bmatrix} af + bh \\ cf + dh \end{bmatrix}"
    )
    VGroup(line11, line12).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(line0, DOWN, buff=0.25, aligned_edge=LEFT)
    line2 = MathTex(
        matrix_to_tex([["ae + bg", "af + bh"], ["ce + dg", "cf + dh"]])
    ).scale(1.25)

    green_indices = [
        [*range(0, 6)],
        [*range(0, 6), 12, 15, 17, 20],
        [*range(0, 6), 12, 15, 17, 20],
        [1, 4, 6, 9, 11, 14, 16, 19],
    ]
    red_indices = [
        [*range(6, 12)],
        [*range(6, 10), 13, 16, 18, 21],
        [*range(6, 10), 13, 16, 18, 21],
        [2, 5, 7, 10, 12, 15, 17, 20],
    ]
    for i, line in enumerate([line0, line11, line12, line2]):
        for j in range(len(line[0])):
            if j in green_indices[i]:
                line[0][j].set_color(gruvbox.GREEN)
            elif j in red_indices[i]:
                line[0][j].set_color(gruvbox.RED)
    #scene.add(line0, line11, line12)
    scene.play(
        previous_line[:6].animate.move_to(line0[0][:6]).set_color(gruvbox.GREEN),
        Transform(previous_line[6:10], line0[0][6:12]),
        Write(line0[0][12:]),
        FadeOut(previous_line[10:]),
        subtitle.animate.become(
            Text("Matrix multiplication", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5 * UP)
        ),
        run_time=1.5
    ),
    scene.remove(previous_line, *line0[0])
    scene.add(line0)
    scene.wait(1)

    copies1 = [
        VGroup(line0[0][:6]).copy(),
        VGroup(line0[0][7], line0[0][9]).copy(),
    ]
    copies2 = [
        VGroup(line0[0][:6]).copy(),
        VGroup(line0[0][8], line0[0][10]).copy()
    ]
    scene.play(
        LaggedStart(
            AnimationGroup(
                copies1[0].animate.move_to(line11[0][:6]).scale(1/1.25),
                copies1[1].animate.move_to(line11[0][7:9]).scale(1/1.25),
            ),
            AnimationGroup(
                copies2[0].animate.move_to(line12[0][:6]).scale(1/1.25),
                copies2[1].animate.move_to(line12[0][7:9]).scale(1/1.25),
            ),
            AnimationGroup(
                FadeIn(line11[0][6], line12[0][6], line11[0][9], line12[0][9]),
            ),
            lag_ratio=0.5
        ),
        run_time=2
    )
    scene.play(Write(line11[0][10:]), Write(line12[0][10:]), run_time=1.5)
    scene.remove(*line11[0], *line12[0], *copies1, *copies2)
    scene.add(line11, line12)
    scene.wait(2)
    final_line = VGroup(line0.copy(), line2.copy()).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
    scene.remove(*scene.mobjects)
    scene.add(title, subtitle, line0, line11, line12)
    scene.play(
        line0.animate.move_to(final_line[0]),
        run_time=1.5
    )
    copies = [
        line11[0][12:22].copy(),
        line12[0][12:22].copy(),
    ]
    scene.play(
        LaggedStart(
            copies[0].animate.move_to(VGroup(final_line[1][0][1:6], final_line[1][0][11:16])).scale(1.25),
            copies[1].animate.move_to(VGroup(final_line[1][0][7:11], final_line[1][0][16:20])).scale(1.25),
            AnimationGroup(
                Write(final_line[1][0][0]),
                Write(final_line[1][0][21]),
            ),
            lag_ratio=0.5
        ),
        run_time=1.5
    )
    scene.remove(*copies, line0, final_line)
    scene.add(final_line)

    scene.wait(0.5)
    scene.play(FadeOut(*line11[0], *line12[0]), run_time=1.5)
    scene.wait(2)

    white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(
        LEFT).shift(0.5 * LEFT).set_opacity(0.25)
    scene.play(FadeIn(white_screen))

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(8 * LEFT + 2.7 * DOWN)
    scene.play(rabbit.animate.shift(2 * RIGHT))

    bubble = Bubble(content_scale_factor=0.5).scale(0.3).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    text = Text("WTH?", color=DANGER).next_to(bubble, UP)
    bubble.add_content(text)
    scene.play(DrawBorderThenFill(bubble), Write(text))
    scene.wait(2)
    scene.play(FadeOut(white_screen, rabbit, bubble, text))

    scene.play(FadeOut(final_line, subtitle), run_time=1.5)
    scene.wait(0.5)

    text = Text("Other way around", color=SECONDARY).shift(1.5*UP)
    scene.play(Write(text))
    scene.wait(2)

    common_coefficient = MathTex("ax + ay = a(x + y)").scale(1.25).move_to(ORIGIN+0.25*UP)
    vector_coefficient = MathTex(vector_to_tex(["ax", "ay"]) + " = a" + vector_to_tex(["x", "y"]))
    matrix_coefficient = MathTex(matrix_to_tex([[r"\delta a", r"\delta b"], [r"\delta c", r"\delta d"]]) + r" = \delta " + matrix_to_tex([["a", "b"], ["c", "d"]]))
    VGroup(vector_coefficient, matrix_coefficient).arrange(RIGHT, buff=1).move_to(ORIGIN + DOWN)

    common_coefficient[0][0].set_color(gruvbox.GREEN)
    common_coefficient[0][3].set_color(gruvbox.GREEN)
    common_coefficient[0][1].set_color(gruvbox.RED)
    common_coefficient[0][4].set_color(gruvbox.RED)
    common_coefficient[0][6].set_color(gruvbox.GREEN)
    common_coefficient[0][8].set_color(gruvbox.RED)
    common_coefficient[0][10].set_color(gruvbox.RED)

    vector_coefficient[0][1].set_color(gruvbox.GREEN)
    vector_coefficient[0][3].set_color(gruvbox.GREEN)
    vector_coefficient[0][7].set_color(gruvbox.GREEN)
    vector_coefficient[0][2].set_color(gruvbox.RED)
    vector_coefficient[0][4].set_color(gruvbox.RED)
    vector_coefficient[0][9].set_color(gruvbox.RED)
    vector_coefficient[0][10].set_color(gruvbox.RED)

    matrix_coefficient[0][1].set_color(gruvbox.GREEN)
    matrix_coefficient[0][3].set_color(gruvbox.GREEN)
    matrix_coefficient[0][5].set_color(gruvbox.GREEN)
    matrix_coefficient[0][7].set_color(gruvbox.GREEN)
    matrix_coefficient[0][11].set_color(gruvbox.GREEN)
    matrix_coefficient[0][2].set_color(gruvbox.RED)
    matrix_coefficient[0][4].set_color(gruvbox.RED)
    matrix_coefficient[0][6].set_color(gruvbox.RED)
    matrix_coefficient[0][8].set_color(gruvbox.RED)
    matrix_coefficient[0][13].set_color(gruvbox.RED)
    matrix_coefficient[0][14].set_color(gruvbox.RED)
    matrix_coefficient[0][15].set_color(gruvbox.RED)
    matrix_coefficient[0][16].set_color(gruvbox.RED)

    scene.play(Write(common_coefficient[0][:5]))
    scene.wait(0.5)
    scene.play(
        TransformFromCopy(VGroup(common_coefficient[0][0], common_coefficient[0][3]), common_coefficient[0][6]),
        TransformFromCopy(VGroup(common_coefficient[0][1], common_coefficient[0][2], common_coefficient[0][4]), common_coefficient[0][8:11]),
        Write(common_coefficient[0][5]), Write(common_coefficient[0][7]), Write(common_coefficient[0][11]),
    )
    scene.wait(1)
    scene.play(Write(vector_coefficient), Write(matrix_coefficient))
    scene.wait(2)
    scene.play(FadeOut(common_coefficient, vector_coefficient, matrix_coefficient))
    scene.wait(1)

    vector_common_matrix = MathTex(vector_to_tex(["x + y", "x"]) + r" = {}?" + vector_to_tex(["x", "y"]))
    line = MathTex(vector_to_tex(["x + y", "x"]) + " = x" + vector_to_tex([1, 1]) + " + y" + vector_to_tex([1, 0]) + " = " + matrix_to_tex([[1, 1], [1, 0]]) + vector_to_tex(["x", "y"])).next_to(vector_common_matrix, DOWN)
    vector_common_matrix[0][1].set_color(gruvbox.GREEN)
    vector_common_matrix[0][3].set_color(gruvbox.RED)
    vector_common_matrix[0][4].set_color(gruvbox.GREEN)
    vector_common_matrix[0][7].set_color(EMPHASIZED)
    vector_common_matrix[0][9].set_color(gruvbox.GREEN)
    vector_common_matrix[0][10].set_color(gruvbox.RED)

    line[0][1].set_color(gruvbox.GREEN)
    line[0][3].set_color(gruvbox.RED)
    line[0][4].set_color(gruvbox.GREEN)
    line[0][7].set_color(gruvbox.GREEN)
    line[0][13].set_color(gruvbox.RED)
    line[0][19:25].set_color(EMPHASIZED)
    line[0][26].set_color(gruvbox.GREEN)
    line[0][27].set_color(gruvbox.RED)

    scene.play(Write(vector_common_matrix))
    scene.wait(1)
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

    scene.play(FadeOut(vector_common_matrix, line, text))
    scene.wait(0.5)

    text = Text("Special matrices").scale(1.5).move_to(ORIGIN)
    rainbow = [gruvbox.RED, gruvbox.ORANGE, gruvbox.YELLOW, gruvbox.GREEN, gruvbox.CYAN, gruvbox.BLUE, gruvbox.PURPLE]
    for i in range(len(text)):
        text[i].set_color(rainbow[i % len(rainbow)])
    scene.play(Write(text))
    scene.wait(2)
    scene.play(FadeOut(text))
    scene.wait(0.5)
    matrix = MathTex(matrix_to_tex([["a", 0], [0, "b"]])).move_to(ORIGIN).scale(1.25)
    matrix[0][1].set_color(gruvbox.PRIMARY)
    matrix[0][4].set_color(gruvbox.SECONDARY)
    subtitle = Text("Diagonal matrix", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5 * UP)
    for i in range(len(subtitle)):
        subtitle[i].set_color(rainbow[i % len(rainbow)])
    scene.play(
        FadeIn(subtitle),
        Write(matrix),
    )
    scene.wait(2)

    diagonal_multiplication_tex = MathTex(
        matrix_to_tex([["a", 0], [0, "b"]]) + matrix_to_tex([["c", 0], [0, "d"]]) + " = " +
        matrix_to_tex([["ac", 0], [0, "bd"]])
    ).scale(1.25).move_to(ORIGIN)
    diagonal_multiplication_tex[0][1].set_color(gruvbox.GREEN)
    diagonal_multiplication_tex[0][4].set_color(gruvbox.GREEN)
    diagonal_multiplication_tex[0][7].set_color(gruvbox.RED)
    diagonal_multiplication_tex[0][10].set_color(gruvbox.RED)
    diagonal_multiplication_tex[0][14].set_color(gruvbox.GREEN)
    diagonal_multiplication_tex[0][15].set_color(gruvbox.RED)
    diagonal_multiplication_tex[0][18].set_color(gruvbox.GREEN)
    diagonal_multiplication_tex[0][19].set_color(gruvbox.RED)

    scene.play(
        matrix.animate.move_to(diagonal_multiplication_tex[0][:6]),
        matrix[0][1].animate.set_color(gruvbox.GREEN).move_to(diagonal_multiplication_tex[0][1]),
        matrix[0][4].animate.set_color(gruvbox.GREEN).move_to(diagonal_multiplication_tex[0][4]),
        Write(diagonal_multiplication_tex[0][6:])
    )

    scene.wait(2)
    identity = MathTex("I = " + matrix_to_tex([[1, 0], [0, 1]])).scale(1.25).move_to(ORIGIN)
    identity[0][3].set_color(gruvbox.PRIMARY)
    identity[0][6].set_color(gruvbox.PRIMARY)
    next_subtitle = Text("Identity matrix", color=gruvbox.SECONDARY).move_to(ORIGIN).shift(1.5 * UP)
    for i in range(len(next_subtitle)):
        next_subtitle[i].set_color(rainbow[i % len(rainbow)])
    scene.play(
        Transform(matrix, identity[0][2:]),
        Write(identity[0][:2]),
        subtitle.animate.become(
            next_subtitle
        ),
        FadeOut(diagonal_multiplication_tex[0][6:]),
    )
    scene.remove(matrix, *identity[0])
    scene.add(identity)

    identity_tex = matrix_to_tex([[1, 0], [0, 1]])
    matrix_tex = matrix_to_tex([["a", "b"], ["c", "d"]])
    vector_tex = r"\begin{bmatrix} x \\ y \end{bmatrix}"
    line0 = MathTex(
        identity_tex + vector_tex + " = " + vector_tex,
        substrings_to_isolate=[identity_tex, vector_tex]
    ).scale(1.25)
    line1 = MathTex(
        identity_tex + matrix_tex + " = " + matrix_tex,
        substrings_to_isolate=[identity_tex, matrix_tex]
    ).scale(1.25).next_to(line0, DOWN, buff=0.5, aligned_edge=LEFT)

    line0[0].set_color(PRIMARY)
    line0[1].set_color(RED)
    line0[3].set_color(RED)

    line1[0].set_color(PRIMARY)
    line1[1].set_color(GREEN)
    line1[3].set_color(GREEN)

    scene.wait(2)
    group = VGroup(line0, line1)
    group.shift(-group.get_center()[0]*RIGHT)
    scene.play(
        LaggedStart(
            AnimationGroup(
                identity[0][2:].copy().animate.move_to(line0[0]).set_color(PRIMARY),
                Write(line0[1:]),
            ),
            AnimationGroup(
                identity[0][2:].copy().animate.move_to(line1[0]).set_color(PRIMARY),
                Write(line1[1:]),
            ),
            lag_ratio=0.3
        ),
        FadeOut(identity),
        run_time=1.5
    )
    scene.remove(*scene.mobjects)
    scene.add(title, subtitle, line0, line1)
    scene.wait(2)

    scene.play(FadeOut(line0, line1, subtitle), run_time=1.5)
    scene.wait(0.5)

    text = Text("Inverse matrices", color=DANGER).scale(1.5).move_to(ORIGIN)
    scene.play(Write(text))
    scene.wait(1)
    scene.play(
        text.animate.scale(1/1.5).move_to(ORIGIN).shift(1.5*UP),
    )
    scene.wait(0.5)
    line0 = MathTex(r"x \cdot \frac{1}{x} = 1").scale(1.25).move_to(ORIGIN)
    line1 = MathTex(matrix_to_tex([["a", "b"], ["c", "d"]]) + matrix_to_tex([["a", "b"], ["c", "d"]]) + "^{-1} = I").scale(1.25).next_to(line0, DOWN, buff=0.5)
    line0[0][0].set_color(gruvbox.SECONDARY)
    line0[0][4].set_color(gruvbox.SECONDARY)

    line1[0][:6].set_color(gruvbox.SECONDARY)
    line1[0][6:12].set_color(SECONDARY)

    scene.play(Write(line0))
    scene.wait(1)
    scene.play(Write(line1))
    scene.wait(4)


def learning_time(scene):
    scene.remove(*scene.mobjects)
    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5*GOLDEN)
    bubble = Bubble().scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    text = Text("Learning time!").next_to(bubble, UP)
    bubble.add_content(text)
    text.scale(1.15)
    scene.play(FadeIn(rabbit))
    scene.wait(0.5)
    scene.play(DrawBorderThenFill(bubble), Write(text), run_time=2)
    scene.wait(2)

    white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(
        LEFT).shift(0.5 * LEFT)
    scene.play(FadeIn(white_screen))

    title = Text("Vectors and Matrices", color=DARK_PURPLE).scale(1.5).move_to(ORIGIN).shift(UP).set_z_index(2)
    timestamp = Text("skip to 0:00", color=BG).move_to(ORIGIN).shift(DOWN).set_z_index(2)
    scene.play(Write(title))
    scene.wait(2)
    scene.play(Write(timestamp))
    scene.wait(2)
    scene.remove(bubble, text, rabbit)
    scene.play(FadeOut(timestamp, title, white_screen), run_time=2)
    scene.wait(1)
    #learning_time_vectors(scene)
    learning_time_matrices(scene)


def matrix_representation(scene):
    scene.remove(*scene.mobjects)

    frame = Rectangle(width=WIDTH / 2, height=HEIGHT / 2 + 2, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(
        RIGHT)

    rabbit_breeder = RabbitBreeder(3, 2, frame, buff=0.1)

    formula = MathTex("P_n = P_{n-1} + P_{n-2}").scale(1.5).to_edge(LEFT)

    formula[0][0:2].set_color(PRIMARY)
    formula[0][3:7].set_color(SECONDARY)
    formula[0][8:].set_color(CYAN)

    scene.add(frame, rabbit_breeder, formula)
    scene.wait(2)

    next_rabbit_breeder = RabbitBreeder(1, 1, frame, buff=0.1)

    pair = MathTex(r"\begin{bmatrix} 1 \\ 1 \end{bmatrix}").scale(1.5).to_edge(LEFT).shift(0.5*RIGHT).set_color(PRIMARY)
    arrow = MathTex(r"\longrightarrow").scale(2).next_to(pair, RIGHT)
    next_pair = MathTex(r"\begin{bmatrix} 2 \\ 1 \end{bmatrix}").scale(1.5).next_to(arrow, RIGHT).set_color(SECONDARY)
    scene.play(
        Transform(rabbit_breeder.babyRabbits, next_rabbit_breeder.babyRabbits),
        Transform(rabbit_breeder.grownRabbits, next_rabbit_breeder.grownRabbits),
        Transform(formula, pair)
    )
    scene.remove(formula, rabbit_breeder)
    rabbit_breeder = next_rabbit_breeder
    scene.add(pair, rabbit_breeder)
    scene.wait(1)

    rabbit_breeder.animate_pass_month(scene, extra_animations=[Write(arrow), TransformFromCopy(pair, next_pair)])
    scene.wait(2)

    arc = ArcBetweenPoints(start=next_pair.get_center(), end=pair.get_center(), angle=-PI/1.5)
    scene.play(FadeOut(pair), MoveAlongPath(next_pair, arc))
    scene.play(next_pair.animate.set_color(PRIMARY), run_time=0.5)
    pair = next_pair.copy()
    scene.remove(next_pair)
    scene.add(pair)
    scene.wait(1)

    next_pair = MathTex(r"\begin{bmatrix} 3 \\ 2 \end{bmatrix}").scale(1.5).next_to(arrow, RIGHT).set_color(SECONDARY)
    rabbit_breeder.animate_pass_month(scene, extra_animations=[TransformFromCopy(pair, next_pair)])
    scene.wait(2)

    scene.play(FadeOut(pair), MoveAlongPath(next_pair, arc))
    scene.play(next_pair.animate.set_color(PRIMARY), run_time=0.5)
    pair = next_pair.copy()
    scene.remove(next_pair)
    scene.add(pair)

    next_pair = MathTex(r"\begin{bmatrix} 5 \\ 3 \end{bmatrix}").scale(1.5).next_to(arrow, RIGHT).set_color(SECONDARY)
    rabbit_breeder.animate_pass_month(scene, extra_animations=[TransformFromCopy(pair, next_pair)])
    scene.wait(2)

    general_arrow = MathTex(r"\longrightarrow").scale(2).move_to(arrow.get_center())
    general_pair = MathTex(r"\begin{bmatrix} x \\ y \end{bmatrix}").scale(1.5).next_to(general_arrow, LEFT).set_color(PRIMARY)
    general_next_pair = MathTex(r"\begin{bmatrix} x+y \\ x \end{bmatrix}").scale(1.5).next_to(general_arrow, RIGHT).set_color(SECONDARY)

    scene.play(Transform(pair, general_pair),
               Transform(arrow, general_arrow),
               Transform(next_pair, general_next_pair))

    line1 = VGroup(general_arrow, general_pair, general_next_pair)
    scene.remove(pair, arrow, next_pair)
    scene.add(line1)
    line2 = MathTex(r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix} ", r"\begin{bmatrix} x \\ y \end{bmatrix}", " = ", r"\begin{bmatrix} x+y \\ x \end{bmatrix}").scale(1.25)

    location = line1.get_center()
    VGroup(line1, line2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    shift = location - line1.get_center()
    line2.shift(shift + 0.25*LEFT)
    line1.shift(shift)

    line2.set_color_by_tex(r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}", PRIMARY)
    line2.set_color_by_tex(r"\begin{bmatrix} x \\ y \end{bmatrix}", SECONDARY)
    line2.set_color_by_tex(r"\begin{bmatrix} x+y \\ x \end{bmatrix}", CYAN)
    cline1 = line1.copy()
    scene.play(line1.animate.shift(1.5*UP), TransformMatchingTex(cline1, line2))
    scene.wait(2)

    line3 = MathTex(r"A", r"\begin{bmatrix} x \\ y \end{bmatrix}", " = ", r"\begin{bmatrix} x+y \\ x \end{bmatrix}").scale(1.25).move_to(line2.get_center())
    line3.set_color_by_tex(r"A", PRIMARY)
    line3.set_color_by_tex(r"\begin{bmatrix} x \\ y \end{bmatrix}", SECONDARY)
    line3.set_color_by_tex(r"\begin{bmatrix} x+y \\ x \end{bmatrix}", CYAN)
    line3.get_part_by_tex("A").scale(1.5)
    scene.play(Transform(line2, line3))
    scene.wait(2)

    A = MathTex("A").scale(2.5).set_color(PRIMARY).to_edge(LEFT).shift(0.5*RIGHT)
    pair = MathTex(r"\begin{bmatrix} 1 \\ 1 \end{bmatrix}").scale(1.5).next_to(A, RIGHT).set_color(SECONDARY)
    equals = MathTex("=").scale(1.5).next_to(pair, RIGHT)

    next_rabbit_breeder = RabbitBreeder(1, 1, frame, buff=0.1)

    scene.remove(line2)

    scene.play(
        FadeOut(line1), Transform(line3, VGroup(A, pair, equals)),
        Transform(rabbit_breeder.babyRabbits, next_rabbit_breeder.babyRabbits),
        Transform(rabbit_breeder.grownRabbits, next_rabbit_breeder.grownRabbits)
    )
    scene.remove(formula, rabbit_breeder)
    rabbit_breeder = next_rabbit_breeder
    scene.add(pair, rabbit_breeder)
    scene.remove(line1, line2, line3)
    scene.add(A, pair, equals)
    scene.wait(2)

    next_pair = MathTex(r"\begin{bmatrix} 2 \\ 1 \end{bmatrix}").scale(1.5).next_to(equals, RIGHT).set_color(CYAN)
    rabbit_breeder.animate_pass_month(scene, extra_animations=[TransformFromCopy(pair, next_pair)])
    scene.wait(2)

    arc = ArcBetweenPoints(start=next_pair.get_center(), end=pair.get_center(), angle=-PI / 1.5)
    scene.play(FadeOut(pair), MoveAlongPath(next_pair, arc))
    scene.play(next_pair.animate.set_color(SECONDARY), run_time=0.5)
    pair = next_pair.copy()
    scene.remove(next_pair)
    scene.add(pair)
    scene.wait(1)

    next_pair = MathTex(r"\begin{bmatrix} 3 \\ 2 \end{bmatrix}").scale(1.5).next_to(equals, RIGHT).set_color(CYAN)
    rabbit_breeder.animate_pass_month(scene, extra_animations=[TransformFromCopy(pair, next_pair)])
    scene.wait(2)

    scene.play(FadeOut(pair), MoveAlongPath(next_pair, arc))
    scene.play(next_pair.animate.set_color(SECONDARY), run_time=0.5)
    pair = next_pair.copy()
    scene.remove(next_pair)
    scene.add(pair)
    scene.wait(1)

    new_A = MathTex(r"A^n").scale(2.5).set_color(PRIMARY).to_edge(LEFT)
    new_pair = MathTex(r"\begin{bmatrix} 1 \\ 1 \end{bmatrix}").scale(1.5).next_to(new_A, RIGHT).set_color(SECONDARY)
    scene.play(
        A.animate.become(new_A),
        pair.animate.become(new_pair).next_to(new_A),
        equals.animate.next_to(new_pair)
    )
    scene.wait(1)

    new_pair = MathTex(r"\begin{bmatrix} F_{n+1} \\ F_{n} \end{bmatrix}").scale(1.5).next_to(equals, RIGHT).set_color(CYAN)
    scene.play(TransformFromCopy(pair, new_pair))
    scene.wait(2)


def conclusion(scene):
    scene.remove(*scene.mobjects)
    arrow = MathTex("\longrightarrow").scale(2).rotate(-PI/2).move_to(ORIGIN)
    text1 = Tex("Finding the n'th Fibonacci number").scale(1.5).next_to(arrow, UP).set_color(PRIMARY)
    text2 = Tex("Calculating ", "$A^n$").scale(1.5).next_to(arrow, DOWN).set_color(SECONDARY)
    text2[1].set_color(CYAN)
    scene.add(text1)
    scene.play(Write(arrow), Write(text2), run_time=2)
    scene.wait(2)

    white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(LEFT).shift(0.5*LEFT).set_opacity(0.25)
    scene.play(FadeIn(white_screen))

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5*GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(8*LEFT + 2.7*DOWN)
    scene.play(rabbit.animate.shift(2*RIGHT))

    bubble = Bubble().scale(0.5).pin_to(rabbit).shift(0.5*DOWN + 0.25*LEFT)
    text = Text("But thats just as hard!").next_to(bubble, UP)
    bubble.add_content(text)
    text.scale(1.15)
    scene.play(DrawBorderThenFill(bubble), Write(text))
    scene.wait(2)
    scene.play(white_screen.animate.set_opacity(1), FadeOut(bubble), FadeOut(text), FadeOut(rabbit))

    matrix = r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
    matrices = [MathTex(matrix, color=BG) for _ in range(5)]

    A = MathTex(r"A^5 =", color=BG).scale(2)
    for i, matrix in enumerate(matrices):
        if i == 0: matrix.next_to(A, RIGHT)
        else: matrix.next_to(matrices[i-1], RIGHT)

    VGroup(A, *matrices).move_to(ORIGIN)

    scene.play(Write(VGroup(A, *matrices)))
    scene.wait(2)
    matrix_num = [[1, 1], [1, 0]]
    next_matrix = None
    for i in range(1, 5):
        next_matrix_num = np.linalg.matrix_power(matrix_num, i+1)
        next_matrix = MathTex(matrix_to_tex(next_matrix_num), color=BG).move_to(matrices[-i-1].get_center())
        scene.play(Transform(matrices[-i], next_matrix), FadeOut(matrices[-i-1]))
        scene.remove(matrices[-i-1], matrices[-i])
        matrices[-i-1] = next_matrix
        scene.add(matrices[-i-1])
        scene.wait(0.5)
    scene.wait(2)
    scene.play(FadeOut(A), FadeOut(next_matrix), FadeOut(white_screen), run_time=2)
    scene.wait(2)
    scene.play(FadeOut(text1, text2, arrow), run_time=2)
    scene.wait(2)


class Chapter2(Scene):
    def construct(self):
        #introduction(self)
        learning_time(self)
        #matrix_representation(self)
        #conclusion(self)