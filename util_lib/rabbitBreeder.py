from manim import *


GOLDEN = 1.61803398875
INGOLDEN = 0.61803398875


def arrange_group(vgroup, center, top=True, max_per_line=5, buff=0.4):
    if len(vgroup) > max_per_line:
        vgroup.arrange_in_grid(buff=buff, cols=max_per_line)
        #vgroup.move_to(center + (len(vgroup) // max_per_line - 1) * UP)
    else:
        vgroup.arrange(RIGHT, buff=buff)
    vgroup.move_to(center)

def grow_rabbits(babyRabbits, grownRabbits, scale, buff, max_per_line):
    center = grownRabbits.get_center()
    if len(grownRabbits) == 0:
        center = UP
    animations = []
    targetGrown = grownRabbits.copy()
    for babyRabbit in babyRabbits:
        grownRabbits.add(babyRabbit)
        targetGrown.add(babyRabbit.copy().scale(GOLDEN*scale))

    arrange_group(targetGrown, center, True, max_per_line, buff)
    for i, rabbit in enumerate(grownRabbits):
        if rabbit in babyRabbits:
            animations.append(rabbit.animate.move_to(targetGrown[i]).scale(GOLDEN*scale))
            babyRabbits.remove(rabbit)
        else:
            animations.append(rabbit.animate.move_to(targetGrown[i]).scale(scale))

    return AnimationGroup(*animations)


def breed_rabbits(babyRabbits, grownRabbits, scale, buff, max_per_line, opacity):
    center = babyRabbits.get_center()
    if len(babyRabbits) == 0:
        center = DOWN
    animations = []
    new_babys = []
    targetBaby = VGroup()
    for grownRabbit in grownRabbits:
        baby = grownRabbit.copy().set_opacity(opacity)
        targetBaby.add(baby.copy().scale(INGOLDEN*scale))
        new_babys.append(baby)
    arrange_group(targetBaby, center, False, max_per_line, buff)
    for i, rabbit in enumerate(new_babys):
        animations.append(rabbit.animate.move_to(targetBaby[i]).scale(INGOLDEN*scale))

    return AnimationGroup(*animations), new_babys


def pass_month(scene, babyRabbits, grownRabbits, scale=1, buff=0.4, max_per_line=5, opacity=1, extra_animations=[], run_time=1):
    previous_height = grownRabbits.get_height()
    anim1, new_babys = breed_rabbits(babyRabbits, grownRabbits, scale, buff, int(max_per_line*GOLDEN), opacity)
    anim2 = grow_rabbits(babyRabbits, grownRabbits, scale, buff, max_per_line)
    scene.play(anim1, anim2, *extra_animations, run_time=run_time)
    babyRabbits.add(*new_babys)
    scene.play(babyRabbits.animate.shift((grownRabbits.get_height() - previous_height)*0.5*DOWN))