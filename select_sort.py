from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import MoveToTarget
from manimlib.constants import LEFT, RIGHT, UP, DOWN, GREEN, BLUE, RED
from manimlib.mobject.geometry import Arrow, Circle
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene import Scene


class SelectSort(Scene):
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

    def sort(self):
        nodes_length = len(self.nodes)
        arrow = Arrow(UP+RIGHT)  # I don't get it
        arrow.scale(1)
        arrow.move_to(UP + 3 * LEFT)
        self.add(arrow)
        for i in range(nodes_length):
            arrow.generate_target()
            arrow.target.move_to(self.nodes[i].circle.get_arc_center() + UP)
            self.play(MoveToTarget(arrow))
            index_min = self.find_index_minimum(i)
            if i != index_min:
                self.swap_nodes(i, index_min)
            self.nodes[i].circle.set_color(GREEN)

    def find_index_minimum(self, from_index):
        arrow = Arrow(DOWN+RIGHT)  # I don't get it
        arrow.scale(0.5)
        arrow.move_to(self.nodes[from_index].circle.get_arc_center() + DOWN)
        arrow.set_color(BLUE)
        self.add(arrow)
        index_min = from_index
        self.nodes[index_min].circle.set_color(BLUE)
        for i in range(from_index + 1, len(self.nodes)):
            arrow.generate_target()
            arrow.target.move_to(self.nodes[i].circle.get_arc_center() + DOWN)
            self.play(MoveToTarget(arrow))
            if self.nodes[i].value < self.nodes[index_min].value:
                self.nodes[index_min].circle.set_color(RED)
                index_min = i
                self.nodes[index_min].circle.set_color(BLUE)

        self.remove(arrow)
        return index_min

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
        self.play(MoveToTarget(from_node.text), MoveToTarget(from_node.circle),
                  MoveToTarget(to_node.text), MoveToTarget(to_node.circle))

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
