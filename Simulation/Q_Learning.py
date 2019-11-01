import numpy as np

Sensor0_bok = np.linspace(0,15,5)
Sensor2_bok = np.linspace(0,15,5)

def get_state(opservation):
    sensor0, sensor2 = opservation
    sensorO_bin = np.digitize(sensor0,Sensor0_bok)
    sensor2_bin = np.digitize(sensor2, Sensor2_bok)
    return (sensorO_bin,sensor2_bin)


def max_action(Q, state, actions=[0, 1, 2]):
    values = np.array([Q[state,a] for a in actions])
    action = np.argmax(values)

    return action

if __name__ == '__main__':
    env = gym.make('MountainCar-v0')
    env._max_episode_steps = 1000
    n_games = 50000
    alpha = 0.1
    gamma = 0.99
    eps = 1.0

    action_space = [0, 1, 2]

    states = []
    for pos in range(21):
        for vel in range(21):
            states.append((pos, vel))

    Q = {}
    for state in states:
        for action in action_space:
            Q[state, action] = 0

    #pickle_in = open('mountaincar.pkl', 'rb')
    #Q = pickle.load(pickle_in)
    #env = wrappers.Monitor(env, "tmp/mountaincar",
                            #video_callable=lambda episode_id: True, force=True)
    score = 0
    total_rewards = np.zeros(n_games)
    for i in range(n_games):
        done = False
        obs = env.reset()
        state = get_state(obs)
        if i % 100 == 0 and i > 0:
            print('episode ', i, 'score ', score, 'epsilon %.3f' % eps)
        score = 0
        while not done:
            action = np.random.choice([0,1,2]) if np.random.random() < eps \
                    else max_action(Q, state)
            obs_, reward, done, info = env.step(action)
            state_ = get_state(obs_)
            score += reward
            action_ = max_action(Q, state_)
            Q[state, action] = Q[state, action] + \
                    alpha*(reward + gamma*Q[state_, action_] - Q[state, action])
            state = state_
        total_rewards[i] = score
        eps = eps - 2/n_games if eps > 0.01 else 0.01

    mean_rewards = np.zeros(n_games)
    for t in range(n_games):
        mean_rewards[t] = np.mean(total_rewards[max(0, t-50):(t+1)])
    plt.plot(mean_rewards)
    plt.savefig('mountaincar.png')

    #f = open("mountaincar.pkl","wb")
    #pickle.dump(Q,f)
    #f.close()