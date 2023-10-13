#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --partition=blanca-cmbmgem
#SBATCH --output=sample-%j.out
#SBATCH --account=blanca-cmbmgem
#SBATCH --qos=blanca-cmbmgem
#SBATCH --mail-type=all
#SBATCH --mail-user=jodo9280@colorado.edu
#SBATCH --output=output.%j.out

module purge #removes any software currently running. Good Practice

module load python

python test.py

#top line is a shebang. Leave as is final shell script for simple python job
