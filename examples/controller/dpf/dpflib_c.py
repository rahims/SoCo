'''
@author: irimi_at_gmx_de
   
   python pydpflib_c port 
   based on dpflib.c by  03/2012 <hackfin@section5.ch>

 Additional packages
  
  - Python Imaging Library (PIL)
  - dpf library (compiled pydpflib_c)
 
 are required
 
 History
 =======
 Version 0.1  2012-03-31 by irimi_at_gmx_de 
 Version 0.2  2012-04-19 by irimi_at_gmx_de : showImage Interface changed: optional param area              
 Version 0.3  2012-04-25 by irimi_at_gmx_de : switch to dpf import based on special dpf-ax patch              
  
'''

import Image
import dpf

PROPERTY_BRIGHTNESS   = 0x01
PROPERTY_FGCOLOR      = 0x02
PROPERTY_BGCOLOR      = 0x03
PROPERTY_ORIENTATION  = 0x10

class dpflib_c(object):
    '''
    DPF access library for AX206 based HW
    '''

    def __init__(self,device,name="dpflib_c"):
        self._device=None
        self.name = name
        self._height = 0
        self._width = 0
        try:
            self._device=dpf.open(device)
        except SystemError as e:
            print e 
            return
        self._width,self._height=self._device.getRes()
        self.setBacklight(3)
        
    def close (self):
        if self._device:
            self._device.close()
    
    def _setProperty(self, prop, value):
        if self._device:
            self._device.setProperty(prop,value)
        
    def __str__(self):
        sret=  "Display = %s " %self.name
        if self._width and self._height:
            if self._width > self._height:
                sret +="in landscape"
            else:
                sret +="in portrait"
            
            sret += " mode:\n\tX resolution = %d\n\tY resolution = %d" %(self._width,self._height)
        else:
            sret += "resolution unknown"
            
        return sret
    def setBacklight(self,value):
        self._setProperty(PROPERTY_BRIGHTNESS, value)

    def setBackgroundColor(self,value):
        self._setProperty(PROPERTY_BGCOLOR, value)

    def setForegroundColor(self,value):
        self._setProperty(PROPERTY_FGCOLOR, value)
        
    def setOrientation(self,value):
        self._setProperty(PROPERTY_ORIENTATION, value)

    def getRes(self):
        return (self._width,self._height)
         
    def showImage(self,image,area=None):
        ''' PIL image instance is required 
            Smaller images as DPF resolution can be placed with x,y parameter
        '''
        if area:
            x=area[0]
            y=area[1]
            w=area[2]
            h=area[3]
        else:
            x=0
            y=0
            w=self._width
            h=self._height
        
        ws,hs = image.size
        if ws+x>self._width or hs+y>self._height:
            w=self._width
            h=self._height
            image=image.resize((self._width -x, self._height-y), Image.BILINEAR)
        
        if image.mode.find("RGBA")==-1:
            image=image.convert("RGBA")

        self._device.showRGBAImage(x, y, w, h, image.tostring())
        
    def clear(self):
        self.showImage(Image.new('RGBA', (self._width, self._height), (0, 0, 0, 0)))
    
class DPFPearl_c(dpflib_c):
    '''
    create PERL DPF vendor / product specific instance
    '''
    def __init__(self):
        dpflib_c.__init__(self,"usb0","Pearl DPF")


class DPFPearlDemo_c(DPFPearl_c):
        
    def test(self):
        import time
        import ImageDraw
        if self._width >0:
            fd = '../gfx/dm.png'
            try:
                im = Image.open(fd)
            except:
                im = Image.new('RGB', (self._width,self._height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(im)
                draw.text((10, self._height / 2 - 20), "Could not open demo picture: %s"%(fd))
                draw.text((10, self._height / 2), "dpflib_c.py demo")
                draw.text((10, self._height / 2 + 20), "by irimi_at_gmx_de")
                
            #self.setBackgroundColor(127)
            #self.setForegroundColor(255)
            self.showImage(im)
            time.sleep(5)
            self.setBacklight(2)
            print ("DPF is dark")
            self.setOrientation(2)
            self.showImage(im)
            time.sleep(5)
            print ("DPF's orientation has changed")
            self.setBacklight(7)
            self.setOrientation(1)
            time.sleep(5)
            print ("DPF's orientation has changed again")
            self.showImage(im)
            #im.show() # 'display' (imagemagick)) or 'xv' has to be installed

if __name__ == '__main__':
    
    dpf=DPFPearlDemo_c()
    print dpf
    dpf.test()
    dpf.close()
    print ("... end of demo")
   
