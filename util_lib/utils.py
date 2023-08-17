from manim import *
from extra.color_schemes.gruvbox import *
from extra.color_schemes import gruvbox
import numpy as np


WIDTH = 14
HEIGHT = 8
GOLDEN = 1.61803398875
INGOLDEN = 0.61803398875

fib_matrix = np.array([[1, 1], [1, 0]])


def fib(n):
    return np.linalg.matrix_power(fib_matrix, n).dot(np.array([1, 1]))[1]


# a curve that gradually decreases from 1 to 0.5

k = 0.75
opacity_curve = lambda x: 0.5+0.5*np.exp(-k*x)

def plot_on_numberline(numberline, num, color=gruvbox.PRIMARY):
    position = numberline.number_to_point(num)
    pin_size = numberline.get_height() * 0.3
    pin = Line(position+pin_size*UP, position-pin_size*UP, color=color, stroke_width=2)
    return pin


def scale_plane_to_fit_frame(plane, frame):
    plane_width = plane.get_width()
    plane_height = plane.get_height()
    frame_width = frame.get_width()
    frame_height = frame.get_height()
    scale_factor = min(frame_width / plane_width, frame_height / plane_height)
    plane.scale(scale_factor)
    return plane


def plot_vector(coords, plane, color=gruvbox.PRIMARY):
    vector = ChillVector(plane.c2p(*coords)[:2] - plane.c2p(0, 0)[:2], color=color)
    shift = plane.c2p(0, 0)[:2] - vector.get_start()[:2]
    vector.shift(shift[0] * RIGHT + shift[1] * UP)
    return vector


def get_vector_label(label, vector, color=None, direction=UP, buff=0.25):
    slope = (vector.get_end()[1] - vector.get_start()[1]) / (vector.get_end()[0] - vector.get_start()[0])
    angle = np.arctan(slope)
    label = Tex(label, color=color)
    if direction is UP:
        angle += PI/2
    elif direction is DOWN: angle -= PI/2

    label.move_to(vector.get_center() + buff*(np.sin(angle)*UP + np.cos(angle)*RIGHT))

    if color is not None:
        label.set_color(color)
    else:
        label.set_color(vector.color)

    return label


def rainbow_text(text):
    rainbow = [gruvbox.RED, gruvbox.ORANGE, gruvbox.YELLOW, gruvbox.GREEN, gruvbox.CYAN, gruvbox.BLUE, gruvbox.PURPLE]

    for i in range(len(text)):
        text[i].set_color(rainbow[i % len(rainbow)])


EpicPlane = lambda dim=(-20, 20, 1): NumberPlane(
        x_range = dim,
        y_range = dim,
        background_line_style = {
            "stroke_color": SECONDARY,
            "stroke_width": 1,
            "stroke_opacity": 1
        },
        faded_line_style = {
            "stroke_color": SECONDARY,
            "stroke_width": 0.75,
            "stroke_opacity": 0.5
        },
        faded_line_ratio = 2,
        axis_config = {
            "stroke_width": 2,
            "stroke_opacity": 1
        },
        x_axis_config = {
            "stroke_color": FG,
            "stroke_width": 2,
            "stroke_opacity": 1
        },
        y_axis_config = {
            "stroke_color": FG,
            "stroke_width": 2,
            "stroke_opacity": 1
        }
    )

class ChillVector(Vector):
    def __init__(self, direction=RIGHT, color=PRIMARY, tip_length=0.2, buff=0, **kwargs):
        super().__init__(direction, buff, tip_length=tip_length, **kwargs)
        self.color = color
        self.stroke_width = 3

    def coordinate_label(
            self,
            integer_labels=True,
            n_dim=2,
            color=None,
            **kwargs,
    ):
        if color is None:
            color = self.color
        return super().coordinate_label(integer_labels, n_dim, color, **kwargs)

    def transformed_coordinate_label(
            self,
            matrix,
            integer_labels=True,
            n_dim=2,
            color=None,
            **kwargs,
    ):
        vect = np.linalg.inv(matrix).dot(np.array(self.get_end()[0:2]))
        if integer_labels:
            vect = np.round(vect).astype(int)
        vect = vect[:n_dim]
        vect = vect.reshape((n_dim, 1))
        label = Matrix(vect, **kwargs)
        label.scale(LARGE_BUFF - 0.2)

        shift_dir = np.array(self.get_end())
        if shift_dir[0] >= 0:  # Pointing right
            shift_dir -= label.get_left() + DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * LEFT
        else:  # Pointing left
            shift_dir -= label.get_right() + DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * RIGHT
        label.shift(shift_dir)
        if color is not None:
            label.set_color(color)
        else:
            label.set_color(self.color)
        return label

    def custom_coordinate_label(
            self,
            coords,
            color=None,
    ):
        vect = np.array([coords[0], coords[1]])
        vect = vect[:2]
        label = MathTex(vector_to_tex(vect))
        label.scale(LARGE_BUFF)

        shift_dir = np.array(self.get_end())
        if shift_dir[0] >= 0:  # Pointing right
            shift_dir -= label.get_left() + DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * LEFT
        else:  # Pointing left
            shift_dir -= label.get_right() + DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * RIGHT
        label.shift(shift_dir)
        if color is not None:
            label.set_color(color)
        else:
            label.set_color(self.color)
        return label


def matrix_to_tex(matrix):
    return r"\begin{bmatrix} " + fr"{matrix[0][0]} & {matrix[0][1]} \\ {matrix[1][0]} & {matrix[1][1]}" + r" \end{bmatrix}"


def vector_to_tex(vector):
    return r"\begin{bmatrix} " + fr"{vector[0]} \\ {vector[1]}" + r" \end{bmatrix}"


def set_up_side_by_side_plane(scene, file, dim, size=6):
    frame1 = Rectangle(height=size, width=size, color=FG, fill_color=BG_FILL, fill_opacity=1).to_edge(LEFT)
    frame2 = Rectangle(height=size, width=size, color=FG).to_edge(RIGHT).set_z_index(2)

    VGroup(frame1, frame2).move_to(ORIGIN).shift(0.5 * DOWN)
    plane1 = scale_plane_to_fit_frame(EpicPlane((-dim, dim, 1)).move_to(frame1), frame1)
    plane2 = scale_plane_to_fit_frame(EpicPlane((-dim, dim, 1)).move_to(frame2), frame2)
    transformed_plane = scale_plane_to_fit_frame(
        ImageMobject(f"assets//scenes//{file}").move_to(frame2), frame2
    )
    return frame1, frame2, plane1, plane2, transformed_plane


def get_tex_debug(tex):
    tex_debug = VGroup()
    colors = [gruvbox.RED, gruvbox.ORANGE, gruvbox.YELLOW, gruvbox.GREEN, gruvbox.CYAN, gruvbox.BLUE, gruvbox.PURPLE]
    for i in range(len(tex)):
        for j in range(len(tex[i])):
            tex_debug.add(
                Text(str(j), color=colors[i % len(colors)]).move_to(tex[i][j]).scale(0.3)
            )
    return tex_debug