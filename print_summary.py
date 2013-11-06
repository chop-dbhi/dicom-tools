import sys
import dicom
import os

study_descriptions = set()
series_descriptions = set()
patient_names = set()

print sys.argv[1]
for root, dirs, files in os.walk(sys.argv[1]):
     for filename in files:
         try:
             ds = dicom.read_file(os.path.join(root,filename))
         except IOError:
             sys.stderr.write("Error reading file %s\n" % os.path.join(root,filename))
             continue
         try:
            study_descr = ds[0x8, 0x1030].value.strip()
            study_descriptions.add(study_descr)
         except KeyError:
            pass

         try:
             series_descr = ds[0x8, 0x103E].value.strip()
             series_descriptions.add(series_descr)
         except KeyError:
             pass
             
         try:
              name = ds[0x10, 0x10].value.strip()
              patient_names.add(name)
         except KeyError:
              pass

print "--------STUDY---------"

for x in study_descriptions:
    print x

print "--------SERIES---------"

for x in series_descriptions:
    print x
    
print "--------NAMES---------"
for x in patient_names:
    print x
