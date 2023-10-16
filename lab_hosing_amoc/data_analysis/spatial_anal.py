#!/usr/bin/env python

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
plt.style.use("ggplot")

# Define the scenarios and freshwater hosing values
scenarios = [
    ("2e1", 1),
    ("2e2", 2),
    ("2e3", 3),
    ("2e4", 4),
    ("2e5", 5),
    ("2e6", 6),
    ("2e7", 7),
    ("2e8", 8),
    ("2e9", 9),
    ("2e10", 10),
    ("2e11", 11),
    ("2e12", 12),
    ("2e13", 13),
    ("2e14", 14),
    ("2e15", 15),
    ("2e16", 16),
    ("2e17", 17)
]

# Open the control dataset
control_ds = xr.open_dataset("../control/fields_biogem_2d.nc")
stream_control = control_ds["phys_opsia"].mean(dim="time")

# Set color levels
colorbar_levels = np.arange(-7, 7)

for scenario, hosing in scenarios:
    ds = xr.open_dataset(f"../{scenario}/fields_biogem_2d.nc")
    amoc_anom = ds["phys_opsia"].mean(dim="time") - stream_control
    
    # Create the plot
    plt.fill_between(amoc_anom["lat_moc"], amoc_anom["zt_moc"].min(), amoc_anom["zt_moc"].max(), color='#695447')
    contour_filled = plt.contourf(amoc_anom["lat_moc"], amoc_anom["zt_moc"], amoc_anom, levels=colorbar_levels, cmap="RdBu_r")
    contour_lines = plt.contour(amoc_anom["lat_moc"], amoc_anom["zt_moc"], amoc_anom, levels=colorbar_levels, colors='k', linewidths=0.5)

    plt.xlabel("Latitude [°]")
    plt.ylabel("Depth [m]")
    cbar = plt.colorbar(contour_filled)
    cbar.set_label("Anomaly [Sv]")
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.1f')
    plt.gca().invert_yaxis()
    
    plt.title(f"AMOC $Ψ$ anomaly under {scenario} $Sv$ freshwater hosing")
    
    # Save the plot
    plt.savefig(f"../figs/amoc_{scenario}.png", dpi=300)
    plt.clf()  # Clear the current plot for the next iteration
