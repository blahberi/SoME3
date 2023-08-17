from manim import *
from extra.color_schemes import gruvbox
from util_lib.SpeechBubble import Bubble
from extra.color_schemes.gruvbox import *
from util_lib.utils import *


def render_transformed_plane(scene):
    scene.camera.background_color = BG_FILL
    plane = EpicPlane((-20, 20, 1)).apply_matrix([[5, -1], [-1, 1]]).scale(0.6)
    scene.add(plane)
    return


def p1_introduction(scene):
    scene.remove(*scene.mobjects)
    title = Text("Chapter 3: Painting the Roses Red").move_to(ORIGIN)
    title[25:28].set_color(gruvbox.RED)
    scene.play(Write(title), run_time=5)
    scene.wait(2)
    scene.play(FadeOut(title), run_time=3)
    scene.wait(2)

    text1 = Text("Finding the n'th Fibonacci number", color=PRIMARY)
    arrow1 = MathTex("\longrightarrow").scale(2).rotate(-PI/2).next_to(text1, DOWN)
    text2 = Tex("Calculating ", "$A^n$", color=SECONDARY).next_to(arrow1, DOWN)
    text2[1].set_color(gruvbox.CYAN)
    VGroup(text1, arrow1, text2).move_to(ORIGIN)
    scene.play(FadeIn(text1, arrow1, text2))
    scene.wait(1)
    scene.play(VGroup(text1, arrow1, text2).animate.shift((text1.get_center()[1])*UP))
    arrow2 = MathTex("\longrightarrow").scale(2).rotate(-PI/2).next_to(text2, DOWN)
    text3 = Text("????", color=gruvbox.RED).next_to(arrow2, DOWN)
    scene.play(Write(arrow2), Write(text3))
    scene.wait(2)


def p1_coordinates(scene):
    scene.remove(*scene.mobjects)
    plane = EpicPlane()
    #scene.play(FadeIn(plane))
    scene.add(plane)
    #scene.wait(2)
    vector = ChillVector([1, 1])
    coords = vector.coordinate_label()
    #scene.play(GrowArrow(vector), Write(coords))
    scene.add(vector)
    scene.wait(2)
    scene.play(Write(coords))
    scene.wait(1)
    next_vector = ChillVector([2, 1])
    next_coords = next_vector.coordinate_label()
    scene.play(Transform(vector, next_vector), Transform(coords, next_coords))
    scene.wait(1)
    next_vector = ChillVector([1, 1])
    next_coords = next_vector.coordinate_label()
    ghost_vector = vector.copy().set_opacity(0.25)
    scene.add(ghost_vector)
    scene.play(FadeOut(vector, coords), run_time=0.5)
    scene.remove(vector, coords)

    vector = ChillVector([1, 1], color=gruvbox.CYAN)
    coords = vector.coordinate_label()
    scene.play(FadeIn(vector), FadeIn(coords))
    scene.wait(2)

    matrix = [[5, -1], [-1, 1]]
    scene.play(
        plane.animate.apply_matrix(matrix),
        coords.animate.become(vector.transformed_coordinate_label(matrix, integer_labels=False)),
        run_time=2
    )
    scene.wait(1)
    next_vector = ChillVector([2, 0.5], color=gruvbox.CYAN)
    next_coords = next_vector.transformed_coordinate_label(matrix, integer_labels=False)
    scene.play(Transform(vector, next_vector), Transform(coords, next_coords))
    scene.wait(0.5)
    text = Text("Different vector!", color=DANGER).scale(1.15).move_to(ORIGIN).shift(2 * UP)
    scene.play(ghost_vector.animate.set_opacity(1), FadeOut(coords))
    scene.wait(1)
    scene.play(FadeIn(text))
    scene.wait(1)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(6 * RIGHT + 2.7 * DOWN)
    scene.play(FadeIn(rabbit))
    bubble = Bubble().scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    bubble_text = Text("Paint A differently").scale(1.25)
    bubble_text[5:6].set_color(SECONDARY)
    bubble.add_content(bubble_text)
    scene.play(DrawBorderThenFill(bubble), Write(bubble_text))
    scene.wait(2)


