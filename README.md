# DIA-Umpire_SearchGUI_automation
![GitHub License](https://img.shields.io/github/license/jbellamycarter/DIA-Umpire_SearchGUI_automation)
![GitHub Release](https://img.shields.io/github/v/release/jbellamycarter/DIA-Umpire_SearchGUI_automation)
![GitHub Tag](https://img.shields.io/github/v/tag/jbellamycarter/DIA-Umpire_SearchGUI_automation)


Scripts for automated processing of Data Independent Acquisition (DIA) preotomics data with [DIA-Umpire](https://github.com/Nesvilab/DIA-Umpire) followed by [SearchGUI](http://compomics.github.io/projects/searchgui). 

## Purpose
This script is designed to automate processing of some DIA data. This has been benchmarked for all-ion fragmentation (AIF) DIA data collected on a Thermo Exactive mass spectrometer. Pseudo-MS2 scans are used to generate the fragment ions for all precursors within a liquid chromatography (LC) peak. Most open-source search engines for proteomics expect data dependent acquisition (DDA) data or DIA with narrow-band isolation windows. Therefore this script first converts the original mass spectrometry data into pseudo-DDA data using [DIA-Umpire](https://github.com/Nesvilab/DIA-Umpire). These data are then searched with open-source engines available within [SearchGUI/CLI](http://compomics.github.io/projects/searchgui) (such as X!Tandem), and peptide identifications and protein inference prepared by [PeptideShaker](http://compomics.github.io/projects/peptide-shaker).

## How to use
Within this repository, the `template/` folder contains a defaut version of the `dia_umpire_automation.py` script along with three parameters file: a FASTA database, DIA Umpire SE parameters and SearchGUI parameters.

1. Copy the `template/` folder to a sensible place.
2. Copy your raw data into the `/raw/` folder. If your data are Thermo .RAW files, the script will use ThermoFileParser to convert the data into `.mzML` files.
3. Update the parameters in `dia_umpire_automation.py` and the other parameter files for your search.
4. Run the script.

## Requirements
* Java 11
* Python >3.7
* DIA Umpire SE module (tested with version 2.2.8)
* SearchGUI (tested with version 4.2.17)
* PeptideShaker (tested with version 2.2.25)
* ThermoRawFileParser (shipped with SearchGUI)

## References
### DIA-Umpire
* https://github.com/Nesvilab/DIA-Umpire
* https://diaumpire.nesvilab.org/DIA_Umpire_Manual_v2.0.pdf
* https://www.nature.com/articles/nmeth.3255

### SearchGUI
* http://compomics.github.io/projects/searchgui
* http://compomics.github.io/projects/searchgui/wiki/SearchCLI
* https://pubs.acs.org/doi/10.1021/acs.jproteome.8b00175

### PeptideShaker
* http://compomics.github.io/projects/peptide-shaker

### ThermoFileParser
* http://compomics.github.io/projects/ThermoRawFileParser
* https://pubs.acs.org/doi/10.1021/acs.jproteome.9b00328
