from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import MoveToTarget
from manimlib.constants import LEFT, RIGHT, UP, GREEN
from manimlib.mobject.geometry import Arrow, Circle
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene import Scene


class InsertSort(Scene):
    nodes = []
    def construct(self):
        self.nodes = [self.buildTextAndCircles(6, 3*LEFT), self.buildTextAndCircles(2, 2*LEFT), self.buildTextAndCircles(7, LEFT),
                      self.buildTextAndCircles(1, 0), self.buildTextAndCircles(8, RIGHT), self.buildTextAndCircles(9, 2*RIGHT), self.buildTextAndCircles(4, 3*RIGHT)
                      ]
        self.initAnimation()
        self.wait()
        self.sort()
        self.finished()
        self.wait(2)

    def finished(self):
        nbIterationsObj = TextMobject("Sorted")
        nbIterationsObj.move_to(2*UP)
        self.add(nbIterationsObj)

        for node in self.nodes:
            node.circle.set_color(GREEN)

    def sort(self):
        nodesLength = len(self.nodes)
        arrow = Arrow(UP+RIGHT) #I don't get it
        arrow.scale(1)
        arrow.move_to(UP + 3 * LEFT)
        self.add(arrow)
        for i in range (1, nodesLength):
            arrow.generate_target()
            arrow.target.move_to(self.nodes[i].circle.get_arc_center() + UP)
            self.play(MoveToTarget(arrow))
            j = i
            while j > 0 and self.nodes[j].value < self.nodes[j-1].value:
                self.swapNodes(j, j - 1)
                j = j - 1
            self.wait(0.1)

    def printNodes(self):
        for node in self.nodes:
            print(node.value)

    def initAnimation(self):
        circleAnimations = []
        for node in self.nodes:
            self.add(node.text)
            circleAnimations.append(GrowFromCenter(node.circle))
        self.play(*circleAnimations)

    def swapNodes(self, fromIndex, toIndex):
        fromNode = self.nodes[fromIndex]
        toNode = self.nodes[toIndex]
        
        toCenter = toNode.circle.get_arc_center()
        fromNode.text.generate_target()
        fromNode.text.target.move_to(toCenter)
        fromNode.circle.generate_target()
        fromNode.circle.target.move_to(toCenter)

        fromCenter = fromNode.circle.get_arc_center()
        toNode.text.generate_target()
        toNode.text.target.move_to(fromCenter)
        toNode.circle.generate_target()
        toNode.circle.target.move_to(fromCenter)
        self.play(MoveToTarget(fromNode.text), MoveToTarget(fromNode.circle), MoveToTarget(toNode.text), MoveToTarget(toNode.circle))

        self.nodes[fromIndex] = toNode
        self.nodes[toIndex] = fromNode

    def buildTextAndCircles(self, value, location):
        textObj = TextMobject(str(value))
        textObj.move_to(location)
        circleObj = Circle()
        circleObj.surround(textObj)
        circleObj.scale(1.5)
        return Node(textObj, circleObj, value)

class Node():
    def __init__(self, text, circle, value):
        self.text = text
        self.circle = circle
        self.value = value