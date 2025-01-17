import numpy as np
import pygame

"""
TODO
Organize + comment code
Connect everything to the rest of the tree code

Connect more things to focal_point and focal_axis
    Azimuth rotation should subtract the focal point
    ..then rotate the focal axis to the z-axis
    ..then perform the azimuth rotation
    ..then rotate the z-axis back to the focal axis
    ..then re-add the focal point.
    Rotation should have option to work current way, OR alternate path:
    Rotate focal axis to z-axis
    ..then perform rotation
    .. then rotate z-axis back to focal axis.
"""

class Graph:
    def __init__(self, perspective_point = [10, 0, 2.5], screen_dir = [-1, 0, 0],
                 focal_axis = [0, 0, 1], width = 400, height = 800, screen_width = 0.3,
                 points = None, title = '3D Grapher', update_func = None):
        self._perspective_point = np.array(perspective_point)
        self._screen_dir = np.array(screen_dir)
        self._screen_dir = self._screen_dir / np.linalg.norm(self._screen_dir) # Make sure it's a unit vector
        self.focal_axis = np.array(focal_axis) # Acts as 'up' direction, also axis about which rotations occur
        self.focal_axis = self.focal_axis / np.linalg.norm(self.focal_axis)
        self.width = width
        self.height = height
        self.draw_axes = False
        self.axes = np.array([[-5, 0, 0],
                         [5, 0, 0],
                         [0, -5, 0],
                         [0, 5, 0],
                         [0, 0, -5],
                         [0, 0, 5]])
        if points is not None:
            self._points = np.array(points)
        else:
            self._points = np.array([])
        self.title = title
        if update_func:
            self.update_func = update_func
        else:
            self.update_func = self.draw
        self.screen_width = screen_width
        self.panning = False
        self.rotating = False
        self.initial_values = {'perspective_point': self._perspective_point,
                               'screen_dir': self._screen_dir,
                               'screen_width': self.screen_width}
        self.find_screen()
        self.matrix = np.eye(3)
        self.points_projected = False
        self.projected_points = self.project_points()
    
    def find_screen(self):
        width = self.screen_width / 2
        height = self.screen_height / 2
        
        v = self.focal_axis - self.screen_dir[2] * self.screen_dir
        v = v / np.linalg.norm(v)
        u = np.cross(self.screen_dir, v)
        u = u / np.linalg.norm(u)
        self.screen_top = 2 * width * u # Points right along top edge
        self.screen_left = -2 * height * v # Points down along left edge
    
    @property # Vector pointing from screen_pos to top left corner of the screen
    def screen_corner(self):
        return (self.screen_top + self.screen_left) / -2

    @property
    def screen_height(self):
        return self.screen_width / self.width * self.height
    
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @property
    def perspective_point(self):
        return self._perspective_point

    @perspective_point.setter
    def perspective_point(self, value):
        self._perspective_point = value

    @property
    def screen_dir(self):
        return self._screen_dir
    
    @screen_dir.setter
    def screen_dir(self, value):
        self._screen_dir = value / np.linalg.norm(value)

    @property
    def screen_pos(self):
        return self.perspective_point + self.screen_dir

    @property # Actual coordinate of the top-left screen corner
    def screen_corner_pos(self):
        return self.screen_pos + self.screen_corner

    def start_panning(self, position):
        if self.panning or self.rotating:
            return
        self.panning = True
        self.initial_position = position
        self.initial_screen_state = np.array([self.screen_dir,
                                              self.screen_left,
                                              self.screen_top])
    
    def pan(self, position):
        if not self.panning:
            return
        dx = position[0] - self.initial_position[0]
        dy = position[1] - self.initial_position[1]
        screen_angle_h = 2 * np.atan(self.screen_width / 2)
        screen_angle_v = 2 * np.atan(self.screen_height / 2)
        d_theta = dx / self.width * screen_angle_h
        d_phi = -dy / self.height * screen_angle_v
        self.screen_dir, self.screen_left, self.screen_top = self.rotate_screen_state(self.initial_screen_state, d_theta, d_phi)
        self.projected_points = self.project_points()
    
    def stop_panning(self):
        if not self.panning:
            return
        self.panning = False
        del self.initial_position, self.initial_screen_state

    def start_rotating(self, position):
        if self.panning or self.rotating:
            return
        self.rotating = True
        self.initial_position = position
        self.initial_matrix = self.matrix
        # Finds the largest radius of any currently on-screen point
        try:
            r = np.max(np.linalg.norm(self.points[:, :2], axis = 1)[((0 <= self.projected_points[:, 0]) & (self.projected_points[:, 0] <= self.width) &
                                                                     (0 <= self.projected_points[:, 1]) & (self.projected_points[:, 1] <= self.height))])
        except ValueError:
            # No on-screen points
            r = 0
        r /= 2
        self.angle_range = 2*np.atan2(-0.5*self.screen_width / np.linalg.norm(self.screen_dir) * (r - np.linalg.norm(self.perspective_point)), r)
    
    def rotate(self, position):
        if not self.rotating:
            return
        dx = position[0] - self.initial_position[0]
        d_theta = dx / self.width * self.angle_range
        self.matrix = self.initial_matrix @ self.get_matrix(zr = d_theta)
        dy = position[1] - self.initial_position[1]
        d_phi = dy / self.height * np.pi / 2
        self.matrix = self.matrix @ self.get_matrix(yr = d_phi)
        self.projected_points = self.project_points()
    
    def stop_rotating(self):
        if not self.rotating:
            return
        self.rotating = False
        del self.initial_position, self.initial_matrix, self.angle_range

    def zoom(self, amount, position):
        if self.panning or self.rotating:
            return
        screen_angle_h = 2 * np.atan(self.screen_width / 2)
        screen_angle_v = 2 * np.atan(self.screen_height / 2)
        
        factor = 1 + abs(amount) / 10
        if amount > 0:
            new_width = self.screen_width / factor
        else:
            new_width = self.screen_width * factor
        min_width = self.initial_values['screen_width'] / 50
        max_width = self.initial_values['screen_width'] * 50
        new_width = min(max(new_width, min_width), max_width)
        factor = new_width / self.screen_width
        self.screen_width = new_width
        self.screen_left *= factor
        self.screen_top *= factor
        # Below code pans the screen so the same point remains under the mouse cursor
        # So, it zooms on the location of the mouse cursor
        # Partly copy/pasted from self.pan()
        dx = (1-factor) * (self.width/2 - position[0])
        dy = (1-factor) * (self.height/2 - position[1])
        d_theta = dx / self.width * screen_angle_h
        d_phi = -dy / self.height * screen_angle_v
        initial_screen_state = np.array([self.screen_dir,
                                         self.screen_left,
                                         self.screen_top])
        self.screen_dir, self.screen_left, self.screen_top = self.rotate_screen_state(initial_screen_state, d_theta, d_phi)
        self.projected_points = self.project_points()

    def restore_azimuth(self):
        if self.rotating: # Fine to do this while panning
            return
        z = self.focal_axis @ self.matrix
        target = np.array([0, 0, 1])
        axis = np.cross(z, target)
        norm = np.linalg.norm(axis)
        if norm == 0:
            matrix = np.eye(3)
        else:
            axis = axis / norm
            angle = np.arccos(min(max(np.dot(z, target), -1), 1))
            K = np.array([[0, -axis[2], axis[1]],
                          [axis[2], 0, -axis[0]],
                          [-axis[1], axis[0], 0]])
            matrix = np.eye(3) + np.sin(-angle) * K + (1 - np.cos(-angle)) * K @ K
        self.matrix = self.matrix @ matrix
        self.projected_points = self.project_points()
    
    def rotate_screen_state(self, screen, theta = 0, phi = 0):
        initial_theta, initial_phi = self.to_spherical(screen[0])[1:]
        screen = self.transform(screen, zr = -initial_theta)
        screen = self.transform(screen, yr = -(np.pi/2 - initial_phi))
        screen = self.transform(screen, yr = phi)
        screen = self.transform(screen, yr = np.pi/2 - initial_phi)
        screen = self.transform(screen, zr = theta)
        screen = self.transform(screen, zr = initial_theta)
        return screen
    
    # Translates a point or array of points by x, y, and z, then rotates clockwise by zr,
    # yr, and xr radians around each axis, in that order
    def transform(self, points, x = 0, y = 0, z = 0, xr = 0, yr = 0, zr = 0):
        points = np.array(points)
        if x or y or z:
            points = points + np.array([x, y, z])
        # Note: @ operator is matrix multiplication operator
        if zr:
            z_matrix = np.array([[np.cos(zr), -np.sin(zr), 0], [np.sin(zr), np.cos(zr), 0], [0, 0, 1]])
            points = points @ z_matrix.T
        if yr:
            y_matrix = np.array([[np.cos(yr), 0, np.sin(yr)], [0, 1, 0], [-np.sin(yr), 0, np.cos(yr)]])
            points = points @ y_matrix.T
        if xr:
            x_matrix = np.array([[1, 0, 0], [0, np.cos(xr), -np.sin(xr)], [0, np.sin(xr), np.cos(xr)]])
            points = points @ x_matrix.T
        return points

    def get_matrix(self, xr = 0, yr = 0, zr = 0):
        # Note: @ operator is matrix multiplication operator
        matrix = np.array([[1., 0, 0], [0, 1, 0], [0, 0, 1]])
        if zr:
            matrix @= np.array([[np.cos(zr), -np.sin(zr), 0], [np.sin(zr), np.cos(zr), 0], [0, 0, 1]]).T
        if yr:
            matrix @= np.array([[np.cos(yr), 0, np.sin(yr)], [0, 1, 0], [-np.sin(yr), 0, np.cos(yr)]]).T
        if xr:
            matrix @= np.array([[1, 0, 0], [0, np.cos(xr), -np.sin(xr)], [0, np.sin(xr), np.cos(xr)]]).T
        return matrix
    
    def resize(self):
        pixels_per_unit = self.width / self.screen_width
        width, height = self.screen.get_size()
        d_width = width / self.width
        d_height = height / self.height
        self.width = width
        self.height = height
        self.screen_width = self.width / pixels_per_unit
        self.screen_top *= d_width
        self.screen_left *= d_height
        self.projected_points = self.project_points()
    
    def to_spherical(self, xyz):
        x, y, z = xyz
        r = np.linalg.norm([x, y, z])
        if r == 0:
            theta = 0
            phi = 0
        else:
            theta = np.atan2(y, x)
            if theta < 0:
                # np.atan2 has range (-π, π) but we need (0, 2π)
                theta += 2*np.pi
            phi = np.acos(z/r)
        return np.array([r, theta, phi])
    
    def to_cartesian(self, r_theta_phi):
        r, theta, phi = r_theta_phi
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.array([x, y, z])

    def find_sizes(self, points):
        # Distance of each point to the camera
        distances = np.linalg.norm(points - self.perspective_point, axis=1)
        # Smaller value = further away from the camera, so smaller size
        inverted_distances = 1 / distances
        # Values now range from 0 to some positive value
        normalized_sizes = inverted_distances / np.min(inverted_distances) - 1
        # Values now range from 0 to 1
        normalized_sizes = normalized_sizes / np.max(normalized_sizes)
        max_size = 4
        min_size = 1
        max_size -= min_size
        # Values now range from min_size to max_size
        sizes = max_size * normalized_sizes + min_size
        sizes = np.round(sizes)
        return sizes
    
    def project_points(self, points = None):
        if points is None:
            points = self.points
            self.points_projected = True
            points = points @ self.matrix
            self.sizes = self.find_sizes(points)
        else:
            points = points @ self.matrix
        d = np.dot(self.screen_dir, self.screen_pos)
        points_vectors = self.perspective_point - points
        ts = (d - np.dot(points, self.screen_dir)) / np.dot(points_vectors, self.screen_dir)
        intersections = points + ts[:, np.newaxis] * points_vectors
        # Distance between point p and line mt + b is |m❌(p-b)| / |m|
        # We have points in intersections and line self.screen_left * t + self.screen_corner
        # Also line self.screen_top * t + self.screen_corner
        # Calculate the distance of each point to these lines
        xs = np.linalg.norm(np.cross(self.screen_left, intersections - self.screen_corner_pos), axis=1) / np.linalg.norm(self.screen_left)
        ys = np.linalg.norm(np.cross(self.screen_top, intersections - self.screen_corner_pos), axis=1) / np.linalg.norm(self.screen_top)
        # Determine direction based on dot product to handle left/right and top/bottom signs
        xs_sign = np.sign(np.dot(intersections - self.screen_corner_pos, self.screen_top))
        ys_sign = np.sign(np.dot(intersections - self.screen_corner_pos, self.screen_left))
        # Apply the signs to the distances
        xs = xs * xs_sign
        ys = ys * ys_sign
        # Normalize the distances based on the screen width and height
        xs = xs / self.screen_width
        ys = ys / self.screen_height
        # Finally, convert to pixels
        xs = np.round(self.width * xs)
        ys = np.round(self.height * ys)
        return np.column_stack([xs, ys])
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEWHEEL:
                self.zoom(event.y, pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left
                    self.start_panning(event.pos)
                elif event.button == 2: # Middle
                    self.restore_azimuth()
                elif event.button == 3: # Right
                    self.start_rotating(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]: # Left
                    self.pan(event.pos)
                if buttons[1]: # Middle
                    pass
                if buttons[2]: # Right
                    self.rotate(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Left
                    self.stop_panning()
                elif event.button == 2: # Middle
                    pass
                elif event.button == 3: # Right
                    self.stop_rotating()
            elif event.type == pygame.WINDOWSIZECHANGED:
                self.resize()
            else:
                pass
                #print(f'{event.type} = {pygame.event.event_name(event.type)}')
        return True

    def draw(self, points_projected):
        if points_projected:
            self.points_projected = False
        self.screen.fill((255, 255, 255))
        if self.draw_axes:
            pygame.draw.line(self.screen, (0, 0, 0), self.axes[0], self.axes[1], 2)
            pygame.draw.line(self.screen, (0, 0, 0), self.axes[2], self.axes[3], 2)
            pygame.draw.line(self.screen, (0, 0, 0), self.axes[4], self.axes[5], 2)
        for i, point in enumerate(self.projected_points):
            size = self.sizes[i]
            if point[0] < -size or point[0] > self.width + size or point[1] < -size or point[1] > self.height + size:
                continue
            color = (255, 0, 0)
            pygame.draw.circle(self.screen, color, point, size)
        pygame.display.flip()
    
    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        running = True
        while running:
            self.update_func(self.points_projected)
            running = self.handle_events()
        print('Exiting')
        pygame.quit()

def generate_cone(n = 1200):
    points = []
    while len(points) < n:
        x = rng.uniform(-1, 1)
        y = rng.uniform(-1, 1)
        z = rng.uniform(0, 5)
        if x**2 + y**2 <= (z-5)**2 / 25:
            points.append([x, y, z])
    return np.array(points)

def generate_cylinder(n = 1200):
    points = []
    while len(points) < n:
        theta = rng.uniform(0, 2*np.pi)
        x = np.cos(theta)
        y = np.sin(theta)
        z = rng.uniform(0, 5)
        points.append([x, y, z])
    return np.array(points)

if __name__ == '__main__':
    rng = np.random.default_rng()
    points = generate_cone()
    graph = Graph(points = points)
    graph.run()
