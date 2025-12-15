import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Any,Optional
from old_qlearn_stuff.env import environment, rewards, UP, DOWN, LEFT, RIGHT, FREE,WALL,PACKAGE,DROPOFF

from dijkstras import dijkstra_agent




#initialise environment
env = environment(13,13,package_location=(8,8),drop_off_location=(5,5))
state = env.reset()

#initialise my agents
agents = list()
dijkstra_agent_1 = dijkstra_agent(env)
agents.append(dijkstra_agent_1)




# build a background image once
img = np.zeros((env.height, env.width, 3), dtype=float)
img[env.grid == FREE]     = (0.95, 0.95, 0.95)
img[env.grid == WALL]     = (0.20, 0.20, 0.20)
img[env.grid == PACKAGE]  = (0.20, 0.60, 1.00)
img[env.grid == DROPOFF]  = (1.00, 0.50, 0.20)

plt.ion()
fig, ax = plt.subplots(figsize=(6,6))
# ax.imshow(img, origin="upper", aspect="equal")

#gonnna have a loop where checks each agents target, path and steps along that path

done = [False for _ in agents]
while not all(done):

    print(len(agents))
    print(agents)
    
    
    # plt loop for agent
    for i, agent in enumerate(agents):
        agent.find_target_and_set_course()
        agent.step_along_path()
        print(agent.path)
        print(agent.pos)
        done[i] = np.array_equal(agent.pos, env.package)
        print(done[i])
        
    # remove old scatters but keep the imshow background
    for c in ax.collections[1:]:
        c.remove()


    # Agents (swap to x=col, y=row)
    xs = [a.pos[1] for a in agents]
    ys = [a.pos[0] for a in agents]


    colors = [a.colour for a in agents]
    ax.scatter(xs, ys, s=140, edgecolors="k", facecolors=colors, zorder=10)

    # optional: mark package & drop
    px, py = env.package; dx, dy = env.drop_off
    ax.scatter([px],[py], s=120, edgecolors="k", facecolors=(0.9,0.9,0.3), zorder=3)
    ax.scatter([dx],[dy], s=120, edgecolors="k", facecolors=(0.9,0.1,0.9), zorder=3)

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)



plt.ioff(); plt.show()