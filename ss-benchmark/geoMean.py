#!/usr/bin/python

# *********************************
# File:		geo_mean_calc.py
#
# Description:	This script finds the IPC for each benchmark output file
#		it calculates the execution time and two geometric means
#		for int and fp. Then it outputs a file with the data collected.
#
# Author:	Raquel Alvarez
#
# Usage:	python geo_mean_calc.py Configuration_Name
# *********************************

# imports
import re
import sys

# Output the data into a file following this format:
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Configuration: Configuration_Name
#
# INTEGER BENCHMARKS
#
#	IPC	Execution Time
# BZIP2	x.x	xxxxxxxxxxxxxx
# HMMER	x.x	xxxxxxxxxxxxxx
# MCF	x.x	xxxxxxxxxxxxxx
# SJENG	x.x	xxxxxxxxxxxxxx
#
# *** Geometric Mean = xxxxxxxxx.x ***
#
#
# FLOATING POINT BENCHMARKS
#
#	IPC	Execution Time
# EQUAK	x.x	xxxxxxxxxxxxxx
# MILC	x.x	xxxxxxxxxxxxxx
#
# *** Geometric Mean = xxxxxxxxx.x ***
#
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


output_f = open('GEOMETRIC_MEANS.txt', 'a')	# open/create the output file for the geometric mean calculations
config_name = open(sys.argv[1])			# should be an output file.
for fNm in config_name.readlines():
    fName = fNm.strip('\n')
    bzip2_f = open('bzip2/results/' + fName + '.out', 'r')		# open output file for bzip2 benchmark
    hmmer_f  = open('hmmer/results/' + fName + '.out', 'r')		# open output file for hmmer benchmark
    mcf_f    = open('mcf/results/' + fName + '.out', 'r')			# open output file for mcf benchmark
    sjeng_f  = open('sjeng/results/' + fName + '.out', 'r')		# open output file for sjeng benchmark
    equake_f = open('equake/results/' + fName + '.out', 'r')		# open output file for equake benchmark
    milc_f   = open('milc/results/' + fName + '.out', 'r')			# open output file for milc benchmark
    GM_f = open('OnlyGeoMeans.txt', 'a')


    # regex patters
    pattern = re.compile("sim_IPC")			# create a pattern "sim_IPC" to find the line of the file containing IPC
    ipc_pattern = re.compile("[0-9]*\.[0-9]*")	# create a pattern "x.xx..x" to find the IPC in the line


    # formula variables
    inst_count = 2500000				# fixed instruction count to 2500000
    cycle_time_static = [100, 110, 130]		# fixed values for issue width [1, 2, 4]
    cycle_time_dynamic = [140, 170, 200]		# fixed values for issue width [2, 4. 8]
    cycle_time = cycle_time_dynamic[2]		# default is set to issue width 1 in static


    # Name: 	get_IPC
    # Args: 	benchmark output file to find IPC
    # Output:	IPC
    def get_IPC(filename):
        for line in filename:			# scan the file line by line
            match_ipc = pattern.match(line)		# check to see if sim_IPC is in the current line
            if match_ipc:                          	# if the line contains sim_IPC, grab the IPC
                print "IPC found!"
                print line
                ipc = ipc_pattern.findall(line)	# grab the IPC from the line
                print type(ipc)
                ipc = float(ipc[0])			# the findall function returns a list, grab the first element
                print 'IPC = %s' % (ipc)
                break
        return ipc


    # Name:		exec_time
    # Args:		IPC
    # Output:	execution time for a given IPC
    def exec_time(ipc):
        return ((inst_count * cycle_time) / (1000000*ipc))	# return the execution time for a given ipc
                                                    # divide by 10^6 to get the time in micro seconds


    # Name:		int_geo_mean
    # Args:		none
    # Output:	geometric mean of the integer benchmarks
    def calc_int_geo_mean():
        prod = bzip2_exec_time * hmmer_exec_time * mcf_exec_time * sjeng_exec_time	# prod = t1 * t2 * t3 * t4
        geo_mean = prod ** (1/4.0)							# geo_mean = prod ^ (1/4)
        return geo_mean


    # Name:		fp_geo_mean
    # Args:		none
    # Output:	geometric mean of the float point benchmarks
    def calc_fp_geo_mean():
        prod = equake_exec_time * milc_exec_time
        geo_mean = prod ** (1/2.0)
        return geo_mean


    # program starts here
    # get IPC for all benchmarks
    bzip2_ipc = get_IPC(bzip2_f)	# call get_IPC function to calculate ipc
    hmmer_ipc = get_IPC(hmmer_f)
    mcf_ipc = get_IPC(mcf_f)
    sjeng_ipc = get_IPC(sjeng_f)
    equake_ipc = get_IPC(equake_f)
    milc_ipc = get_IPC(milc_f)

    # calc execution times
    bzip2_exec_time = exec_time(bzip2_ipc)	# call exec_time function to calculate execution time
    hmmer_exec_time = exec_time(hmmer_ipc)
    mcf_exec_time = exec_time(mcf_ipc)
    sjeng_exec_time = exec_time(sjeng_ipc)
    equake_exec_time = exec_time(equake_ipc)
    milc_exec_time = exec_time(milc_ipc)

    # calculate geometric means
    #  int
    int_geo_mean = calc_int_geo_mean()
    #  fp
    fp_geo_mean = calc_fp_geo_mean()

    # GEOMETRIC_MEAN.TXT FORMATTING AND EDITING:
    # 1: Configuration: fName
    # 2:
    # 3: INTEGER BENCHMARKS
    # 4:
    # 5: \tIPC\tExecution Time(usec)
    # 6: BZIP2\tx.x\txxxxxxxxx us
    # ...
    # 9: SJENG\tx.x\txxxxxxxxx
    # 10:
    # 11:*** Geometric Mean = xxxxxxxx.xx ***
    # 12:
    # 13:
    # 14:FLOATING POINT BENCHMARKS
    # 15:
    # 16:\tIPC\tExecution Time(usec)
    # 17:EQUAK\tx.x\txxxxxxxx us
    # 18:MILC\tx.x\txxxxxxxxx
    # 19:
    # 20:*** Geometric Mean = xxxxxxxx.xx ***
    # 21:

    # start editing output file
    output_f.write('Configuration: ' + fName + '\n\n')
    output_f.write('INTEGER BENCHMARKS\n\n')
    output_f.write('\tIPC\tExecution Time (usec)\n')
    output_f.write('BZIP2\t' + str(bzip2_ipc) + '\t' + str(bzip2_exec_time) + '\n')
    output_f.write('HMMER\t' + str(hmmer_ipc) + '\t' + str(hmmer_exec_time) + '\n')
    output_f.write('MCF\t' + str(mcf_ipc) + '\t' + str(mcf_exec_time) + '\n')
    output_f.write('SJENG\t' + str(sjeng_ipc) + '\t' + str(sjeng_exec_time) + '\n\n')
    output_f.write('*** Geometric Mean = %.3f ***\n\n\n' % (int_geo_mean))			# other way to format output
    GM_f.write(fName + '\t' + 'INT = %.3f\tFP = %.3f\n' %(int_geo_mean, fp_geo_mean))
    output_f.write('FLOATING POINT BENCHMARKS\n\n')
    output_f.write('\tIPC\tExecution Time (psec)\n')
    output_f.write('EQUAK\t%.4f\t%.3f\n' % (equake_ipc, equake_exec_time))	# only output 4 decimals for ipc and 3 for exec time
    output_f.write('MILC\t%.4f\t%.3f\n\n' % (milc_ipc, milc_exec_time))
    output_f.write('*** Geometric Mean = %.3f ***\n\n' % (fp_geo_mean))
