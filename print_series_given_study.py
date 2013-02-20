import sys
import dicom
import os

series = set()
for root, dirs, files in os.walk(sys.argv[1]):
     for filename in files:
         try:
             ds = dicom.read_file(os.path.join(root,filename))
         except IOError:
             continue
         study_uid = ds[0x20,0xD].value.strip()
         if study_uid == sys.argv[2]
            series.add(ds[0x20,0xE].value.strip())

for x in series:
    print x
