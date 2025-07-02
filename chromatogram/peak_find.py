import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp, find_peaks, peak_widths, peak_prominences, find_peaks_cwt


def draw_peaks(data_file: str) -> None:
	# Load data
	data_file = "results/doge.txt"
	data_array = np.loadtxt(data_file, delimiter="\t", skiprows=1)
	rt = data_array[:, 0]
	ri_resp = data_array[:,1]

	peaks, peak_properties = find_peaks(ri_resp, height=0.1, width=10, distance=10)

	plt.figure(figsize=[18, 8])
	plt.title("Chromatogram")
	plt.xlabel("Retention Time (Min)")
	plt.ylabel("Response (mV)")
	plt.legend(loc='upper right')

	# Draw response
	plt.plot(rt, ri_resp, color='r', label="RI Response")

	# Mark peaks
	plt.plot(rt[peaks], ri_resp[peaks], 'x')
	plt.show()


def main():
	argparser = argparse.ArgumentParser(description="Draw peaks from chromatogram data.")
	argparser.add_argument('file', help="Path to the data file")
	args = argparser.parse_args()
	if not os.path.exists(args.file):
		print(f"File {args.file} does not exist.")
		return
	draw_peaks(args.file)


if __name__ == "__main__":
	main()