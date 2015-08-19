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
#=============================================================================
#
# file :        imXPAD.py
#
# description : Python source for the imXPAD and its commands.
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#         (c) - Bliss - ESRF
#=============================================================================
#
import PyTango
import os
from Lima import Core
from Lima import imXpad as XpadAcq
#from LimaCCDs import CallableReadEnum,CallableWriteEnum
from AttrHelper import get_attr_4u, get_attr_string_value_list


class imXPAD(PyTango.Device_4Impl):

    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,*args) :
        PyTango.Device_4Impl.__init__(self,*args)

        self.init_device()

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass
    
#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def init_device(self):
        

        try:
            
            self.set_state(PyTango.DevState.ON)
            self.get_device_properties(self.get_device_class())
        
        except Exception, e:
            print "Error in init_device Method"
            print e
            
        #Dictionaries with the Types. 
        self.AcquisitionModes = {'Standard':XpadAcq.Camera.XpadAcquisitionMode.Standard,
                                 'ComputerBurst':XpadAcq.Camera.XpadAcquisitionMode.ComputerBurst,
                                 'DetectorBurst':XpadAcq.Camera.XpadAcquisitionMode.DetectorBurst,
                                 # 'SingleBunch16bits':XpadAcq.Camera.XpadAcquisitionMode.SingleBunch16bits,
                                 # 'SingleBunch32bits':XpadAcq.Camera.XpadAcquisitionMode.SingleBunch32bits,
                                 # 'Stacking16bits':XpadAcq.Camera.XpadAcquisitionMode.Stacking16bits,
                                 # 'Stacking32bits':XpadAcq.Camera.XpadAcquisitionMode.Stacking32bits,
                                 }

        self.OutputSignals = {'ExposureBusy':XpadAcq.Camera.XpadOutputSignal.ExposureBusy,
            'ShutterBusy':XpadAcq.Camera.XpadOutputSignal.ShutterBusy,
            'BusyUpdateOverflow':XpadAcq.Camera.XpadOutputSignal.BusyUpdateOverflow,
            'PixelCounterEnabled':XpadAcq.Camera.XpadOutputSignal.PixelCounterEnabled,
            'ExternalGate':XpadAcq.Camera.XpadOutputSignal.ExternalGate,
            'ExposureReadDone':XpadAcq.Camera.XpadOutputSignal.ExposureReadDone,
            'DataTransfer':XpadAcq.Camera.XpadOutputSignal.DataTransfer,
            'RAMReadyImageBusy':XpadAcq.Camera.XpadOutputSignal.RAMReadyImageBusy,
            'XPADToLocalDDR':XpadAcq.Camera.XpadOutputSignal.XPADToLocalDDR,
            'LocalDDRToPC':XpadAcq.Camera.XpadOutputSignal.LocalDDRToPC}
         
        self.TriggerModes = {'INTERNAL_TRIGGER':0,
                            'EXTERNAL_TRIGGER':2,
                            'EXTERNAL_GATE':1,
                            'EXTERNAL_MULTI_TRIGGER':3}
        
        self.ImageFileFormats = {'Ascii':XpadAcq.Camera.XpadImageFileFormat.Ascii,
                       'Binary':XpadAcq.Camera.XpadImageFileFormat.Binary}
        
        ##Set DEFAULT configuration to store input values
        ##(there are no getters for these attributes) 

        # print("Setting values by Default")
        
        self.AcquisitionMode ='Standard'
        _imXPADCam.setAcquisitionMode(self.AcquisitionModes[self.AcquisitionMode])

        self.FlatFieldCorrectionFlag = 1 # Enabled by default
        _imXPADCam.setFlatFieldCorrectionFlag(self.FlatFieldCorrectionFlag)
        
        self.GeometricalCorrectionFlag = 1
        _imXPADCam.setGeometricalCorrectionFlag(self.GeometricalCorrectionFlag)       
        self.ImageFileFormat = 'Binary'
        _imXPADCam.setImageFileFormat(self.ImageFileFormats[self.ImageFileFormat])
        self.OutputSignalMode = 'BusyUpdateOverflow'
        _imXPADCam.setOutputSignalMode(self.OutputSignals[self.OutputSignalMode])
        
    @Core.DEB_MEMBER_FUNCT
