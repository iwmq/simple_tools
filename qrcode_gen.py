"""
Generate QR code for a URL (Mostly completed by Copilot on zed editor).

Args:
    url: The URL to encode in the QR code
    output_path: Optional output file path. If None, uses url-based filename
    size: Size of each box in the QR code (default: 10)
    border: Border size in boxes (default: 4)

Returns:
    Path to the generated QR code image
"""
import argparse
from pathlib import Path
from typing import Optional

import qrcode


def generate_qr_code(
    url: str, output_path: Optional[str] = None, size: int = 10, border: int = 4
) -> Path:
    """
    Generate a QR code for the given URL.

    Args:
        url: The URL to encode in the QR code
        output_path: Optional output file path. If None, uses url-based filename
        size: Size of each box in the QR code (default: 10)
        border: Border size in boxes (default: 4)

    Returns:
        Path to the generated QR code image
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Determine output path
    if output_path is None:
        # Create filename from URL
        safe_filename = url.replace("://", "_").replace("/", "_").replace("?", "_")
        safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in "_-.")
        output_path = f"qr_{safe_filename}.png"

    output_file = Path(output_path)

    # Save the image
    with open(output_file, "wb") as f:
        img.save(f, "PNG")

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Generate QR code for a URL")
    parser.add_argument("url", help="URL to encode in QR code")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=10,
        help="Size of each box in QR code (default: 10)",
    )
    parser.add_argument(
        "-b", "--border", type=int, default=4, help="Border size in boxes (default: 4)"
    )

    args = parser.parse_args()

    try:
        output_file = generate_qr_code(
            url=args.url, output_path=args.output, size=args.size, border=args.border
        )
        print(f"QR code generated successfully: {output_file.absolute()}")

    except Exception as e:
        print(f"Error generating QR code: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
