import os                                                                       
from multiprocessing import Pool                                                
import datetime                                                                             
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                      
                      
if __name__ == '__main__':
	  from multiprocessing import Pool
	  root_dir = r'E:\july10'
	  duration = '4'  #PDF = r'C:\Users\user\Desktop\File_%s.pdf' % ite
	  wav_fname = os.path.join(r"E:\waves\audiocheck.net_sin_7000Hz_0dBFS_.1s.wav")
	  
	  start_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f').replace(" ", "_").replace(":","_")
	  print ("START TIME: ", start_time)
	  
	  try: 
		  os.mkdir(root_dir)
	  except:
		  pass
			
	  try:
		  os.mkdir(os.path.join(root_dir,'video'))
	  except:
		  pass
	  try:
		  os.mkdir(os.path.join(root_dir,'audio'))
	  except:
		  pass
	  try:
		  os.mkdir(os.path.join(root_dir,'times'))
	  except:
		  pass
			
			
	  processes = (
		#r'c:\data\national_instruments\ttl_pulse.py'+" "+root_dir+ " " + duration,
		r'c:\data\national_instruments\play_wav.py'+" "+root_dir+ " " + duration+" "+wav_fname+" "+start_time,
		r'c:\data\national_instruments\record_video.py'+" "+root_dir+ " " + duration+" "+start_time,
		r'c:\data\national_instruments\record_audio.py'+" "+root_dir+ " " + duration+" "+start_time)                                    

	  with Pool(3) as pool:
	     res = pool.map(run_process, processes)
    
                                                              
#pool = Pool(processes=3)                                                        
#pool.map(run_process, processes) 
