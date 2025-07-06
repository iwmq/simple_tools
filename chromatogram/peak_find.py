from argparse import ArgumentParser, Namespace
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapezoid
from scipy.signal import chirp, find_peaks, peak_widths, peak_prominences, find_peaks_cwt


def draw_peaks(data_file: str) -> None:
	# Load data
	data_array = np.loadtxt(data_file, delimiter="\t", skiprows=1)
	rt = data_array[:, 0]
	ri_resp = data_array[:,1]

	peaks, peak_properties = find_peaks(ri_resp, height=0.1, width=10, distance=10)
	prominences, left_bases, right_bases = peak_prominences(ri_resp, peaks)


	plt.figure(figsize=[18, 8])
	plt.title("Chromatogram")
	plt.xlabel("Retention Time (Min)")
	plt.ylabel("Response (mV)")

	# Draw response
	ax = plt.gca()
	ax.plot(rt, ri_resp, color='r', label="RI Response")
	ax.legend(loc='upper right')

	# Calculate peak area for each peak
	# The method is naive
	for i, p in enumerate(peaks):
		left_base = left_bases[i]
		right_base = right_bases[i]
		left_base_value = ri_resp[left_base]
		right_base_value = ri_resp[right_base]
		baseline = np.linspace(left_base_value, right_base_value, right_base - left_base + 1)
		peak_value = ri_resp[left_base:right_base + 1]
		peak_area = trapezoid(peak_value - baseline)
		text = f"Area: {peak_area:.2f}, height: {prominences[i]:.2f}"
		plt.text(rt[p], ri_resp[p] + 1, text, fontsize=12, ha='center')

	# Mark peaks
	plt.plot(rt[peaks], ri_resp[peaks], 'x')
	plt.show()


def main():
	argparser = ArgumentParser(description="Draw peaks from chromatogram data.")
	argparser.add_argument('file', help="Path to the data file")
	args: Namespace = argparser.parse_args()
	if not os.path.exists(args.file):
		print(f"File {args.file} does not exist.")
		return
	draw_peaks(args.file)


if __name__ == "__main__":
	main()