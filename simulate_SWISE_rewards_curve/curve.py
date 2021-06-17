import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI

# instantiate coingecko api
cg = CoinGeckoAPI()

# get eth and swise prices
eth_price = cg.get_price(ids='ethereum', vs_currencies='usd')[
    'ethereum']['usd']
swise_price = cg.get_token_price(id='ethereum', contract_addresses='0x48c3399719b582dd63eb5aadf12a40b4c3f52fa2', vs_currencies='usd')[
    '0x48c3399719b582dd63eb5aadf12a40b4c3f52fa2']['usd']

# function to generate sample data


def simulate_curves(functions, reward=1e6, sim_accs=1e3, min_eth_amount=0.1, max_eth_amount=1e3, swise_price=swise_price, eth_price=eth_price, amounts_apply=lambda x: x, mult_swise=True):
    """
    reward : amount of SWISE to allocate
    sim_accs : accounts to simulate the curves for
    min_eth_amount : lower bound for eth amount of simulated accounts
    max_eth_amount : upper bound for eth amount of simulated accounts
    swise_price : price of SWISE
    eth_price : price of ETH
    amounts apply : function to apply to linearly generated amounts
    mult_swise : multiply by the price of SWISE to get dollar value of returns
    """

    # multiply or not by price
    multiplier = {True: swise_price, False: 1}

    # generating sample data
    accounts = [f'account {n}' for n in range(int(sim_accs))]
    amounts = amounts_apply(np.linspace(
        min_eth_amount, max_eth_amount, int(sim_accs)))
    value = amounts*eth_price
    perc_pool = value/np.sum(value)
    monthly_reward = perc_pool*reward*multiplier[mult_swise]
    monthly_apr = (monthly_reward*swise_price)/value
    yearly_apr = (monthly_reward*swise_price*12)/value

    # creating dict
    sample_data = {
        'account': accounts,
        'amounts': amounts,
        'value': value,
        'original_perc_pool': perc_pool,
        'original_monthly_reward': monthly_reward,
        'original_monthly_apr': monthly_apr,
        'original_yearly_apr': yearly_apr
    }

    # monthly rewards in SWISE
    for name, function in functions.items():
        # functions param length
        if len(functions.keys()) > 1:
            funcname = f'_{name}'
        else:
            funcname = ''

        # apply function to values
        after_apply = function(sample_data['value'])

        # new theoretical percentage of pool after apply
        sample_data[f'new_perc_pool{funcname}'] = after_apply/sum(after_apply)

        # new reward with theoretical pool percentage
        sample_data[f'new_monthly_reward{funcname}'] = multiplier[mult_swise] * reward * \
            sample_data[f'new_perc_pool{funcname}']

        # monthly APR after apply
        sample_data[f'new_monthly_apr{funcname}'] = (
            swise_price*sample_data[f'new_monthly_reward{funcname}'])/value

        # yearly APR after apply
        sample_data[f'new_yearly_apr{funcname}'] = (
            swise_price*sample_data[f'new_monthly_reward{funcname}']*12)/value

    return pd.DataFrame(sample_data)


# function to generate plots
def plot_simulation(df, fontsize=35, figsize=(20, 40), linewidth=4, x_axis=3*['amounts'], y_axis=['monthly_reward', 'monthly_apr', 'yearly_apr'], usd_or_swise='SWISE', savefig=True):
    """
    df : dataframe to plot
    fontsize : font size for the figure axes/legend
    figsize : plot size
    linewidth : line width
    x_axis : x-axis to use as index in the plots
    y_axis : columns to comparatively plot
    """
    # rcParams
    plt.rcParams.update({
        'font.size': fontsize,
        'figure.figsize': figsize
    })

    # instantiating figure and axes
    fig, ax = plt.subplots(len(y_axis), tight_layout=True)

    # legend names
    y_axis_labels = [x.replace('_', ' ') for x in y_axis]

    # plotting loop
    for n in range(len(y_axis)):
        # filter col
        filt_df = df[[f'original_{y_axis[n]}', f'new_{y_axis[n]}']]
        filt_df.index = df[x_axis[n]]

        # plot
        ax[n].plot(filt_df.loc[:, f'original_{y_axis[n]}'],
                   label=f'Original {y_axis_labels[n]}', linewidth=linewidth)
        ax[n].plot(filt_df.loc[:, f'new_{y_axis[n]}'],
                   label=f'New {y_axis_labels[n]}', linewidth=linewidth)

        # axes names
        ax[n].set_xlabel(x_axis[n])
        ax[n].set_ylabel(y_axis[n].replace('_', ' '))

        # legend
        ax[n].legend()

        # plot title
        ax[n].set_title(f'{y_axis_labels[n]} per {x_axis[n]}')

    # savefig
    if savefig == True:
        fig.savefig('simulation.png', dpi=300, bbox_inches='tight')

    # legend
    plt.show()


# defining the function to flatten the curve by quantiles
# default qty param
qtys = 200

# function itself
def quantile_flatten(col, functions=qtys*[np.power], quantiles=np.linspace(0.01, 1, qtys), powers=np.linspace(105, 100, qtys)/100):
    # separate arrays by quantile
    arrays = []
    for i, q in enumerate(quantiles):
        if i == 0:
            new_col_section = col[col < np.quantile(col, q)]
        elif i > 0:
            new_col_section = col[(col >= np.quantile(
                col, quantiles[i-1])) & (col <= np.quantile(col, q))]
        arrays.append(functions[i](new_col_section, powers[i]))

    # concatenate and return
    return np.concatenate(arrays)


# functions to simulate for
functions = {
    'test': quantile_flatten
}

# running the functions
df = simulate_curves(functions=functions, reward=6e6,
                     amounts_apply=lambda x: x, mult_swise=False)
plot_simulation(df, figsize=(40, 70))
