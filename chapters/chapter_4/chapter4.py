from manim import *
from extra.color_schemes import gruvbox
from util_lib.SpeechBubble import Bubble
from extra.color_schemes.gruvbox import *
from util_lib.utils import *
from util_lib import rabbitBreeder
from util_lib.rabbit_breeder import RabbitBreeder

PHI = GOLDEN
PSI = -INGOLDEN


def introduction(scene):
    scene.remove(*scene.mobjects)
    title = Text("Chapter 4: Who Are You?").move_to(ORIGIN)
    scene.play(Write(title), run_time=5)
    scene.wait(2)
    scene.play(FadeOut(title), run_time=3)
    scene.wait(2)

    text = Text("Which basis?", color=DANGER).scale(1.5).shift(2*UP)
    tex = MathTex("B = " + matrix_to_tex([["a", 0], [0, "b"]])).scale(1.25)
    tex[0][0].set_color(PRIMARY)
    tex[0][3].set_color(SECONDARY)
    tex[0][6].set_color(CYAN)

    scene.play(Write(tex), FadeIn(text), run_time=1.5)
    scene.wait(2)
    scene.play(FadeOut(tex, text))
    scene.wait(2)


def eigenbasis(scene):
    scene.remove(*scene.mobjects)
    plane = EpicPlane()
    transition_matrix = [[PHI, PSI], [1, 1]]
    plane.apply_matrix(transition_matrix)

    u1 = ChillVector(np.dot(transition_matrix, [1, 0]), color=gruvbox.GREEN)
    u2 = ChillVector(np.dot(transition_matrix, [0, 1]), color=gruvbox.RED)

    u1_label = Tex("$u_1$", color=gruvbox.GREEN).move_to(u1.get_center() + 0.25*DOWN + 0.25*RIGHT)
    u2_label = Tex("$u_2$", color=gruvbox.RED).move_to(u2.get_center() + 0.25*DOWN + 0.3*LEFT)

    u1_coords = u1.transformed_coordinate_label(transition_matrix)
    u2_coords = u2.transformed_coordinate_label(transition_matrix)

    scene.play(FadeIn(plane, u1, u2))
    scene.wait(1)
    scene.play(Write(u1_label), Write(u2_label))
    scene.wait(1)
    scene.play(Write(u1_coords), Write(u2_coords))
    scene.wait(2)

    b_tex = matrix_to_tex([[r"\lambda_1", 0], [0, r"\lambda_2"]])
    diagonal_b = MathTex("B = " + b_tex).scale(1.25).to_corner(UL).shift(0.25*DOWN + 0.25*RIGHT)
    diagonal_b[0][0].set_color(PRIMARY)
    diagonal_b[0][3:5].set_color(SECONDARY)
    diagonal_b[0][7:9].set_color(CYAN)
    scene.play(Write(diagonal_b))
    scene.wait(2)

    u1_ghost = u1.copy().set_opacity(0.5)
    u2_ghost = u2.copy().set_opacity(0.5)

    lines = VGroup(
        MathTex(
            b_tex + vector_to_tex([1, 0]) + " = " + vector_to_tex([r"\lambda_1", 0]),
            substrings_to_isolate=[b_tex, vector_to_tex([1, 0]), vector_to_tex([r"\lambda_1", 0])]
        ).next_to(diagonal_b, DOWN, aligned_edge=LEFT),

        MathTex(
            b_tex + vector_to_tex([0, 1]) + " = " + vector_to_tex([0, r"\lambda_2"]),
            substrings_to_isolate=[b_tex, vector_to_tex([0, 1]), vector_to_tex([0, r"\lambda_2"])]
        ),
    )
    lines[1].next_to(lines[0], DOWN, aligned_edge=LEFT)

    lines[0][0].set_color(PRIMARY)
    lines[0][1].set_color(GREEN)
    lines[0][3].set_color(GREEN)

    lines[1][0].set_color(PRIMARY)
    lines[1][1].set_color(RED)
    lines[1][3].set_color(RED)


    scene.add(u1_ghost)
    next_vector = ChillVector(np.dot(transition_matrix, [PHI, 0]), color=gruvbox.GREEN)
    scene.play(
        u1.animate.become(next_vector),
        u1_coords.animate.become(next_vector.custom_coordinate_label([r"\lambda_1", 0])),
        u1_label.animate.move_to(next_vector.get_center() + 0.25 * DOWN + 0.25 * RIGHT),
        Write(lines[0]),
        run_time=1.5
    )
    scene.wait(2)
    scene.add(u2_ghost)
    next_vector = ChillVector(np.dot(transition_matrix, [0, PSI]), color=gruvbox.RED)
    scene.play(
        u2.animate.become(next_vector),
        u2_coords.animate.become(next_vector.custom_coordinate_label([0, r"\lambda_2"])),
        u2_label.animate.move_to(next_vector.get_center() + 0.25 * DOWN + 0.3 * LEFT),
        Write(lines[1]),
        run_time=1.5
    )
    scene.wait(2)
    line1 = Line(
        (*np.dot(transition_matrix, [0, -5]), 0),
        (*np.dot(transition_matrix, [0, 5]), 0),
        stroke_width=3, color=gruvbox.YELLOW
    ).shift((*np.dot(transition_matrix, [0, -10]), 0))
    line2 = Line(
        (*np.dot(transition_matrix, [-5, 0]), 0),
        (*np.dot(transition_matrix, [5, 0]), 0),
        stroke_width=3, color=gruvbox.YELLOW
    ).shift((*np.dot(transition_matrix, [-10, 0]), 0))

    u2.set_z_index(1)
    u2_coords.set_z_index(1)
    scene.play(line1.animate.shift((*np.dot(transition_matrix, [0, 10]), 0)), run_time=2)
    scene.wait(1)

    A_tex = matrix_to_tex([[1, 1], [1, 0]])
    A = MathTex("A = " + A_tex).scale(1.25).to_corner(UL).shift(0.25*DOWN + 0.25*RIGHT)
    A[0][0].set_color(PRIMARY)
    A[0][2:].set_color(CYAN)

    u1.set_z_index(1)
    u1_coords.set_z_index(1)
    scene.play(
        line2.animate.shift((*np.dot(transition_matrix, [10, 0]), 0)),
        run_time=2,
    )
    u1_ghost.set_z_index(1)
    u2_ghost.set_z_index(1)
    scene.play(
        plane.animate.apply_matrix(np.linalg.inv(transition_matrix)),
        diagonal_b.animate.become(A),
        FadeOut(lines[0], lines[1]),
        FadeOut(u1, u1_coords, u2, u2_coords),
        u1_label.animate.move_to(u1_ghost.get_center() + 0.25*DOWN + 0.25*RIGHT),
        u2_label.animate.move_to(u2_ghost.get_center() + 0.25 * DOWN + 0.3 * LEFT),
        u1_ghost.animate.set_opacity(1),
        u2_ghost.animate.set_opacity(1),
        run_time=2
    )
    A = diagonal_b
    scene.wait(2)

    u1_transform = u1_ghost.copy()
    u2_transform = u2_ghost.copy()

    u1_ghost.set_opacity(0.5).set_z_index(0)
    u2_ghost.set_opacity(0.5).set_z_index(0)
    scene.play(
        Transform(u1_transform, u1),
        Transform(u2_transform, u2),
        u1_label.animate.move_to(u1.get_center() + 0.25 * DOWN + 0.25 * RIGHT),
        u2_label.animate.move_to(u2.get_center() + 0.25 * DOWN + 0.3 * LEFT),
        run_time=1.5
    )
    scene.remove(u1_transform, u2_transform, u1, u2)
    scene.add(u1, u2)
    scene.wait(2)
    u1_ghost.set_z_index(1)
    u2_ghost.set_z_index(1)
    scene.play(
        FadeOut(u1, u2, u1_label, u2_label),
        u1_ghost.animate.set_opacity(1),
        u2_ghost.animate.set_opacity(1),
        run_time=1.5
    )
    scene.wait(1)

    u1 = u1_ghost
    u2 = u2_ghost

    slope1 = 1/PHI
    slope2 = 1/PSI
    angle1 = np.arctan(slope1)
    angle2 = np.arctan(slope2)
    tangent1 = np.arctan(slope1) + DEGREES*90
    tangent2 = np.arctan(slope2) + DEGREES*90

    text1 = Text("Eigenvector").move_to(
        u1.get_center() + 0.3*(np.sin(tangent1)*UP + np.cos(tangent1)*RIGHT) +
        0.5*(np.sin(angle1)*UP + np.cos(angle1)*RIGHT)
    ).rotate(angle1).scale(0.6)
    rainbow_text(text1)

    text2 = Text("Eigenvector").move_to(
        u2.get_center() - 0.3*(np.sin(tangent2)*UP + np.cos(tangent2)*RIGHT) +
        -0.75*(np.sin(angle2)*UP + np.cos(angle2)*RIGHT)
    ).rotate(angle2).scale(0.6)
    rainbow_text(text2)

    scene.play(Write(text1), Write(text2))
    scene.wait(1)

    text3 = Tex(r"Eigenvalue = $\lambda_1$").move_to(
        u1.get_center() - 0.3*(np.sin(tangent1)*UP + np.cos(tangent1)*RIGHT) +
        0.75*(np.sin(angle1)*UP + np.cos(angle1)*RIGHT)
    ).rotate(angle1).scale(0.75)
    text4 = Tex(r"Eigenvalue = $\lambda_2$").move_to(
        u2.get_center() - 0.75*(np.sin(tangent2)*UP + np.cos(tangent2)*RIGHT) +
        -0.8*(np.sin(angle2)*UP + np.cos(angle2)*RIGHT)
    ).rotate(angle2).scale(0.75)

    text3[0][:10].set_color(PRIMARY)
    text3[0][11:].set_color(gruvbox.GREEN)
    text4[0][:10].set_color(PRIMARY)
    text4[0][11:].set_color(gruvbox.RED)

    scene.play(Write(text3), Write(text4))
    scene.wait(2)

    u1_label.move_to(u1.get_center() + 0.25 * DOWN + 0.25 * RIGHT)
    u2_label.move_to(u2.get_center() + 0.25 * DOWN + 0.3 * LEFT)
    scene.play(
        plane.animate.apply_matrix(transition_matrix),
        FadeIn(u1_label, u2_label),
        FadeOut(text1, text2, text3, text4, line1, line2, A),
        run_time=2
    )
    scene.wait(1)
    scene.play(
        u1_label.animate.become(
            Tex("?", color=DANGER).move_to(u1.get_center() + 0.25 * DOWN + 0.25 * RIGHT)
        ),
        u2_label.animate.become(
            Tex("?", color=DANGER).move_to(u2.get_center() + 0.25 * DOWN + 0.3 * LEFT)
        ),
    )
    scene.wait(1)
    diagonal_b = MathTex("B = " + b_tex).scale(1.25).to_corner(UL).shift(0.25 * DOWN + 0.25 * RIGHT)
    diagonal_b[0][0].set_color(PRIMARY)
    diagonal_b[0][3:5].set_color(SECONDARY)
    diagonal_b[0][7:9].set_color(CYAN)
    scene.play(
        Write(diagonal_b),
        run_time=1.5
    )
    scene.wait(2)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5*GOLDEN)
    rabbit.move_to(8*LEFT + 2.7*DOWN)
    scene.play(rabbit.animate.shift(2 * RIGHT))
    bubble = Bubble(fill_opacity=0.5, content_scale_factor=0.8).scale(0.4).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    tex = MathTex(r"A0 = 0 = \lambda 0").set_z_index(1)
    tex[0][0].set_color(PRIMARY)
    tex[0][5].set_color(SECONDARY)
    bubble.add_content(tex)
    scene.play(DrawBorderThenFill(bubble), Write(tex))
    next_tex = MathTex(r"A0 = \lambda 0").set_z_index(1)
    next_tex[0][0].set_color(PRIMARY)
    next_tex[0][3].set_color(SECONDARY)
    bubble.add_content(next_tex)
    scene.play(Transform(tex, next_tex))
    scene.wait(2)

    second_rabbit = rabbit.copy().shift(12*RIGHT)
    scene.play(FadeIn(second_rabbit))
    bubble2 = Bubble(fill_opacity=0.5, content_scale_factor=0.8).scale(0.5).pin_to(second_rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    tex2 = Tex("0 doesnt count").set_z_index(1)
    bubble2.add_content(tex2)
    scene.play(DrawBorderThenFill(bubble2), Write(tex2))
    scene.wait(2)

    
def find_eigenbasis(scene):
    scene.remove(*scene.mobjects)
    frame = Rectangle(height=5, width=5, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(RIGHT, buff=0.5)
    plane = scale_plane_to_fit_frame(EpicPlane((-3, 3, 1)).move_to(frame), frame)
    vector = plot_vector([PHI, 1], plane, color=PRIMARY)
    vector_label = get_vector_label(r"$v$", vector)

    ghost_vector = vector.copy().set_opacity(0.5)
    next_vector = plot_vector([PHI**2, PHI], plane, color=PRIMARY)
    next_vector_label = get_vector_label(r"$\lambda v$", next_vector, buff=0.4)

    line0 = MathTex(r"Av = \lambda v").scale(1.5).move_to(ORIGIN + UP + 3*LEFT)
    line0[0][0].set_color(PRIMARY)
    line0[0][3].set_color(SECONDARY)

    scene.add(frame, plane, vector, vector_label)
    scene.wait(1)
    scene.add(ghost_vector)
    scene.play(
        Write(line0),
        vector.animate.become(next_vector),
        vector_label.animate.become(next_vector_label),
        run_time=1.5
    )
    scene.wait(2)

    A_tex = matrix_to_tex([[1, 1], [1, 0]])
    v_tex = vector_to_tex(["x", "y"])
    line1 = MathTex(
        A_tex + v_tex + " = " + r"\lambda" + v_tex,
        substrings_to_isolate=[A_tex, v_tex, r"\lambda"]
    ).scale(1.25).move_to(ORIGIN + UP + 3*LEFT)
    line1[1].set_color(PRIMARY)
    line1[3].set_color(SECONDARY)
    line1[4].set_color(PRIMARY)

    scene.play(
        Transform(line0[0][0], line1[0]),
        Transform(line0[0][1], line1[1]),
        Transform(line0[0][2], line1[2]),
        Transform(line0[0][3], line1[3]),
        Transform(line0[0][4], line1[4]),
    )
    scene.remove(line0)
    scene.add(line1)
    scene.wait(2)

    line2 = MathTex(
        r" \begin{cases}"
        r" x + y = \lambda x \\"
        r"x = \lambda y"
        r"\end{cases}",
    ).scale(1.25).move_to(ORIGIN + UP + 3*LEFT)

    secondary_indices = [5, 9]

    scene.play(
        Transform(line1, line2)
    )
    scene.remove(line1)
    scene.add(line2)
    scene.wait(2)
    animations = []
    for i in secondary_indices:
        animations.append(line2[0][i].animate.set_color(SECONDARY))
    scene.play(*animations)
    scene.wait(2)

    line3 = MathTex(
        r"\lambda y + y = \lambda^2 y",
    ).next_to(line2, DOWN, aligned_edge=LEFT).scale(1.25).shift(UP)
    line3[0][0].set_color(SECONDARY)
    line3[0][5].set_color(SECONDARY)

    cline2 = line2.copy()
    scene.play(
        line2.animate.shift(UP),
        cline2[0][2].animate.move_to(line3[0][2]),
        cline2[0][3].animate.move_to(line3[0][3]),
        cline2[0][4].animate.move_to(line3[0][4]),
        TransformFromCopy(cline2[0][9:], line3[0][5:]),
        Transform(cline2[0][9:], line3[0][0:2]),
    )
    scene.remove(cline2)
    scene.add(line3)
    scene.wait(1)

    line4 = MathTex(
        r"\lambda^2 y - \lambda y - y = 0",
    ).scale(1.25).next_to(line3, DOWN, aligned_edge=LEFT)
    line4[0][0].set_color(SECONDARY)
    line4[0][4].set_color(SECONDARY)

    arc = ArcBetweenPoints(start=line3[0][5:].get_center(), end=line4[0][:3].get_center(), angle=-PI/1.5)

    scene.play(
        MoveAlongPath(line3[0][5:].copy(), arc),
        line3[0][:2].copy().animate.move_to(line4[0][4:6]),
        line3[0][3].copy().animate.move_to(line4[0][7]),
        Transform(line3[0][2].copy(), line4[0][6]),
        Transform(line3[0][4].copy(), line4[0][8]),
        Write(line4[0][9])
    )
    scene.remove(*scene.mobjects)
    scene.add(frame, plane, vector, ghost_vector, vector_label, line2, line3, line4)
    scene.wait(2)

    line5 = MathTex(
        r"y(\lambda^2 - \lambda - 1) = 0"
    ).scale(1.25).next_to(line3, DOWN, aligned_edge=LEFT)
    line5[0][2].set_color(SECONDARY)
    line5[0][5].set_color(SECONDARY)

    scene.play(
        line4[0][2].animate.move_to(line5[0][0]),
        line4[0][5].animate.move_to(line5[0][0]),
        line4[0][7].animate.move_to(line5[0][0]),
        line4[0][0:2].animate.move_to(line5[0][2:4]),
        line4[0][4].animate.move_to(line5[0][5]),
        line4[0][3].animate.move_to(line5[0][4]),
        line4[0][6].animate.move_to(line5[0][6]),
        line4[0][8].animate.move_to(line5[0][9]),
        line4[0][9].animate.move_to(line5[0][10]),
        FadeIn(line5[0][7], line5[0][8], line5[0][1]),
    )
    scene.remove(line4)
    scene.add(line5)
    scene.wait(2)

    line6 = MathTex(
        r"\lambda^2 - \lambda - 1 = 0"
    ).scale(1.25).next_to(line5, DOWN, aligned_edge=LEFT)
    line6[0][0].set_color(SECONDARY)
    line6[0][3].set_color(SECONDARY)

    cline5 = line5.copy()
    scene.play(
        cline5[0][2:8].animate.become(line6[0][:6]),
        cline5[0][9:].animate.become(line6[0][6:])
    )
    scene.remove(cline5)
    scene.add(line6)
    scene.wait(2)

    line7 = MathTex(
        r"\lambda_{1,2} = \frac{1 \pm \sqrt{5}}{2} = \varphi, \psi"
    ).scale(1.25).next_to(line6, DOWN, aligned_edge=LEFT)
    line7[0][0:4].set_color(SECONDARY)
    line7[0][13].set_color(gruvbox.GREEN)
    line7[0][15].set_color(gruvbox.RED)

    scene.play(Write(line7))
    scene.wait(2)

    scene.wait(2)
    scene.remove(*scene.mobjects)
    scene.add(frame, plane, vector, ghost_vector, vector_label, line2, line3, line5, line6, line7)
    scene.play(FadeOut(line3, line5, line6, line7))
    scene.wait(1)

    line3 = MathTex(r"x = \varphi y \\ x = \psi y").scale(1.25).next_to(line2, DOWN, aligned_edge=LEFT)
    line3[0][0].set_color(PRIMARY)
    line3[0][2].set_color(gruvbox.GREEN)
    line3[0][4].set_color(PRIMARY)
    line3[0][6].set_color(gruvbox.RED)

    scene.play(
        LaggedStart(
            TransformFromCopy(line2[0][7:], line3[0][:4]),
            TransformFromCopy(line2[0][7:], line3[0][4:]),
            lag_ratio=0.25
        ),
        run_time=1.5
    )
    scene.wait(2)
    scene.remove(*line3[0])
    scene.add(line3)

    implies = MathTex(r"\implies", color=EMPHASIZED).scale(1.25).rotate(-PI/2).next_to(line3, DOWN)
    line4 = MathTex(
        "u_1=" + vector_to_tex([r"\varphi", 1]) + r" \quad u_2=" + vector_to_tex([r"\psi", 1])
    ).scale(1.25).next_to(implies, DOWN)
    line4[0][:2].set_color(gruvbox.GREEN)
    line4[0][3:7].set_color(gruvbox.GREEN)
    line4[0][7:9].set_color(gruvbox.RED)
    line4[0][10:].set_color(gruvbox.RED)

    scene.play(LaggedStart(
        Write(implies), Write(line4), lag_ratio=0.25
    ), run_time=1.5)
    scene.wait(0.5)

    cvector_label = vector_label.copy()
    scene.play(
        vector.animate.become(plot_vector([PSI, 1], plane, color=gruvbox.RED)),
        cvector_label.animate.become(get_vector_label(r"$u_2$", plot_vector([PSI, 1], plane, color=gruvbox.RED), buff=0.4, direction=DOWN)),
        ghost_vector.animate.set_opacity(1).set_color(gruvbox.GREEN),
        vector_label.animate.become(get_vector_label(r"$u_1$", plot_vector([PHI, 1], plane, color=gruvbox.GREEN), buff=0.4, direction=UP)),
        run_time=1.5
    )

    u1 = ghost_vector
    u2 = vector
    u1_label = vector_label.set_z_index(1)
    u2_label = cvector_label.set_z_index(1)

    u1_ghost = u1.copy().set_opacity(0.5)
    u2_ghost = u2.copy().set_opacity(0.5)

    u1.set_z_index(1)
    u2.set_z_index(1)

    line1 = Line(
        plane.c2p(-3, -3/PHI), plane.c2p(3, 3/PHI),
        stroke_width=2, color=EMPHASIZED
    )
    line2 = Line(
        plane.c2p(3*PSI, 3), plane.c2p(-3*PSI, -3),
        stroke_width=2, color=EMPHASIZED
    )
    scene.play(
        LaggedStart(
            Create(line1), Create(line2),
            lag_ratio=0.25
        ),
        run_time=1.5
    )

    scene.add(u1_ghost)
    scene.add(u2_ghost)
    scene.play(
        u1.animate.become(plot_vector([PHI**2, PHI], plane, color=gruvbox.GREEN)),
        u1_label.animate.become(get_vector_label(r"$\lambda_1 u_1$", plot_vector([PHI**2, PHI], plane, color=gruvbox.GREEN), buff=0.5, direction=DOWN)),
        u2.animate.become(plot_vector([PSI**2, PSI], plane, color=gruvbox.RED)),
        u2_label.animate.become(get_vector_label(r"$\lambda_2 u_2$", plot_vector([PSI**2, PSI], plane, color=gruvbox.RED), buff=0.25, direction=DOWN).shift(0.3*LEFT)),
        run_time=1.5
    )
    scene.wait(2)
    scene.play(FadeOut(*scene.mobjects))
    scene.wait(1)


def the_golden_ratio(scene):
    scene.remove(*scene.mobjects)
    text = Text("the Golden Ratio", color=PRIMARY).scale(1.5).to_edge(UP)
    tex = MathTex(r"\varphi = 1 + \frac{1}{\varphi}").scale(1.5).move_to(ORIGIN)
    tex[0][0].set_color(EMPHASIZED)
    tex[0][6].set_color(EMPHASIZED)
    scene.play(
        LaggedStart(
            Write(text), Write(tex),
            lag_ratio=0.25
        ),
        run_time=3
    )
    scene.wait(2)

    tex2 = MathTex(r"\psi = 1 + \frac{1}{\psi}").scale(1.5).move_to(ORIGIN)
    tex2[0][0].set_color(DANGER)
    tex2[0][6].set_color(DANGER)
    scene.play(
        Transform(tex, tex2),
    )

    white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(LEFT).shift(0.5*LEFT).set_opacity(0.25)
    scene.play(FadeIn(white_screen))

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5*GOLDEN)
    rabbit.move_to(8*LEFT + 2.7*DOWN)
    scene.play(rabbit.animate.shift(2 * RIGHT))
    bubble = Bubble(content_scale_factor=0.8).scale(0.45).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    tex = Tex(r"Why is the \\ golden ratio here?")
    bubble.add_content(tex)
    scene.play(DrawBorderThenFill(bubble), Write(tex))
    scene.wait(1)

    rabbit2 = rabbit.copy().shift(12*RIGHT)
    scene.play(FadeIn(rabbit2))
    bubble2 = Bubble(content_scale_factor=0.8).scale(0.4).pin_to(rabbit2).shift(0.5 * DOWN + 0.25 * LEFT)
    tex2 = Tex(r"And why is \\ it an eigenvalue?")
    bubble2.add_content(tex2)
    scene.play(DrawBorderThenFill(bubble2), Write(tex2))
    scene.wait(2)
    scene.play(FadeOut(*scene.mobjects))
    scene.wait(1)


def relationship_to_fibonacci(scene):
    scene.remove(*scene.mobjects)
    rabbit = SVGMobject("assets/rabbit.svg").scale(0.4)
    pair = VGroup(rabbit.copy(), rabbit.copy().shift(0.4 * RIGHT))
    grownPair = pair.copy().scale(GOLDEN).shift(RIGHT)
    babyRabbits = VGroup(*[pair.copy() for _ in range(3)]).arrange(RIGHT).move_to(ORIGIN).shift(2*DOWN)
    grownRabbits = VGroup(*[grownPair.copy() for _ in range(5)]).arrange(RIGHT, buff=0.4).move_to(ORIGIN)

    divide_line = Line(6*LEFT, 6*RIGHT, color=FG).shift(DOWN)

    text = Text("What's the ratio?", color=PRIMARY).scale(1.5).to_edge(UP)
    scene.play(
        FadeIn(babyRabbits, grownRabbits)
    )
    scene.play(
        LaggedStart(
            Write(text),
            Write(divide_line),
            lag_ratio=0.75
        ),
        run_time=2
    )
    scene.wait(4)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.3)
    pair = VGroup(rabbit.copy(), rabbit.copy().shift(0.3 * RIGHT))
    grownPair = pair.copy().scale(GOLDEN).shift(RIGHT)
    next_grownRabbits = VGroup(*[grownPair.copy() for _ in range(5)]).arrange(RIGHT, buff=0.1).move_to(ORIGIN + 2*UP)
    next_babyRabbits = VGroup(*[pair.copy() for _ in range(3)]).arrange(RIGHT, buff=0.1*GOLDEN).move_to(ORIGIN + 0.5*UP)

    scene.play(
        Transform(grownRabbits, next_grownRabbits), Transform(babyRabbits, next_babyRabbits),
        FadeOut(text, divide_line)
    )

    tex = Tex("mature $=F_{n-1}$").shift(DOWN)
    tex2 = Tex("babies $=F_{n-2}$").next_to(tex, DOWN)

    tex[0][:6].set_color(gruvbox.PRIMARY)
    tex2[0][:6].set_color(gruvbox.SECONDARY)

    tex[0][7:].set_color(gruvbox.PRIMARY)
    tex2[0][7:].set_color(gruvbox.SECONDARY)

    grownRabbits_temp = VGroup(*[grownPair.copy() for _ in range(3)]).arrange(RIGHT, buff=0.02).move_to(ORIGIN + 2*UP + 4*LEFT)
    babyRabbits_temp = VGroup(*[pair.copy() for _ in range(2)]).arrange(RIGHT, buff=0.2).move_to(ORIGIN + UP + 4*LEFT)

    cgrownRabbits = grownRabbits.copy()
    animations = []
    for i in range(len(cgrownRabbits)):
        if i < len(grownRabbits_temp):
            animations.append(Transform(cgrownRabbits[i], grownRabbits_temp[i]))
        else:
            animations.append(Transform(cgrownRabbits[i], babyRabbits_temp[i-len(grownRabbits_temp)]))

    scene.play(babyRabbits.animate.set_opacity(0.5))
    scene.play(
        grownRabbits.animate.shift(3 * RIGHT),
        babyRabbits.animate.shift(3 * RIGHT),
        *animations,
        Write(tex),
        run_time=1.5
    )
    scene.wait(1)
    cbabyRabbits = cgrownRabbits[:3].copy()
    scene.play(
        Transform(cbabyRabbits, babyRabbits.copy().set_opacity(1)),
        Write(tex2),
        run_time=1.5
    )
    scene.remove(cbabyRabbits, babyRabbits)
    scene.add(babyRabbits.set_opacity(1))
    scene.wait(1)
    scene.play(
        FadeOut(cgrownRabbits),
        grownRabbits.animate.shift(3 * LEFT),
        babyRabbits.animate.shift(3 * LEFT),
        run_time=1.5,
    )
    scene.wait(1)

    line = MathTex(r"\frac{\text{mature}}{\text{babies}} = \frac{F_{n-1}}{F_{n-2}}").scale(1.25).to_edge(LEFT)
    line[0][0:6].set_color(gruvbox.PRIMARY)
    line[0][7:13].set_color(gruvbox.SECONDARY)
    line[0][14:18].set_color(gruvbox.PRIMARY)
    line[0][19:23].set_color(gruvbox.SECONDARY)
    scene.play(
        VGroup(grownRabbits, babyRabbits, tex, tex2).animate.shift(3*RIGHT),
        Write(line),
        run_time=1.5
    )
    scene.wait(2)

