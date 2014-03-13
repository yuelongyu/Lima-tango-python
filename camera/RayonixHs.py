############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2014
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
# file :        RayonixHs.py
#
# description : Python source for the RayonixHs and its commands. 
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
import sys, types, os, time

from Lima import Core
from Lima import RayonixHs as RayonixHsModule
# import some useful helpers to create direct mapping between tango attributes
# and Lima interfaces.
from AttrHelper import get_attr_4u, get_attr_string_value_list

class RayonixHs(PyTango.Device_4Impl):

    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')
    
#==================================================================
#   RayonixHs Class Description:
#
#
#==================================================================

class RayonixHs(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------
    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.init_device()
        # dictionnaries to be used with AttrHelper.get_attr_4u
        self.__FastTrigger = {'ON':True,
                           'OFF':False}
        self.__Cooler = {'ON': True,
                             'OFF': False}
        self.__ShutterLevel = {'LOW':0,
                                   'HIGH':1}       
        self.__Attribute2FunctionBase = {'fast_trigger': 'FastExtTrigger',
                                         'shutter_level': 'ShutterLevel',
                                         'temperature': 'Temperature',
                                         'temperature_sp': 'TemperatureSP',
                                         'cooler': 'Cooler',
                                         'cooling_status': 'CoolingStatus',
                                         }
                                               
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
        self.set_state(PyTango.DevState.ON)

        # Load the properties
        self.get_device_properties(self.get_device_class())

        # Apply properties if any
        #if self.p_gain:
        #    _RayonixHsInterface.setPGain(self.p_gain)
            
            
        #if self.shutter_level:
        #    _RayonixHsInterface.setShutterLevel(self.__ShutterLevel[self.shutter_level])

#==================================================================
#
#    RayonixHs read/write attribute methods
#
#==================================================================


    def __getattr__(self,name) :
        return get_attr_4u(self, name, _RayonixHsInterface)


    ## @brief return the timing times, exposure and latency
    #  
    def read_timing(self, attr):
        timing=[]
        timing.append(_RayonixHsCamera.getExpTime())
        timing.append(_RayonixHsCamera.getLatTime())
        
        attr.set_value(timing,2)        
        

#==================================================================
#
#    RayonixHs command methods
#
#==================================================================

#------------------------------------------------------------------
#    getAttrStringValueList command:
#
#    Description: return a list of authorized values if any
#    argout: DevVarStringArray   
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        return get_attr_string_value_list(self, attr_name)
    

#==================================================================
#
#    RayonixHs class definition
#
#==================================================================
class RayonixHsClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }

    #    Device Properties
    device_property_list = {
        'config_path':
        [PyTango.DevString,
         'configuration path directory', []],
        }


    #    Command definitions
    cmd_list = {
        'getAttrStringValueList':
        [[PyTango.DevString, "Attribute name"],
         [PyTango.DevVarStringArray, "Authorized String value list"]]
        }


    #    Attribute definitions
    attr_list = {
        'fast_trigger':
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':'Fast trigger mode, see manual for usage',
             'unit': 'N/A',
             'format': '',
             'description': 'OFF or ON',
             }],
        }

#------------------------------------------------------------------
#    RayonixHsClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)

            
#----------------------------------------------------------------------------
#                              Plugins
#----------------------------------------------------------------------------
from Lima  import RayonixHs as RayonixHsAcq

_RayonixHsCamera = None
_RayonixHsInterface = None

def get_control(**keys) :
    #properties are passed here as string
    global _RayonixHsCamera
    global _RayonixHsInterface
    if _RayonixHsCamera is None:
        print '\n\nStarting and configuring the RayonixHs camera ...'
        _RayonixHsCamera = RayonixHsAcq.Camera()
        _RayonixHsInterface = RayonixHsAcq.Interface(_RayonixHsCamera)
        print '\n\nRayonixHs Camera (%s:%s) is started'%(_RayonixHsCamera.getDetectorType(),_RayonixHsCamera.getDetectorModel())
    return Core.CtControl(_RayonixHsInterface)

    
def get_tango_specific_class_n_device():
    return RayonixHsClass,RayonixHs

