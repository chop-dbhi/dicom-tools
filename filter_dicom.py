import sys
import dicom
import os
import json
import shutil
import difflib
from optparse import OptionParser

STUDY_IUID = (0x20, 0xD)
SERIES_IUID = (0x20, 0xE)
SOP_IUID = (0x8, 0x18)

DICOM_ATTR_MAP = {
    STUDY_IUID: "study iuid",
    SERIES_IUID: "series iuid",
    SOP_IUID: "sop iuid"
}

def move(source, dest, root):
    if not dest.endswith(os.path.sep):
        dest += os.path.sep

    if not root.endswith(os.path.sep):
        root += os.path.sep

    if dest.startswith(root):
        raise Exception("Destination directory cannot be inside"
            "or equal to source directory")

    if not source.startswith(root):
        raise Exception("The file to be moved must be in the root directory")

    s = difflib.SequenceMatcher(a=root, b=source)
    m = s.find_longest_match(0, len(root), 0, len(source))

    if not (m.a == m.b == 0):
        raise Exception("Unexpected file paths: source and root share no"
            " common path.")

    sub_path = os.path.dirname(source)[m.size:]

    destination_dir = os.path.join(dest, sub_path)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    shutil.move(source, os.path.join(destination_dir, os.path.basename(source)))

def filter_dicom(studies, series, instances, start_dir, 
    move_dir = "", delete = False):

    if not move_dir and not delete:
        raise Exception("Must supply move directory or specify delete.")

    levels = (("studies", set(studies), STUDY_IUID),
      ("series", set(series), SERIES_IUID),
      ("instances", set(instances), SOP_IUID))

    for root, dirs, files in os.walk(start_dir):
         for filename in files:
             try:
                 ds = dicom.read_file(os.path.join(root,filename))
             except IOError:
                 sys.stderr.write("Error reading file %s\n" % os.path.join(root,
                     filename))
                 continue

             for level, elements, index in levels:
                 try:
                    element = ds[index].value.strip()
                 except KeyError:
                    sys.stderr.write("%s has no attribute %s" % \
                        (os.path.join(root, filename), index))
                    continue
                 if element in elements:
                     action = "deleting" if delete else "moving"
                     sys.stdout.write("%s matched on %s( = to %s), %s.\n" % \
                          (os.path.join(root, filename), index, element, action))
                     try:
                        if delete:
                            os.remove(os.path.join(root, filename))
                        else:
                            move(os.path.join(root, filename), move_dir, root)
                     except Exception, e:
                         sys.stderr.write("Error move or deleting %s: %s\n" \
                            % (os.path.join(root, filename), e))
                         sys.exit()
                     break

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s", "--series", default="", dest="series", 
        action="store", help="Comma separated list series IUIDs")
    parser.add_option("-S", "--studies", default = "", dest="studies", 
        action="store", help="Comma separated list of study IUIDs")
    parser.add_option("-i", "--instances", default = "", dest="instances", 
        action="store", help="Comma separated list of SOP IUIDs")
    parser.add_option("-j", "--json_file", default = "" , dest="filename", 
        action="store", help="File containing JSON object describing studies,"
        " series, and instances")
    parser.add_option("-f", "--from", default="", dest="from_dir", action="store", 
        help="Location of files to move");
    parser.add_option("-t", "--to", default="", dest="to_dir", action="store", 
        help="Location to move matching files");
    parser.add_option("-d", "--delete", default=False, dest='delete', 
        action="store_true", help="Delete matching files (instead of move)")


    (options, args) = parser.parse_args()
    if not (options.series or options.studies or options.instances \
        or options.filename):
        sys.stderr.write("Must supply series, study, instance or filename.")
        sys.exit()
    if not (options.from_dir and (options.to_dir or options.delete)):
        sys.stderr.write("Must supply from and to directory"
            " (or specify delete).")
        sys.exit()


    levels = (("studies", set(), STUDY_IUID), 
       ("series", set(), SERIES_IUID),
       ("instances",set(), SOP_IUID))

    if options.filename:
        try:
            scheme = json.loads(open(options.filename, "r"))
        except e:
            sys.stderr.write(e)
            sys.exit()

        for level, elements, ignore in levels:
           if schema.has_key(level):
                elements.update([x.strip() for x in scheme[level]])

    for level, elements, ignore in levels:
        if getattr(options, level):
            elements.update([x.strip() for x in getattr(options, level).split(",")])

    filter_dicom(levels[0][1], levels[1][1], levels[2][1], 
        options.from_dir, options.to_dir, options.delete)


