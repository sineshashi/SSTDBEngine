SSTable

This is initial project intended to apply SSTable from scratch using txt files. Currently, it has only set and get methods where set takes constant time but get iterates through all the lines in the txt file and tries to find given key. There are other flaws like set simply adds new line instead of updating the existing one or deleting old one which can cause too much data.
