Background Substraction
=======================

The Background substraction correction is a simple operation you can active when a detector has some dark-current 
noise independent of the dose of photons it will receive.
To set the correction  you must provide to the device a background image file (**setBackgroundImage** command) and 
then start the correction (**start** command). Instead of providing an external image file you can simply ask the device
to use an image taken. Call the command **takeNextAcquistionAsBackground** to set the internal background image from an acquisition image.
One can apply an extra offset correction using the **offset** attribute value.

Properties
----------
This device has no property.

Attributes
----------

======================= ======= ======================= ==========================================================================
Attribute name		RW	Type			Description
======================= ======= ======================= ==========================================================================
delete_dark_after_read  rw      DevBoolean              If true the device will delete the file after reading
                                                        Can be useful to not keep obsolete dark image file after use	
offset			rw	DevLong			Set a offset level to be applied in addition to the background correction
RunLevel		rw	DevLong                 Run level in the processing chain, from 0 to N
State		 	ro	State			OFF or ON (stopped or started)
Status		 	ro	DevString		"OFF" "ON" (stopped or started)
======================= ======= ======================= ==========================================================================


Commands
--------

================================ =============== ======================= ==============================================
Command name			 Arg. in	 Arg. out		 Description
================================ =============== ======================= ==============================================
Init				 DevVoid	 DevVoid		 Do not use
setBackgroundImage      	 DevString       DevVoid                 Full path of background image file
Start                   	 DevVoid         DevVoid		 Start the correction for next image
State				 DevVoid	 DevLong		 Return the device state
Status				 DevVoid	 DevString		 Return the device state as a string
Stop                    	 DevVoid         DevVoid                 Stop the correction after the next image 
takeNextAcquisitionAsBackground	 DevVoid	 DevVoid		 next taken image will replace the background
================================ =============== ======================= ==============================================


