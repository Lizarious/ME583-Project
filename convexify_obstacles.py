import numpy as np

def circles_overlap(c1, c2):

    dx = c1[0] - c2[0]
    dy = c1[1] - c2[1]
    dist2 = dx*dx + dy*dy
    r_sum = c1[2] + c2[2]
    return dist2 <= r_sum**2


def build_overlap_groups(circles):

    circles = np.asarray(circles)
    N = circles.shape[0]
    visited = np.zeros(N, dtype=bool)
    groups = []

    for i in range(N):
        if visited[i]:
            continue
        stack = [i]
        group = []
        visited[i] = True
        while stack:
            u = stack.pop()
            group.append(u)
            for v in range(N):
                if not visited[v] and circles_overlap(circles[u], circles[v]):
                    visited[v] = True
                    stack.append(v)
        groups.append(group)

    return groups


def convex_hull(points):

    points = np.asarray(points)
    if len(points) <= 1:
        return points

    # Sort by x, then y
    pts = points[np.lexsort((points[:, 1], points[:, 0]))]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(tuple(p))

    # Build upper hull
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(tuple(p))

    hull = np.array(lower[:-1] + upper[:-1])
    return hull


def to_convex_hull(circles, num_samples=32):

    circles = np.asarray(circles)
    if circles.size == 0:
        return []

    groups = build_overlap_groups(circles)
    hulls = []

    angles = np.linspace(0, 2*np.pi, num_samples, endpoint=False)

    for group in groups:
        pts = []
        for idx in group:
            x, y, r = circles[idx]
            xs = x + r * np.cos(angles)
            ys = y + r * np.sin(angles)
            pts.append(np.stack([xs, ys], axis=1))
        pts = np.concatenate(pts, axis=0)
        hull = convex_hull(pts)
        hulls.append(hull)

    return hulls
