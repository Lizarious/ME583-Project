import numpy as np
import matplotlib.pyplot as plt



# Arbitrary "mountainous terrain" function to promote curvy trajectory
def terrain_function(x, y, amp=2, freq=.2):
    return amp * np.sin(freq*x) * np.cos(freq*y) - amp * np.sin(freq/2 * x+2) * np.cos(freq*y+3)

# Potential field functions
def attractive_force(pos, target):
    return target - pos

def repulsive_force(pos, obstacles, radius):
    force = np.zeros(2)
    for obs in obstacles:
        direction = pos - obs
        distance = np.linalg.norm(direction)
        if distance < radius:
            repulse = direction / (distance + 1e-6)
            force += repulse
    return force



def environment_gen(num_obstacles=10,obst_scale=0.5,obst_var=0.2,map_size=10,step_size=0.1,seed=None,return_markers=False,target=False):

    if seed:
        print("Seed Set")
        np.random.seed(seed)
        
    # Parameters
    momentum = 0.90
    max_iters = map_size*50
    goal_threshold = 3
    waypoint_threshold = 3


    # Generate obstacles
    obstacle_pos = np.random.uniform(-map_size/2, map_size/2, size=(num_obstacles, 2))

    obstacle_radii = np.random.uniform(obst_scale - obst_var, obst_scale + obst_var, size=(num_obstacles, 1))

    obstacles = np.hstack([obstacle_pos, obstacle_radii])


    if target:

        # Start, goal, and random waypoints
        start = np.array([1.0, 1.0])
        goal = np.array([map_size, map_size])
        waypoint1 = np.array([np.random.uniform(map_size/5, map_size/3), np.random.uniform(map_size/5, map_size/1.2)])
        waypoint2 = np.array([np.random.uniform(map_size/1.5, map_size/1.2), np.random.uniform(map_size/5, map_size/1.2)])

        # Initial position and random direction
        position = start.copy()
        velocity = np.abs(np.random.normal(.1, 1.0, size=2))
        velocity /= np.linalg.norm(velocity) + 1e-6

        # Path list
        path = [position.copy()]
        hit_waypoint1, hit_waypoint2 = False, False

        for i in range(max_iters):
            # Determine current target
            if not hit_waypoint1:
                target = waypoint1
                if np.linalg.norm(position - waypoint1) < waypoint_threshold: hit_waypoint1 = True
            elif not hit_waypoint2:
                target = waypoint2
                if np.linalg.norm(position - waypoint2) < waypoint_threshold: hit_waypoint2 = True
            else:
                target = goal

            # Forces
            to_target = attractive_force(position, target)
            #away_from_obstacles = repulsive_force(position, obstacles, obstacle_radius)

            # Create gradient from forces and terrain function
            grad = to_target + terrain_function(position[0], position[1]) * np.array([1, 1]) #+ away_from_obstacles

            # Smooth path w/ momentum
            grad = grad / (np.linalg.norm(grad) + 1e-6)
            velocity = momentum * velocity + (1 - momentum) * grad
            velocity = velocity / (np.linalg.norm(velocity) + 1e-6)

            # Update position
            position += step_size * velocity
            path.append(position.copy())

            # Stop if goal reached
            if hit_waypoint1 and hit_waypoint2 and np.linalg.norm(position - goal) < goal_threshold:
                print(f"Reached goal in {i+1} steps")
            """for j in range(max_iters-i):
                path.append(position.copy())"""
            break
            
    
    if return_markers:
        markers = {"start":{"threshold":0,"pos":start},
                   "waypoint1":{"threshold":waypoint_threshold,"pos":waypoint1},
                   "waypoint2":{"threshold":waypoint_threshold,"pos":waypoint2},
                   "goal":{"threshold":goal_threshold,"pos":goal}}
        return obstacles, np.array(path), markers
    else:
        return obstacles