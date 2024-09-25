import pygame
import math

# Base class for game objects
class TriangleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def point_in_circle(self, point, circle_center, circle_radius):
        return math.hypot(point[0] - circle_center[0], point[1] - circle_center[1]) <= circle_radius

    def line_intersects_circle(self, p1, p2, circle_center, circle_radius):
        # Check if either endpoint is inside the circle
        if self.point_in_circle(p1, circle_center, circle_radius) or self.point_in_circle(p2, circle_center, circle_radius):
            return True

        # Vector from p1 to p2
        p1_to_p2 = pygame.Vector2(p2) - pygame.Vector2(p1)
        # Vector from p1 to circle center
        p1_to_center = pygame.Vector2(circle_center) - pygame.Vector2(p1)

        # Project p1_to_center onto p1_to_p2, clamped to the segment
        projection_length = p1_to_center.dot(p1_to_p2) / p1_to_p2.length()
        projection_length = max(0, min(projection_length, p1_to_p2.length()))
        closest_point = pygame.Vector2(p1) + p1_to_p2.normalize() * projection_length

        # Check if the closest point is inside the circle
        return self.point_in_circle(closest_point, circle_center, circle_radius)

    def collission_check(self, other):
        # Define the vertices of the triangle
        point1 = (self.position.x, self.position.y - self.radius)
        point2 = (self.position.x - self.radius, self.position.y + self.radius)
        point3 = (self.position.x + self.radius, self.position.y + self.radius)
        points = [point1, point2, point3]

        # Check if any vertex is inside the circle
        for point in points:
            if self.point_in_circle(point, other.position, other.radius):
                return True

        # Check if any edge intersects the circle
        edges = [(point1, point2), (point2, point3), (point3, point1)]
        for edge in edges:
            if self.line_intersects_circle(edge[0], edge[1], other.position, other.radius):
                return True

        return False