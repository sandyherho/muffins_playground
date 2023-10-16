#!/usr/bin/env python

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import seaborn as sns
plt.style.use("ggplot")

# Data file paths
data_paths = ["../control/fields_biogem_2d.nc", "../2e1/fields_biogem_2d.nc", "../2e2/fields_biogem_2d.nc", "../2e3/fields_biogem_2d.nc", "../2e4/fields_biogem_2d.nc",
              "../2e5/fields_biogem_2d.nc", "../2e6/fields_biogem_2d.nc", "../2e7/fields_biogem_2d.nc", "../2e8/fields_biogem_2d.nc", "../2e9/fields_biogem_2d.nc",
              "../2e10/fields_biogem_2d.nc", "../2e11/fields_biogem_2d.nc", "../2e12/fields_biogem_2d.nc", "../2e13/fields_biogem_2d.nc", "../2e14/fields_biogem_2d.nc",
              "../2e15/fields_biogem_2d.nc", "../2e16/fields_biogem_2d.nc", "../2e17/fields_biogem_2d.nc"]

# Load control data and calculate means
ds_control = xr.open_dataset(data_paths[0])
control_data = ds_control["phys_opsia"].mean(dim="time").to_numpy().flatten()

# Load data and calculate means for other conditions
data_means = {"Control": control_data}
for i, path in enumerate(data_paths[1:]):
    ds = xr.open_dataset(path)
    amoc = ds["phys_opsia"].mean(dim="time")
    data_means[f"2E{i+1}"] = amoc.to_numpy().flatten()

# Create a DataFrame
df = pd.DataFrame(data_means)

# Perform Mann-Whitney U tests
p_values = {}
for column in df.columns[1:]:
    u_statistic, p_value = mannwhitneyu(control_data, df[column], alternative='two-sided')
    p_values[column] = (round(u_statistic, 3), round(p_value, 3))

# Create a box plot
colors = {column: "#d11727" for column in df.columns[1:]}
colors["Control"] = "#048191"

fig, ax = plt.subplots(figsize=(20, 10))
bx = sns.boxplot(data=df, palette=colors)
ax.set_xlabel("Atlantic Streamfunction [Sv]", size=20)
ax.set_ylabel("Freshwater hosing [Sv]", size=20)
plt.savefig("../figs/amoc_dist.png", dpi=300)
