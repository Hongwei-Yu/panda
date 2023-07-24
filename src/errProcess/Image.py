import os,time

def SaveImage(driver,step_name):
    Rawpath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'./Image')
    NewPicture = Rawpath+'\\'+time.strftime('%Y:%y:%d:%H:%M:%S')+'_'+step_name+".png"
    driver.get_screenshot_as_file(NewPicture)