#     def getAttrStringValueList(self, attr_name):
# #### old implementation
# #        valueList=[]
# #        dict_name = '_' + self.__class__.__name__ + '__' + ''.join([x.title() for x in attr_name.split('_')])
# #        d = getattr(self,dict_name,None)
# #        if d:
# #            valueList = d.keys()
# #
# #        return valueList
#         #use AttrHelper
#         return get_attr_string_value_list(self, attr_name)


    @Core.DEB_MEMBER_FUNCT
    def loadConfig(self,config_prefix) :
        config_path = self.config_path
        _imXPADCam.loadConfigGFromFile(os.path.join(config_path,'%s.cfg' % config_prefix))
        _imXPADCam.loadConfigLFromFile(os.path.join(config_path,'%s.cfl' % config_prefix))

    @Core.DEB_MEMBER_FUNCT
    def saveConfig(self,config_prefix) :
        config_path = self.config_path
        _imXPADCam.saveConfigGToFile(os.path.join(config_path,'%s.cfg' % config_prefix))
        _imXPADCam.saveConfigLToFile(os.path.join(config_path,'%s.cfl' % config_prefix))
        
#     def __getattr__(self,name) :
# #### old implementation
# #        if name.startswith('read_') or name.startswith('write_') :
# #            split_name = name.split('_')[1:]
# #            attr_name = ''.join([x.title() for x in split_name])
# #            dict_name = '_' + self.__class__.__name__ + '__' + attr_name
# #            d = getattr(self,dict_name,None)
# #            attr_name = self.__Attribute2FunctionBase.get('_'.join(split_name),attr_name)
# #            if d:
# #                if name.startswith('read_') :
# #                    functionName = 'get' + attr_name
# #                    function2Call = getattr(_XpadAcq,functionName)
# #                    callable_obj = CallableReadEnum(d,function2Call)
# #                else:
# #                    functionName = 'set' + attr_name
# #                    function2Call = getattr(_XpadAcq,function2Call)
# #                    callable_obj = CallableWriteEnum(d,function2Call)
# #                self.__dict__[name] = callable_obj
# #                return callable_obj
# #        raise AttributeError('Xpad has no attribute %s' % name)
#         #use AttrHelper
#         return get_attr_4u(self,name,XpadAcq)

     
#==================================================================
#
#    imXPAD command methods
#
#==================================================================

    def calibrationOTNPulse(self, attr):
        print ("OTNpulseCalibration in %s", attr)
        _imXPADCam.calibrationOTNPulse(attr)
    
    def calibrationOTN(self,attr):
        print ("OTNcalibration in %s", attr)
        _imXPADCam.calibrationOTN(attr)
        
    def calibrationBEAM(self, values):
        print ("BeamCalibration in %s", values)
        time = int(values[0])
        ITHLmax = int(values[1])
        calibConfig = int(values[2])
        _imXPADCam.calibrationBEAM(time, ITHLmax, calibConfig)

    def ITHLIncrease(self):
        print ("ITHLIncrease")
        #pass
        _imXPADCam.ITHLIncrease()

    def ITHLDecrease(self):
        print ("ITHLDecrease")
        #pass
        _imXPADCam.ITHLDecrease()
    
    def setAcquisitionMode(self, attr):    
        print ("setAcquisitionMode in %s", attr)    
        _imXPADCam.setAcquisitionMode(self.AdquisitionModes[attr])
        

    def setFlatFieldCorrectionFlag(self,attr):
        print ("setFlatFieldCorrectionFlag in %s", attr)
        _imXPADCam.setFlatFieldCorrectionFlag(attr)
     
    def setGeometricalCorrectionFlag(self, attr):
        print ("setGeometricalCorrectionFlag in %s", attr)
        _imXPADCam.setGeometricalCorrectionFlag(attr)

    def askReady(self):
        print ("In askReady Command")
        val= _imXPADCam.askReady()
        return bool(val == 0)
    
    def getModuleMask(self):
        print ("Get module mask")
        try:
            val= _imXPADCam.getModuleMask()
        except Exception, e:
            print e
            raise e
        return val
    
    def abort(self):       
        print ("In abort")
        pass
    
    def resetModules(self):
        _imXPADCam.resetModules()
        
    def setOutputSignalMode(self, attr):
        print ("setOutputSignalMode in %s", attr)
        self.OutputSignalMode = self.OutputSignals[attr]
        _imXPADCam.setOutputSignalMode(self.OutputSignalMode)
      
    def saveConfigLToFile(self,config_prefix) :
        print ("saveConfigLToFile in %s", config_prefix)
        config_path = self.config_path
        full_path = os.path.join(config_path,'%s.cfl' % config_prefix)
        _imXPADCam.saveConfigLToFile(full_path)  
        
    def loadConfigLFromFile(self,config_prefix) :
        print ("loadConfigLFromFile in %s", config_prefix)
        config_path = self.config_path
        full_path = os.path.join(config_path,'%s.cfl' % config_prefix)
        _imXPADCam.loadConfigLFromFile(full_path)
    
    def saveConfigGToFile(self,config_prefix) :
        print ("saveConfigGToFile in %s", config_prefix)
        config_path = self.config_path
        full_path = os.path.join(config_path,'%s.cfg' % config_prefix)
        _imXPADCam.saveConfigGToFile(full_path)
        
    def loadConfigGFromFile(self,config_prefix) :
        print ("loadConfigGFromFile %s", config_prefix)
        config_path = self.config_path
        full_path = os.path.join(config_path,'%s.cfg' % config_prefix)
        _imXPADCam.loadConfigGFromFile(full_path)
        
    def loadConfigG(self, config):
        print ("loadConfigG in %s", config)
        reg = long(config[0])
        value = long(config[1])
        val = _imXPADCam.loadConfigG(reg, value)
        return val
    
    def readConfigG (self, config):
        print ("readConfigG in %s", config)
        reg = long(config)
