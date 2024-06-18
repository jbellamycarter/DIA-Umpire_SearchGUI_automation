#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# (c) 2023 Jedd Bellamy-Carter
# MIT License

"""
Script to run DIA Umpire Signal Extraction on raw .mzML files,
followed by clean up of unneeded files.

Assumes the following files structure:

./                      - top-level directory that this script is run from
    raw/                - all raw.mzML files are stored in this subdirectory
    processed/          - all resulting pseudo-DDA files will be placed in here
    searched/           - all outputs from SearchCLI will be stored here

    umpire-se.params    - parameter file for DIA Umpire, must be provided.
    search.par          - search gui parameters
    database.fasta      - target-decoy database
"""

import os
import subprocess
import fnmatch
import sys
import time
import logging

__version__ = "1.0.3"

#----------------------------------------#
# 0. Set up folder structure and logging #
#----------------------------------------#

top_dir = os.getcwd()
log_file = os.path.join(top_dir, "dia_umpire_automation.log")
if os.path.exists(log_file):
    os.remove(log_file)
logging.basicConfig(level = logging.INFO, format = "%(levelname)-8s %(message)s",
                    handlers = [logging.FileHandler(log_file),
                                logging.StreamHandler()])
script_start_time = time.time()
logging.info("Script started {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(script_start_time))))
logging.info(f"Top directory is {top_dir}")

logging.info("Setting up working directory")

raw_dir = os.path.join(top_dir, "raw")
if not os.path.isdir(raw_dir):
    logging.error("./raw folder for raw data not found, please make one and provide data!")
    sys.exit()

proc_dir = os.path.join(top_dir, "processed")
if not os.path.isdir(proc_dir):
    os.mkdir(proc_dir)

search_dir = os.path.join(top_dir, "searched")
if not os.path.isdir(search_dir):
    os.mkdir(search_dir)

# Executables, update to actual location, use absolute path.
java_exec = r"C:\Users\cmjb5\Apps\FragPipe\fragpipe\jre\bin\java.exe"
dia_umpire_se = r"C:\Users\cmjb5\Apps\DIA_Umpire\DIA_Umpire_SE-2.2.8.jar"
search_gui = r"C:\Users\cmjb5\Apps\SearchGUI\SearchGUI-4.2.17\SearchGUI-4.2.17.jar"
peptide_shaker = r"C:\Users\cmjb5\Apps\PeptideShaker\PeptideShaker-2.2.25\PeptideShaker-2.2.25.jar"
thermo_file_parser = r"C:\Users\cmjb5\Apps\SearchGUI\SearchGUI-4.2.17\resources\ThermoRawFileParser\ThermoRawFileParser.exe"

## Check if all executables exist
if os.path.exists(java_exec):
    logging.info(f"Java exectuable found at {java_exec}")
else:
    logging.error("Java executable not found, please provide a correct location")
    sys.exit()

if os.path.exists(dia_umpire_se):
    logging.info(f"DIA Umpire SE exectuable found at {dia_umpire_se}")
else:
    logging.error("DIA Umpire SE not found, please provide a correct location")
    sys.exit()

if os.path.exists(search_gui):
    logging.info(f"SearchGUI exectuable found at {search_gui}")
else:
    logging.error("SearchGUI not found, please provide a correct location")
    sys.exit()

if os.path.exists(peptide_shaker):
    logging.info(f"PeptideShaker exectuable found at {peptide_shaker}")
else:
    logging.error("SearchGUI not found, please provide a correct location")
    sys.exit()

if os.path.exists(thermo_file_parser):
    logging.info(f"Thermo File Parser exectuable found at {thermo_file_parser}")
else:
    logging.warning("Thermo File Parser not found, will only process .mzML files")

# Parameter files, change the default names for these here:
_dia_umpire_params = "umpire-se.params"
_search_params = "search.par"
_database = "database.fasta"

## Check if parameter files exist
dia_umpire_params = os.path.join(top_dir, _dia_umpire_params)
if os.path.exists(dia_umpire_params):
    logging.info(f"Found parameter file '{_dia_umpire_params}' for DIA-Umpire Signal Extraction")
else:
    logging.error(f"'{_dia_umpire_params}' not found, please put in top-level folder")
    sys.exit()

search_params = os.path.join(top_dir, _search_params)
if os.path.exists(search_params):
    logging.info(f"Found parameter file '{_search_params}' for SearchGUI CLI Database Search")
else:
    logging.error(f"'{_search_params}' not found, please put in top-level folder")
    sys.exit()

database = os.path.join(top_dir, _database)
if os.path.exists(database):
    logging.info(f"Found FASTA Database file '{_database}' for SearchGUI CLI Database Search")
else:
    logging.error(f"'{_database}' not found, please put in top-level folder")
    sys.exit()


print("Please give this data a reference name:")
ref_name = str(input())
if ref_name == "":
    ref_name = os.path.basename(top_dir)

logging.info(f"Reference name will be '{ref_name}'")

#----------------------------------------#
# 1. Check and convert raw files in /raw #
#----------------------------------------#

raw_files = []
thermo_raw_files = []
if os.path.isdir(raw_dir):
    fnames = os.listdir(raw_dir)
    for f in fnames:
        if f.endswith(".mzML"):
            raw_files.append(f)
        elif f.endswith(".raw"):
            thermo_raw_files.append(f)
        else:
            continue
else:
    logging.error("No directory called ./raw, please create one.")
    sys.exit()

raw_file_base = [f[:-5] for f in raw_files]
needs_converting = []
for thermo_raw in thermo_raw_files:
    if thermo_raw[:-4] not in raw_file_base:
        needs_converting.append(thermo_raw)

if len(needs_converting) > 0 and os.path.exists(thermo_file_parser):
    logging.info("There are {} Thermo RAW files that need converting to .mzML, will try this now.".format(len(needs_converting)))
    convert_start_time = time.time()
    for thermo_raw in needs_converting:
        raw_file = thermo_raw[:-4] + ".mzML"
        # Call Thermo File Parser and convert with default settings
        logging.info(f"Converting {thermo_raw} with Thermo File Parser")
        return_code = subprocess.call([thermo_file_parser,
                                      "-i", os.path.join(raw_dir, thermo_raw),
                                      "-b", os.path.join(raw_dir, raw_file)],
                                      universal_newlines=True)
        if return_code == 0:
            logging.info(f"Successfully converted to {raw_file}")
            raw_files.append(raw_file)
    convert_end_time = time.time()
raw_file_count = len(raw_files)
if raw_file_count == 0:
    logging.warning("No raw .mzML files to process, exiting script now.")

#------------------------------------------#
# 2. Run DIA Umpire on all files in ./raw/ #
#------------------------------------------#

umpire_start_time = time.time()
logging.info("==========")
logging.info("{} files to process with DIA Umpire.".format(raw_file_count))
count = 0

bad_files = []
for raw_file in raw_files:
    count += 1
    logging.info("Processing {} ({}/{}) with DIA Umpire...".format(raw_file, count, raw_file_count))
    _proc_time = time.time()
    umpire_process = subprocess.run([java_exec, "-jar", "-Xmx8G", dia_umpire_se,
                                     os.path.join(raw_dir,raw_file), dia_umpire_params],
                                    capture_output=True, universal_newlines=True)
    os.replace("./raw/diaumpire_se.log", "./raw/{}_diaumpire.log".format(raw_file[:-5]))
    if not umpire_process.returncode == 0:
        logging.warning("Something went wrong, please check ./raw/{}_diaumpire.log".format(raw_file[:-5]))
        if count < raw_file_count:
            logging.info("Will try with remaining files.")
        bad_files.append(raw_file)
        continue
    else:
        logging.info("Processed in {} min:sec".format(time.strftime("%M:%S", time.gmtime(time.time()-_proc_time))))

if bad_files:
    for f in bad_files:
        raw_files.remove(f)

logging.info("{} files successfully processed with DIA Umpire.".format(len(raw_files)))

umpire_end_time = time.time()

#--------------------------------#
# 3a. Cleaning up unneeded files #
#--------------------------------#
logging.info("==========")
logging.info("Cleaning up unneeded files...")

unneeded_filetypes = (".DIAWindowsFS",
                      ".RTidxFS",
                      ".ScanClusterMapping_Q1",
                      ".ScanClusterMapping_Q2",
                      ".ScanClusterMapping_Q3",
                      ".ScanidxFS",
                      ".ScanPosFS",
                      ".ScanRTFS",
                      "_diasetting.ser",
                      "_params.ser")

logging.info("Removing files ending in {}".format(", ".join(unneeded_filetypes)))
current_files = os.listdir(raw_dir)

for f in current_files:
      if f.endswith(tuple(unneeded_filetypes)):
          os.remove(os.path.join(raw_dir, f))
      if f.endswith("_Peak"):
          peak_dir = os.path.join(raw_dir, f)
          if os.path.isdir(peak_dir):
              for _f in os.listdir(peak_dir):
                  os.remove(os.path.join(peak_dir, _f))
              os.rmdir(os.path.join(raw_dir, f))

#----------------------------------#
# 3b. Moving output files to /proc #
#----------------------------------#

ext_to_move = ["_Q1.mgf", "_Q2.mgf", "_Q3.mgf",
               "_Q1.mzML", "_Q2.mzML", "_Q3.mzML",
               "_PeakCluster.csv"]

raw_names = [x[:-5] for x in raw_files]
for raw_name in raw_names:
    logging.info(f"Moving files for sample {raw_name} to ./processed/...")
    for ext in ext_to_move:
        if os.path.exists(os.path.join(raw_dir, raw_name+ext)):
            os.replace(os.path.join(raw_dir, raw_name+ext), os.path.join(proc_dir, raw_name+ext))

#--------------------------------------#
# 4. Database searching with SearchGUI #
#--------------------------------------#

logging.info("==========")
logging.info("Running database search with SearchGUI CLI...")

search_start_time = time.time()

search_engine = "-xtandem"
logging.info(f"Using {search_engine} search engine")

# Make list of files to search
qt_dict = {'1': "_Q1.mgf", '2': "_Q2.mgf", '3':"_Q3.mgf",
           '12':"_Q1Q2_combined.mgf", '13':"_Q1Q3_combined.mgf", '23':"_Q2Q3_combined.mgf",
           '123':"_Q1Q2Q3_combined.mgf"}

# Select desired Quality Tiers (QT), make sure you enclose the number in quotes.
qt_to_search = ['1']
to_search = []

logging.info("Searching files:")
for raw_name in raw_names:
    for qt in qt_to_search:
        fname = os.path.join(proc_dir, raw_name+qt_dict[qt])
        if os.path.exists(fname):
            if os.path.getsize(fname) > 0:
                to_search.append(fname)
                logging.info("{}".format(raw_name+qt_dict[qt]))
            else:
                logging.info("{} is empty, will not be searched.".format(raw_name+qt_dict[qt]))
        elif qt in ['12', '13', '23', '123']:
            # Create concatenated .mgf files
            tiers = [i for i in qt]
            logging.info("Concatenating quality tiers {} for {}".format(", ".join(tiers), raw_name))
            for tier in tiers:
                _fname = os.path.join(proc_dir, raw_name+qt_dict[tier])
                if not os.path.exists(_fname):
                    logging.warning(f"{_fname} does not exist, cannot be concatenated. Please make sure the file exists.")
                    continue

            with open(fname, "w") as outfile:
                for tier in tiers:
                    with open(os.path.join(proc_dir, raw_name+qt_dict[tier]), "r") as infile:
                        outfile.write(infile.read())
            if os.path.getsize(fname) > 0:
                to_search.append(fname)
                logging.info("{}".format(raw_name+qt_dict[qt]))
            else:
                logging.info("{} is empty, will not be searched.".format(raw_name+qt_dict[qt]))

        else:
            logging.warning("{} will not be searched.".format(raw_name+qt_dict[qt]))

search_process = subprocess.run([java_exec, "-cp", search_gui, "eu.isas.searchgui.cmd.SearchCLI",
                               "-spectrum_files", ', '.join(to_search),
                               "-fasta_file", database,
                               "-output_folder", search_dir,
                               "-id_params", search_params,
                               search_engine, "1",
                               "-output_default_name", ref_name,
                               "-output_data", "1"],
                               capture_output=True,
                               universal_newlines=True)

search_end_time = time.time()
logging.info(f"Searches completed, results can be found in ./searched/{ref_name}.zip")

# Save log file of SearchCLI output
with open(os.path.join(search_dir, "search_cli.log"), "w") as outfile:
          outfile.write("Command line arguments\n")
          outfile.write("----------------------\n")
          outfile.write(" ".join(search_process.args))
          outfile.write("\n\nRun Log\n-------\n")
          outfile.write(search_process.stdout)
          outfile.write(search_process.stderr)

logging.info("Log of search can be found in ./searched/search_cli.log")

# Remove html file automatically generated by SearchGUI
for f in fnmatch.filter(os.listdir(search_dir), "SearchGUI*.html"):
    os.remove(os.path.join(search_dir, f))

#---------------------------------#
# 5. Prepare PeptideShaker Report #
#---------------------------------#
logging.info("==========")
logging.info("Preparing PeptideShaker file...")

shaker_start_time = time.time()
shaker_process = subprocess.run([java_exec, "-cp", peptide_shaker, "eu.isas.peptideshaker.cmd.PeptideShakerCLI",
                             "-reference", ref_name,
                             "-identification_files", os.path.join(search_dir, ref_name+".zip"),
                             #"-spectrum_files", ', '.join(to_search),
                             #"-fasta_file", database,
                             #"-id_params", search_params,
                             "-out", os.path.join(search_dir, ref_name+".psdb")],
                             capture_output=True,
                             universal_newlines=True)
shaker_end_time = time.time()

logging.info(f"Import complete, results can be found in ./searched/{ref_name}.psdb")

# Save log file of PeptideShakerCLI output
with open(os.path.join(search_dir, "shaker_cli.log"), "w") as outfile:
          outfile.write("Command line arguments\n")
          outfile.write("----------------------\n")
          outfile.write(" ".join(shaker_process.args))
          outfile.write("\n\nRun Log\n-------\n")
          outfile.write(shaker_process.stdout)
          outfile.write(shaker_process.stderr)
logging.info("Log can be found in ./searched/shaker_cli.log")

# Remove html file automatically generated by SearchGUI
for f in fnmatch.filter(os.listdir(search_dir), "PeptideShaker*.html"):
    os.remove(os.path.join(search_dir, f))

# Summarise script performance

logging.info("============================")
logging.info(" Summary")
logging.info("============================")
logging.info("Successfully processed:")
logging.info("\n         ".join(raw_files))
if bad_files:
    logging.info("Failed to process:")
    logging.info("\n         ".join(bad_files))
logging.info("==========")
if needs_converting:
    convert_run_time = convert_end_time - convert_start_time
    logging.info("Thermo RAW File Parser converted {} files in {} mins:seconds".format(len(needs_converting), time.strftime("%M:%S", time.gmtime(convert_run_time))))
umpire_run_time = umpire_end_time - umpire_start_time
logging.info("DIA Umpire processed {} files in {} mins:seconds".format(len(raw_files), time.strftime("%M:%S", time.gmtime(umpire_run_time))))
search_run_time = search_end_time - search_start_time
logging.info("SearchGUI searched {} files in {} mins:seconds".format(len(to_search), time.strftime("%M:%S", time.gmtime(search_run_time))))
shaker_run_time = shaker_end_time - shaker_start_time
logging.info("PeptideShaker report generated in {} mins:seconds".format(time.strftime("%M:%S", time.gmtime(shaker_run_time))))
script_end_time = time.time()
total_time = script_end_time - script_start_time
logging.info("Script finished {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(script_end_time))))
logging.info("Total time = {} mins:seconds".format(time.strftime("%M:%S", time.gmtime(total_time))))

