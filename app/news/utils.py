import datetime
import os
import uuid


def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex + fileinfo[-1]
    return filename