def convergence(scene):
    scene.remove(*scene.mobjects)
    frame = Rectangle(height=5.5, width=7.5, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(RIGHT, buff=0.3)
    breeder = RabbitBreeder(1, 1, frame)
    scene.add(frame, breeder)

    month = 2
    def create_ratio():
        res = MathTex(
            r"\frac{F_{"+str(month-1)+"}}{F_{"+str(month-2)+"}} ="
        ).to_edge(LEFT, buff=2).shift(UP)

        digits = len(str(month-1))

        res[0][:digits+1].set_color(gruvbox.PRIMARY)
        res[0][digits+2:-1].set_color(gruvbox.SECONDARY)
        return res

    ratio = always_redraw(create_ratio)

    approximation = DecimalNumber(
        fib(month-1)/fib(month-2),
        num_decimal_places=4,
        color=EMPHASIZED
    ).next_to(ratio, RIGHT)

    numberline = NumberLine(
        x_range=[0, 2, 0.1],
        length=5,
        include_numbers=True,
        decimal_number_config={"num_decimal_places": 0, "color": SECONDARY},
        numbers_to_include=[0, 1, 2],
        numbers_with_elongated_ticks=[0, 1, 2],
        color=FG,
    ).to_edge(LEFT).shift(2*DOWN)
    scene.add(ratio, approximation, numberline)
    pins = []
    pin = plot_on_numberline(numberline, fib(month-1)/fib(month-2), color=PRIMARY)
    pins.append(pin)
    pin_arrow = Arrow(start=pin.get_top()+0.8*UP, end=pin.get_top() + 0.2*DOWN, color=EMPHASIZED)
    scene.play(
        Write(pin),
        Write(pin_arrow),
    )

    scene.wait(1)
    for i in range(10):
        month += 1
        pin = plot_on_numberline(numberline, fib(month-1)/fib(month-2), color=PRIMARY).scale(opacity_curve(i))
        pins.append(pin)
        breeder.animate_pass_month(scene, extra_animations=[
            ratio.animate.become(create_ratio()),
            approximation.animate.set_value(fib(month-1)/fib(month-2)),
            Write(pin),
            pin_arrow.animate.shift((pin.get_center()[0] - pin_arrow.get_center()[0])*RIGHT),
            *[p.animate.set_opacity(opacity_curve(j)) for j, p in enumerate(reversed(pins[:-1]))]
        ])
        scene.wait(1)


def learning_time_introduction(scene):
    white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(LEFT).shift(0.5*LEFT)
    scene.play(FadeIn(white_screen))
    scene.remove(*scene.mobjects)
    scene.add(white_screen)
    scene.wait(1)

    title = Text("Convergence", color=DARK_PURPLE).scale(1.5).move_to(ORIGIN).shift(UP).set_z_index(2)
    timestamp = Text("skip to 0:00", color=BG).move_to(ORIGIN).shift(DOWN).set_z_index(2)
    scene.play(Write(title))
    scene.wait(2)
    scene.play(Write(timestamp))
    scene.wait(2)

    scene.play(FadeOut(title, timestamp, white_screen))


def learning_time_convergence(scene):
    #example 1
    sequence = MathTex(
        r"S = \frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \frac{1}{16}, \dots"
    )
    sequence[0][:1].set_color(PRIMARY)

    numberline = NumberLine(
        x_range=[-1, 1, 0.1],
        length=8,
        include_numbers=True,
        decimal_number_config={"num_decimal_places": 0, "color": SECONDARY},
        numbers_to_include=[-1, 0, 1],
        numbers_with_elongated_ticks=[-1, 0, 1],
        color=FG,
    ).shift(2*DOWN)

    scene.wait(1)
    scene.play(Write(sequence), run_time=2)
    scene.wait(2)
    scene.play(Write(numberline))
    scene.wait(1)

    pins = []
    pin = plot_on_numberline(numberline, 0.5, color=PRIMARY)
    pins.append(pin)
    pin_arrow = Arrow(start=pin.get_top()+0.8*UP, end=pin.get_top() + 0.2*DOWN, color=EMPHASIZED)
    scene.play(
        Write(pin),
        Write(pin_arrow)
    )
    scene.wait(0.25)

    for i in range(10):
        pin = plot_on_numberline(numberline, 1/2**(i+2), color=PRIMARY).scale(opacity_curve(i))
        pins.append(pin)
        scene.play(
            Write(pin),
            pin_arrow.animate.shift((pin.get_center()[0] - pin_arrow.get_center()[0])*RIGHT),
            *[p.animate.set_opacity(opacity_curve(j)) for j, p in enumerate(reversed(pins[:-1]))]
        )
        scene.wait(0.25)
    scene.wait(2)

    text = Tex("S converges to 0", color=EMPHASIZED).scale(2).to_edge(UP)
    scene.play(Write(text), run_time=1.5)
    scene.wait(2)
    tex = MathTex(r"\lim_{n \to \infty} S_n = 0").scale(1.25)
    tex[0][3].set_color(PRIMARY)
    tex[0][6:8].set_color(PRIMARY)
    scene.play(sequence.animate.shift(1.5*UP), Write(tex))
    scene.wait(2)

    #example 2
    next_sequence = MathTex(
        r"S = \frac{1}{2}, \frac{3}{4}, \frac{7}{8}, \frac{15}{16}, \dots"
    ).shift(1.5*UP)
    next_sequence[0][:1].set_color(PRIMARY)
    scene.play(
        sequence.animate.become(next_sequence),
        FadeOut(tex, *pins, pin_arrow, text),
    )
    scene.wait(1)
    pins = []
    pin = plot_on_numberline(numberline, 0.5, color=PRIMARY)
    pins.append(pin)
    pin_arrow = Arrow(start=pin.get_top()+0.8*UP, end=pin.get_top() + 0.2*DOWN, color=EMPHASIZED)
    scene.play(
        Write(pin),
        Write(pin_arrow),
        run_time=0.5
    )
    scene.wait(0.1)

    for i in range(10):
        pin = plot_on_numberline(numberline, (2**(i+2)-1)/2**(i+2), color=PRIMARY).scale(opacity_curve(i))
        pins.append(pin)
        scene.play(
            Write(pin),
            pin_arrow.animate.shift((pin.get_center()[0] - pin_arrow.get_center()[0])*RIGHT),
            *[p.animate.set_opacity(opacity_curve(j)) for j, p in enumerate(reversed(pins[:-1]))],
            run_time=0.5
        )
        scene.wait(0.1)
    scene.wait(2)

    tex = MathTex(r"\lim_{n \to \infty} S_n = 1").scale(1.25)
    tex[0][3].set_color(PRIMARY)
    tex[0][6:8].set_color(PRIMARY)
    scene.play(Write(tex))
    scene.wait(2)


def convergence_proof(scene):
    scene.remove(*scene.mobjects)
    line0 = MathTex(r"R_n = \frac{F_{n-1}}{F_{n-2}}").move_to(ORIGIN + 3*UP)
    line1 = MathTex(r"\lim_{n \to \infty} R_n = x").next_to(line0, DOWN)
    line2 = MathTex(r"\lim_{n \to \infty} R_{n+1} = x").next_to(line1, DOWN)
    line3 = MathTex(
        r"R_{n+1} = \frac{F_{n}}{F_{n-1}} = \frac{F_{n-1} + F_{n-2}}{F_{n-1}} = 1 + \frac{F_{n-2}}{F_{n-1}} = 1 + \frac{1}{R_n}"
    ).next_to(line2, DOWN)
    line30 = line3[0][:12]
    line31 = line3[0][12:27]
    line32 = line3[0][27:39]
    line33 = line3[0][39:]

    line4 = MathTex(r"R_{n+1} = 1 + \frac{1}{R_n}").move_to(line3)
    line5 = MathTex(r"\lim_{n \to \infty} R_{n+1} = \lim_{n \to \infty} 1 + \frac{1}{R_n}").move_to(line4)
    line6 = MathTex(r"x = 1 + \frac{1}{x}").move_to(line4)

    line7 = MathTex(r"x = \varphi").next_to(line6, DOWN).set_color(EMPHASIZED)

    numberline = NumberLine(
        x_range=[0, 2, 0.1],
        length=8,
        include_numbers=True,
        decimal_number_config={"num_decimal_places": 0, "color": SECONDARY},
        numbers_to_include=[0, 1, 2],
        numbers_with_elongated_ticks=[0, 1, 2],
        color=FG,
    ).to_edge(DOWN)

    pins = [
        plot_on_numberline(numberline, fib(i+1)/fib(i), color=PRIMARY).scale(opacity_curve(i)).set_opacity(opacity_curve(i)) for i in range(11)
    ]
    pin_arrow = Arrow(start=numberline.number_to_point(PHI) + 0.95*UP, end=numberline.number_to_point(PHI) + 0.05*DOWN, color=EMPHASIZED)
    arrow_label = Tex("$x$", color=EMPHASIZED).next_to(pin_arrow, UP, buff=SMALL_BUFF)

    scene.play(Write(numberline), Write(line0))
    scene.play(LaggedStart(*[Create(pin) for pin in pins], lag_ratio=0.25))
    scene.play(Write(pin_arrow), Write(line1), Write(arrow_label))

    animations = []
    for i, pin in enumerate(pins):
        if i == 0:
            animations.append(FadeOut(pins[0]))
        else:
            animations.append(Transform(pins[i], pins[i-1], path_arc=PI/2))
    animations.append(Write(line2))

    pins = pins[1:]
    sequence1 = MathTex("R_n = R_1, R_2, R_3, R_4, \dots").next_to(numberline, 1.5*UP).shift(LEFT)
    sequence2 = MathTex("R_{n+1} = R_2, R_3, R_4, R_5, \dots").next_to(numberline, 1.5*UP).shift(LEFT)
    scene.wait(1)
    scene.play(Write(sequence1))
    scene.wait(0.5)
    scene.play(
        LaggedStart(*animations, lag_ratio=0.5),
        Transform(sequence1[0][:2], sequence2[0][:4]),
        Transform(sequence1[0][2], sequence2[0][4]),
        FadeOut(sequence1[0][3:6]),
        Transform(sequence1[0][6:15], sequence2[0][5:14]),
        Transform(sequence1[0][15:], sequence2[0][14:]),
    )
    scene.remove(*sequence1[0], *sequence2[0])
    scene.add(sequence2)
    scene.wait(2)

    sublines3 = [line30.next_to(line2, DOWN), line31, line32, line33]
    for i in range(len(sublines3)):
        group = VGroup(*[_.copy() for _ in sublines3[:i+1]]).arrange(RIGHT).next_to(line2, DOWN)
        animations = []
        for j, subline in enumerate(sublines3[:i]):
            animations.append(subline.animate.move_to(group[j]))
        sublines3[i].move_to(group[i])
        scene.play(AnimationGroup(*animations), Write(sublines3[i]))
        scene.wait(1)
    scene.remove(*sublines3)
    scene.add(line3)
    scene.wait(1)
    scene.play(
        FadeOut(line3[0][5:40]),
        VGroup(line3[0][:5], line3[0][40:]).animate.arrange(RIGHT).next_to(line2, DOWN)
    )
    scene.wait(2)
    scene.remove(*line3[0])
    scene.add(line4)
    scene.play(
        Write(line5[0][:6]),
        Write(line5[0][11:17]),
        line4[0][:5].animate.move_to(line5[0][6:11]),
        line4[0][5:].animate.move_to(line5[0][17:]),
    )
    scene.remove(*line4[0])
    scene.add(line5)
    scene.wait(1)

    scene.play(
        Transform(line5[0][:10], line6[0][0]),
        Transform(line5[0][10], line6[0][1]),
        FadeOut(line5[0][11:17]),
        Transform(line5[0][17:21], line6[0][2:6]),
        Transform(line5[0][21:], line6[0][6:])
    )
    scene.wait(2)

    scene.remove(*scene.mobjects)
    scene.add(numberline, sequence2, *pins, pin_arrow, arrow_label, line0, line1, line2, line6)

    scene.play(Write(line7), arrow_label.animate.become(
        Tex(r"$\varphi$", color=EMPHASIZED).next_to(pin_arrow, UP, buff=SMALL_BUFF)
    ))
    scene.wait(2)
    scene.play(FadeOut(*scene.mobjects))


def convergence_to_eigenvalue(scene):
    scene.remove(*scene.mobjects)
    lines = VGroup(
        MathTex(r"\frac{F_{n-1}}{F_{n-2}} = R_n \implies F_{n-1} = R_nF_{n-2}"),
        MathTex(r"F_{n} = R_{n+1}F_{n-1}"),
        MathTex(
            r"A" + vector_to_tex(["F_{n-1}", "F_{n-2}"]) + " = " + vector_to_tex(["F_{n}", "F_{n-1}"]) +
            " = " + vector_to_tex(["R_{n+1}F_{n-1}", "R_nF_{n-2}"])
        ),
        MathTex(
            r"A" + vector_to_tex([r"\frac{F_{n-1}}{F_{n-2}}", r"\frac{F_{n-2}}{F_{n-2}}"]) + " = " +
            vector_to_tex([r"R_{n+1}\frac{F_{n-1}}{F_{n-2}}", r"R_n\frac{F_{n-2}}{F_{n-2}}"])
        ),
        MathTex(r"A" + vector_to_tex([r"R_n", 1]) + " = " + vector_to_tex([r"R_{n+1}R_n", r"R_n"])),
        MathTex(r"A" + vector_to_tex([r"R_n", 1]) + " = R_n" + vector_to_tex([r"R_{n+1}", 1])),
        MathTex(r"\lim_{n \to \infty} A" + vector_to_tex([r"R_n", "1"]) + r" = \lim_{n \to \infty} R_n" + vector_to_tex([r"R_{n+1}", 1])),
        MathTex(r"A" + vector_to_tex([r"\varphi", 1]) + r" = \varphi" + vector_to_tex([r"\varphi", 1]))
    )
    scene.wait(1)

    lines[:2].move_to(ORIGIN).arrange(DOWN)
    scene.play(Write(lines[0]))
    scene.wait(1)

    scene.play(Write(lines[1]))
    scene.wait(1)

    scene.play(
        lines[:2].animate.to_edge(UP),
        Write(lines[2][0][:21])
    )
    cline0 = lines[0][0][19:].copy()
    cline1 = lines[1][0][3:].copy()
    scene.play(
        LaggedStart(
            AnimationGroup(
                Transform(cline0, lines[2][0][22:30]),
                Transform(cline1, lines[2][0][30:36])
            ),
            AnimationGroup(
                Write(lines[2][0][21]),
                Write(lines[2][0][36])
            ),
            lag_ratio=0.5
        )
    )
    scene.remove(cline0, cline1, *lines[2][0])
    scene.add(lines[2])
    scene.wait(1)

    scene.play(Transform(lines[2], lines[3]))
    scene.remove(*lines[2][0], *lines[3][0])
    scene.add(lines[3])
    scene.wait(1)

    scene.play(Transform(lines[3], lines[4]))
    scene.remove(*lines[3][0], *lines[4][0])
    scene.add(lines[4])
    scene.wait(1)

    scene.play(Transform(lines[4], lines[5]), FadeOut(lines[:2]))
    scene.remove(*lines[4][0], *lines[5][0])
    scene.add(lines[5])
    scene.wait(1)

    scene.play(Transform(lines[5], lines[6]))
    scene.remove(*lines[5][0], *lines[6][0])
    scene.add(lines[6])
    scene.wait(1)

    scene.play(Transform(lines[6], lines[7]))
    scene.wait(2)


def almost_done(scene):
    scene.remove(*scene.mobjects)
    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5)
    pair = VGroup(rabbit.copy(), rabbit.copy().shift(0.5 * RIGHT))
    grownRabbit = pair.copy().move_to(ORIGIN + UP).scale(GOLDEN)
    babyRabbit = pair.copy().move_to(ORIGIN + DOWN)
    scene.add(grownRabbit, babyRabbit)
    scene.wait(1)

    bubble1 = Bubble(content_scale_factor=0.8).scale(0.4).pin_to(grownRabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    tex1 = Tex(r"Almost done!")
    bubble1.add_content(tex1)
    scene.play(DrawBorderThenFill(bubble1), Write(tex1))
    scene.wait(0.5)
    bubble2 = Bubble(content_scale_factor=0.7).scale(0.3).rotate(PI).pin_to(babyRabbit).shift(3*DOWN + 2.25*RIGHT)
    tex2 = Tex(r"What are we \\ doing again?")
    bubble2.add_content(tex2)
    tex2.shift(0.5*DOWN)

    scene.play(DrawBorderThenFill(bubble2), Write(tex2))
    scene.wait(2)


def recap(scene):
    scene.remove(*scene.mobjects)
    arrow = MathTex("\longrightarrow").scale(2).rotate(-PI/2).move_to(ORIGIN)
    text1 = Tex("Finding the n'th Fibonacci number").scale(1.5).next_to(arrow, UP).set_color(PRIMARY)
    text2 = Tex("Calculating ", "$A^n$").scale(1.5).next_to(arrow, DOWN).set_color(SECONDARY)
    text2[1].set_color(CYAN)
    scene.add(text1)
    scene.play(Write(arrow), Write(text2), run_time=2)
    scene.wait(2)

    scene.remove(*scene.mobjects)
    frame1, frame2, plane1, plane2, transformed_plane = set_up_side_by_side_plane(scene, "transformed_plane3x3", 3)
    frame1_text = Text("Multiply by A", color=PRIMARY).move_to(frame1.get_edge_center(UP)).shift(0.65 * DOWN)
    frame2_text = Text("Multiply by B", color=PRIMARY).move_to(frame2.get_corner(UP)).shift(0.65 * DOWN)
    frame2_text.set_z_index(2)
    text = Tex(r"$A$ and $B$ are similar!", color=EMPHASIZED).to_edge(UP, buff=0.6)
    vector1 = plot_vector([1, 1], plane1, color=gruvbox.RED)
    vector2 = vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - vector2.get_start()[:2]
    vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    vector2.set_z_index(2)
    scene.add(frame1, frame2, frame1_text, frame2_text, plane1, vector1, vector2, text, transformed_plane)
    scene.wait(1)
    next_vector1 = plot_vector([2, 1], plane1, color=gruvbox.RED)
    next_vector2 = next_vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - next_vector2.get_start()[:2]
    next_vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    next_vector2.set_z_index(2)

    text2 = Tex(r"$\Longleftrightarrow$ Same operation!", color=EMPHASIZED)
    group = VGroup(text.copy(), text2.copy()).arrange(RIGHT).to_edge(UP, buff=0.6)
    text2.move_to(group[1])
    scene.play(
        Transform(vector1, next_vector1), Transform(vector2, next_vector2),
        Write(text2),
        text.animate.move_to(group[0]),
        run_time=2
    )
    scene.wait(2)

    scene.remove(*scene.mobjects)
    transition = [[5, -1], [-1, 1]]
    plane = EpicPlane().apply_matrix(transition)
    vector = ChillVector([1, 1])
    coords = vector.transformed_coordinate_label(transition)
    scene.add(plane, vector, coords)

    line0 = MathTex("v").to_corner(UL, buff=0.75).scale(1.5).to_corner(UL, buff=0.75)
    line1 = MathTex("Mv").scale(1.5).to_corner(UL, buff=0.75)
    line2 = MathTex("AMv").scale(1.5).to_corner(UL, buff=0.75)
    line3 = MathTex("M^{-1}AMv").scale(1.5).to_corner(UL, buff=0.75)
    line4 = MathTex("Bv = M^{-1}AMv").scale(1.5).to_corner(UL, buff=0.75)

    line1[0][0].set_color(gruvbox.SECONDARY)

    line2[0][0].set_color(gruvbox.PRIMARY)
    line2[0][1].set_color(gruvbox.SECONDARY)

    line3[0][:3].set_color(gruvbox.SECONDARY)
    line3[0][3].set_color(gruvbox.PRIMARY)
    line3[0][4].set_color(gruvbox.SECONDARY)

    line4[0][0].set_color(gruvbox.CYAN)
    line4[0][3:6].set_color(gruvbox.SECONDARY)
    line4[0][6].set_color(gruvbox.PRIMARY)
    line4[0][7].set_color(gruvbox.SECONDARY)


    scene.play(Write(line0))
    scene.wait(0.5)
    scene.play(
        plane.animate.apply_matrix(np.linalg.inv(transition)), coords.animate.become(vector.coordinate_label()),
        Transform(line0, line1[0][1]), Write(line1[0][0]), run_time=2
    )
    scene.remove(line0)
    scene.add(line1)

    scene.play(vector.animate.become(ChillVector([2, 1])), coords.animate.become(ChillVector([2, 1]).coordinate_label()),
               line1.animate.move_to(line2[0][1:]), Write(line2[0][0]))
    scene.remove(line1)
    scene.add(line2)

    scene.play(plane.animate.apply_matrix(transition), coords.animate.become(vector.transformed_coordinate_label(transition, integer_labels=False)),
               line2.animate.move_to(line3[0][3:]), Write(line3[0][:3]), run_time=2)
    scene.remove(line2)
    scene.add(line3)

    scene.play(line3.animate.move_to(line4[0][3:]), Write(line4[0][:3]))
    scene.remove(line3)
    scene.add(line4)
    scene.wait(0.5)

    line = MathTex("B = M^{-1}AM").scale(1.5).to_corner(UL, buff=0.75)
    line[0][0].set_color(gruvbox.CYAN)
    line[0][2:5].set_color(gruvbox.SECONDARY)
    line[0][5].set_color(gruvbox.PRIMARY)
    line[0][6].set_color(gruvbox.SECONDARY)
    scene.play(
        line4[0][2:-1].animate.move_to(line[0][1:]),
        FadeOut(line4[0][1], line4[0][-1]),
    )
    scene.wait(1)

    scene.remove(*scene.mobjects)
    plane = EpicPlane()
    transition_matrix = [[PHI, PSI], [1, 1]]
    plane.apply_matrix(transition_matrix)

    u1 = ChillVector(np.dot(transition_matrix, [1, 0]), color=gruvbox.GREEN)
    u2 = ChillVector(np.dot(transition_matrix, [0, 1]), color=gruvbox.RED)

    u1_label = Tex("$u_1$", color=gruvbox.GREEN).move_to(u1.get_center() + 0.25 * DOWN + 0.25 * RIGHT)
    u2_label = Tex("$u_2$", color=gruvbox.RED).move_to(u2.get_center() + 0.25 * DOWN + 0.3 * LEFT)

    u1_coords = u1.transformed_coordinate_label(transition_matrix)
    u2_coords = u2.transformed_coordinate_label(transition_matrix)

    b_tex = matrix_to_tex([[r"\lambda_1", 0], [0, r"\lambda_2"]])
    diagonal_b = MathTex("B = " + b_tex).scale(1.25).to_corner(UL).shift(0.25 * DOWN + 0.25 * RIGHT)
    diagonal_b[0][0].set_color(PRIMARY)
    diagonal_b[0][3:5].set_color(SECONDARY)
    diagonal_b[0][7:9].set_color(CYAN)

    u1_ghost = u1.copy().set_opacity(0.5)
    u2_ghost = u2.copy().set_opacity(0.5)

    lines = VGroup(
        MathTex(
            b_tex + vector_to_tex([1, 0]) + " = " + vector_to_tex([r"\lambda_1", 0]),
            substrings_to_isolate=[b_tex, vector_to_tex([1, 0]), vector_to_tex([r"\lambda_1", 0])]
        ).next_to(diagonal_b, DOWN, aligned_edge=LEFT),

        MathTex(
            b_tex + vector_to_tex([0, 1]) + " = " + vector_to_tex([0, r"\lambda_2"]),
            substrings_to_isolate=[b_tex, vector_to_tex([0, 1]), vector_to_tex([0, r"\lambda_2"])]
        ),
    )
    lines[1].next_to(lines[0], DOWN, aligned_edge=LEFT)

    lines[0][0].set_color(PRIMARY)
    lines[0][1].set_color(GREEN)
    lines[0][3].set_color(GREEN)

    lines[1][0].set_color(PRIMARY)
    lines[1][1].set_color(RED)
    lines[1][3].set_color(RED)

    scene.add(plane, u1, u2, u1_label, u2_label, u1_coords, u2_coords, diagonal_b)
    scene.wait(1)

    next_vector = ChillVector(np.dot(transition_matrix, [PHI, 0]), color=gruvbox.GREEN)
    scene.play(
        u1.animate.become(next_vector),
        u1_coords.animate.become(next_vector.custom_coordinate_label([r"\lambda_1", 0])),
        u1_label.animate.move_to(next_vector.get_center() + 0.25 * DOWN + 0.25 * RIGHT),
        Write(lines[0]),
        run_time=1.5
    )
    scene.wait(0.5)
    scene.add(u2_ghost)
    next_vector = ChillVector(np.dot(transition_matrix, [0, PSI]), color=gruvbox.RED)
    scene.play(
        u2.animate.become(next_vector),
        u2_coords.animate.become(next_vector.custom_coordinate_label([0, r"\lambda_2"])),
        u2_label.animate.move_to(next_vector.get_center() + 0.25 * DOWN + 0.3 * LEFT),
        Write(lines[1]),
        run_time=1.5
    )
    scene.wait(1)

    scene.remove(*scene.mobjects)
    frame = Rectangle(height=5, width=5, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(RIGHT, buff=0.5)
    plane = scale_plane_to_fit_frame(EpicPlane((-3, 3, 1)).move_to(frame), frame)

    line2 = MathTex(
        r" \begin{cases}"
        r" x + y = \lambda x \\"
        r"x = \lambda y"
        r"\end{cases}",
    ).scale(1.25).move_to(ORIGIN + 2*UP + 3 * LEFT)
    secondary_indices = [5, 9]
    for i in secondary_indices:
        line2[0][i].set_color(SECONDARY)

    line3 = MathTex(r"x = \varphi y \\ x = \psi y").scale(1.25).next_to(line2, DOWN, aligned_edge=LEFT)
    line3[0][0].set_color(PRIMARY)
    line3[0][2].set_color(gruvbox.GREEN)
    line3[0][4].set_color(PRIMARY)
    line3[0][6].set_color(gruvbox.RED)

    implies = MathTex(r"\implies", color=EMPHASIZED).scale(1.25).rotate(-PI / 2).next_to(line3, DOWN)
    line4 = MathTex(
        "u_1=" + vector_to_tex([r"\varphi", 1]) + r" \quad u_2=" + vector_to_tex([r"\psi", 1])
    ).scale(1.25).next_to(implies, DOWN)
    line4[0][:2].set_color(gruvbox.GREEN)
    line4[0][3:7].set_color(gruvbox.GREEN)
    line4[0][7:9].set_color(gruvbox.RED)
    line4[0][10:].set_color(gruvbox.RED)

    u1 = plot_vector([PHI, 1], plane, color=gruvbox.GREEN)
    u2 = plot_vector([PSI, 1], plane, color=gruvbox.RED)
    u1_label = get_vector_label(r"$u_1$", u1).set_z_index(1)
    u2_label = get_vector_label(r"$u_2$", u2).set_z_index(1)

    u1_ghost = u1.copy().set_opacity(0.5)
    u2_ghost = u2.copy().set_opacity(0.5)

    u1.set_z_index(1)
    u2.set_z_index(1)

    scene.add(line2)

    line1 = Line(
        plane.c2p(-3, -3 / PHI), plane.c2p(3, 3 / PHI),
        stroke_width=2, color=EMPHASIZED
    )
    line2 = Line(
        plane.c2p(3 * PSI, 3), plane.c2p(-3 * PSI, -3),
        stroke_width=2, color=EMPHASIZED
    )

    scene.add(
        frame, plane, line1, line2, line4, implies, line2, line3, line4, line1, line2, line3, line4,
        u1, u2, u1_label, u2_label, u1_ghost, u2_ghost
    )
    scene.wait(1)

    scene.play(
        u1.animate.become(plot_vector([PHI ** 2, PHI], plane, color=gruvbox.GREEN)),
        u1_label.animate.become(
            get_vector_label(r"$\lambda_1 u_1$", plot_vector([PHI ** 2, PHI], plane, color=gruvbox.GREEN), buff=0.5,
                             direction=DOWN)),
        u2.animate.become(plot_vector([PSI ** 2, PSI], plane, color=gruvbox.RED)),
        u2_label.animate.become(
            get_vector_label(r"$\lambda_2 u_2$", plot_vector([PSI ** 2, PSI], plane, color=gruvbox.RED), buff=0.25,
                             direction=DOWN).shift(0.3 * LEFT)),
        run_time=1.5
    )
    scene.wait(2)
    scene.play(FadeOut(*scene.mobjects))
    scene.wait(2)


def finish(scene):
    scene.remove(*scene.mobjects)
    lines = VGroup(
        MathTex(r"u_1 = " + vector_to_tex([r"\varphi", 1]) + r" \quad u_2 = " + vector_to_tex([r"\psi", 1])),
        MathTex(r"M = " + matrix_to_tex([[r"\varphi", r"\psi"], [1, 1]])),
        MathTex(r"B = " + matrix_to_tex([[r"\varphi", 0], [0, r"\psi"]])),
        MathTex(r"B = M^{-1}AM"),
        Tex("$A^n$ and $B^n$ are also similar!"),
        MathTex(r"\Longrightarrow B^n = M^{-1}A^nM"),
        MathTex(r"A^n = M B^n M^{-1}"),
        MathTex(
            r"A^n = " + matrix_to_tex([[r"\varphi", r"\psi"], [1, 1]]) +
            matrix_to_tex([[r"\varphi^n", 0], [0, r"\psi^n"]]) + r"\frac{1}{\sqrt{5}}" +
            matrix_to_tex([[1, r"-\psi"], [-1, r"\varphi"]])
        ),
        MathTex(
            r"A^n" + vector_to_tex([1, 1]) + r" = " +
            matrix_to_tex([[r"\varphi", r"\psi"], [1, 1]]) +
            matrix_to_tex([[r"\varphi^n", 0], [0, r"\psi^n"]]) + r"\frac{1}{\sqrt{5}}" +
            matrix_to_tex([[1, r"-\psi"], [-1, r"\varphi"]]) + vector_to_tex([1, 1]) + " = "
            + r"\frac{1}{\sqrt{5}}" + vector_to_tex([r"\varphi^{n+2} - \psi^{n+2}", r"\varphi^{n+1} - \psi^{n+1}"])
        ),
        MathTex(r"\Longrightarrow").rotate(-PI/2),
        MathTex(
            r"F_n = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}"
        )
    )
    lines.arrange(DOWN).to_edge(UP, buff=0.5)

    scene.play(Write(lines[0]))
    scene.wait(0.5)
    scene.play(Write(lines[1]))
    scene.wait(1)
    scene.play(Write(lines[2]))
    scene.wait(1)
    scene.play(Write(lines[3]))
    scene.wait(1)
    scene.play(Write(lines[4]))
    scene.wait(1)
    group = VGroup(lines[4].copy(), lines[5]).arrange(RIGHT).next_to(lines[3], DOWN)
    scene.play(
        lines[4].animate.move_to(group[0]),
        Write(lines[5])
    )
    scene.wait(1)
    scene.play(FadeOut(lines[4], lines[5][0][:2]), lines[5][0][2:].animate.next_to(lines[3], DOWN))
    lines[6].next_to(lines[3], DOWN)
    scene.play(
        Transform(lines[5][0][2:4], lines[6][0][4:6]),
        Transform(lines[5][0][8:10], lines[6][0][:2]),
        Transform(lines[5][0][4], lines[6][0][2]),
        Transform(lines[5][0][5:8], lines[6][0][6:9], path_arc=PI/2),
        Transform(lines[5][0][10], lines[6][0][3], path_arc=PI/2),
    )
    scene.remove(*lines[5][0], *lines[6][0])
    scene.add(lines[6])
    scene.wait(1)
    scene.play(
        FadeOut(lines[:3], lines[3], lines[6]),
        Write(lines[7].move_to(ORIGIN + UP)),
        run_time=2
    )
    scene.wait(1)
    scene.play(TransformFromCopy(lines[7], lines[8].move_to(ORIGIN + DOWN).scale(0.75)))
    scene.wait(1)

    lines[9:].next_to(lines[8], DOWN).shift(1.5*UP)
    lines[10].set_color(EMPHASIZED)
    scene.play(Write(lines[9:]), lines[7:9].animate.shift(1.5*UP))
    scene.wait(2)

    scene.play(FadeOut(lines[7:10]), lines[10].animate.move_to(ORIGIN).scale(1.25))
    scene.wait(2)
    scene.play(FadeOut(lines[10]), run_time=2)
    scene.wait(2)

    text = Text("The End", color=PRIMARY, font="Edwardian Script ITC").scale(2)
    scene.play(Write(text), run_time=5)
    scene.wait(3)
    scene.play(FadeOut(text), run_time=3)
    scene.wait(2)


class Chapter4(Scene):
    def construct(self):
        #introduction(self)
        #eigenbasis(self)
        #find_eigenbasis(self)
        #the_golden_ratio(self)
        relationship_to_fibonacci(self)
        #convergence(self)
        #learning_time_introduction(self)
        #learning_time_convergence(self)
        #convergence_proof(self)
        #convergence_to_eigenvalue(self)
        #almost_done(self)
        #recap(self)
        #finish(self)


#TODO: missing the animation for the - in one of the liens in find_eigenbasis
#TODO: add 1 - phi to the eigenvalue solutions
#TODO: change from gamma to the actual values on find_eigenbasis and recap (im talking about the thing on the label)
#TODO: add the gamma on the label in eigenbasis when doing the transformation