def p1_same_operation(scene):
    scene.remove(*scene.mobjects)
    frame1, frame2, plane1, plane2, transformed_plane = set_up_side_by_side_plane(scene, "transformed_plane6x6", 6)
    frame1_text = Text("Multiply by A", color=PRIMARY).move_to(frame1.get_edge_center(UP)).shift(0.65*DOWN)
    frame2_text = Text("Multiply by B", color=PRIMARY).move_to(frame2.get_corner(UP)).shift(0.65*DOWN)
    frame2_text.set_z_index(2)
    text = Text("Same operation!", color=EMPHASIZED).to_edge(UP, buff=0.6)
    vector1 = plot_vector([1, 1], plane1, color=gruvbox.RED)
    vector2 = vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - vector2.get_start()[:2]
    vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    vector2.set_z_index(2)
    scene.add(frame1, frame2, frame1_text, frame2_text, plane1, vector1, vector2, text, transformed_plane)

    next_vector1 = plot_vector([2, 1], plane1, color=gruvbox.RED)
    next_vector2 = next_vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - next_vector2.get_start()[:2]
    next_vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    next_vector2.set_z_index(2)
    scene.play(Transform(vector1, next_vector1), Transform(vector2, next_vector2), run_time=2)
    scene.wait(1)
    text.target = Tex("$A$ and $B$ are similar!", color=EMPHASIZED).scale(1.15).to_edge(UP)
    scene.play(MoveToTarget(text))
    scene.wait(2)
    matrix = [[1, 1], [1, 0]]
    next_coords = [2, 1]
    for i in range(2):
        next_coords = np.dot(matrix, next_coords)
        next_vector1 = plot_vector(next_coords, plane1, color=gruvbox.RED)
        next_vector2 = next_vector1.copy().move_to(plane2.c2p(0, 0))
        shift = plane2.c2p(0, 0)[:2] - next_vector2.get_start()[:2]
        next_vector2.shift(shift[0] * RIGHT + shift[1] * UP)
        scene.play(Transform(vector1, next_vector1), Transform(vector2, next_vector2))
        scene.wait(0.5)
    scene.wait(2)
    # white_screen = Rectangle(width=WIDTH + 1, height=HEIGHT + 1, color=FG, fill_color=FG, fill_opacity=1).to_edge(
    #     LEFT).shift(0.5 * LEFT).set_opacity(0.25)
    # scene.play(FadeIn(white_screen))

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(8 * LEFT + 2.7 * DOWN)
    scene.play(rabbit.animate.shift(2 * RIGHT))

    bubble = Bubble().scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    bubble_text = Tex(r"$A^n$ and $B^n$ \\ are also similar!")
    bubble.add_content(bubble_text)
    scene.play(DrawBorderThenFill(bubble), Write(bubble_text))
    scene.wait(2)


def p1_conclusion(scene):
    scene.remove(*scene.mobjects)
    text1 = Text("Finding the n'th Fibonacci number", color=PRIMARY)
    arrow1 = MathTex("\longrightarrow").scale(2).rotate(-PI/2).next_to(text1, DOWN)
    text2 = Tex("Calculating ", "$A^n$", color=SECONDARY).next_to(arrow1, DOWN)
    text2[1].set_color(gruvbox.CYAN)
    arrow2 = MathTex("\longrightarrow").scale(2).rotate(-PI/2).next_to(text2, DOWN)
    text3_before = Text("????", color=gruvbox.RED).next_to(arrow2, DOWN)
    text3 = Tex("Calculating ", "$B^n$", color=gruvbox.RED).next_to(arrow2, DOWN)
    text3[1].set_color(PRIMARY)
    VGroup(text1, arrow1, text2, arrow2, text3_before, text3).move_to(ORIGIN)
    scene.add(text1, arrow1, text2, arrow2, text3_before)
    scene.wait(1)
    scene.play(Transform(text3_before, text3))
    scene.wait(2)


