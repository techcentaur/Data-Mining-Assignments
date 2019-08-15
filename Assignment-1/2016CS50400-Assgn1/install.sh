#!/bin/bash

repository="https://github.com/techcentaur/Data-Mining-Assignments.git"
git clone "$repository"

module load lib/gnu/710/boost/1.64.0/gnu
module load compiler/python/3.6.0/ucs4/gnu/447
module load pythonpackages/3.6.0/matplotlib/3.0.2/gnu

