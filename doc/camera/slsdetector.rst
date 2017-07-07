SlsDetector Tango device
========================

This is the reference documentation of the PSI SlsDetector Tango device.

You can also find some useful information about the camera models/prerequisite/installation/configuration/compilation in the :ref:`SlsDetector camera plugin <camera-slsdetector>` section.


Properties
----------

=============== =============== =============== ==============================================================
Property name	Mandatory	Default value	Description
=============== =============== =============== ==============================================================
config_fname	Yes		-		Path to the SlsDetector config file
=============== =============== =============== ==============================================================


Attributes
----------
======================= ======= ======================= ===========================================================
Attribute name		RW	Type			Description
======================= ======= ======================= ===========================================================
config_fname		ro	DevString		Path to the SlsDetector config file
hostname_list		ro	DevVarStringArray	The list of the Eiger half-modules' hostnames
dac_name_list		ro	DevVarStringArray	The list of the DAC signals' names
dac_<signal_name>	rw	DevVarLongArray		Array with the DAC <signal_name> value for each half-module, in A/D units
dac_name_list_mv	ro	DevVarStringArray	The list of the DAC signals' names supporting milli-volt units
dac_<signal_name>_mv	rw	DevVarLongArray		Array with the DAC <signal_name> value for each half-module, in milli-volt units
adc_name_list		ro	DevVarStringArray	The list of the ADC signals' names
adc_<signal_name>	rw	DevVarDoubleArray	Array with the ADC <signal_name> value for each half-module, in user units (deg C, etc.)
pixel_depth		rw	DevString		The image pixel bit-depth:
							 - **4** (not implemented in LImA yet)
							 - **8**
							 - **16**
							 - **32**
raw_mode		rw	DevBoolean		Publish image as given by the Receivers (no SW reconstruction)
threshold_energy	rw	DevLong			The energy (in eV) the pixel discriminator thresholds (Vcmp & Trim bits) is set at
all_trim_bits		rw	DevVarLongArray		Array with the pixel trimming value [0-63] for each half-module, if all the pixels in the half-module have the same trimming value, -1 otherwise
clock_div		rw      DevString               The readout clock divider:
							 - **FULL_SPEED**
							 - **HALF_SPEED**
							 - **QUARTER_SPEED**
							 - **SUPER_SLOW_SPEED**
readout_flags		rw	DevString		The flags affecting the readout mode (Parallel|NonParallel|Safe + StoreInRAM|Continous):
							 - **PARALLEL + STORE_IN_RAM**
							 - **PARALLEL + CONTINUOUS**
							 - **NON_PARALLEL + STORE_IN_RAM**
							 - **NON_PARALLEL + CONTINUOUS**
							 - **SAFE + STORE_IN_RAM**
							 - **SAFE + CONTINUOUS**
======================= ======= ======================= ===========================================================

Please refer to the *PSI/SLS Eiger User's Manual* for more information about the above specfic configuration parameters.

Commands
--------

=======================	=============== =======================	===========================================
Command name		Arg. in		Arg. out		Description
=======================	=============== =======================	===========================================
Init			DevVoid 	DevVoid			Do not use
State			DevVoid		DevLong			Return the device state
Status			DevVoid		DevString		Return the device state as a string
getAttrStringValueList	DevString:	DevVarStringArray:	Return the authorized string value list for
			Attribute name	String value list	a given attribute name
putCmd			DevString	DevVoid			Command setting a SlsDetector parameter (no response)
getCmd			DevString	DevString		Command getting a SlsDetector parameter (with response)
			get command	command result 
=======================	=============== =======================	===========================================