def p2_introduction(scene):
    scene.remove(*scene.mobjects)
    frame1, frame2, plane1, plane2, transformed_plane = set_up_side_by_side_plane(scene, "transformed_plane3x3", 3, 6)
    frame1_text = Text("Multiply by A", color=PRIMARY).move_to(frame1.get_edge_center(UP)).shift(0.65*DOWN)
    frame2_text = Text("Multiply by B", color=PRIMARY).move_to(frame2.get_corner(UP)).shift(0.65*DOWN)
    frame2_text.set_z_index(2)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(4 * RIGHT + 2.7 * DOWN)
    bubble = Bubble(fill_opacity=0.5).scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT).set_z_index(2)
    bubble_text = Tex(r"Only difference is \\ the coordinate system").set_z_index(2)
    bubble.add_content(bubble_text)
    bubble_text.scale(1.25)

    vector1 = plot_vector([1, 1], plane1, color=gruvbox.RED)
    vector2 = vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - vector2.get_start()[:2]
    vector2.shift(shift[0] * RIGHT + shift[1] * UP)

    scene.add(frame1, frame2, frame1_text, frame2_text, plane1, plane2, transformed_plane, rabbit, bubble, bubble_text, vector1, vector2)
    scene.wait(1)

    next_vector1 = plot_vector([2, 1], plane1, color=gruvbox.RED)
    next_vector2 = next_vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - next_vector2.get_start()[:2]
    next_vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    next_vector2.set_z_index(2)
    scene.play(Transform(vector1, next_vector1), Transform(vector2, next_vector2), run_time=2)
    scene.wait(1)

    arrow = MathTex(r"\longleftrightarrow", color=EMPHASIZED).scale(2.25).move_to(ORIGIN).shift(frame1.get_center()[1]*UP)
    text = Text("Translate between coordinates", color=SECONDARY).to_edge(UP, buff=0.75)


    group1 = Group(frame1, frame1_text, plane1, vector1)
    group2 = Group(frame2, frame2_text, plane2, vector2, transformed_plane)
    vector2.set_z_index(2)
    scene.play(
        Write(arrow), Write(text),
        group1.animate.scale(9/10).to_edge(LEFT),
        group2.animate.scale(9/10).to_edge(RIGHT),
        FadeOut(rabbit, bubble, bubble_text)
    )
    scene.wait(1)


