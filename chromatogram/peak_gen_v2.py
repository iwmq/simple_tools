"""
A simple script to generate chromatograph for learning signal processing.

This is refactor of peak_gen.py
"""
from typing import NoReturn

import numpy as np
import matplotlib.pyplot as plt


# Number of data points
POINT_NUMBER = 5000
# Time interval between two adjacent points
POINT_INTERVAL = 0.02


def gen_resp() -> tuple[np.ndarray, np.ndarray]:
	# Retention time (RT)
	points = np.arange(POINT_NUMBER)
	rt = points * POINT_INTERVAL

	# Specify 7 peaks with various locations, widths, and heights
	peak_number = 7
	peak_indexes = np.array([300, 500, 900, 1400, 2300, 3100, 4000])
	peak_widths = np.array([0.3, 0.6, 0.8, 0.5, 0.8, 0.7, 0.9])
	peak_heights = np.array([11.5, 31.7, 21.4, 11.2, 21.1, 12.3, 15.4])

	# Generate a linear baseline
	resp = np.fromfunction(lambda i: i * 0.0005 + 0.15, (POINT_NUMBER,))

	# Add each peak in the baseline
	for i in range(peak_number):
		peak_index = peak_indexes[i] * POINT_INTERVAL
		peak_width = peak_widths[i]
		peak_height = peak_heights[i]

		# Peaks are Gaussian 
		resp += peak_height / (peak_width*np.sqrt(2*np.pi))*np.exp(-(rt-peak_index)**2/(2*peak_width**2))

	return rt, resp


def save_peek_data(rt: np.ndarray, resp: np.ndarray) -> NoReturn:
	# Put retetion time (RT) and response together, then save the mergered data in the text file
	data_gen = np.hstack((rt.reshape(POINT_NUMBER, 1), resp.reshape(POINT_NUMBER, 1)))
	data_file = open('results/peak_data.txt', 'w')
	np.savetxt(data_file, data_gen, fmt='%1.2f', delimiter='\t', header='RT (min)\tResp')


def plot_chromatogram(rt: np.ndarray, resp: np.ndarray) -> NoReturn:
	# Plot the generated chromatography
	plt.figure(figsize=[18, 8])
	plt.plot(rt, resp, color='r', label="RI Response")
	plt.title("Chromatogram")
	plt.xlabel("Retention Time (Min)")
	plt.ylabel("Response (mV)")
	plt.legend(loc='upper right')
	ax = plt.gca()
	ax.axhline(0, color='k')
	plt.savefig("results/chromatogram.png")


def main() -> NoReturn:
	rt, resp = gen_resp()
	save_peek_data(rt, resp)
	plot_chromatogram(rt, resp)


if __name__ == "__main__":
	main()