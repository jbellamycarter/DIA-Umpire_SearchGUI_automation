DIA Umpire Automation Script
============================

Copy this folder structure to use the `dia_umpire_automation.py` script.

# 1. Update Executables locations
Before running the script, ensure that the locations of the required exectuables
are up to date and correct. Update these in `dia_umpire_automation.py` itself.

Defaults are as follows:

`java_exec = r"C:\DIA_Umpire_Automation\java11\jre\bin\java.exe"`

`dia_umpire_se = r"C:\DIA_Umpire_Automation\DIA_Umpire_SE-2.2.8.jar"`

`search_gui = r"C:\DIA_Umpire_Automation\SearchGUI\SearchGUI-4.2.17\SearchGUI-4.2.17.jar"`

`peptide_shaker = r"C:\DIA_Umpire_Automation\PeptideShaker\PeptideShaker-2.2.25\PeptideShaker-2.2.25.jar"`

`thermo_file_parser = r"C:\DIA_Umpire_Automation\SearchGUI\SearchGUI-4.2.17\resources\ThermoRawFileParser\ThermoRawFileParser.exe"`

# 2. Update parameter files
There are three parameters files which are required for successful operation:

|  |  |
| --- | --- |
| FASTA Database | `database.fasta` |
| DIA Umpire SE parameters | `umpire-se.params` |
| SearchGUI parameters | `search.par` |

# 3. Copy RAW data into ./raw/ folder
If no raw data files are provided, the script will terminate.
If Thermo RAW data files are provided, the script will automatically try to convert these to .mzML.

# 4. Run the script
The script should run with any version of Python 3, using only default libraries.
If your python distribution is found at the command prompt level, you only need to do the following:

(Windows specific commands, adjust for *nix)
1. Open the working folder in your file explorer
2. Press `Alt+D`, which will select the address bar in edit mode
3. Type '`cmd`' and press Enter
4. Simply type '`dia_umpire_automation.py`' and hit Enter; the script will now run.

If python is not recognised at the command prompt level, then you will need to specify the location of your python executable.