import os
import zipfile

def ignore_walk(directory, ignore_files=None, ignore_dirs=None):
    '''Ignore defined files and directories when doing the walk.'''

    # TODO: this does not currently take wild cards into account.  For example,
    # if you wanted to exclude *.pyc files ... should fix that.  Perhaps
    # consider moving this entirely into the below function (or making it more
    # reusable for other apps).
    for dirpath, dirnames, filenames in os.walk(directory):
        if ignore_dirs:
            dirnames[:] = [dn for dn in dirnames if dn not in ignore_dirs]
        if ignore_files:
            filenames[:] = [fn for fn in filenames if fn not in ignore_files]
        yield dirpath, dirnames, filenames

def zipdir(dir, zip_file, ignore_files=None, ignore_dirs=None):
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in ignore_walk(dir, ignore_files, ignore_dirs):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file