#    value = long(config[1])
        val = _imXPADCam.readConfigG(reg)
        return val
    
    def getUSBDeviceList(self):
        print ("getUSBDeviceList in")
        val = _imXPADCam.getUSBDeviceList()
        print val
        return val

    def xpadInit(self):
        print (" in xpadInit")
        _imXPADCam.xpadInit()
      
    def setUSBDevice(self, module):
        print ("setUSBDevice in %s", module)
        val =long(module)
        _imXPADCam.setUSBDevice(val)

    def defineDetectorModel(self, model):
        print(" in defineDetectorModel Method")
        val = model
        _imXPADCam.defineDetectorModel(val)

    def digitalTest(self, mode):
        print(" in digitalTest Method")
        val = mode
        _imXPADCam.digitalTest(val)

    def loadFlatConfigL(self, value):
        print("In loadFlatConfigL")
        val = value
        _imXPADCam.loadFlatConfigL(val)    

    def exit(self):
        _imXPADCam.exit()

    def loadDefaultConfigGValues(self):
        _imXPADCam.loadDefaultConfigGValues()
#==================================================================
#
#    imXPAD read/write attribute methods
#
#==================================================================       
#------------------------------------------------------------------
#    Read Acquisition_Mode attribute
#------------------------------------------------------------------
    def read_Acquisition_Mode(self, attr):
        print "In ", self.get_name(), "::read_Acquisition_Mode()"
        attr.set_value(str(self.AcquisitionMode))

#------------------------------------------------------------------
#    Write Acquisition_Mode attribute
#------------------------------------------------------------------
    def write_Acquisition_Mode(self, attr):
        print "In ", self.get_name(), "::write_Acquisition_Mode()"
        val = attr.get_write_value()
        self.AcquisitionMode = self.AcquisitionModes[val]
        _imXPADCam.setAcquisitionMode(self.AcquisitionMode)
        print "Leaving ", self.get_name(), "::write_Acquisition_Mode()"
   
#------------------------------------------------------------------
#    read Flat_Field_Correction_Flag attribute
#------------------------------------------------------------------
    def read_Flat_Field_Correction_Flag(self, attr):
        print "In ", self.get_name(), "::read_Flat_Field_Correction_Flag()"
        attr.set_value(self.FlatFieldCorrectionFlag)
     
