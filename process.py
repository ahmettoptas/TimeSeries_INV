import pickle
import pandas as pd
import stumpy
import numpy as np



steam_df = pd.read_csv("KGE_TAP_v2.csv")
copy_df_1 = steam_df.fillna(axis=0, method="ffill")
copy_df_2 = steam_df.fillna(axis=0, method="bfill")
temp = (copy_df_1.iloc[:, 1:] + copy_df_2.iloc[:, 1:]) / 2
shiftedDf = temp.shift(-1)
differenceDf = shiftedDf.iloc[:-1, :] - temp.iloc[:-1, :]
differenceDf.radiation_value = temp.radiation_value.iloc[:-1]
differenceDf.drop(['ekk_TAP', 'radiation_value'], axis=1, inplace=True)

m = 48
mps__ = {}  # Store the 1-dimensional matrix profiles
motifs_idx_anomaly = {}
for dim_name in differenceDf.columns:
    mps__[dim_name] = stumpy.stump(differenceDf[dim_name], m)
    motifs_idx_anomaly[dim_name] = np.argsort(mps__[dim_name][:, 0])[::-1]


def save_obj(obj, name ):
    with open(name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


f = open("processData.txt","w+")
f.write(str(m))
save_obj(mps__,"mps__")
save_obj(motifs_idx_anomaly,"motifs_idx_anomaly")
differenceDf.to_csv("differenceDf.csv",index=False)


