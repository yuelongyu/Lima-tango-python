############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2011
# European Synchrotron Radiation Facility
# BP 220, Grenoble 38043
# FRANCE
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################

import itertools
import weakref
import PyTango
import sys
import numpy
import processlib
import time
import struct
from Lima import Core
from Lima.Server.plugins.Utils import BasePostProcess
#pixmaptools
import os
try:
    from bliss.data.routines.pixmaptools import qt4 as pixmaptools
except ImportError:
    os.environ["QUB_SUBPATH"]="qt4"
    from Qub.CTools import pixmaptools #for 16-bits to 8-bits conversionimport time
import Image
import cStringIO
import base64



def grouper(n, iterable, padvalue=None):
    return itertools.izip(*[itertools.chain(iterable, itertools.repeat(padvalue, n-1))]*n)



#==================================================================
#   Bpm Class Description:
#
#
#==================================================================


class BpmDeviceServer(BasePostProcess):

#--------- Add you global variables here --------------------------
    BPM_TASK_NAME = "BpmTask"
#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        self.__softOp = None
        self.__bpmManager = None
        self.bvdata = None
        self.autoscale = False
        self.color_map = False
        self.lut_method = "LINEAR"
#######PALETTE INIT
        color_palette =  pixmaptools.LUT.Palette(pixmaptools.LUT.Palette.TEMP)
        greyscale_palette = pixmaptools.LUT.Palette(pixmaptools.LUT.Palette.GREYSCALE)
        a = numpy.fromstring(color_palette.getPaletteData(), dtype=numpy.uint8)
        a.shape = (65536, 4)
        # BGR<=>RGB conversion
        r = numpy.array(a.T[2])
        b = numpy.array(a.T[0])
        a.T[0]=r; a.T[2]=b
        color_palette.setPaletteData(a)
        self.palette = { pixmaptools.LUT.Palette.TEMP: color_palette, pixmaptools.LUT.Palette.GREYSCALE: greyscale_palette }
#######
        BasePostProcess.__init__(self,cl,name)
        self.init_device()


    def init_device(self):
        print "In ", self.get_name(), "::init_device()"
        self.get_device_properties(self.get_device_class())

        for attr in ("Intensity", "Proj_X", "Proj_Y",
                     "Fwhm_X", "Fwhm_Y", "tXY", "X", "Y"):
            self.set_change_event(attr, True, False)


    def set_state(self,state) :
        if(state == PyTango.DevState.OFF) :
            if(self.__softOp) :
                self.__softOp = None
                self.__bpmManager = None
                ctControl = _control_ref()
                extOpt = ctControl.externalOperation()
                extOpt.delOp(self.PEAK_FINDER_TASK_NAME)
        elif(state == PyTango.DevState.ON) :
            if not self.__bpmManager:
                ctControl = _control_ref()
                extOpt = ctControl.externalOperation()
                self.__softOp = extOpt.addOp(Core.BPM,self.BPM_TASK_NAME,
                                                    self._runLevel)
                self.__bpmManager = self.__softOp.getManager()
                

        PyTango.Device_4Impl.set_state(self,state)

#------------------------------------------------------------------
#    Read BufferSize attribute
#------------------------------------------------------------------
    def read_BufferSize(self, attr):
        value_read = self.__bpmManager.historySize()
        attr.set_value(value_read)


#------------------------------------------------------------------
#    Write BufferSize attribute
#------------------------------------------------------------------
    def write_BufferSize(self, attr):
        data = attr.get_write_value()
        self.__bpmManager.resizeHistory(data)



