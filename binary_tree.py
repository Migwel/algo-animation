from manimlib.animation.fading import FadeOut
from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import MoveToTarget
from manimlib.constants import UP, RIGHT, LEFT, DOWN
from manimlib.mobject.geometry import Circle, Line, Arrow
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.scene.scene import Scene


class Leaf:
    def __init__(self, text: TextMobject, circle: Circle, value: int, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.circle = circle
        self.value = value
        self.lChild = None
        self.lEdge = None
        self.rChild = None
        self.rEdge = None

    def display(self):
        circle_animations = []
        self.display_internal(circle_animations)
        return circle_animations

    def display_internal(self, circle_animations):
        circle_animations.append(GrowFromCenter(self.text))
        circle_animations.append(GrowFromCenter(self.circle))
        if self.lChild is not None:
            self.lChild.display_internal(circle_animations)
            circle_animations.append(GrowFromCenter(self.lEdge))
        if self.rChild is not None:
            self.rChild.display_internal(circle_animations)
            circle_animations.append(GrowFromCenter(self.rEdge))


class BinaryTree:
    root = None
    MAX_LEVEL = 3
    ROOT_LOCATION = 2 * UP

    def __init__(self, scene):
        self.scene = scene

    def add_value(self, value, animate=False):
        if self.root is None:
            self.build_root(value, animate)
            return

        arrow_group = None
        if animate:
            node = self.build_node(value, 0)
            arrow = Arrow(UP+RIGHT)  # I don't get it
            arrow.next_to(node.circle, DOWN)
            arrow_group = VGroup(*[node.text, node.circle, arrow])
            arrow_group.move_to(self.root.circle.get_arc_center() + 1.1 * UP)
            self.scene.add(arrow_group)

        self.root = self.add_recursive(self.root, value, arrow_group, animate)

    def build_root(self, value, animate=False):
        text_obj = TextMobject(str(value))
        text_obj.move_to(self.ROOT_LOCATION)
        circle_obj = Circle()
        circle_obj.surround(text_obj)
        circle_obj.scale(1.5)
        self.root = Leaf(text_obj, circle_obj, value)
        if animate:
            animations = [GrowFromCenter(self.root.circle), GrowFromCenter(self.root.text)]
            self.scene.play(*animations)

    def swap_nodes(self, from_node, to_node):
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
        self.scene.play(MoveToTarget(from_node.text), MoveToTarget(from_node.circle), MoveToTarget(to_node.text),
                        MoveToTarget(to_node.circle))

    @staticmethod
    def build_node(value, location):
        text_obj = TextMobject(str(value))
        text_obj.move_to(location)
        circle_obj = Circle()
        circle_obj.surround(text_obj)
        circle_obj.scale(1.5)
        return Leaf(text_obj, circle_obj, value)

    def add_recursive(self, current: Leaf, value: int, arrow: VGroup, animate: bool = False, level: float = 0):
        if animate:
            arrow.generate_target()
            arrow.target.move_to(current.circle.get_arc_center() + 1.1 * UP)
            self.scene.play(MoveToTarget(arrow))

        if value == current.value:
            return current

        if value < current.value:
            if current.lChild is None:
                current.lChild = self.build_node(value,
                                                 current.circle.get_arc_center() + DOWN + (self.MAX_LEVEL - level) * LEFT)
                current.lEdge = Line()
                current.lEdge.put_start_and_end_on(current.circle.get_edge_center(DOWN), current.lChild.circle.get_edge_center(UP))
                if animate:
                    self.scene.add(current.lEdge)
                    arrow.generate_target()
                    arrow.target.move_to(current.lChild.circle.get_arc_center() + 1.1 * UP)
                    animations = [GrowFromCenter(current.lChild.circle), GrowFromCenter(current.lChild.text), FadeOut(arrow)]
                    self.scene.play(MoveToTarget(arrow))
                    self.scene.play(*animations)

            else:
                self.add_recursive(current.lChild, value, arrow, animate, level + 1.2)

        if value > current.value:
            if current.rChild is None:
                current.rChild = self.build_node(value, current.circle.get_arc_center() + DOWN + (self.MAX_LEVEL - level) * RIGHT)
                current.rEdge = Line()
                current.rEdge.put_start_and_end_on(current.circle.get_edge_center(DOWN), current.rChild.circle.get_edge_center(UP))
                if animate:
                    self.scene.add(current.rEdge)
                    arrow.generate_target()
                    arrow.target.move_to(current.rChild.circle.get_arc_center() + 0.75 * UP)
                    animations = [GrowFromCenter(current.rChild.circle), GrowFromCenter(current.rChild.text), FadeOut(arrow)]
                    self.scene.play(MoveToTarget(arrow))
                    self.scene.play(*animations)
            else:
                self.add_recursive(current.rChild, value, arrow, animate, level + 1.2)

        return current


class Insertion(Scene):
    def construct(self):
        tree = BinaryTree(self)
        tree.add_value(5, True)
        tree.add_value(2, True)
        tree.add_value(6, True)
        tree.add_value(3, True)
        tree.add_value(4, True)
        tree.add_value(1, True)
        tree.add_value(8, True)
        tree.add_value(7, True)
        tree.add_value(9, True)
        self.wait(3)

    def initAnimation(self, tree):
        self.play(*tree.root.display())