#------------------------------------------------------------------
#    Write Flat_Field_Correction_Flag attribute
#------------------------------------------------------------------
    def write_Flat_Field_Correction_Flag(self, attr):
        print "In ", self.get_name(), "::write_Flat_Field_Correction_Flag()"
        self.FlatFieldCorrectionFlag = bool(attr.get_write_value())
        _imXPADCam.setFlatFieldCorrectionFlag(self.FlatFieldCorrectionFlag)
        print "Leaving ", self.get_name(), "::write_Field_Correction_Flag()"
   
#------------------------------------------------------------------
#    read Image_Transfer_Flag attribute
#------------------------------------------------------------------
    def read_Image_Transfer_Flag(self, attr):
        print "In ", self.get_name(), "::read_Image_Transfer_Flag()"
        self.ImageTransferFlag = _imXPADCam.getImageTransferFlag()
        attr.set_value(self.ImageTransferFlag)
        print "Leaving ", self.get_name(), "::read_Image_Transfer_Flag()"

#------------------------------------------------------------------
#    Write Image_Transfer_Flag attribute
#------------------------------------------------------------------
    def write_Image_Transfer_Flag(self, attr):
        print "In ", self.get_name(), "::write_Image_Transfer_Flag()"
        self.ImageTransferFlag = bool(attr.get_write_value())
        _imXPADCam.setImageTransferFlag(self.ImageTransferFlag)
        print "Leaving ", self.get_name(), "::write_Image_Transfer_Flag()"

#------------------------------------------------------------------
#    read Over_Flow_Time attribute
#------------------------------------------------------------------
    def read_Over_Flow_Time(self, attr):
        print "In ", self.get_name(), "::read_Over_Flow_Time()"
        self.OverflowTime = _imXPADCam.getOverflowTime()
        attr.set_value(self.OverflowTime)
     
#------------------------------------------------------------------
#    Write Image_Transfer_Flag attribute
#------------------------------------------------------------------
    def write_Over_Flow_Time(self, attr):
        print "In ", self.get_name(), "::write_Over_Flow_Time()"
        self.OverflowTime = bool(attr.get_write_value())
        _imXPADCam.setOverflowTime(self.OverflowTime)
        print "Leaving ", self.get_name(), "::write_Over_Flow_Time()"
        
#------------------------------------------------------------------
#    read Flat_Field_Correction_Flag attribute
#------------------------------------------------------------------
    def read_Geometrical_Correction_Flag(self, attr):
        print "In ", self.get_name(), "::read_Geometrical_Correction_Flag()"
        attr.set_value(self.GeometricalCorrectionFlag)
   
#------------------------------------------------------------------
#    Write Geometrical_Correction_Flag attribute
#------------------------------------------------------------------
    def write_Geometrical_Correction_Flag(self, attr):
        print "In ", self.get_name(), "::write_Geometrical_Correction_Flag()"
        self.GeometricalCorrectionFlag = bool(attr.get_write_value())
        _imXPADCam.setGeometricalCorrectionFlag(self.GeometricalCorrectionFlag)
        print "Leaving ", self.get_name(), "::write_Geometrical_Correction_Flag()"
   
#------------------------------------------------------------------
#    read Output_Signal attribute
#------------------------------------------------------------------
    def read_Output_Signal(self, attr):
        print "In ", self.get_name(), "::read_Output_Signal()"
        attr.set_value(self.OutputSignalMode)
   
#------------------------------------------------------------------
#    Write Output_Signal attribute
#------------------------------------------------------------------
    def write_Output_Signal(self, attr):
        print "In ", self.get_name(), "::write_Output_Signal()"
        self.OutputSignalMode = attr.get_write_value()
        _imXPADCam.setOutputSignalMode(self.OutputSignals[self.OutputSignalMode])
        print "Leaving ", self.get_name(), "::write_Output_Signal()"
   
#------------------------------------------------------------------
#    read Trigger_Mode attribute
#------------------------------------------------------------------
    def read_Trigger_Mode(self, attr):
        print "In ", self.get_name(), "::read_Trigger_Mode()"
        val = _imXPADCam.getTrigMode()
        for i in self.TriggerModes:
            if self.TriggerModes[i] == val:
                val = i
        attr.set_value(str(val))
   
