import pygame
from pygame.math import Vector3


class Cube:

    def __init__(self, vectors, screen_width, screen_height, initial_angle=25):
        self.vertices, self.angle, self.screen_width, self.screen_height = vectors, initial_angle, screen_width, screen_height

        # Define the vectors that compose each of the 6 faces
        self.faces = [(0,1,2,3),
                      (1,5,6,2),
                      (5,4,7,6),
                      (4,0,3,7),
                      (0,4,5,1),
                      (3,2,6,7)]

        self.colors = [(0xee,0xee,0xff),
                       (0x7f,0x7c,0xaf),
                       (0x9f,0xb4,0xc7),
                       (0x28,0x58,0x7b),
                       (0x9f,0xb7,0x98),
                       (0xdb,0x29,0x55)]

        tmp = []
        for vector in self.vertices:
            rotated_vector = vector.rotate_x(initial_angle).rotate_y(initial_angle).rotate_z(initial_angle)
            tmp.append(rotated_vector)

        self.vertices = tmp

    def transform_vectors(self, new_angle_x, new_angle_y):
        # It will hold transformed vectors.
        transformed_vectors = []

        for vector in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            mod_vector = vector.rotate_x(new_angle_x)
            mod_vector = mod_vector.rotate_y(new_angle_y)
            # Transform the point from 3D to 2D
            mod_vector = self.project(mod_vector, self.screen_width, self.screen_height, 512, 2)
            # Put the point in the list of transformed vectors
            transformed_vectors.append(mod_vector)

        return transformed_vectors

    def project(self, vector, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + vector.z)
        x = vector.x * factor + win_width / 2
        y = -vector.y * factor + win_height / 2
        return Vector3(x, y, vector.z)

    def calculate_average_z(self, points):
        avg_z = []
        for i, face in enumerate(self.faces):
            # for each point of a face calculate the average z value
            z = (points[face[0]].z +
                 points[face[1]].z +
                 points[face[2]].z +
                 points[face[3]].z) / 4.0
            avg_z.append([i, z])

        return avg_z

    def create_polygon(self, face, transformed_vectors):
        return [(int(transformed_vectors[f].x), int(transformed_vectors[f].y)) for f in face]

pygame.init()

screen = pygame.display.set_mode((400, 600))

clock = pygame.time.Clock()

cube = Cube([
    Vector3(0, 0.5, -0.5),
    Vector3(0.5, 0.5, -0.5),
    Vector3(0.5, 0, -0.5),
    Vector3(0, 0, -0.5),
    Vector3(0, 0.5, 0),
    Vector3(0.5, 0.5, 0),
    Vector3(0.5, 0, 0),
    Vector3(0, 0, 0)
], screen.get_width(), screen.get_height())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    (x,y) = pygame.mouse.get_pos()

    clock.tick(50)
    screen.fill((0,0,0))

    polygons = []
    transformed_vectors = cube.transform_vectors(x,y)
    avg_z = cube.calculate_average_z(transformed_vectors)

    for z in avg_z:
        face_index = z[0]
        face = cube.faces[face_index]
        pointlist = cube.create_polygon(face, transformed_vectors)
        polygons.append((pointlist, z[1], cube.colors[face_index]))

    for poly in sorted(polygons, key=lambda x: x[1], reverse=True):
        pygame.draw.polygon(screen, poly[2], poly[0])
        pygame.draw.polygon(screen, (0,0,0), poly[0], 3)

    pygame.display.flip()
pygame.quit()