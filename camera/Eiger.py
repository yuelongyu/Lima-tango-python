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
# file :        Eiger.py
#
# description : Python source for the Eiger and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Eiger are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys

from Lima import Core
from Lima.Server import AttrHelper

#==================================================================
#   Eiger Class Description:
#
#
#==================================================================


class Eiger(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------
    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.init_device()

        self.__CountrateCorrection = {'ON':True,
                                      'OFF':False}
        self.__FlatfieldCorrection = {'ON':True,
                                      'OFF':False}
        self.__AutoSummation = {'ON':True,
                                'OFF':False}
        self.__EfficiencyCorrection = {'ON':True,
                                       'OFF':False}
        self.__VirtualPixelCorrection = {'ON':True,
                                         'OFF':False}
        self.__PixelMask = {'ON':True,
                            'OFF':False}


#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())
            
#------------------------------------------------------------------
#    getAttrStringValueList command:
#
#    Description: return a list of authorized values if any
#    argout: DevVarStringArray   
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        return AttrHelper.get_attr_string_value_list(self,attr_name)
#----------------------------------------------------------------------------
#                      delete all memory files
#----------------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def deleteMemoryFiles(self):
        _EigerCamera.deleteMemoryFiles()

#==================================================================
#
#    Eiger read/write attribute methods
#
#==================================================================
    def __getattr__(self,name) :
        return AttrHelper.get_attr_4u(self,name,_EigerCamera)

#==================================================================
#
#    Eiger command methods
#
#==================================================================

#==================================================================
#
#    EigerClass class definition
#
#==================================================================
class EigerClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'detector_ip_address':
        [PyTango.DevString,
         "Detector ip address",[]],
        }


    #    Command definitions
    cmd_list = {
        'getAttrStringValueList':
        [[PyTango.DevString, "Attribute name"],
         [PyTango.DevVarStringArray, "Authorized String value list"]],
        'deleteMemoryFiles':
        [[PyTango.DevVoid, ""],
         [PyTango.DevVoid, ""]],
        }


    #    Attribute definitions
    attr_list = {
        'temperature':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ]],
        'humidity':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ]],
        'countrate_correction':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'flatfield_correction':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'auto_summation':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'efficiency_correction':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'virtual_pixel_correction':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'pixel_mask':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'threshold_energy':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'photon_energy':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        }


#------------------------------------------------------------------
#    EigerClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)

#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------
from Lima import Eiger as EigerAcq

_EigerIterface = None
_EigerCamera = None

def get_control(detector_ip_address = "0",**keys) :
    global _EigerIterface
    global _EigerCamera
    if _EigerIterface is None:
        _EigerCamera = EigerAcq.Camera(detector_ip_address)
        _EigerIterface = EigerAcq.Interface(_EigerCamera)
    return Core.CtControl(_EigerIterface)

def get_tango_specific_class_n_device() :
    return EigerClass,Eiger
