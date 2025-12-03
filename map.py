import matplotlib.pyplot as plt
import numpy as np

def update_plot(i, reference_trajectory, robot_controls, reference_controls, obstacles, fig, axs, robot_trajectory_A = None, robot_trajectory_B = None, acc_lims=None, vel_lims=None, convex_hulls=None,):
    axs[0].cla()
    axs[1].cla()
    axs[2].cla()
    #axs[3].cla()
    
    num_time_steps = reference_trajectory.shape[0]

    # Obst
    for obst in range(obstacles.shape[0]):
        axs[0].add_patch(plt.Circle(obstacles[obst,:2], obstacles[obst,2], color='C3', alpha=0.4))
    
    axs[0].plot(obstacles[:, 0], obstacles[:, 1],'g^', label='Obstacles')


    # Combined obstacles (e.g. convex hull polygons)
    if convex_hulls is not None:
        # combined_obst is assumed to be an iterable of (K, 2) arrays of vertices
        for hull in convex_hulls:
            hull = np.asarray(hull)
            axs[0].fill(hull[:, 0], hull[:, 1], alpha=0.3, color='C4')



    # Robot Pos A
    if robot_trajectory_A is not None:
        axs[0].plot(robot_trajectory_A[:, 0], robot_trajectory_A[:, 1], color='C0')
        axs[0].scatter(robot_trajectory_A[i:i+1, 0], robot_trajectory_A[i:i+1, 1], s=30, color='C0')

    # Robot Pos B
    if robot_trajectory_B is not None:
        axs[0].plot(robot_trajectory_B[:, 0], robot_trajectory_B[:, 1], color='C2')
        axs[0].scatter(robot_trajectory_B[i:i+1, 0], robot_trajectory_B[i:i+1, 1], s=30, color='C2')

    # Ref Pos
    axs[0].plot(reference_trajectory[:, 0], reference_trajectory[:, 1],color='C1', linestyle='--')
    axs[0].scatter(reference_trajectory[i:i+1, 0], reference_trajectory[i:i+1, 1], s=30, color='C1')

    # Formatting
    axs[0].grid()
    axs[0].legend()
    axs[0].axis("equal")
    axs[0].set_title("Simulation")


    # v_act Plot
    axs[1].plot(robot_controls[:,0], color='C0')
    axs[1].plot(reference_controls[:,0], color='C1', linestyle='--')
    axs[1].scatter([i], robot_controls[i:i+1, 0], label="v_act", color='C0')
    if vel_lims:axs[1].hlines([vel_lims[0], vel_lims[1]], 0, num_time_steps-1, color='C2', linestyle='--')
    axs[1].set_xlim([0, num_time_steps])
    #axs[1].set_ylim([-0.5, 1])
    axs[1].set_title("States and Inputs")
    axs[1].legend()
    axs[1].grid()


    # w_act Plot
    axs[2].plot(robot_controls[:,1], color='C0')
    axs[2].plot(reference_controls[:,1], color='C1', linestyle='--')
    axs[2].scatter([i], robot_controls[i:i+1, 1], label="w_act", color='C0')
    if acc_lims: axs[2].hlines([acc_lims[0], acc_lims[1]], 0, num_time_steps-1, color='C2', linestyle='--')
    axs[2].set_xlim([0, num_time_steps])
    #axs[2].set_ylim([-1, 1])
    axs[2].legend()
    axs[2].grid()


    # theta Plot
    """axs[3].plot(robot_trajectory[:, -1], markersize=3, color='C2', label="Velocity")
    axs[3].scatter([i], robot_trajectory[i:i+1, 2], color='C2')
    #axs[3].hlines([vel_lims[0], vel_lims[1]], 0, num_time_steps-1, color='C3', linestyle='--')
    axs[3].set_xlim([0, num_time_steps])
    axs[3].set_ylim([-5, 5])
    axs[3].legend()
    axs[3].grid()"""

    

    fig.canvas.draw_idle()