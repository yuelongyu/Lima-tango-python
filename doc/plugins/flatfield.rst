FlatField
===========

The flat fied  correction can be used to remove artifacts from the images  that are caused by variations in the pixel-to-pixel sensitivity of the detector and/or by the distortions in the optical path. Here the correction consists in providing a reference image taken using a uniform photon exposure. Then each raw image will be corrected by dividing the pixel values by their corresponding reference values (flatfield image pixels).

To set the correction  you must provide to the device a flatfield image file (**setFlatFieldImage** command) and then start the correction (**start** command).

Properties
----------

This device has no property.

Attributes
----------
================ ======= ======================= =======================================================================
Attribute name   RW	 Type			 Description
================ ======= ======================= =======================================================================
RunLevel	 rw	 DevShort	 	 Run level in the processing chain, from 0 to N
normalize	 rw	 DevBoolean	 	 If true the flatfield image will be normalized first (using avg signal)
State		 ro	 State			 OFF or ON (stopped or started)
Status		 ro	 DevString		 "OFF" "ON" (stopped or started)
================ ======= ======================= =======================================================================

Commands
----------

=======================	=============== =======================	===========================================
Command name		Arg. in		Arg. out		Description
=======================	=============== =======================	===========================================
Init			DevVoid	 	DevVoid		 	Do not use
setFlatFieldImage       DevString       DevVoid                 Full path to flatfield image file
Start                   DevVoid         DevVoid		 	Start the correction for next image
State			DevVoid	 	DevLong		 	Return the device state
Status			DevVoid	 	DevString		Return the device state as a string
Stop                    DevVoid         DevVoid                 Stop the correction after the next image 
=======================	=============== =======================	===========================================