#==================================================================
#
#    Bpm command methods
#
#==================================================================
    def validate_number(self, x, fallback_value=-1, min_value=0, max_value=None):
        if x is None:
          return fallback_value
        if not numpy.isfinite(x):
          return fallback_value
        if numpy.isnan(x):
          return fallback_value
        if min_value is not None and x < min_value:
          return fallback_value
        if max_value is not None and x > max_value:
          return fallback_value
        return x

    def getResults(self, from_index=0) :
        results = self.__bpmManager.getHistory(from_index)
        result_array = numpy.zeros((len(results),7))
        dim = _control_ref().image().getImageDim().getSize()
        max_width = dim.getWidth()
        max_height = dim.getHeight()
        for i,r in enumerate(results):
            result_array[i][0] = r.timestamp
            result_array[i][1] = self.validate_number(r.beam_intensity)
            result_array[i][2] = self.validate_number(r.beam_center_x, max_value=max_width)
            result_array[i][3] = self.validate_number(r.beam_center_y, max_value=max_height)
            result_array[i][4] = self.validate_number(r.beam_fwhm_x, fallback_value=0)
            result_array[i][5] = self.validate_number(r.beam_fwhm_y, fallback_value=0)
            result_array[i][6] = r.frameNumber
        return result_array.ravel()

    def SaveCalibration(self, calib):
        calib_x = calib[0]; calib_y = calib[1]
        tango_db = PyTango.DeviceProxy("sys/database/2")
        tango_db.DbPutDeviceProperty([self.get_name(), "1", "calibration_x", "1", str(calib_x)])
        tango_db.DbPutDeviceProperty([self.get_name(), "1", "calibration_y", "1", str(calib_y)])

    def LockBeamMark(self, bm):
        x = bm[0]; y=bm[1]
        tango_db = PyTango.DeviceProxy("sys/database/2")
        tango_db.DbPutDeviceProperty([self.get_name(), "1", "beam_x", "1", str(x)])
        tango_db.DbPutDeviceProperty([self.get_name(), "1", "beam_y", "1", str(y)])

    """
##############BACKGROUND : will see later
    def take_background(self):
        if self.getAcqStatus()=='Running':
            raise RuntimeError, "Acquisition has not finished (or Live mode is on)"
        self.get_position()
        self._set_background()


    def _set_background(self):
        if self.bkg_substraction_handler is not None:
            self._ext.delOp("bkg")
        im = self.ccd_control.ReadImage()
        self.bkg_substraction_handler = self._ext.addOp(self.Lima.Core.BACKGROUNDSUBSTRACTION, "bkg", 0)
        self.bkg_substraction_handler.setBackgroundImage(im)
        self._ext_change_event.set()


    def _has_background(self):
        return self.bkg_substraction_handler is not None


    def reset_background(self):
        if self.bkg_substraction_handler is not None:
            self._ext.delOp("bkg")
        self.bkg_substraction_handler = None
        self._ext_change_event.set()
##############
    """

