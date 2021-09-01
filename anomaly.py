import streamlit as st
import pandas as pd
import stumpy
import numpy as np
import matplotlib.pyplot as plt


steam_df = pd.read_csv("KGE_TAP_v2.csv")
copy_df_1 = steam_df.fillna(axis = 0, method = "ffill")
copy_df_2= steam_df.fillna(axis = 0, method = "bfill")
temp = (copy_df_1.iloc[:,1:] + copy_df_2.iloc[:,1:]) / 2
shiftedDf = temp.shift(-1)
differenceDf = shiftedDf.iloc[:-1,:] - temp.iloc[:-1,:]
differenceDf.radiation_value = temp.radiation_value.iloc[:-1]
differenceDf.drop(['ekk_TAP', 'radiation_value'], axis=1, inplace = True)

m = 48
mps__ = {}  # Store the 1-dimensional matrix profiles
motifs_idx_anomaly = {}
for dim_name in differenceDf.columns:
    mps__[dim_name] = stumpy.stump(differenceDf[dim_name], m)
    motifs_idx_anomaly[dim_name] = np.argsort(mps__[dim_name][:, 0])[::-1]
    
st.markdown("<h1 style='text-align: center; color: blue;'>Discords(Anomalies) in The INV Time Series</h1>", unsafe_allow_html=True)    

fig, axs = plt.subplots(len(mps__), sharex=True, gridspec_kw={'hspace': 0},figsize=(50,50))

for i, dim_name in enumerate(list(mps__.keys())):
    axs[i].set_ylabel(dim_name, fontsize='20')
    axs[i].plot(differenceDf[dim_name])
    axs[i].set_xlabel('Time', fontsize ='20')
    for index,idx in enumerate(motifs_idx_anomaly[dim_name]):
        if index == 4:
            break
        axs[i].plot(differenceDf[dim_name].iloc[idx:idx+m], c='red', linewidth=4)
        axs[i].axvline(x=idx, linestyle="dashed", c='black',linewidth=1)

st.pyplot(fig)
