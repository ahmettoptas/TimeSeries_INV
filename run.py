import pickle

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

f = open("processData.txt","r")
m = int(f.readline())

mps__ = load_obj("mps__")
motifs_idx_anomaly = load_obj("motifs_idx_anomaly")
differenceDf = pd.read_csv("differenceDf.csv")


st.markdown("<h1 style='text-align: center; color: blue;'>Discords(Anomalies) in The INV Time Series</h1>",
            unsafe_allow_html=True)

fig, axs = plt.subplots(len(mps__), sharex=True, gridspec_kw={'hspace': 0}, figsize=(50, 50))

for i, dim_name in enumerate(list(mps__.keys())):
    axs[i].set_ylabel(dim_name, fontsize='20')
    axs[i].plot(differenceDf[dim_name])
    axs[i].set_xlabel('Time', fontsize='20')
    for index, idx in enumerate(motifs_idx_anomaly[dim_name]):
        if index == 4:
            break
        axs[i].plot(differenceDf[dim_name].iloc[idx:idx + m], c='red', linewidth=4)
        axs[i].axvline(x=idx, linestyle="dashed", c='black', linewidth=1)

st.pyplot(fig)