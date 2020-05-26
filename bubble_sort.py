from manimlib.constants import UP, LEFT, RIGHT, GREEN
from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import MoveToTarget
from manimlib.mobject.geometry import Arrow, Circle
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene import Scene


class BubbleSort(Scene):
    nodes = []

    def construct(self):
        self.nodes = [self.build_text_and_circles(6, 3 * LEFT), self.build_text_and_circles(2, 2 * LEFT),
                      self.build_text_and_circles(7, LEFT), self.build_text_and_circles(1, 0),
                      self.build_text_and_circles(8, RIGHT), self.build_text_and_circles(9, 2 * RIGHT),
                      self.build_text_and_circles(4, 3 * RIGHT)
                      ]
        self.init_animation()
        self.wait()
        self.sort()
        self.finished()
        self.wait(2)

    def finished(self):
        sorted_text = TextMobject("Sorted")
        sorted_text.move_to(2*UP)
        self.add(sorted_text)

        for node in self.nodes:
            node.circle.set_color(GREEN)

    def sort(self):
        nodes_length = len(self.nodes)
        swapped = True
        nb_iterations = 1
        nb_iterations_text = None
        while swapped:
            self.remove(nb_iterations_text)
            nb_iterations_text = TextMobject("Iteration " + str(nb_iterations))
            nb_iterations_text.move_to(2*UP)
            self.add(nb_iterations_text)

            swapped = False
            arrow = Arrow(UP+RIGHT)  # I don't get it
            arrow.scale(1)
            arrow.move_to(UP + 3 * LEFT)
            self.add(arrow)
            for i in range(nodes_length - 1):
                arrow.generate_target()
                arrow.target.move_to(self.nodes[i].circle.get_arc_center() + UP)
                self.play(MoveToTarget(arrow))
                if self.nodes[i+1].value < self.nodes[i].value:
                    self.swap_nodes(i, i + 1)
                    swapped = True

            self.remove(arrow)
            nb_iterations = nb_iterations + 1
            self.wait(0.1)

        self.remove(nb_iterations_text)

    def print_nodes(self):
        for node in self.nodes:
            print(node.value)

    def init_animation(self):
        circle_animations = []
        for node in self.nodes:
            self.add(node.text)
            circle_animations.append(GrowFromCenter(node.circle))
        self.play(*circle_animations)

    def swap_nodes(self, from_index, to_index):
        from_node = self.nodes[from_index]
        to_node = self.nodes[to_index]
        
        to_center = to_node.circle.get_arc_center()
        from_node.text.generate_target()
        from_node.text.target.move_to(to_center)
        from_node.circle.generate_target()
        from_node.circle.target.move_to(to_center)

        from_center = from_node.circle.get_arc_center()
        to_node.text.generate_target()
        to_node.text.target.move_to(from_center)
        to_node.circle.generate_target()
        to_node.circle.target.move_to(from_center)
        self.play(MoveToTarget(from_node.text),
                  MoveToTarget(from_node.circle),
                  MoveToTarget(to_node.text),
                  MoveToTarget(to_node.circle))

        self.nodes[from_index] = to_node
        self.nodes[to_index] = from_node

    @staticmethod
    def build_text_and_circles(value, location):
        text_obj = TextMobject(str(value))
        text_obj.move_to(location)
        circle_obj = Circle()
        circle_obj.surround(text_obj)
        circle_obj.scale(1.5)
        return Node(text_obj, circle_obj, value)


class Node:
    def __init__(self, text, circle, value):
        self.text = text
        self.circle = circle
        self.value = value
