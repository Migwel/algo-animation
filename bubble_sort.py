from manimlib.imports import *

class BubbleSort(Scene):
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
        swapped = True
        nbIterations = 1
        nbIterationsObj = None
        while swapped:
            self.remove(nbIterationsObj)
            nbIterationsObj = TextMobject("Iteration " + str(nbIterations))
            nbIterationsObj.move_to(2*UP)
            self.add(nbIterationsObj)

            swapped = False
            arrow = Arrow(UP+RIGHT) #I don't get it
            arrow.scale(1)
            arrow.move_to(UP + 3 * LEFT)
            self.add(arrow)
            for i in range(nodesLength - 1):
                arrow.generate_target()
                arrow.target.move_to(self.nodes[i].circle.get_arc_center() + UP)
                self.play(MoveToTarget(arrow))
                if self.nodes[i+1].value < self.nodes[i].value:
                    self.switchNodes(i, i+1)
                    swapped = True

            self.remove(arrow)
            nbIterations = nbIterations + 1
            self.wait(0.5)

        self.remove(nbIterationsObj)



    def printNodes(self):
        for node in self.nodes:
            print(node.value)

    def initAnimation(self):
        circleAnimations = []
        for node in self.nodes:
            self.add(node.text)
            circleAnimations.append(GrowFromCenter(node.circle))
        self.play(*circleAnimations)

    def switchNodes(self, fromIndex, toIndex):
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