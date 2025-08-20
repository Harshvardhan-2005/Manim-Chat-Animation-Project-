from manim import *
import numpy as np

def lorenz_points(sigma=10.0, beta=8/3, rho=28.0, dt=0.005, steps=12000, start=np.array([0.0,1.0,1.05])):
    p = np.zeros((steps, 3))
    p[0] = start
    for i in range(1, steps):
        x, y, z = p[i-1]
        dx = sigma*(y - x)
        dy = x*(rho - z) - y
        dz = x*y - beta*z
        p[i] = p[i-1] + dt*np.array([dx, dy, dz])
    return p

class LorenzScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-30,30,10], y_range=[-30,30,10], z_range=[0,60,10])
        self.set_camera_orientation(phi=70*DEGREES, theta=45*DEGREES, zoom=1)
        self.add(axes)
        pts = lorenz_points()
        pts = (pts - pts.mean(axis=0)) * 0.25
        path_points = [axes.c2p(*p) for p in pts]
        path = VMobject()
        path.set_points_smoothly(path_points[:2])
        self.add(path)
        n = ValueTracker(2)
        def update_path(m):
            k = int(n.get_value())
            m.set_points_smoothly(path_points[:max(2,k)])
        path.add_updater(update_path)
        self.play(n.animate.set_value(len(path_points)), run_time=8, rate_func=linear)
        path.remove_updater(update_path)
        self.wait(1)