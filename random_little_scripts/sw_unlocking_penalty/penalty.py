import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# time options, this could be dynamic or day-based
# t = 365 (12m)
# t = 180 (6m)
# t = 90 (3m)
# t = 30 (1m)
for t in [30,90,180,365]:

    # plot ranges
    total_range = np.arange(0,t,1)
    plot_range = np.arange(0,t-2,1)

    # penalty function
    fn = lambda x: np.min([0.8, ((7/np.log(t))*(x/t))**(1/4)])

    # penalty values
    penalty = np.concatenate([np.array([fn(x) for x in plot_range]), np.zeros(np.arange(t-2,t,1).shape[0])])

    # plot params
    font = {
        'size':20,
        'weight':'bold'
    }
    plt.rc('font', **font)
    fig, ax = plt.subplots(1,1, figsize=(20,10))
    plot = sns.lineplot(x=total_range, y=penalty)
    ax.set_ylabel('Penalty (Proportion lost)')
    ax.set_xlabel('Time (Days)')
    plt.savefig(f'penalty_{t}.jpeg')

    # data
    data = pd.DataFrame({
        'day':total_range,
        'penalty':np.round(penalty,2)
    })
    data.to_markdown(f'penalty_{t}.csv', index=False)
