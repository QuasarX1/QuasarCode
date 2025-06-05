from enum import Enum

from ..Data._Rect import DiscreteRect

class ScreenResolution(Enum):
    """
    16:9 Screen Resolutions:
        nHD     :    640 x   360 = (2/3)K
        FWVGA   :    854 x   480 = (427/480)K
        qHD     :    960 x   540 = 1K
        HD      :  1,280 x   720 = (4/3)K
        WXGA    :  1,366 x   768 = (683/480)K
        HD+     :  1,600 x   900 = (5/3)K
        Full HD :  1,920 x 1,080 = 2K
        QHD     :  2,560 x 1,440 = (8/3)K
        QHD+    :  3,200 x 1,800 = (10/3)K
        4K UHD  :  3,840 x 2,160 = 4K
        5K      :  5,120 x 2,880 = 5K
        8K UHD  :  7,680 x 4,320 = 8K
        16K UHD : 15,360 x 8,640 = 16K
    """

    nHD       = DiscreteRect.create_from_size(0, 0, 640, 360)
    FWVGA     = DiscreteRect.create_from_size(0, 0, 854, 480)
    qHD       = DiscreteRect.create_from_size(0, 0, 960, 540)
    HD        = DiscreteRect.create_from_size(0, 0, 1280, 720)
    WXGA      = DiscreteRect.create_from_size(0, 0, 1366, 768)
    HD_PLUS   = DiscreteRect.create_from_size(0, 0, 1600, 900)
    FULL_HD   = DiscreteRect.create_from_size(0, 0, 1920, 1080)
    QHD       = DiscreteRect.create_from_size(0, 0, 2560, 1440)
    QHD_PLUS  = DiscreteRect.create_from_size(0, 0, 3200, 1800)
    FOUR_K    = DiscreteRect.create_from_size(0, 0, 3840, 2160)
    FIVE_K    = DiscreteRect.create_from_size(0, 0, 5120, 2880)
    EIGHT_K   = DiscreteRect.create_from_size(0, 0, 7680, 4320)
    SIXTEEN_K = DiscreteRect.create_from_size(0, 0, 15360, 8640)

    @staticmethod
    def get_all():
        """
        Returns all screen resolutions.
        """
        return ScreenResolution.__members__.values()

    @staticmethod
    def get_16_by_9():
        """
        Returns all 16:9 screen resolutions.
        """
        return [res for name, res in ScreenResolution.__members__ if name in (
            "nHD",
            "FWVGA",
            "qHD",
            "HD",
            "WXGA",
            "HD_PLUS",
            "FULL_HD",
            "QHD",
            "QHD_PLUS",
            "FOUR_K",
            "FIVE_K",
            "EIGHT_K",
            "SIXTEEN_K"
        )]

    @staticmethod
    def get_720p():
        """
        Returns the HD resolution (1280x720).
        """
        return ScreenResolution.HD

    @staticmethod
    def get_1080p():
        """
        Returns the Full HD resolution (1920x1080).
        """
        return ScreenResolution.FULL_HD

    @staticmethod
    def get_4K():
        """
        Returns the 4K resolution (3840x2160).
        """
        return ScreenResolution.FOUR_K
