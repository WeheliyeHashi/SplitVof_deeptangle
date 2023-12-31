
from tierpsy.helper.misc import IMG_EXT

from .Readers.ReadVideoFFMPEG import ReadVideoFFMPEG
from .Readers.readVideoHDF5 import readVideoHDF5
from .Readers.readDatFiles import readDatFiles
from .Readers.readImages import readImages
from .Readers.readVideoCapture import readVideoCapture
from .Readers.readLoopBio import readLoopBio

import os


def selectVideoReader(video_file):
    # open video to read
    isHDF5video = video_file.endswith('hdf5')
    isMJPGvideo = video_file.endswith('.mjpg')
    isDATfiles = video_file.endswith('spool.dat')
    isLoopBio = video_file.endswith('.yaml')

    isImages = any(video_file.endswith(x) for x in IMG_EXT)

    if isHDF5video:
        # use tables to read hdf5 with lz4 compression generated by the Gecko
        # plugin
        vid = readVideoHDF5(video_file)
    elif isMJPGvideo:
        # use previous ffmpeg that is more compatible with the Gecko MJPG
        # format
        vid = ReadVideoFFMPEG(video_file)
    elif isDATfiles:
        video_dir = os.path.split(video_file)[0]
        vid = readDatFiles(video_dir)
    elif isLoopBio:
        # use opencv VideoCapture
        vid = readLoopBio(video_file)
    elif isImages:
        # I am assuming I am recieving the first file
        # of a directory full of images.
        video_dir, fname = os.path.split(video_file)
        bn, f_ext = os.path.splitext(fname)

        vid = readImages(video_dir, f_ext)
    else:
        vid = readVideoCapture(video_file)

    # raise an error if it is not a valid video (cannot read a frame)
    if vid.width == 0 or vid.height == 0:
        raise RuntimeError

    return vid
