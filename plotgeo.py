import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv('/Users/adamk/Downloads/IEDcoordinates.csv') # Coordinates data

df.head()

BBox = (68.5, 70, 33.98, 35.2) # Boundary for Afghanistan
#BBox = (68.552, 70.0000, 33.854, 35.1000) # Boundary for Afghanistan

lat = []
lon = []

for row in df['longitude']:
    try:
        lon.append(row)
    except:
        # append a missing value to lon
        lon.append(np.NaN)

for row in df['latitude']:
        # Split the row by comma and append
        # everything after the comma to lat
    try:
        lat.append(row)
    # If error
    except:
        lat.append(np.NaN)
#Create new lat/lon arrays for reduced, focused dataset
lon_new = []
lat_new = []
i=0
j=0
for i, j in zip(lon,lat):
    if (((i > BBox[0]) & (i < BBox[1])) & ((j > BBox[2]) & (j < BBox[3]))):
        lon_new.append(i)
        lat_new.append(j)
        i+=1
        j+=1

map_img = mpimg.imread('/Users/adamk/Downloads/map-3.png') # Background map image
fig, bx = plt.subplots(figsize = (8,7))
bx.set_title('Afghanistan IED Discrete Density Map (2014)')
bx.set_xlim(BBox[0], BBox[1])
bx.set_ylim(BBox[2], BBox[3])
ax = sns.kdeplot(lon_new, lat_new, cmap="magma_r", shade=False, bw=0.11, kernel='gau')
bins = plt.hexbin(lon_new, lat_new, gridsize=20, cmap='Blues')
cb = plt.colorbar(label='count in bin')
bin_xy = bins.get_offsets()
bin_counts = bins.get_array()
#print(bin_xy)
#print(bin_counts)
ax.collections[0].set_alpha(0)

fig, cx = plt.subplots(figsize = (8,7))
cx.set_title('Afghanistan IED Kernel Density Estimate Map (2008)')
cx.set_xlim(BBox[0], BBox[1])
cx.set_ylim(BBox[2], BBox[3])
cx.scatter(lon_new, lat_new, zorder=1, alpha = 0.2, c='b', s = 10)
plt.imshow(map_img, zorder=0, extent=[BBox[0], BBox[1], BBox[2], BBox[3]])
ax = sns.kdeplot(lon_new, lat_new, cmap="magma_r", shade=False, bw=0.11, kernel='gau')
plt.show()
