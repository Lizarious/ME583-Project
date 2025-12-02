import matplotlib.pyplot as plt
import numpy as np

def update_plot(i, robot_trajectory, robot_future_traj, robot_controls, robot_radius, obstacles, obstacle_radius, acc_lims, vel_lims, num_time_steps, fig, axs):
    axs[0].cla()
    axs[1].cla()
    
    robot_position = robot_trajectory[i, :2]
    #axs[0].add_patch(plt.Circle(robot_position, robot_radius/2, color='C0', alpha=0.4, label='Drone Pos'))
    #axs[0].add_patch(plt.Circle(robot_position, sensor_range, color='C0', alpha=0.2, label='Obst. Sensor Range'))

    for obst in range(obstacles.shape[0]):
        axs[0].add_patch(plt.Circle(obstacles[obst], obstacle_radius[obst], color='C1', alpha=0.4))
    
    axs[0].plot(obstacles[:, 0], obstacles[:, 1],'g^', label='Obstacles')
    axs[0].plot(robot_trajectory[:, 0], robot_trajectory[:, 1], color='black')
    #axs[0].plot(robot_future_traj[i][:, 0], robot_future_traj[i][:, 1], "o-", markersize=3, color='red')
    #axs[0].plot(sqp_list[i][j][:, 0], sqp_list[i][j][:, 1], "o-", markersize=3, color='green', alpha=0.4)
    #axs[0].plot(path[:, 0], path[:, 1], 'b--', label='Target Path')
    axs[0].scatter(robot_trajectory[i:i+1, 0], robot_trajectory[i:i+1, 1], s=30, color='C0')
    axs[0].grid()
    axs[0].legend()
    axs[0].axis("equal")
    axs[0].set_title("Simulation")

    axs[1].plot(robot_controls)
    axs[1].scatter([i], robot_controls[i:i+1, 0], label="v_act", color='C0')
    axs[1].scatter([i], robot_controls[i:i+1, 1], label="w_act", color='C1')
    axs[1].hlines([acc_lims[0], acc_lims[1]], 0, num_time_steps-1, color='C1', linestyle='--')
    #axs[1].plot(robot_trajectory[:, -1], markersize=3, color='C2', label="Velocity")
    #axs[1].scatter([i], robot_trajectory[i:i+1, 3], color='C2')
    axs[1].hlines([vel_lims[0], vel_lims[1]], 0, num_time_steps-1, color='C2', linestyle='--')
    axs[1].set_xlim([0, num_time_steps])
    axs[1].set_ylim([-5, 5])
    axs[1].set_title("States and Inputs")
    axs[1].legend()
    axs[1].grid()

    fig.canvas.draw_idle()