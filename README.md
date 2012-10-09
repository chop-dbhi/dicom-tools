This repository contains a few small dicom utility scripts.

1. ```./split.sh <dira> <dirb>``` <br>
This is just small script that will take the first 65000 files
from a dira and move that to dirb. This is used because the dcm4che
dcmsnd utility has a bug where it cannot send more than 65355 files in
one run, so it is necessary to put the files in separate directories.


1. ```./retrieve.sh <AE>@<SERVER>:<PORT> <studyuidfile>``` <br>
This is a script that uses the dcm4che2 toolkit to retrieve the files
in studyuidfile and send them to a receiving DICOM server. Please note this must be used in conjunction with the dcmrcv command (from the dcm4che2 library), which will setup a local DICOM server to actually receive the files. This only tells the server to move them to AE DCMQR. You will need to have the DCMQR AE configured on your PACS to point to your computer, and run the following to actually receive and save the files to local computer </br>
```dcmrcv DCMQR@<your-local-ip>:11112 -dest <directory-to-place-files>``` <br>
Also, dcmqr (dcm4che2 DICOM query utility) must be on your path. 

1. ```./dicom_push.rb <AE>@<SERVER>:<PORT> <directory>```
Push all the files in directory to the specified DICOM server. This uses the ruby-dicom library, which must be installed. It requires ruby 1.9.2.
There is an issue with 1.8.7. You may also need to set the following environment variable:<br>
```export RUBYOPT="rubygems"```
This utility is an alternative to using the dcmsend utility, which is used as following:<br>
```dcmsnd <AE>@<SERVER>:<PORT> <directory>```



