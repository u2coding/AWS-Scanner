# ACK-Scanner

ACK-Scanner (Automated Censys Knowledge Scanner) is a purely educational and test tool designed to scan for various configuration files and sensitive information on web servers. It can perform searches using the Censys API or scan a list of IPs provided in a text file.

## Features

- Search for configuration files and sensitive information on web servers.
- Perform new searches using the Censys API.
- Scan existing lists of IPs from a text file.
- Save results to a specified folder (by default the 'results' folder).

## Requirements

- Python 3.x
- `requests` library
- `urllib3` library
- `curses` library (included in the Python standard library)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/HackerKnownAsAICG/AWS-Scanner.git
   cd ack-scanner
   ```
   
   OR download the [.zip file](https://github.com/HackerKnownAsAICG/AWS-Scanner/archive/refs/heads/master.zip).

2. Create a virtual environment and install dependencies:

   ### On Windows:

   ```sh
   setup.bat
   ```

   ### On Unix-based systems:

   ```sh
   chmod +x setup.sh
   ./setup.sh
   ```

## Usage

1. Run the tool via ``setup.bat`` or ``setup.sh`` depending on your system.

2. Choose an option:

   - **1. New Censys search & scan**: Enter your Censys API ID, API Secret, and search query to perform a new search.
   - **2. Scan existing list of IPs**: Enter the filename (ending in `.txt`) containing the list of IPs to scan.

3. The tool will scan the specified IPs and save the results in the `results` folder.

## Example

To perform a new Censys search and scan:

1. Run the tool via ``setup.bat`` or ``setup.sh`` depending on your system.

2. Choose option `1` and enter your Censys API credentials and search query.

3. The tool will fetch data from Censys, save the IPs to `ips.json` and `ips.txt`, and start scanning the IPs. Found AWS credentials will be saved to results/aws_keys.txt in a format suitable for testing via [Kingbased's Keychecker](https://github.com/kingbased/keychecker/) (accesskey:secretkey).

To scan an existing list of IPs:

1. Run the tool via setup.bat or setup.sh depending on your system.

2. Choose option `2` and enter the filename (e.g., `ips.txt`).

3. The tool will start scanning the IPs listed in the specified file and print to the 'results' folder. Found AWS credentials will be saved to results/aws_keys.txt in a format suitable for testing via [Kingbased's Keychecker](https://github.com/kingbased/keychecker/) (accesskey:secretkey).

## Disclaimer

This tool is intended for educational and testing purposes only. Use it responsibly and only on systems you have permission to scan. The author is not responsible for any misuse of this tool.

## License

This project is licensed under the MIT License. 

## Credit
This project was created and distributed by the kind, intelligent souls at [g/aicg/ - AI Chatbot General](https://boards.4chan.org/g/catalog#s=aicg)

---
