Mask
=======
The mask correction is very useful when you have some defective pixels on your detector sensor. Then you can provide a mask image file
which can either applies a fixed value for those defective pixel (mask type == **DUMMY**) or sets those pixels to zero count (mask type = **STANDARD**).

To set the correction  you must provide to the device a flatfield image file (**setFlatMaskImage** command) and then start the correction (**start** command).

Properties
----------
This device has no property.

Attributes
----------
======================= ======= ============= ======================================================================
Attribute name		RW	Type			Description
======================= ======= ============= ======================================================================
RunLevel		rw	DevShort      Run level in the processing chain, from 0 to N
type			rw	DevString     Set the type of mask correction:
					       - **DUMMY**, replace the pixel value with the mask image pixel value
					       - **STANDARD**, if the mask pixel value is equal to zero set the image pixel value to zero otherwise keep the image pixel value unchanged

State		 	ro 	State	      OFF or ON (stopped or started)
Status		 	ro	DevString     "OFF" "ON" (stopped or started)
======================= ======= ============= ======================================================================

Commands
--------

=======================	=============== =======================	===========================================
Command name		Arg. in		Arg. out		Description
=======================	=============== =======================	===========================================
getAttrStringValueList	DevString:	DevVarStringArray:	Return the authorized string value list for
			Attribute name	String value list	a given attribute name
Init			DevVoid 	DevVoid			Do not use
setMaskImage		DevString	DevVoid			full path for the mask image file
Start			DevVoid		DevVoid			set the correction active
State			DevVoid		DevLong			Return the device state
Status			DevVoid		DevString		Return the device state as a string
Stop			DevVoid		DevVoid			set the correction inactive 
=======================	=============== =======================	===========================================