def p2_basis(scene):
    scene.remove(*scene.mobjects)
    plane = EpicPlane()
    scene.add(plane)
    scene.wait(2)

    vector = ChillVector([3, 2])
    scene.add(vector)
    coords = vector.coordinate_label(color=PRIMARY)
    scene.play(Write(coords))
    scene.wait(2)

    vector_1 = ChillVector([3, 0], color=gruvbox.GREEN)
    vector_2 = ChillVector([0, 2], color=gruvbox.RED).shift(3*RIGHT)
    scene.play(GrowArrow(vector_1))
    scene.play(GrowArrow(vector_2))
    scene.wait(2)

    next_vector = ChillVector([-5, -1])
    scene.play(GrowArrow(next_vector))
    next_coords = next_vector.coordinate_label(color=PRIMARY)
    scene.play(Write(next_coords))
    scene.play(
        vector_1.animate.become(ChillVector([-5, 0], color=gruvbox.GREEN))
    )
    scene.play(vector_2.animate.become(
        ChillVector([0, -1], color=gruvbox.RED).shift(5 * LEFT)
    ))
    scene.wait(2)
    text = Text("What is a step?", color=EMPHASIZED).scale(1.5).to_edge(UP)
    scene.play(Write(text), FadeOut(vector_1, vector_2, next_coords, next_vector))
    scene.remove(next_coords, next_vector, vector_1, vector_2)
    scene.wait(2)
    i_hat = ChillVector([1, 0], color=gruvbox.GREEN)
    j_hat = ChillVector([0, 1], color=gruvbox.RED)

    i_label = Tex("$\\hat{i}$", color=gruvbox.GREEN).move_to(i_hat.get_center() + 0.35*DOWN)
    j_label = Tex("$\\hat{j}$", color=gruvbox.RED).move_to(j_hat.get_center() + 0.35*LEFT)

    scene.play(GrowArrow(i_hat))
    scene.wait(2)
    scene.play(GrowArrow(j_hat))
    scene.wait(1)
    scene.play(Write(i_label), Write(j_label))
    scene.wait(2)
    scene.play(FadeOut(text), FadeOut(i_label, j_label))
    scene.wait(1)
    transition = [[1, 4], [-1, 1]]
    move_i_hat = [[1, 0], [-1, 1]]
    move_j_hat = [[5, 4], [0, 1]]
    scene.play(
        plane.animate.apply_matrix(move_i_hat),
        i_hat.animate.become(ChillVector([1, -1], color=gruvbox.GREEN))
    )
    scene.wait(0.25)
    scene.play(
        plane.animate.apply_matrix(move_j_hat),
        j_hat.animate.become(ChillVector([4, 1], color=gruvbox.RED)),
        run_time=2
    )
    new_coords = Matrix([[-1], [1]], element_alignment_corner=DOWN).move_to(coords.get_center()).shift(0.15*RIGHT).scale(0.75).set_color(PRIMARY)
    scene.play(coords.animate.become(new_coords))
    scene.wait(2)

    # new_plane = plane.copy().apply_matrix(np.linalg.inv(transition))
    # new_i_hat = ChillVector([1, 0], color=gruvbox.GREEN)
    # new_j_hat = ChillVector([0, 1], color=gruvbox.RED)
    # scene.play(
    #     FadeOut(plane),
    #     FadeOut(i_hat),
    #     FadeOut(j_hat),
    #     FadeIn(new_plane),
    #     FadeIn(new_i_hat),
    #     FadeIn(new_j_hat),
    #     coords.animate.become(vector.coordinate_label(color=PRIMARY))
    # )
    # plane = new_plane
    # i_hat = new_i_hat
    # j_hat = new_j_hat
    scene.play(
        plane.animate.apply_matrix(np.linalg.inv(transition)),
        i_hat.animate.become(ChillVector([1, 0], color=gruvbox.GREEN)),
        j_hat.animate.become(ChillVector([0, 1], color=gruvbox.RED)),
        coords.animate.become(vector.coordinate_label(color=PRIMARY)),
        run_time=2
    )

    scene.wait(2)
    new_plane = plane.copy().apply_matrix(transition)
    new_i_hat = ChillVector(np.dot(transition, [1, 0]), color=gruvbox.GREEN)
    new_j_hat = ChillVector(np.dot(transition, [0, 1]), color=gruvbox.RED)
    scene.play(
        FadeOut(plane),
        FadeOut(i_hat),
        FadeOut(j_hat),
        FadeIn(new_plane),
        FadeIn(new_i_hat),
        FadeIn(new_j_hat),
        FadeOut(coords),
    )


