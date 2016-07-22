# Pthreaded Driver Benchmarks

## Overview
This repo is for converting drivers into pthreaded benchmarks programs.
The idea is to call multiple driver entry points concurrently, each on their
own pthread, to see if there are racing drivers.

##
The original driver sources, as obtained for this repo, came from the Whoop
project, started by Pantazis Deligiannis.



