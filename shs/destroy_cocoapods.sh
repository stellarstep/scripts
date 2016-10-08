#!/bin/bash
#remove gems
for i in $( gem list --local --no-version | grep cocoapods );
do 
	gem uninstall $i; 
done
#remove cache
rm -rf ~/.cocoapods/