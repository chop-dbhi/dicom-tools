This repository contains a few small DICOM utility scripts.

1. `./split.sh <dira> <dirb>` <br>
This is just small script that will take the first 65000 files
from a dira and move that to dirb. This is used because the dcm4che
dcmsnd utility has a bug where it cannot send more than 65355 files in
one run, so it is necessary to put the files in separate directories.


1. `./retrieve.sh <AE>@<SERVER>:<PORT> <studyuidfile>` <br>
This is a script that uses the dcm4che2 toolkit to retrieve the files
in studyuidfile and send them to a receiving DICOM server. Please note this must be used in conjunction with the dcmrcv command (from the dcm4che2 library), which will setup a local DICOM server to actually receive the files. This only tells the server to move them to AE DCMQR. You will need to have the DCMQR AE configured on your PACS to point to your computer, and run the following to actually receive and save the files to local computer </br>
```dcmrcv DCMQR@<your-local-ip>:11112 -dest <directory-to-place-files>``` <br>
Also, dcmqr (dcm4che2 DICOM query utility) must be on your path. 

1. `./dicom_push.rb <AE>@<SERVER>:<PORT> <directory>` <br>
Push all the files in directory to the specified DICOM server. This uses the ruby-dicom library, which must be installed. It requires ruby 1.9.2.
There is an issue with 1.8.7. You may also need to set the following environment variable:<br>
```export RUBYOPT="rubygems"```<br>
This utility is an alternative to using the dcmsend utility, which is used as following:<br>
```dcmsnd <AE>@<SERVER>:<PORT> <directory>```

1. `./filter_dicom.py -S 1.12.32.32 -f /source/dir -t /dest/dir` <br>
This script allows you to specify comma separated lists of study (-S), series (-s) and instance (-i) uids and will recursively go through a directory (specified by the -f flag) removing all DICOM files that match _one_ of the specified requirements to a different directory (specified by the -t flag). It also takes a -d flag, which causes the files to be deleted. You can also pass a JSON formatted filename with the -j flag in addition to or instead of the other command line arguments. The file can be used to specify the filters you would like applied and must be in this format:

```javascript
{
   "studies":   ["<LIST>", 
                 "<OF>", 
                 "<STUDY IUIDS>"],
   "series":    ["<LIST>", 
                 "<OF>", 
                 "<SERIES IUIDS>"],
   "instances": ["<LIST>", 
                 "<OF>", 
                 "<SOP IUIDS>"]
}
```
1. `./print_summary.py <directory>` <br>
Given a directory of DICOM files, print out a summary of all unique study descriptions, series descriptions and patient names.