def p2_change_of_basis(scene):
    scene.remove(*scene.mobjects)

    lines = [
        MathTex(
            r"[u_1]_E = \begin{bmatrix} \alpha \\ \beta \end{bmatrix}, [u_2]_E = \begin{bmatrix} \gamma \\ \delta \end{bmatrix}"
        ),
        MathTex(r"u_1 = \alpha \hat{i} + \gamma \hat{j} \\ u_2 = \beta \hat{i} + \delta \hat{j}"),
        MathTex(r"[v]_U = \begin{bmatrix} x \\ y \end{bmatrix}"),
        MathTex(r"\implies v = x u_1 + y u_2"),
        MathTex(r"v = x (\alpha \hat{i} + \gamma \hat{j}) + y (\beta \hat{i} + \delta \hat{j})"),
        MathTex(r"v = (x \alpha + y \beta) \hat{i} + (x \gamma + y \delta) \hat{j}"),
        MathTex(r"[v]_E = \begin{bmatrix} x \alpha + y \beta \\ x \gamma + y \delta \end{bmatrix}"),
    ]

    secondary_indices = [
        [7, 8, 18, 19],
        [3, 7, 13, 17],
        [],
        [],
        [4, 8, 15, 19],
        [4, 7, 13, 17],
        [7, 10, 12, 15]
    ]
    primary_indices = [
        [],
        [],
        [6, 7],
        [4, 8],
        [2, 13],
        [3, 6, 13, 16],
        [6, 9, 11, 14]
    ]
    green_indices = [
        [],
        [4, 5, 14, 15],
        [],
        [],
        [5, 6, 16, 17],
        [9, 10],
        []
    ]
    red_indices = [
        [],
        [8, 9, 18, 19],
        [],
        [],
        [9, 10, 20, 21],
        [19, 20],
        []
    ]

    for i in range(len(lines)):
        for j in range(len(lines[i][0])):
            if j in primary_indices[i]:
                lines[i][0][j].set_color(PRIMARY)
            elif j in secondary_indices[i]:
                lines[i][0][j].set_color(SECONDARY)
            elif j in green_indices[i]:
                lines[i][0][j].set_color(gruvbox.GREEN)
            elif j in red_indices[i]:
                lines[i][0][j].set_color(gruvbox.RED)

    lines[6][0][0:4].set_color(gruvbox.CYAN),

    lines[0].to_corner(UL)
    lines[3].next_to(lines[2], RIGHT)

    vlines = VGroup(
        lines[0],
        lines[1],
        VGroup(lines[2], lines[3]),
        lines[4],
        lines[5],
        lines[6]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).scale(0.6).to_corner(UL).shift(0.25*UP).set_z_index(2).shift(DOWN)

    frame = SurroundingRectangle(vlines, color=FG, buff=0.5, fill_color=BG_FILL, fill_opacity=0.75).set_z_index(1).set_height(HEIGHT - 0.4).shift(0.15*UP)

    text = Text("generalized", color=EMPHASIZED).scale(0.85).move_to(frame.get_edge_center(UP)).shift(0.5*DOWN).set_z_index(2)

    transition = [[1, 4], [-1, 1]]
    plane = EpicPlane().apply_matrix(transition)
    vector = ChillVector([3, 2])
    coords = vector.transformed_coordinate_label(transition)

    u1 = ChillVector(np.dot(transition, [1, 0]), color=gruvbox.GREEN)
    u2 = ChillVector(np.dot(transition, [0, 1]), color=gruvbox.RED)

    u1_label = Tex("$u_1$", color=gruvbox.GREEN).move_to(u1.get_center() + 0.25*DOWN + 0.3*LEFT)
    u2_label = Tex("$u_2$", color=gruvbox.RED).move_to(u2.get_center() + 0.3*UP + 0.25*LEFT)

    u1_coords = u1.coordinate_label(color=gruvbox.GREEN)
    u2_coords = u2.coordinate_label(color=gruvbox.RED)

    scene.add(plane, vector, u1, u2)
    scene.play(
        Write(u1_label), Write(u2_label),
        DrawBorderThenFill(frame), Write(text),
    )
    scene.wait(2)
    scene.play(
        Write(u1_coords), Write(u2_coords),
        Write(lines[0])
    )
    scene.play(TransformFromCopy(lines[0], lines[1]))
    scene.wait(2)

    u1_scaled = ChillVector(np.dot(transition, [-1, 0]), color=gruvbox.GREEN)
    u2_scaled = ChillVector(np.dot(transition, [0, 1]), color=gruvbox.RED).shift((*np.dot(transition, [-1, 0]), 0))

    u1_scaled_label = Tex("$-1u_1$", color=gruvbox.GREEN).move_to(u1_scaled.get_center() + 0.25*DOWN + 0.3*LEFT)
    u2_scaled_label = Tex("$1u_2$", color=gruvbox.RED).move_to(u2_scaled.get_center() + 0.3*UP + 0.25*LEFT)

    scene.play(
        FadeOut(u1_coords, u2_coords),
        Write(lines[2]),
        Write(coords)
    )
    scene.wait(0.5)
    scene.play(
        TransformFromCopy(lines[2], lines[3]),
        Transform(u1, u1_scaled),
        Transform(u2, u2_scaled),
        Transform(u1_label, u1_scaled_label),
        Transform(u2_label, u2_scaled_label)
    )
    scene.wait(2)

    u1_i = ChillVector([np.dot(transition, [-1, 0])[0], 0], color=gruvbox.GREEN)
    u1_j = ChillVector([0, np.dot(transition, [-1, 0])[1]], color=gruvbox.RED).shift(np.dot(transition, [-1, 0])[0]*RIGHT)
    u1_i_scale = np.dot(transition, [-1, 0])[0]
    u1_j_scale = np.dot(transition, [-1, 0])[1]
    u1_i_label = Tex("$" + str(u1_i_scale) + " \hat{i}$", color=gruvbox.GREEN).move_to(u1_i.get_center()).shift(0.35*DOWN)
    u1_j_label = Tex("$" + str(u1_j_scale) + " \hat{j}$", color=gruvbox.RED).move_to(u1_j.get_center()).shift(0.35*LEFT)

    u2_i = ChillVector([np.dot(transition, [0, 1])[0], 0], color=gruvbox.GREEN)
    u2_j = ChillVector([0, np.dot(transition, [0, 1])[1]], color=gruvbox.RED).shift((*np.dot(transition, [-1, 0]), 0))
    u2_i_scale = np.dot(transition, [0, 1])[0]
    u2_j_scale = np.dot(transition, [0, 1])[1]
    u2_i = u2_i.shift(u2_j_scale*UP + u1_i_scale*RIGHT)
    u2_i.shift(u2_j_scale*UP)
    u2_i_label = Tex("$" + str(u2_i_scale) + " \hat{i}$", color=gruvbox.GREEN).move_to(u2_i.get_center()).shift(0.35*DOWN)
    u2_j_label = Tex("$" + str(u2_j_scale) + " \hat{j}$", color=gruvbox.RED).move_to(u2_j.get_center()).shift(0.35*LEFT)

    scene.play(
        Transform(u1, VGroup(u1_i, u1_j)),
        Transform(u2, VGroup(u2_i, u2_j)),
        Transform(u1_label, VGroup(u1_i_label, u1_j_label)),
        Transform(u2_label, VGroup(u2_i_label, u2_j_label)),
        TransformFromCopy(lines[3], lines[4])
    )
    scene.wait(2)
    scene.remove(u1, u2, u1_label, u2_label)

    i_hat = ChillVector([3, 0], color=gruvbox.GREEN)
    j_hat = ChillVector([0, 2], color=gruvbox.RED).shift(3*RIGHT)
    i_label = Tex("$3 \hat{i}$", color=gruvbox.GREEN).move_to(i_hat.get_center()).shift(0.35*DOWN)
    j_label = Tex("$2 \hat{j}$", color=gruvbox.RED).move_to(j_hat.get_center()).shift(0.35*LEFT)
    scene.play(
        Transform(VGroup(u1_i, u2_i), i_hat),
        Transform(VGroup(u1_j, u2_j), j_hat),
        Transform(VGroup(u1_i_label, u2_i_label), i_label),
        Transform(VGroup(u1_j_label, u2_j_label), j_label),
        TransformFromCopy(lines[4], lines[5])
    )
    scene.remove(u1_i, u1_j, u2_i, u2_j, u1_i_label, u1_j_label, u2_i_label, u2_j_label)
    scene.add(i_hat, j_hat, i_label, j_label)
    scene.wait(0.5)
    scene.play(TransformFromCopy(lines[5], lines[6]))
    scene.wait(2)

    scene.play(
        FadeOut(
            plane, vector, coords, i_hat, j_hat, i_label, j_label,
            *[line for line in lines if line != lines[6]],
            frame, text
        ),
    )
    scene.wait(0.5)
    scene.play(
        lines[6].animate.scale(2).move_to(ORIGIN),
    )

    scene.wait(1)
    line = MathTex(r"[v]_E = \begin{bmatrix} \alpha & \beta \\ \gamma & \delta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = M [v]_U")
    line.scale(1.2).move_to(ORIGIN)
    line[0][0:4].set_color(gruvbox.CYAN)
    line[0][6].set_color(gruvbox.SECONDARY)
    line[0][7].set_color(gruvbox.SECONDARY)
    line[0][8].set_color(gruvbox.SECONDARY)
    line[0][9].set_color(gruvbox.SECONDARY)
    line[0][12].set_color(gruvbox.PRIMARY)
    line[0][13].set_color(gruvbox.PRIMARY)
    line[0][16].set_color(gruvbox.SECONDARY)
    line[0][17:].set_color(gruvbox.PRIMARY)
    scene.play(Transform(lines[6], line))
    scene.remove(lines[6])
    scene.add(line)
    scene.wait(2)

    text = Text("Other way around", color=EMPHASIZED).scale(1.25).to_edge(UP).shift(0.5*DOWN)
    inverse_line = MathTex(r"[v]_U = M^{-1} [v]_E").scale(1.2).move_to(ORIGIN)
    inverse_line[0][0:4].set_color(gruvbox.CYAN)
    inverse_line[0][5:8].set_color(gruvbox.SECONDARY)
    inverse_line[0][8:].set_color(gruvbox.PRIMARY)
    scene.wait(2)
    scene.play(
        FadeOut(line[0][5:16]),
        Transform(line[0][:5], inverse_line[0][:5]),
        Transform(line[0][16], inverse_line[0][5:8]),
        Transform(line[0][17:], inverse_line[0][8:]),
        Write(text),
        run_time=2
    )
    scene.wait(2)