#==================================================================
#
#    BpmDeviceServer read/write attribute methods
#
#==================================================================
    #
    def get_bpm_result(self, frameNumber=None, timestamp=None):
        if frameNumber==None:
            t = time.time()
            result = self.__bpmManager.getResult()
        else:
            t = timestamp
            result = self.__bpmManager.getResult(0,frameNumber)
        if result.errorCode != self.__bpmManager.OK:
           result.beam_center_x = -1
           result.beam_center_y = -1
           result.beam_intensity = -1
           result.beam_fwhm_x = 0
           result.beam_fwhm_y = 0
           result.max_pixel_value = 0
        else:
            dim = _control_ref().image().getImageDim().getSize()
            max_width = dim.getWidth()
            max_height = dim.getHeight()
            acq_time=t
            x  = self.validate_number(result.beam_center_x, max_value=max_width)
            y  = self.validate_number(result.beam_center_y, max_value=max_height)
            intensity = self.validate_number(result.beam_intensity)
            fwhm_x = self.validate_number(result.beam_fwhm_x, fallback_value=0)
            fwhm_y = self.validate_number(result.beam_fwhm_y, fallback_value=0)
            max_intensity = self.validate_number(result.max_pixel_value, fallback_value=0)
            
            try:
                profile_x = result.profile_x.buffer.astype(numpy.int)
            except:
                profile_x = numpy.array([],dtype=numpy.int)
            try:
                profile_y = result.profile_y.buffer.astype(numpy.int)
            except:
                profile_y = numpy.array([],dtype=numpy.int)

        result_array = [acq_time,x,y,intensity,fwhm_x,fwhm_y,max_intensity,profile_x,profile_y]
        return result_array


    def read_tXY(self, attr):
        last_acq_time, last_x, last_y, _, _, _, _, _, _ = self.get_bpm_result()
        value = numpy.array([last_acq_time, last_x, last_y], numpy.double)
        attr.set_value(value)

    def read_X(self, attr):
        _, last_x, _, _, _, _, _, _, _ = self.get_bpm_result()
        attr.set_value(last_x)

    def read_Y(self, attr):
        _, _, last_y, _, _, _, _, _, _ = self.get_bpm_result()
        attr.set_value(last_y)

    def read_Intensity(self, attr):
        _, _, _, last_intensity, _, _, _, _, _ = self.get_bpm_result()
        attr.set_value(last_intensity)

    def read_Fwhm_X(self, attr):
        _, _, _, _, last_fwhm_x, _, _, _, _ = self.get_bpm_result()
        attr.set_value(last_fwhm_x)

    def read_Fwhm_Y(self, attr):
        _, _, _, _, _, last_fwhm_y, _, _, _ = self.get_bpm_result()
        attr.set_value(last_fwhm_y)

    def read_MaxIntensity(self, attr):
        _, _, _, _, _, _, last_max_intensity, _, _ = self.get_bpm_result()
        attr.set_value(last_max_intensity)

    def read_Proj_X(self, attr):
        _, _, _, _, _, _, _, last_proj_x, _ = self.get_bpm_result()
        attr.set_value(last_proj_x)

    def read_Proj_Y(self, attr):
        _, _, _, _, _, _, _, _, last_proj_y = self.get_bpm_result()
        attr.set_value(last_proj_y)

    def read_AutomaticAOI(self,attr):
        aoi = self.__softOp.getTask().mRoiAutomatic
        attr.set_value(aoi)

    def write_AutomaticAOI(self,attr):
        aoi = attr.get_write_value()
        self.__softOp.getTask().mRoiAutomatic = aoi

    def read_AutoScale(self,attr):
        attr.set_value(self.autoscale)

    def write_AutoScale(self,attr):
        data = attr.get_write_value()
        self.autoscale = data

    def read_LutMethod(self,attr):
        attr.set_value(self.lut_method)

    def write_LutMethod(self,attr):
        data = attr.get_write_value()
        if data == "LINEAR" or data == "LOG":
            self.lut_method=data
        else:
            print "wrong lut method" #maybe error message
    
    def read_Colors(self,attr):
        attr.set_value(self.color_map)

    def write_Colors(self,attr):
        data = attr.get_write_value()
        self.color_map=data


#need to see how bpm will deal with bvdata 
    def read_BVData(self,attr):
        image = _control_ref().ReadImage() 
        last_acq_time, last_x, last_y, last_intensity, last_fwhm_x, last_fwhm_y, last_max_intensity, last_proj_x, last_proj_y = self.get_bpm_result(image.frameNumber, image.timestamp) 
        lima_roi = _control_ref().image().getRoi()
        roi_top_left = lima_roi.getTopLeft()
        roi_size = lima_roi.getSize()
        height, width = image.buffer.shape
        jpegFile = cStringIO.StringIO()
        if self.lut_method=="LINEAR":
            lut_method = pixmaptools.LUT.LINEAR
        else:
            lut_method = pixmaptools.LUT.LOG
        if self.color_map==True:
            color_map = pixmaptools.LUT.Palette.TEMP
        else:
            color_map = pixmaptools.LUT.Palette.GREYSCALE

        if self.autoscale:
            img_buffer = pixmaptools.LUT.transform_autoscale(image.buffer, self.palette[color_map], lut_method)[0]
        else:
            img_buffer = pixmaptools.LUT.transform(image.buffer, self.palette[color_map], lut_method, 0, 4*4096)[0]
        img_buffer.shape = (height, width, 4)
        I = Image.fromarray(img_buffer, "RGBX").convert("RGB")
        I.save(jpegFile, "jpeg", quality=95)
        raw_jpeg_data = jpegFile.getvalue()
        image_jpeg = base64.b64encode(raw_jpeg_data)
        profil_x = str(last_proj_x.tolist())
        profil_y = str(last_proj_y.tolist())
        self.bvdata_format='!ddddliiiidd%ds%ds%ds' %(len(profil_x),len(profil_y),len(image_jpeg))
        #msg sent is tuple(struct.pack,format) for decode purpose
        self.bvdata = struct.pack(
                self.bvdata_format,
		        last_acq_time,
		        last_x,
		        last_y,
		        last_intensity,
		        last_max_intensity,
		        roi_top_left.x,
		        roi_top_left.y,
		        roi_size.getWidth(),
		        roi_size.getHeight(),
		        last_fwhm_x,
		        last_fwhm_y,
                profil_x,
                profil_y,
                image_jpeg)

        attr.set_value(self.bvdata_format,self.bvdata)
        #self.push_change_event("BVData", self.bvdata[1], self.bvdata[0])


