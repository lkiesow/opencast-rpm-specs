#!/bin/bash 

# ibalik() {
# existuje spec file {
#    pro vsechny zavislosti ve spec file zavolej ibalik(zavilost)
#    # tak tady uz neni zadna zavislost a my muzem kompilovat
#    pokud je balik jiz naisalovany lokalne (ne pres yum) { continue }
#    zkompiluj, naistaluj, vytvor rpm
# } else {
#    neni balik naistalovany {
#    naistaluj pomoci yum
#    }
# }
# }

# Variables
specdir=$HOME/matterhorn-rpms/specs/
sourcedir=~/rpmbuild/SOURCES/

debug="1"

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
    specfile="$2"

    message "Install spec $specfile, rpm $rpm"

    line="$(yum list installed $rpm | egrep "^$rpm.*")" 
    message "Package list item from yum: $line"

    # application installed from local rpm?
    if echo "$line" | egrep "^$rpm.*(@/$rpm|installed)" >& /dev/null; then
	echo "Package $rpm installed from spec, skip package"
	return 0
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

function init()
{
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
}

function help()
{
    echo "$0 [init] target"
    echo "$0 init ffmpeg"
    exit 0
}

if [ "$1" = "init" ]; then
    init
    target="$2"
else
    target="$1"
fi

[ -z "$target" ] && help

message "Start with target $target"

# spec file exists?
# remove -devel suffix (devel version goes from its original package)
# add suffix .spec
specfile="$specdir/${target%%-devel}.spec"
if [ -f "$specfile" ]; then
    message "Specfile $specfile exists, following dependencies"
    # Solve dependencies via rekursion calls
    breqs="$(xeval "/usr/local/bin/rpmspec -q --buildrequires $specfile")"
    for breq in $breqs; do
        message "Run $0 $breq"
        $0 $breq
    done
    install_specs $target $specfile 
else
    message "Install target $target via yum"
    xeval "yum install -y $target"
fi
