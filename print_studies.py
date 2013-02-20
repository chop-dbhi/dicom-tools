import sys
import dicom
import os

studies = set()
for root, dirs, files in os.walk(sys.argv[1]):
     for filename in files:
         try:
             ds = dicom.read_file(os.path.join(root,filename))
         except IOError:
             continue
         study_uid = ds[0x20,0xD].value.strip()
         studies.add(study_uid)

for x in studies:
    print x
