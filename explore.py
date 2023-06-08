## IMPORTS
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

import warnings
warnings.filterwarnings('ignore')

import wrangle as w

## FUNCTIONS
# defining a function to display distribution of target
def get_target_dist(df, target):
    sns.histplot(data=df[target])
    plt.title('Histplot of numbers of bird strikes associated with each level of damage')
    plt.xticks(ticks=['N','M','S','D'], labels=['None', 'Minor', 'Substantial', 'Destroyed'])
    plt.show()
    
    return

# defining a function to display distribution of target with only Minor/Substantial/Destroyed
def get_target_dist_MSD(df, target):
    sns.histplot(data=df[target])
    plt.title('Histplot of numbers of bird strikes associated with M/S/D levels of damage')
    plt.xticks(ticks=['M','S','D'], labels=['Minor', 'Substantial', 'Destroyed'])
    plt.show()
    
    return

# defining a function to create categorical plots for visualizataioin
def get_damage_catfeature_plot(df, feature, target='damage_level'):
    """
    This function will
    - accept the bird_strike df with at least two categorical variables: feature and target(default 'damage_level')
    - make a crosstab of target vs feature
    - plot that cross tab
    - make a crosstab of target without damage_level 'N'
    - plot that crosstab
    """
    # make crosstabs
    observed = pd.crosstab(df[target], df[feature])
    # this crosstab drops out the Negligible Damage numers so we can better see the actual damaged numbers
    temp_df = df[df[target] != 'N'][[target, feature]]
    observed_dsm = pd.crosstab(temp_df[target], temp_df[feature])
    
    # plot crosstabs
    observed.plot.bar(rot=0)
    plt.title(f'Histplot of {target} vs {feature} category')
    plt.xlabel('Destroyed,       Minor,       None,       Substantial')
    plt.show()

    observed_dsm.plot.bar(rot=0)
    plt.title(f'Histplot of M/S/D categories of {target} vs {feature} category')
    plt.xlabel('Destroyed,       Minor,       Substantial')
    plt.show()
    
# Defining a function to automate categorical testing
def get_chi2(df, feature, target='damage_level'):
    """
    This function will
    - accept a dataframe with at least two categorical variables: feature and target(default 'damage_level')
    - run a chi2 on a crosstab of the target vs the feature
    - return chi2 results: chi2, p, degf, expected
    """
    # make crosstab
    observed = pd.crosstab(df[target], df[feature])
    
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print('---- Observed Crosstab ----')
    display(observed)
    print('---- Expected Crosstab from chi2 test ----')
    display(pd.DataFrame(expected, index=observed.index, columns=observed.columns).round().astype(int))
    print(f'chi2 = {chi2},  p = {p},  degf = {degf}')
    
    return