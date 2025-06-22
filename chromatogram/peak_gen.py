"""
A simple script to generate chromatograph for learning signal processing.

This is a very simple and stupid script writen in 2019. I was not good at
programming in Python. The file is useless, but I would like to keep it here
to remember what my skill looked like before making live as a programmer.

Nothing modified except this docstr.
"""
import numpy as np
import matplotlib.pyplot as plt

# Specify the total data points and time interval between two adjacent points
point_number = 5000
point_interval = 0.02

# Retention time (RT)
points = np.arange(point_number)
rt = points * point_interval

# Specify 7 peaks with various locations, widths, and heights
peak_number = 7
peak_indexes = np.array([300, 500, 900, 1400, 2300, 3100, 4000])
peak_widths = np.array([0.3, 0.6, 0.8, 0.5, 0.8, 0.7, 0.9])
peak_heights = np.array([11.5, 31.7, 21.4, 11.2, 21.1, 12.3, 15.4])

# Generate a linear baseline
resp = np.fromfunction(lambda i:i*0.0005+0.15, (point_number,))

# Add each peak in the baseline
for i in range(peak_number):
	peak_index = peak_indexes[i]*point_interval
	peak_width = peak_widths[i]
	peak_height = peak_heights[i]

	# Peaks are Gaussian 
	resp += peak_height/(peak_width*np.sqrt(2*np.pi))*np.exp(-(rt-peak_index)**2/(2*peak_width**2))

# Put retetion time (RT) and response together, then save the mergered data in the text file
data_gen = np.hstack((rt.reshape(point_number, 1), resp.reshape(point_number, 1)))
data_file = open('peak_data.txt', 'w')
np.savetxt(data_file, data_gen, fmt='%1.2f', delimiter='\t', header='RT (min)\tResp')

# Plot the generated chromatography
plt.figure(figsize=[18, 8])
plt.plot(rt, resp, color='r', label="RI Response")
plt.title("Chromatogram")
plt.xlabel("Retention Time (Min)")
plt.ylabel("Response (mV)")
plt.legend(loc='upper right')
ax = plt.gca()
ax.axhline(0, color='k')
# plt.show()
plt.savefig("chromatogram.png")