Opencast RPM Specs
==================

This repository contains the spec files to create all necessary RPMs for
Opencast. This includes:

 - Opencast itself
 - 3rd-Party-Tools

For CentOS and Scientific Linux, The inclusion of the EPEL repository from the
Fedora project is necessary to build and run these files. For Fedora, RPMFusion
is required.


Source RPMs
-----------

This repository only contains the spec files. The source files can be either
retrieved directly from upstream or bundled with the specs from the source
repository located at:

 - [http://repo.virtuos.uos.de/srpms/](http://repo.virtuos.uos.de/srpms/)

If you only want to build your own RPM repository, I recommend using the source
RPMs instead of downloading all source files by yourself. If you have
improvements for the specs however, it would be nice if you fork this git
repository and send pull requests for the improved specs, so that I can
integrate them into the source repository and everyone can benefit from your
changes.


Ready-To-Use: Binary Opencast RPM Repository
--------------------------------------------

If you only want to install Opencast on your system, have a look at the RPM
repository provided by the University of Osnabrück. It contains all necessary
pre-compiled RPMs for an up-to-date Opencast installation. The repository can
be found at:

 - [http://repo.virtuos.uos.de](http://repo.virtuos.uos.de)
