import sonoscontroller, sys, logging
import Image
import ui_out

from dpf.dpflib_c import DPFPearl_c





class ImageToLcd(DPFPearl_c):
        
    def put_image(self, image_path, alt_text='***'):
        import ImageDraw
        if self._width >0:
            fd = image_path
            try:
                im = Image.open(fd)
            except:
                im = Image.new('RGB', (self._width,self._height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(im)
                draw.text((10, self._height / 2 - 20), "file: %s"%(fd))
                draw.text((10, self._height / 2), alt_text)
                draw.text((10, self._height / 2 + 20), "by me")
                
            #self.setBackgroundColor(127)
            #self.setForegroundColor(255)
            self.showImage(im)
           



class LcdFilter(logging.Filter):
	
  def __init__(self):
    self.lcd = ImageToLcd()
  
  def put_image( self, image_path, alt_text):
    print image_path
    self.lcd.put_image( image_path, alt_text)
  
  def filter(self, rec):
	  
    if rec.levelno == logging.CRITICAL:
      print 'LCD mental'
      return True
	  
    if ui_out.cmd_start in rec.msg:
      print 'start lcd'
      return True
      
    if ui_out.cmd_stop in rec.msg:
      'stop lcd'
      return True

    if ui_out.cmd_stream_start in rec.msg:
      args = rec.msg.split( ',')
      args += ["Unknown"] * (3 - len(args))
      print 'len is '  + str(len (args))
      self.put_image(args[2], args[1])
      return True
          
    return True		



    
