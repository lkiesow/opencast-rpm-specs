#!/bin/bash 

# Variables
specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/

debug="1"

# separator
oldIFS="$IFS"

function message()
{
    echo "$(date +%F-%T) M: $@"
}

function error()
{
    echo "$(date +%F-%T) E: $@"
    exit 1
}

function xeval()
{
    cmd=$@
    [ "$debug" == "1" ] && echo "$(date +%F-%T) D: $cmd"
    eval $cmd || error "$cmd"
}

function install_specs()
{
    rpm="$1"	

    message "Install specs $rpm"

    line="$(yum list installed $rpm | egrep "^$rpm.*")" 
    message "Package list item: $line"

    # application installed from local rpm?
    if echo "$line" | egrep "^$rpm.*(@/$rpm|installed)" >& /dev/null; then
	echo "package $rpm installed from specs, continue"
	continue
    elif [ -n "$line" ]; then
	echo "package $prm installed via online repo, remove and install via specs"
	# remove package without dependencies
	#sudo yum remove -y $rpm
	xeval "sudo rpm -e $rpm --nodeps"
    fi

    # Get source(s)
    cd "$sourcedir"
    xeval "spectool --all --get-files \"$specdir/${rpm}.spec\""

    # Get dependencies
    cd "$specdir" 
    xeval "sudo yum-builddep -y ${rpm}.spec"

    # Build package
    xeval "rpmbuild -ba \"$specdir/${rpm}.spec\""

    # Install package
    xeval "sudo yum localinstall -y ~/rpmbuild/RPMS/x86_64/*${rpm}*"
}

# Install basic packages
xeval "sudo yum install -y rpmdevtools.noarch rpmlint.noarch createrepo.noarch vim"

# Setup build dirs
cd ~
xeval "rpmdev-setuptree"

# Enable EPEL and Rpmforge repositories.
#sudo yum localinstall --nogpgcheck \
#  http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
if ! yum list installed epel-release.noarch >& /dev/null; then
    cd /tmp/
    xeval "wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    xeval "sudo rpm -Uvh epel-release-6*.rpm"
fi

# Copy patches to working directory
cd "$sourcedir"
xeval "cp $HOME/matterhorn-rpms/patch/*.patch ./"

# We solve dependencies with this order
# 1) make rpm via specs, required if patches are needed
# 2) online repository, yum install
# 3) download rpm,  yum localinstall

# external rpms dependencies. RPMS storage is inside direcotry ./rpms
# package depends_on_rpms
#faad2 id3lib*
#gpac js-*
bdependencies="
"
IFS="
"
for d in $bdependencies; do
    target="$(echo "$d" | cut -d' ' -f1)"
    rpms="$(echo "$d" | cut -d' ' -f2-)"
    message "Install localinstall $rpms"
    xeval "sudo yum localinstall ~/matterhorn-rpms/rpms/$rpms"
done

# First install these specs packages
# package depends_on_specs
#gpac xvidcore
sdependencies="
"
for d in $sdependencies; do
    target="$(echo "$d" | cut -d' ' -f1)"
    specs="$(echo "$d" | cut -d' ' -f2-)"
    for s in $specs; do
        install_specs $s
    done
done

# We have patches for these packages, install it via specs
# Packages order is important
# Remove gpack, can not download sources and 
#pack_with_patches="libgdither libmad a52dec faac faad2 gavl gpac x264"
pack_with_patches="libgdither libmad a52dec faac faad2 gavl x264"

# Install specs in this order
list="$pack_with_patches"

IFS="$oldIFS"
for rpm in $list; do
    install_specs $rpm
done
