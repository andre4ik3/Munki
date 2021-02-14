#!/bin/sh
# Simple script to convert the munkitools mpkg to separate pkgs
# I could build the separate pkgs from source but... this is just easier
# Also this should work for all pkgs - can use this to slim down mpkgs
# into just what you need.
# Extremely useful in my opinion.

set -e

# them defaults

usage() {
    cat <<EOF
Usage: $(basename "$0") <-p package> [-o dir] [-s cert]

    -p package  The package to unpack
    -o DIR      The output directory. If not specified, the package name without
                the file extension in the current directory will be used
    -s cert_cn  Sign every package with a Developer ID Installer certificate
                from keychain. Provide the certificate Common Name. Ex: 
                "Developer ID Installer: Munki (U8PN57A5N2)"

EOF
}

while getopts "p:o:s:h" option
do
    case $option in
        "p")
            PACKAGE="$OPTARG"
            ;;
        "o")
            OUTPUTDIR="$OPTARG"
            ;;
        "s")
            PKGSIGNINGCERT="$OPTARG"
            ;;
        "h" | *)
            usage
            exit 1
            ;;
    esac
done

if [ ! -f "$PACKAGE" ] ; then
    echo "Package file specified is empty or does not exist!"
    usage
    exit 1
elif [[ "$OUTPUTDIR" == "" ]] ; then
    OUTPUTDIR="$PWD/${PACKAGE%.*}"
fi

if [ -f "$PWD/$PACKAGE" ] ; then
    PACKAGE="$PWD/$PACKAGE"
fi

if [ -d "$OUTPUTDIR" ] ; then
    echo "$OUTPUTDIR already exists!"
    echo "Do this from a clean working dir or use -o for a custom directory!"
    exit 1
else
    mkdir $OUTPUTDIR
fi

cd "$OUTPUTDIR"
xar -xf "$PACKAGE"
rm "Distribution"
for DIR in $(ls "$OUTPUTDIR")
do
    cd $OUTPUTDIR/$DIR
    lsbom -s "Bom" > "filelist"
    mkbom -si "filelist" "Bom"
    rm "filelist"
    cd "$OUTPUTDIR"
    pkgutil --flatten "$DIR" "$DIR-flattened"

    if [[ "$PKGSIGNINGCERT" != "" ]] ; then
        productsign --sign "$PKGSIGNINGCERT" "$DIR-flattened" "$DIR-signed.pkg"
        rm -rf "$DIR" "$DIR-flattened"
        mv "$DIR-signed.pkg" "$DIR"
    else
        rm -rf "$DIR"
        mv "$DIR-flattened" "$DIR"
    fi
done