#------------------------------------------------------------------
#    Write Output_Signal attribute
#------------------------------------------------------------------
    def write_Trigger_Mode(self, attr):
        print "In ", self.get_name(), "::write_Trigger_Mode()"
        val = attr.get_write_value()      
        _imXPADCam.setTrigMode(self.TriggerModes[val])
        print "Leaving ", self.get_name(), "::write_Trigger_Mode()"
      
#------------------------------------------------------------------
#    read Image_Format attribute
#------------------------------------------------------------------
    def read_Image_Format(self, attr):
        print "In ", self.get_name(), "::read_Image_Format()"
        val = self.ImageFileFormat
        attr.set_value(val)
   
#------------------------------------------------------------------
#    Write Output_Signal attribute
#------------------------------------------------------------------
    def write_Image_Format(self, attr):
        print "In ", self.get_name(), "::write_Image_Format()"
        val = self.ImageFileFormats[attr.get_write_value()]
        _imXPADCam.setImageFileFormat(val)
        print "Leaving ", self.get_name(), "::write_Image_Format()"
   
   
   
#------------------------------------------------------------------
#    read Exp_Time attribute
#------------------------------------------------------------------
    def read_Exp_Time(self, attr):
        print "In ", self.get_name(), "::read_Exp_Time()"
        self.Exp_Time = _imXPADCam.getExpTime()
        attr.set_value(self.ExpTime)
   
#------------------------------------------------------------------
#    Write Output_Signal attribute
#------------------------------------------------------------------
    def write_Exp_Time(self, attr):
        print "In ", self.get_name(), "::write_Output_SignalExp_Time()"
        self.Exp_Time = attr.get_write_value()
        _imXPADCam.setExpTime(self.ExpTime)
        print "Leaving ", self.get_name(), "::write_setExpTime()"   
        
        
#------------------------------------------------------------------
#    read NbFrames attribute
#------------------------------------------------------------------
    def read_NbFrames(self, attr):
        print "In ", self.get_name(), "::read_NbFrames()"
        self.NbFrames = _imXPADCam.getNbTime()
        attr.set_value(self.NbFrames)
   
#------------------------------------------------------------------
#    Write Output_Signal attribute
#------------------------------------------------------------------
    def write_Exp_Time(self, attr):
        print "In ", self.get_name(), "::write_NbFrames()"
        self.NbFrames = attr.get_write_value()
        _imXPADCam.setNbFrames(self.NbFrames)
        print "Leaving ", self.get_name(), "::write_NbFrames()"   
                
        
      