def p2_essence(scene):
    scene.remove(*scene.mobjects)
    transformation = [[1, 4], [-1, 1]]
    plane = EpicPlane().apply_matrix(transformation)
    vector = ChillVector([3, 2])
    coords = vector.transformed_coordinate_label(transformation)

    i_hat = ChillVector([1, -1], color=gruvbox.GREEN)
    j_hat = ChillVector([4, 1], color=gruvbox.RED)

    scene.add(plane, vector, coords, i_hat, j_hat)
    scene.wait(2)
    scene.play(
        plane.animate.apply_matrix(np.linalg.inv(transformation)),
        coords.animate.become(vector.coordinate_label()),
        i_hat.animate.become(ChillVector([1, 0], color=gruvbox.GREEN)),
        j_hat.animate.become(ChillVector([0, 1], color=gruvbox.RED)),
        run_time=3
    )
    scene.wait(3)
    scene.play(
        plane.animate.apply_matrix(transformation),
        coords.animate.become(vector.transformed_coordinate_label(transformation)),
        i_hat.animate.become(ChillVector([1, -1], color=gruvbox.GREEN)),
        j_hat.animate.become(ChillVector([4, 1], color=gruvbox.RED)),
        run_time=3
    )
    scene.wait(2)


def recap(scene):
    scene.remove(*scene.mobjects)
    frame1, frame2, plane1, plane2, transformed_plane = set_up_side_by_side_plane(scene, "transformed_plane3x3", 3, 6)
    frame1_text = Text("Multiply by A", color=PRIMARY).move_to(frame1.get_edge_center(UP)).shift(0.65*DOWN)
    frame2_text = Text("Multiply by B", color=PRIMARY).move_to(frame2.get_corner(UP)).shift(0.65*DOWN)
    frame2_text.set_z_index(2)

    vector1 = plot_vector([1, 1], plane1, color=gruvbox.RED)
    vector2 = vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - vector2.get_start()[:2]
    vector2.shift(shift[0] * RIGHT + shift[1] * UP)

    arrow = MathTex(r"\longleftrightarrow", color=EMPHASIZED).scale(2.25).move_to(ORIGIN).shift(frame1.get_center()[1]*UP)
    text = Tex("Trying to find $B$!", color=EMPHASIZED).to_edge(UP, buff=0.7).scale(1.25)

    scene.add(frame1, frame2, frame1_text, frame2_text, plane1, plane2, transformed_plane, vector1, vector2, text)
    scene.wait(1)
    next_vector1 = plot_vector([2, 1], plane1, color=gruvbox.RED)
    next_vector2 = next_vector1.copy().move_to(plane2.c2p(0, 0))
    shift = plane2.c2p(0, 0)[:2] - next_vector2.get_start()[:2]
    next_vector2.shift(shift[0] * RIGHT + shift[1] * UP)
    next_vector2.set_z_index(2)
    scene.play(Transform(vector1, next_vector1), Transform(vector2, next_vector2), run_time=2)
    scene.wait(2)


