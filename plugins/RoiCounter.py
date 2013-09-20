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
from Lima import Core
from Utils import getDataFromFile,BasePostProcess

def grouper(n, iterable, padvalue=None):
    return itertools.izip(*[itertools.chain(iterable, itertools.repeat(padvalue, n-1))]*n)

#==================================================================
#   RoiCounter Class Description:
#
#
#==================================================================


class RoiCounterDeviceServer(BasePostProcess) :

#--------- Add you global variables here --------------------------
    ROI_COUNTER_TASK_NAME = "RoiCounterTask"
#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
	self.__roiCounterMgr = None
        self.__roiName2ID = {}
        self.__roiID2Name = {}
        self.__currentRoiId = 0
	BasePostProcess.__init__(self,cl,name)
	RoiCounterDeviceServer.init_device(self)
        try:
            ctControl = _control_ref()
            config = ctControl.config()

            class _RoiConfigSave(Core.CtConfig.ModuleTypeCallback) :
                def __init__(self,cnt):
                    Core.CtConfig.ModuleTypeCallback.__init__(self,"RoiCounters")
                    self.__cnt = weakref.ref(cnt)
                def store(self) :
                    cnt = self.__cnt()
                    return cnt.get_current_config()
                def restore(self,c) :
                    cnt = self.__cnt()
                    cnt.apply_config(c)

            self.__roiConfigsave = _RoiConfigSave(self)
            config.registerModule(self.__roiConfigsave)
        except AttributeError:
            pass

    def set_state(self,state) :
	if(state == PyTango.DevState.OFF) :
	    if(self.__roiCounterMgr) :
		self.__roiCounterMgr = None
		ctControl = _control_ref()
		extOpt = ctControl.externalOperation()
		extOpt.delOp(self.ROI_COUNTER_TASK_NAME)
	elif(state == PyTango.DevState.ON) :
	    if not self.__roiCounterMgr:
                ctControl = _control_ref()
                extOpt = ctControl.externalOperation()
                self.__roiCounterMgr = extOpt.addOp(Core.ROICOUNTERS,self.ROI_COUNTER_TASK_NAME,
                                                    self._runLevel)
            self.__roiCounterMgr.clearCounterStatus()
            
	PyTango.Device_4Impl.set_state(self,state)

#------------------------------------------------------------------
#    Read BufferSize attribute
#------------------------------------------------------------------
    def read_BufferSize(self, attr):
	value_read = self.__roiCounterMgr.getBufferSize()
	attr.set_value(value_read)


#------------------------------------------------------------------
#    Write BufferSize attribute
#------------------------------------------------------------------
    def write_BufferSize(self, attr):
	data = attr.get_write_value()
        self.__roiCounterMgr.setBufferSize(data)


#------------------------------------------------------------------
#    Read CounterStatus attribute
#------------------------------------------------------------------
    def read_CounterStatus(self, attr):
	value_read = self.__roiCounterMgr.getCounterStatus()
	attr.set_value(value_read)


