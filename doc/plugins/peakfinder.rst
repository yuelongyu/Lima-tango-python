PeakFinder
===========

This is a nice plugin developed at DESY which can find peaks on an image and returns the positions of the peaks.

Once the configuration is ok you can start the task using **Start** command and stop the task calling the **Stop** command.


Properties
----------
This device has no property.

Attributes
----------
======================= ======= ======================= ===================================================
Attribute name		RW	Type			Description
======================= ======= ======================= ===================================================
BufferSize		rw	DevLong	      		Circular buffer size in image, default is 128
ComputingMode		rw	DevString     		The computing algorithm :
					       		 - **MAXIMUM**, find peak at maximum 
					       		 - **CM**, find peak at center of mass

CounterStatus		ro	DevLong	      		 Counter related to the current number of proceeded images
RunLevel		rw	DevLong	      		 Run level in the processing chain, from 0 to N		
State		 	ro 	State	      		 OFF or ON (stopped or started)
Status		 	ro	DevString     		 "OFF" "ON" (stopped or started)
======================= ======= ======================= ===================================================


Commands
--------
=======================	================== ======================= =======================================
Command name		Arg. in		   Arg. out		   Description
=======================	================== ======================= =======================================
Init			DevVoid 	   DevVoid		   Do not use
readPeaks		DevVoid		   DevVarDoubleArray	   Return the peaks positions
					   frame0,x,y,frame1,..
setMaskFile		DevVarStringArray  DevVoid		   Full path of mask file
Start			DevVoid		   DevVoid		   Start the operation on image
State			DevVoid		   DevLong		   Return the device state
Status			DevVoid		   DevString		   Return the device state as a string
Stop			DevVoid		   DevVoid		   Stop the operation on image
=======================	================== ======================= =======================================
