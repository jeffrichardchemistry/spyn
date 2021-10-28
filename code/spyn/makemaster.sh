#!/bin/bash
underdirect="$PWD/qe/qe-6.3"

cd $PWD/qe/qe-6.3/qe-gipaw-6.3/

./configure --with-qe-source=$underdirect
