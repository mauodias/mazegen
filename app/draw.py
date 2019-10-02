import svgwrite

class Drawer():

    def __init__(self, filename=None):
        self.filename = filename
        self.drawing = svgwrite.Drawing(self.filename, profile='tiny')

    def line(self, startx, starty, endx, endy, color=(0,0,0,'%')):
        l = self.drawing.line((startx+5, starty+5), (endx+5, endy+5), stroke=svgwrite.rgb(*color))
        self.drawing.add(l)

    def save(self):
        self.drawing.save()

    def get_contents(self):
        return self.drawing.tostring()
