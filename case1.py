import numpy as np
import matplotlib.pyplot as plt
from quadtree import Point, Rect, QuadTree, Vector
from matplotlib import gridspec
import random

DPI = 72
random.seed = 123
# np.random.seed(60)
random.random()
width, height = 600, 400

N = 500
coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
# points = [Point(*coord) for coord in coords]

# Max length of ray/vector
max_length = 50

vectors = []
points = []
for i in range(N):
    dir = (Point(random.random()-0.5, random.random()-0.5)) * random.randint(5, max_length)
    start_point = Point(random.randint(max_length//2,width-max_length//2), random.randint(max_length//2,height-max_length//2))
    end_point = start_point + dir
    vectors.append(Vector(start_point, end_point))
    points.append(end_point)

domain = Rect(width/2, height/2, width, height, type="divided")
qtree = QuadTree(domain, 3)
for point in points:
    qtree.insert(point)

print('Number of points in the domain =', len(qtree))
plt.clf()
fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
qtree.draw(ax)
for vector in vectors:
    vector.draw(ax)

ax.scatter([p.x for p in points], [p.y for p in points], s=4)
ax.set_xticks([])
ax.set_yticks([])

region = Rect(width/2, height/2, width, height)
found_points = []
qtree.query(region, found_points)
print('Number of found points =', len(found_points))
#
ax.scatter([p.x for p in found_points], [p.y for p in found_points],
           facecolors='none', edgecolors='r', s=32)

# region.draw(ax, c='r')

ax.invert_yaxis()
plt.tight_layout()
plt.savefig('search-quadtree.png')
plt.show()