import turtle
import math


WIDTH, HEIGHT = 800, 800
SCALE = 100  
FPS = 30
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("4D Tesseract Projection")
screen.tracer(0)  
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.pensize(2)
pen.color("white")
pen.up()


def generate_tesseract_vertices():
    
    vertices = []
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                for w in (-1, 1):
                    vertices.append([x, y, z, w])
    return vertices


def rotate4d(point, angle_xw, angle_yz):
    x, y, z, w = point
    cos_xw = math.cos(angle_xw)
    sin_xw = math.sin(angle_xw)
    x_, w_ = x * cos_xw - w * sin_xw, x * sin_xw + w * cos_xw
    cos_yz = math.cos(angle_yz)
    sin_yz = math.sin(angle_yz)
    y_, z_ = y * cos_yz - z * sin_yz, y * sin_yz + z * cos_yz

    return [x_, y_, z_, w_]


def project4d_to_3d(point4d, perspective=2.5):
    x, y, z, w = point4d
    w_offset = perspective
    factor = w_offset / (w_offset - w)
    return [x * factor, y * factor, z * factor]


def project3d_to_2d(point3d, perspective=4.0):
    x, y, z = point3d
    z_offset = perspective
    factor = z_offset / (z_offset - z)
    return [x * factor, y * factor]


def tesseract_edges(vertices):
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            diff = sum(a != b for a, b in zip(vertices[i], vertices[j]))
            if diff == 1:
                edges.append((i, j))
    return edges


def draw_wireframe(points2d, edges):
    pen.clear()
    for i, j in edges:
        x1, y1 = points2d[i]
        x2, y2 = points2d[j]
        pen.up()
        pen.goto(x1, y1)
        pen.down()
        pen.goto(x2, y2)
        pen.up()

#main loop
vertices = generate_tesseract_vertices()
edges = tesseract_edges(vertices)

def animate(angle_xw=0.0, angle_yz=0.0):
    
    projected_points = []
    for v in vertices:
        v_rot = rotate4d(v, angle_xw, angle_yz)
        v_3d = project4d_to_3d(v_rot)
        v_2d = project3d_to_2d(v_3d)
     
        x = v_2d[0] * SCALE + WIDTH // 2
        y = v_2d[1] * SCALE + HEIGHT // 2
        projected_points.append((x - WIDTH // 2, y - HEIGHT // 2))

    draw_wireframe(projected_points, edges)
    screen.update()

    
    angle_xw += math.radians(1.5)
    angle_yz += math.radians(1.1)
    screen.ontimer(lambda: animate(angle_xw, angle_yz), int(1000 / FPS))


animate()
turtle.done()