#==================================================================
#
#    RoiCounter command methods
#
#==================================================================
    def add(self,argin):
        roi_id = []
        for roi_name in argin:
            if not self.__roiName2ID.has_key(roi_name):
                self.__roiName2ID[roi_name] = self.__currentRoiId
                self.__roiID2Name[self.__currentRoiId] = roi_name
                roi_id.append(self.__currentRoiId)
                self.__currentRoiId += 1
            else:
                roi_id.append(self.__roiName2ID[roi_name])
        return roi_id

    def remove(self,argin):
        if self.__roiCounterMgr :
            self.__roiCounterMgr.remove(argin)
        for roi_name in argin:
            roi_id = self.__roiName2ID.pop(roi_name,None)
            self.__roiID2Name.pop(roi_id,None)
            
    def setRoi(self,argin) :
        if self.__roiCounterMgr is None:
            raise RuntimeError('should start the device first')
        
        if not len(argin) % 5:
            roi_list = []
            for roi_id,x,y,width,height in grouper(5,argin):
                roi_name = self.__roiID2Name.get(roi_id,None)
                if roi_name is None:
                    raise RuntimeError('should call add method before setRoi')
                roi_list.append((roi_name,Core.Roi(x,y,width,height)))
            self.__roiCounterMgr.update(roi_list)
        else:
            raise AttributeError('should be a vector as follow [roi_id0,x0,y0,width0,height0,...')
        
    def setArcRoi(self,argin) :
        if self.__roiCounterMgr is None:
            raise RuntimeError('should start the device first')
        
        if not len(argin) % 7:
            arc_list = []
            for roi_id,x,y,r1,r2,start,end in grouper(7,argin):
                roi_name = self.__roiID2Name.get(roi_id)
                if roi_name is None:
                    raise RuntimeError('should call add method before setRoi')
                arc_list.append((roi_name,Core.ArcRoi(x,y,r1,r2,start,end)))
            self.__roiCounterMgr.update(arc_list)
        else:
            raise AttributeError('should be a vector as follow [roi_id,centerX,centerY,rayon1,rayon2,angle_start,angle_end,...]')

    def get_current_config(self):
        try:
            returnDict = {}
            if self.__roiCounterMgr:
                returnDict["active"] = True
                returnDict["runLevel"] = self._runLevel
                for name,roiTask in self.__roiCounterMgr.getTasks() :
                    rType = roiTask.getType()
                    if rType == roiTask.SQUARE:
                        x,y,width,height = roiTask.getRoi()
                        returnDict[name] = {"type":rType,"x":x,"y":y,
                                            "width":width,
                                            "height":height}
                    else:
                        if rType == roiTask.LUT:
                            x,y,data = roiTask.getLut()
                        else:
                            x,y,data = roiTask.getLutMask()
                        returnDict[name] = {"type":rType,
                                            "x":x,"y":y,"data":data}
            else:
                returnDict["active"] = False
            return returnDict
        except:
            import traceback
            traceback.print_exc()
            
    def apply_config(self,c) :
        try:
            active = c.get("active",False)
            self.Stop()
            if active:
                self._runLevel = c.get("runLevel",0)
                self.Start()
                namedRois = []
                names = []
                for name,d in c.iteritems() :
                    try:
                        if isinstance(d,dict):
                            rType = d.get("type",None)
                            if rType == Core.Processlib.Tasks.RoiCounterTask.SQUARE:
                                x = d["x"]
                                y = d["y"]
                                width = d["width"]
                                height = d["height"]
                                namedRois.append((name,Core.Roi(x,y,width,height)))
                            elif rType == Core.Processlib.Tasks.RoiCounterTask.MASK:
                                x = d["x"]
                                y = d["y"]
                                data = d["data"]
                                self.__roiCounterMgr.setLutMask(name,Core.Point(x,y),data)
                            elif rType == Core.Processlib.Tasks.RoiCounterTask.LUT:
                                x = d["x"]
                                y = d["y"]
                                data = d["data"]
                                self.__roiCounterMgr.setLut(name,Core.Point(x,y),data)
                            names.append(name)
                    except KeyError as err:
                        PyTango.Except.throw_exception('Config error',
                                                       'Missing key %s in roi named %s'%(err,name),
                                                       'RoiCounterDeviceServer Class')
                self.__roiCounterMgr.update(namedRois)
                self.add(names)
        except:
            import traceback
            traceback.print_exc()
            
    def clearAllRoi(self):
        self.__roiCounterMgr.clearAllRoi()

    def setMaskFile(self,argin) :
        mask = getDataFromFile(*argin)
        self.__roiCounterMgr.setMask(mask)
    
    def readCounters(self,argin) :
        roiResultCounterList = self.__roiCounterMgr.readCounters(argin)
        if roiResultCounterList:
            minListSize = len(roiResultCounterList[0][1])
            for roiId,resultList in roiResultCounterList:
                if minListSize > len(resultList):
                    minListSize = len(resultList)

            
            if minListSize :
                returnArray = numpy.zeros(minListSize * len(roiResultCounterList) * 7,dtype = numpy.double)
                returnArray[0] = float(minListSize)
                indexArray = 0
                for roiName,resultList in roiResultCounterList:
                    roi_id = self.__roiName2ID.get(roiName)
                    for result in resultList[:minListSize] :
                        returnArray[indexArray:indexArray+7] = (float(roi_id),
                                                                float(result.frameNumber),
                                                                result.sum,
                                                                result.average,
                                                                result.std,
                                                                result.minValue,
                                                                result.maxValue)
                        indexArray += 7
                return returnArray
        return numpy.array([],dtype = numpy.double)

#==================================================================
#
#    RoiCounterClass class definition
#
#==================================================================
class RoiCounterDeviceServerClass(PyTango.DeviceClass):

    #	 Class Properties
    class_property_list = {
	}


    #	 Device Properties
    device_property_list = {
	}


    #	 Command definitions
    cmd_list = {
        'add':
        [[PyTango.DevVarStringArray,"rois alias"],
         [PyTango.DevVarLongArray,"rois' id"]],
        'remove':
        [[PyTango.DevVarStringArray,"rois alias"],
         [PyTango.DevVoid,""]],
        'setRoi':
        [[PyTango.DevVarLongArray,"roi vector [roi_id0,x0,y0,width0,height0,roi_id1,x1,y1,width1,heigh1,...]"],
	[PyTango.DevVoid,""]],
        'setArcRoi':
        [[PyTango.DevVarDoubleArray,"roi arc vector [roi_id,centerX,centerY,rayon1,rayon2,angle_start,angle_end,...]"],
	[PyTango.DevVoid,""]],
        'clearAllRoi':
        [[PyTango.DevVoid,""],
         [PyTango.DevVoid,""]],
        'setMaskFile':
        [[PyTango.DevVarStringArray,"Full path of mask file"],
         [PyTango.DevVoid,""]],
        'readCounters':
        [[PyTango.DevLong,"from which frame"],
         [PyTango.DevVarDoubleArray,"roi_id,frame number,sum,average,std,min,max,..."]],
	'Start':
	[[PyTango.DevVoid,""],
	 [PyTango.DevVoid,""]],
	'Stop':
	[[PyTango.DevVoid,""],
	 [PyTango.DevVoid,""]],
	}


    #	 Attribute definitions
    attr_list = {
	'BufferSize':
	    [[PyTango.DevLong,
	    PyTango.SCALAR,
	    PyTango.READ_WRITE]],
	'CounterStatus':
	    [[PyTango.DevLong,
	    PyTango.SCALAR,
	    PyTango.READ]],
	'RunLevel':
	    [[PyTango.DevLong,
	    PyTango.SCALAR,
	    PyTango.READ_WRITE]],
	}


#------------------------------------------------------------------
#    RoiCounterDeviceServerClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
	PyTango.DeviceClass.__init__(self, name)
	self.set_type(name);



_control_ref = None
def set_control_ref(control_class_ref) :
    global _control_ref
    _control_ref= control_class_ref

def get_tango_specific_class_n_device() :
   return RoiCounterDeviceServerClass,RoiCounterDeviceServer
