Merlin Tango device
=========

This is the reference documentation of the Merlin Tango device.

you can also find some useful information about the camera models/prerequisite/installation/configuration/compilation in the :ref:`Merlin camera plugin <camera-merlin>` section.

Properties
----------

================= =============== =============== =========================================================================
Property name	  Mandatory       Default value   Description
================= =============== =============== =========================================================================
HostName          Yes             none            The detector IP address
CmdPort           No              6431            The tcp command port
DataPort          No              6432            The tcp data port
ImageWidth        No              512             The number of detector pixels
ImageHeight       No              512             The number of detector rasters
Chips             No              4               The number of detector medipix3 chips
Simulate          No              0               Command simulation mode
================= =============== =============== =========================================================================



Attributes
----------
======================= ======= ================ ======================================================================
Attribute name		    RW	    Type			 Description
======================= ======= ================ ======================================================================
acqRunning              ro      DevBoolean       Is acquisition active
chargeSumming           rw      DevString        Charge Summming mode (**ON/OFF**)
colourMode              rw      DevString        Colour mode (**MONOCHROME/COLOUR**)
continuousRW            rw      DevString        Continuous Collection (**ON/OFF**)
counter                 rw      DevString        Counter (**COUNTER0/COUNTER1/BOTH**)
depth                   rw      DevString        Counter depth (**BPP1/BPP6/BPP12/BPP24**)
fileDirectory           rw      DevString        Directory name if saving on Merlin PC
fileEnable              rw      DevString        Enable file saving to Merlin PC (**ON/OFF**)
fileName                rw      DevString        Filename if saving on Merlin PC
gain                    rw      DevString        Gain Settings (**SHGM/HGM/LGM/SLGM**)
operatingEnergy         rw      DevFloat         Energy keV  (0 < e < 999.99)             
softwareVersion         ro      DevFloat         Software version number
temperature             ro      DevFloat         Temperature degrees C
threshold0              rw      DevFloat         Threshold 0 keV (0 < th < 999.99)
threshold1              rw      DevFloat         Threshold 1 keV (0 < th < 999.99)
threshold2              rw      DevFloat         Threshold 2 keV (0 < th < 999.99)
threshold3              rw      DevFloat         Threshold 3 keV (0 < th < 999.99)
threshold4              rw      DevFloat         Threshold 4 keV (0 < th < 999.99)
threshold5              rw      DevFloat         Threshold 5 keV (0 < th < 999.99)
threshold6              rw      DevFloat         Threshold 6 keV (0 < th < 999.99)
threshold7              rw      DevFloat         Threshold 7 keV (0 < th < 999.99)
triggerStartType        rw      DevString        Trigger start mode (**INTERNAL/RISING_EDGE_TTL/FALLING_EDGE_TTL/RISING_EDGE_LVDS/FALLING_EDGE_LVDS/SOFT**)
triggerStopType         rw      DevString        Trigger stop mode (**INTERNAL/RISING_EDGE_TTL/FALLING_EDGE_TTL/RISING_EDGE_LVDS/FALLING_EDGE_LVDS/SOFT**)
triggerOutTTL           rw      DevString        TTL Trigger stop mode (**TTL/LVDS/TTL_DELAYED/LVDS_DELAYED/FOLLOW_SHUTTER/ONE_PER_ACQ_BURST/SHUTTER_AND_SENSOR_READ/OUTPUT_BUSY**)
triggerOutLVDS          rw      DevString        LVDS Trigger stop mode (**TTL/LVDS/TTL_DELAYED/LVDS_DELAYED/FOLLOW_SHUTTER/ONE_PER_ACQ_BURST/SHUTTER_AND_SENSOR_READ/OUTPUT_BUSY**)
triggerOutTTLInvert     rw      DevString        TTL Trigger invert mode (**NORMAL/INVERTED**)
triggerOutLVDSInvert    rw      DevString        LVDS Trigger invert mode (**NORMAL/INVERTED**)
triggerOutTTLDelay      rw      DevLong64        TTL Trigger delay ns (0 < del < 68719476720)
triggerOutLVDSDelay     rw      DevLong64        LVDS Trigger delay ns (0 < del < 68719476720)
triggerUseDelay         rw      DevString        Use Trigger delay (**ON/OFF**)
thScanNum               rw      DevLong          Threshold number to scan (0 < n < 7)
thStart                 rw      DevFloat         Threshold scan start energy keV (0 < e < 999.99)
thStep                  rw      DevFloat         Threshold scan step energy keV (0 < e < 999.99)
thStop                  rw      DevFloat         Threshold scan stop energy keV (0 < e < 999.99)
======================= ======= ======================= ======================================================================

Commands
--------

=======================	================ ======================= ===========================================
Command name		    Arg. in		     Arg. out		         Description
=======================	================ ======================= ===========================================
Init			        DevVoid 	     DevVoid                 Do not use
State			        DevVoid		     DevLong                 Return the device state
Status			        DevVoid		     DevString               Return the device state as a string
SoftTrigger             DevVoid          DevVoid			     Perform soft trigger
Abort                   DevVoid          DevVoid                 Abort
THScan                  DevVoid          DevVoid                 Perform threshold scan
ResetHW                 DevVoid          DevVoid                 Reset
=======================	================ ======================= ===========================================
