#!/bin/bash

# irodsctl is not really mandatory, can be removed if the configure.pl
# script is modified

iRODSPATH=iRODS
iRODSCLIENTPATH=iRODSClient

FILELIST=("irodsctl"
		  "Makefile"
		  "LICENSE.txt"
		  "scripts/configure"
          "scripts/runperl"
          "scripts/perl/configure.pl"
		  "scripts/perl/utils_paths.pl"
		  "scripts/perl/utils_print.pl"
		  "scripts/perl/utils_file.pl"
		  "scripts/perl/utils_platform.pl"
		  "scripts/perl/utils_config.pl"
		  "scripts/perl/joinlines.pl"
		  "config/irods.config.template"
		  "config/config.mk.in"
		  "config/platform.mk.template"
		  "config/api.mk"
		  "config/common.mk"
		  "config/directories.mk"
		  "clients/icommands/Makefile"
		  "clients/icommands/src/*"
		  "COPYRIGHT/*"

		  )
		  
LIBS=("api" "core" "md5" "rbudp" "sha1")
		  
SERVER=("core" "icat" "drivers" "re")

# Create the output folder

if [ ! -d "$iRODSCLIENTPATH" ]; then
	mkdir $iRODSCLIENTPATH
fi

# This directory has to exist
mkdir -p $iRODSCLIENTPATH/modules/extendedICAT

mkdir -p $iRODSCLIENTPATH/clients/icommands/obj
touch $iRODSCLIENTPATH/clients/icommands/obj/empty.txt
mkdir -p $iRODSCLIENTPATH/clients/icommands/bin
touch $iRODSCLIENTPATH/clients/icommands/bin/empty.txt

cd $iRODSPATH

# Copy all files

for i in "${FILELIST[@]}"
do
	cp --parents -r $i ../$iRODSCLIENTPATH
done



# Manage libs

cp --parents -r "lib/Makefile" ../$iRODSCLIENTPATH
cp --parents -r "lib/README.txt" ../$iRODSCLIENTPATH

for i in "${LIBS[@]}"
do
	mkdir -p ../$iRODSCLIENTPATH/lib/$i/obj
	mkdir -p ../$iRODSCLIENTPATH/lib/$i/include
	mkdir -p ../$iRODSCLIENTPATH/lib/$i/src
	# Will be useful for distutil (non empty dir won't be included in tar.gz)
	touch ../$iRODSCLIENTPATH/lib/$i/obj/empty.txt
	
	if [ -d "./lib/$i/README.txt" ]; then
		cp ./lib/$i/README.txt ../$iRODSCLIENTPATH/lib/$i
	fi
	cp ./lib/$i/include/*.h ../$iRODSCLIENTPATH/lib/$i/include
	cp ./lib/$i/src/*.c ../$iRODSCLIENTPATH/lib/$i/src
done

# Manage server

cp --parents -r "server/config/server.config.in" ../$iRODSCLIENTPATH

for i in "${SERVER[@]}"
do
	mkdir -p ../$iRODSCLIENTPATH/server/$i/obj
	mkdir -p ../$iRODSCLIENTPATH/server/$i/include
	mkdir -p ../$iRODSCLIENTPATH/server/$i/src
	# Will be useful for distutil (non empty dir won't be included in tar.gz)
	touch ../$iRODSCLIENTPATH/server/$i/obj/empty.txt
	cp ./server/$i/README.txt ../$iRODSCLIENTPATH/server/$i
	cp ./server/$i/include/*.h ../$iRODSCLIENTPATH/server/$i/include
	cp ./server/$i/src/*.c ../$iRODSCLIENTPATH/server/$i/src
done
  



