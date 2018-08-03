Bpm
=======================

This is the new Bpm device, it replaces "BeamViewer" which was use to do a lot of different tasks.
This one is only use for Bpm purpose.
It takes images and calculate beam position using the Core.BPM module. Can also push Tango event containing modified image and several statistics and informations(listed above) in a DevEncoded attribut name bvdata.

Bpm plugin is launched through **LimaCCDs camera_name** script.


Properties
----------

====================    ====== ====================  ================================================================================================================
Propertie name          RW     Type                  Description                                                                               
====================    ====== ====================  ================================================================================================================
calibration             RW     DevVarDoubleArray     Contains the calibration in X and Y ([X,Y]), not affecting the image taken, just the way it is display.                                                                  |
beammark                RW     DevVarLongArray       Contains coordonates (X,Y) in pixels of a beam mark set by the user.
====================    ====== ====================  ================================================================================================================


Attributes
----------

====================    === ==========     ================================================================================================================
Attribute name		    RW	Type			Description
====================    === ==========     ================================================================================================================
buffersize              RW  DevLong         Size of the buffer where a certain amount of images will be store before re-writing on the first one.
txy                     RO  DevDouble       Intensity of the pixel with the coordinates (x,y) pass as argument.
x                       RO  DevDouble       coordinate on the x axis of the beam return by the BPM task. If the algorithm couldn't find a X value then it 
                                            is set at -1.
y                       RO  DevDouble       Same as x but for Y axis.
automaticaoi            RW  DevBoolean      true or false for the AOI mode.
intensity               RO  DevDouble       Intensity of the area around beam.
max_intensity           RO  DevDouble       Maximum intensity on the image.
proj_x                  RO  DevLong         Array containing sum of all pixel´s intensity on axis x
proj_y                  RO  DevLong         Same as proj_x but on y axis.
fwhm_x                  RO  DevDouble       Full width at half of maximum on the profil X.
fwhm_y                  RO  DevDouble       same as fwhm_x but on y axis profil.
autoscale               RW  DevBoolean      Activate autoscale transformation on the image. (use min and max intensity on it in order to scale).
lut_method              RW  DevString       Method used in the transformation of image. can be "LOG" or "LINEAR".
color_map               RW  DevBoolean      Image in black and white(color_map=false), or use a color map to display colors based on intensity.
bvdata                  RO  DevEncoded      Attribute regrouping the image (jpeg format) and numerous information on it, such as timestamp,
                                                number of the frame, x, y, txy, ...
                                                Everything is pack throught struck module and is either send in a Tango event or directly read.
                                                WARNING : You need to have the decode function in order to read (can be found in the webserver
                                                          Bpm, currently here : https://gitlab.esrf.fr/limagroup/bpm-web )
calibration             RW  DevDouble       Attribute version of the calibration property.
beammark                RW  DevLong         Attribute version of the beammark property.
====================    === ==========     ================================================================================================================


Commands
----------

====================    ==================== ====================     ================================================================================================================
Commands name		    Arg.IN               Arg.OUT			      Description
====================    ==================== ====================     ================================================================================================================
Start                   DevVoid              DevVoid                  Start Bpm device.
Stop                    DevVoid              DevVoid                  Stop Bpm device.
getResults              DevLong              DevVarDoubleArray        Take a number as parameter and return an array containing (framenb,x,y) values, starting to the
                                                                      frame number ask until there is no more image.
GetPixelIntensity       DevVarLongArray      DevLong                  Return the intensity of pixel (x,y) passed as parameters
HasBackground           DevVoid              DevBoolean               Is there a background already in place ?
TakeBackground          DevVoid              DevVoid                  Take the current image and set it as Background, using the Core.BACKGROUNDSUBSTRACTION module.
ResetBackground         DevVoid              DevVoid                  Reset the Background.
====================    ==================== ====================     ================================================================================================================

NOTE
----------
This plugin is suppose to replace old BeamViewer but there is only the Bpm functionnality for the moment.
Some other plugins will be create in the futur.
For the moment this plugin is mainly use in the bpm webserver application. (https://gitlab.esrf.fr/limagroup/bpm-web)
                                