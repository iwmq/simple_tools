"""
A simple script to generate chromatograph for learning signal processing.

This is second refactor of peak_gen.py. The data is generated randomly.
"""
import random
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

	# Randomly choose number of peaks between 5 and 10
	peak_number = random.randint(5, 10)
	# Randomly choose peak index, width, and height
	peak_indexes = np.random.randint(100, 4500, size=peak_number)
	peak_indexes.sort()
	peak_widths = np.random.uniform(0.3, 1.0, size=peak_number)
	peak_heights = np.random.uniform(10.0, 100.0, size=peak_number)

	# Generate a linear baseline
	resp = np.fromfunction(lambda i: i * 0.0005 + 0.15, (POINT_NUMBER,))

	# Add each peak in the baseline
	for i in range(peak_number):
		peak_index = peak_indexes[i] * POINT_INTERVAL
		peak_width = peak_widths[i]
		peak_height = peak_heights[i]

		# Peaks are Gaussian
		peak_shape = np.exp(-(rt-peak_index)**2 / (2*peak_width**2)) / np.sqrt(2 * np.pi)
		peak_resp = peak_shape * peak_height / peak_width
		resp += peak_resp

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