#==================================================================
#
#    imXPADClass class definition
#
#==================================================================
class imXPADClass(PyTango.DeviceClass):

    class_property_list = {}

    device_property_list = {
        'cam_ip_address' :
        [PyTango.DevString,
         "Camera ip address",[]],
        'port' :
        [PyTango.DevLong,
         'ip port',[]],
        'config_path' :
        [PyTango.DevString,
         "Config path",[]]
        }
    
    
    cmd_list = {
#        'getAttrStringValueList':
#        [[PyTango.DevString, "Attribute name"],
#         [PyTango.DevVarStringArray, "Authorized String value list"]],
                
       'getUSBDeviceList':
        [[PyTango.DevVoid, "getUSBDeviceList"],
         [PyTango.DevString,""]],
        
        'setUSBDevice':
        [[PyTango.DevLong, "set USB Device"],
         [PyTango.DevVoid,""]],         
                
        'defineDetectorModel':
        [[PyTango.DevLong, "set Detector Model"],
         [PyTango.DevVoid,""]],                         
                         
        'xpadInit':
        [[PyTango.DevVoid, ""],
         [PyTango.DevVoid,""]],           
                           
        'askReady':
        [[PyTango.DevVoid, "Ask the detector if ready"],
         [PyTango.DevBoolean,""]],
                
        'getModuleMask':
        [[PyTango.DevVoid, ""],
         [PyTango.DevULong,"Mask of the available modules"]], # Hexadecimal?
                
        'digitalTest':
        [[PyTango.DevLong, "digitalTest"],
         [PyTango.DevVoid,""]],
               
        'saveConfigGToFile':
        [[PyTango.DevString, "Save G Config file prefix"],
         [PyTango.DevVoid,""]],    
                 
        'saveConfigLToFile':
        [[PyTango.DevString, "Save L Config file prefix"],
         [PyTango.DevVoid,""]],                  
        
        'calibrationOTN':
        [[PyTango.DevLong, "OTN  Calibration"],
         [PyTango.DevVoid,""]],
                   
        'calibrationOTNPulse':
        [[PyTango.DevLong, "OTN Pulse Calibration "],
         [PyTango.DevVoid,""]],
                       
        'calibrationBEAM':
        [[PyTango.DevVarLongArray, "Beam Calibration"],
         [PyTango.DevVoid,""]],        
               
        'loadConfig':
        [[PyTango.DevVarStringArray, "Config file prefix"], 
         [PyTango.DevVoid,""]],
        
        'loadConfigG':
        [[PyTango.DevVarStringArray, "Config file prefix"], # input 2 parameters (reg,value)
         [PyTango.DevVoid,""]],
        
        'readConfigG':
        [[PyTango.DevVarLongArray, "readConfigG"],
         [PyTango.DevVoid,""]], # return integer array          
                            
        'loadDefaultConfigGValues':
        [[PyTango.DevVoid, "loadDefaultConfigGValues"],
         [PyTango.DevVoid,""]],
                    
        'loadFlatConfigL':
        [[PyTango.DevLong, "Load of flat config of value: flat_value (on each pixel)"],
         [PyTango.DevVoid,""]],
                     
        'loadConfigLFromFile':
        [[PyTango.DevString, "Load of config of File"],
         [PyTango.DevVoid,""]],
                
        'loadConfigGFromFile':
        [[PyTango.DevString, "Load of config of File"],
         [PyTango.DevVoid,""]],
                
        'exit':
        [[PyTango.DevVoid, ""],
         [PyTango.DevVoid,""]],

        'ITHLIncrease':
        [[PyTango.DevVoid, "Increment of one unit in the global ITHL register"],
         [PyTango.DevVoid,""]],                 

        'ITHLDecrease':
        [[PyTango.DevVoid, "Decrement of one unit in the global ITHL register"],
         [PyTango.DevVoid,""]],

        'setOutputSignalMode':
        [[PyTango.DevString, "Type OutputSignalMode"],
         [PyTango.DevVoid,""]],    
                
            }

    attr_list = {                  
        "Acquisition_Mode":
        [[PyTango.DevString, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
                 
        "Trigger_Mode":
        [[PyTango.DevString, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
                 
        "Output_Signal":
        [[PyTango.DevString, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
                 
        "Flat_Field_Correction_Flag":
        [[PyTango.DevShort, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
                 
        "Image_Transfer_Flag":
        [[PyTango.DevShort, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
        
        "Over_Flow_Time":
        [[PyTango.DevShort, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],
                 
        "Geometrical_Correction_Flag":
        [[PyTango.DevShort, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],    
                          
        "Image_Format":
        [[PyTango.DevString, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],      
                  
        "Trigger_Mode":
        [[PyTango.DevString, 
         PyTango.SCALAR, 
         PyTango.READ_WRITE]],               
#           "ITHL":
#           [[PyTango.DevShort, 
#           PyTango.SCALAR, 
#           PyTango.READ_WRITE]],                   
        }

    def __init__(self,name) :
        PyTango.DeviceClass.__init__(self,name)
        self.set_type(name)

#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------
_imXPADCam = None
_imXPADInterface = None

def get_control(cam_ip_address = "localhost",port=3456,**keys) :
    print cam_ip_address,port
    global _imXPADCam
    global _imXPADInterface
    port = int(port)
    print "Getting control for IMXPAD: %s / %s" % (cam_ip_address, port)
    if _imXPADCam is None:
		_imXPADCam = XpadAcq.Camera(cam_ip_address,port)
		_imXPADInterface = XpadAcq.Interface(_imXPADCam)
    return Core.CtControl(_imXPADInterface)

def get_tango_specific_class_n_device():
    return imXPADClass,imXPAD
