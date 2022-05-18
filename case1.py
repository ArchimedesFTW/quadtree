import numpy as np
import matplotlib.pyplot as plt
from quadtree import Point, Rect, QuadTree, Vector
from matplotlib import gridspec
import random

DPI = 72
random.seed(123)
# np.random.seed(60)
random.random()
width, height = 600, 400

N = 20
coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
# points = [Point(*coord) for coord in coords]

# Max length of ray/vector
max_length = 100

inside_areas = []
inside_areas.append(Rect(width*0.2, height*0.3, width*0.4, height*0.3, type="Room"))
inside_areas.append(Rect(width*0.55, height*0.45, width*0.30, height*0.8, type="Room"))
inside_areas.append(Rect(width*0.60, height*0.88, width*0.10, height*0.2, type="Room"))
inside_areas.append(Rect(width*0.75, height*0.65, width*0.4, height*0.25, type="Room"))

delete_boxes = []
delete_boxes.append(Rect(width*0.4, height*0.3, width*0.05, height*0.25, type="Delete"))
delete_boxes.append(Rect(width*0.59, height*0.55, width*0.2, height*0.6, type="Delete"))
delete_boxes.append(Rect(width*0.70, height*0.65, width*0.05, height*0.24, type="Delete"))
delete_boxes.append(Rect(width*0.60, height*0.85, width*0.102, height*0.02, type="Room"))
# delete_boxes.append(Rect(width*0.4, height*0.3, width*0.05, height*0.25, type="Delete"))




padding=2
arrow_length=20
vectors = []
points = []

for area in inside_areas:

    for i in range(int((N//len(inside_areas))*(area.area**0.9)/50)):
        start_point = Point(random.randint(area.west_edge+padding, area.east_edge-padding),
                            random.randint(area.north_edge+padding, area.south_edge-padding)) # Y

        end_point = Point(start_point.x + random.randint(-arrow_length, arrow_length), start_point.y + random.randint(-arrow_length, arrow_length))

        # Snap to y-axis or x axis
        rnd = random.random()
        if (rnd >= 0.75):
            end_point.x = area.west_edge
        elif (rnd >= 0.5):
            end_point.x = area.east_edge
        elif (rnd >= 0.25):
            end_point.y = area.north_edge
        else:
            end_point.y = area.south_edge

        # Make sure they are in bounds
        end_point.x = min(max(end_point.x, area.west_edge), area.east_edge)
        end_point.y = min(max(end_point.y, area.north_edge), area.south_edge)


        if (end_point.distance_to(start_point) < max_length):
            in_delete_box = False
            for box in delete_boxes:
                if box.contains(end_point):
                    in_delete_box = True
                    break

            if not in_delete_box:
                vectors.append(Vector(start_point, end_point))
                points.append(end_point)

        #
        # dir = (Point(random.random()-0.5, random.random()-0.5)) * random.randint(5, max_length)
        # start_point = Point(random.randint(max_length//2,width-max_length//2), random.randint(max_length//2,height-max_length//2))
        # end_point = start_point + dir


domain = Rect(width/2, height/2, width, height, type="divided")
qtree = QuadTree(domain, 1)
for point in points:
    qtree.insert(point)

print('Number of points in the domain =', len(qtree))
plt.clf()
fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()



ax.set_xlim(0, width)
ax.set_ylim(0, height)


# Draw interior
for area in inside_areas:
    area.draw(ax)

qtree.draw(ax)
# Draw graph
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
# ax.scatter([p.x for p in found_points], [p.y for p in found_points],
#            facecolors='none', edgecolors='r', s=32)

# region.draw(ax, c='r')

ax.invert_yaxis()
plt.tight_layout()
plt.savefig('search-quadtree.png')
plt.show()