def finding_b(scene):
    scene.remove(*scene.mobjects)
    transition = [[5, -1], [-1, 1]]
    plane = EpicPlane().apply_matrix(transition)
    vector = ChillVector([1, 1])
    coords = vector.transformed_coordinate_label(transition)
    scene.add(plane, vector, coords)
    scene.wait(2)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    rabbit.set_z_index(2)
    rabbit.move_to(6 * RIGHT + 2.7 * DOWN)
    bubble = Bubble(fill_opacity=0.5).scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT).set_z_index(2)
    bubble_text = Tex(r"Convert \\ between coordinates").set_z_index(2)
    bubble.add_content(bubble_text)
    bubble_text.scale(1.15)

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


    scene.play(FadeIn(rabbit, bubble, bubble_text), Write(line0))
    scene.wait(1)
    scene.play(plane.animate.apply_matrix(np.linalg.inv(transition)), coords.animate.become(vector.coordinate_label()),
               FadeOut(rabbit, bubble, bubble_text), Transform(line0, line1[0][1]), Write(line1[0][0]), run_time=2)
    scene.remove(line0)
    scene.add(line1)
    scene.wait(2)

    scene.play(vector.animate.become(ChillVector([2, 1])), coords.animate.become(ChillVector([2, 1]).coordinate_label()),
               line1.animate.move_to(line2[0][1:]), Write(line2[0][0]), run_time=2)
    scene.remove(line1)
    scene.add(line2)
    scene.wait(2)

    scene.play(plane.animate.apply_matrix(transition), coords.animate.become(vector.transformed_coordinate_label(transition, integer_labels=False)),
               line2.animate.move_to(line3[0][3:]), Write(line3[0][:3]), run_time=2)
    scene.remove(line2)
    scene.add(line3)
    scene.wait(1)
    scene.play(line3.animate.move_to(line4[0][3:]), Write(line4[0][:3]), run_time=2)
    scene.remove(line3)
    scene.add(line4)
    scene.wait(2)

    line = MathTex("B = M^{-1}AM").scale(1.5).to_corner(UL, buff=0.75)
    line[0][0].set_color(gruvbox.CYAN)
    line[0][2:5].set_color(gruvbox.SECONDARY)
    line[0][5].set_color(gruvbox.PRIMARY)
    line[0][6].set_color(gruvbox.SECONDARY)
    scene.play(
        line4[0][2:-1].animate.move_to(line[0][1:]),
        FadeOut(line4[0][1], line4[0][-1]),
    )

    scene.remove(*scene.mobjects)
    scene.add(plane, vector, coords, line)

    scene.wait(0.5)
    scene.play(
        line.animate.scale(1.25).move_to(ORIGIN),
        FadeOut(plane, vector, coords),
        run_time=2
    )
    scene.wait(2)
    scene.play(FadeOut(line))
    scene.wait(2)