#==================================================================
#
#    BpmClass class definition
#
#==================================================================
class BpmDeviceServerClass(PyTango.DeviceClass):

    #	 Class Properties
    class_property_list = {
	}


    #	 Device Properties
    device_property_list = {
        "calibration_y":
        [PyTango.DevDouble,
        "Pixel size Y",
        [1] ],
        "beam_x":
        [PyTango.DevDouble,
        "Beam position X",
        [0] ],
        "beam_y":
        [PyTango.DevDouble,
        "Beam position Y",
        [0] ],
	}


    #	 Command definitions
    cmd_list = {
        'getResults':
            [[PyTango.DevLong,"from frame number"],
             [PyTango.DevVarDoubleArray,"frame number,x,y"]],
	    'Start':
            [[PyTango.DevVoid,""],
             [PyTango.DevVoid,""]],
	    'Stop':
            [[PyTango.DevVoid,""],
             [PyTango.DevVoid,""]],
        'GetPixelIntensity':
            [[PyTango.DevVarLongArray, "pixel coordinate"],
             [PyTango.DevLong], "return intensity on last image"]

	}


    #	 Attribute definitions
    attr_list = {
        'BufferSize': [[PyTango.DevLong, PyTango.SCALAR, PyTango.READ_WRITE]],
        'tXY': [[PyTango.DevDouble, PyTango.SPECTRUM, PyTango.READ, 3 ]],
        'X': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ ]],
        'Y': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ ]],
#        'AcquisitionSpectrum': [[PyTango.DevDouble, PyTango.IMAGE, PyTango.READ, 10000000, 7 ]],
#        'ResultSize': [[PyTango.DevLong, PyTango.SCALAR, PyTango.READ ]],
        'AutomaticAOI': [[PyTango.DevBoolean, PyTango.SCALAR, PyTango.READ_WRITE ]],
        'Intensity': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ ]],
        'MaxIntensity': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ]],
        'Proj_X': [[PyTango.DevLong, PyTango.SPECTRUM, PyTango.READ, 2048 ]],
        'Proj_Y': [[PyTango.DevLong, PyTango.SPECTRUM, PyTango.READ, 2048 ]],
        'Fwhm_X': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ]],
        'Fwhm_Y': [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ]],
        'AutoScale': [[PyTango.DevBoolean, PyTango.SCALAR, PyTango.READ_WRITE ]],
        'LutMethod' : [[PyTango.DevString, PyTango.SCALAR, PyTango.READ_WRITE ]],
        'Colors': [[PyTango.DevBoolean, PyTango.SCALAR, PyTango.READ_WRITE ]],
        'BVData':[[PyTango.DevEncoded, PyTango.SCALAR, PyTango.READ]],
        'Calibration': [[PyTango.DevDouble, PyTango.SPECTRUM, PyTango.READ_WRITE, 2 ]],
        'BeamMark': [[PyTango.DevLong, PyTango.SPECTRUM, PyTango.READ_WRITE, 2 ]]
    }


#------------------------------------------------------------------
#    BpmDeviceServerClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)



_control_ref = None
def set_control_ref(control_class_ref) :
    global _control_ref
    _control_ref= control_class_ref

def get_tango_specific_class_n_device() :
   return BpmDeviceServerClass,BpmDeviceServer