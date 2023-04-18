import pandas as pd
import numpy as np
from collections import defaultdict

def read_data(filepath):
    df = pd.read_excel(filepath)

    #standardize x/m count - upper to lowercase
    df = df.replace('X', 'x')
    df = df.replace('M', 'm')

    #get count of Xs and Ms
    cols = df.columns
    count_x_dict = {c: df.loc[:, c].value_counts()['x'] if 'x' in df.loc[:, c].value_counts() else 0 for c in cols}
    count_m_dict = {c: df.loc[:, c].value_counts()['m'] if 'm' in df.loc[:, c].value_counts() else 0 for c in cols}

    #replace x by 10, for plotting
    df = df.replace('x', '10')
    df = df.replace('m', '0')

    #cast dataframe to integer
    df = df.astype(int)

    #get average of group of 6 arrows
    round_scores_to_df = defaultdict(lambda: [])
    for c in cols:
        vals = df.loc[:, c]
        round_scores_to_df['date'].append(c)
        for i in range(12): 
            round_scores_to_df[i+1].append(np.mean(vals[i: i + 6]))
    round_scores_df = pd.DataFrame.from_dict(round_scores_to_df).melt(id_vars=['date'], var_name='ronda', value_name='promedio')
    round_scores_avg = round_scores_df[['ronda', 'promedio']].groupby(['ronda']).mean().reset_index()

    #get scores by date, long format
    scores_long = df.melt(var_name='date', value_name='puntaje')
    scores_avg = scores_long.groupby(['date']).mean().reset_index().rename(columns={'puntaje':'promedio'})
    scores_total = scores_long.groupby(['date']).sum().reset_index()
    scores_all = scores_avg.merge(scores_total)
    
    #merge Xs and Ms
    x_m_df = pd.DataFrame.from_dict([{"date": key, "x": val, "m": count_m_dict.get(key)} for key, val in count_x_dict.items()])
    
    return {
        'scores_long': scores_long,
        'scores_agg': scores_all,
        'round_scores_df': round_scores_df,
        'round_scores_avg': round_scores_avg,
        'x_m_df': x_m_df,
    }