def mystery(scene):
    scene.remove(*scene.mobjects)

    rabbit = SVGMobject("assets/rabbit.svg").scale(0.5 * GOLDEN)
    bubble = Bubble().scale(0.5).pin_to(rabbit).shift(0.5 * DOWN + 0.25 * LEFT)
    bubble_text = Tex(r"Which basis will \\ make B diagonal?")
    bubble.add_content(bubble_text)
    bubble.content.scale(1.15)

    scene.add(rabbit)
    scene.play(DrawBorderThenFill(bubble), Write(bubble.content), run_time=2)
    scene.wait(2)
    scene.play(FadeOut(rabbit), FadeOut(bubble), run_time=2)
    scene.wait(0.5)

    scene.remove(bubble.content)
    scene.add(bubble_text)

    target_text = Tex("Which basis will make B diagonal?", color=PRIMARY).move_to(ORIGIN).scale(1.3)
    target_text1 = target_text[0][:14]
    target_text2 = target_text[0][14:]

    scene.play(
        bubble_text[0][:14].animate.become(target_text1).move_to(target_text1),
        bubble_text[0][14:].animate.become(target_text2).move_to(target_text2),
        run_time=2
    )
    scene.wait(2)
    scene.play(FadeOut(bubble_text), run_time=2)
    scene.wait(2)


class Chapter3(Scene):
    def construct(self):
        # render_transformed_plane(self) # this is for rendering the image used in same_operation

        p1_introduction(self)
        p1_coordinates(self)
        p1_same_operation(self)
        p1_conclusion(self)
        p2_introduction(self)
        p2_basis(self)
        p2_change_of_basis(self)
        p2_essence(self)
        recap(self)
        finding_b(self)
        mystery(self)


#TODO: fix fast-paced timings
#TODO: a bit more polishing, just look at the video and see what you can do to make it better
#TODO: change the color of ^-1 of inverse matrices (also in chapter 4 in the recap)