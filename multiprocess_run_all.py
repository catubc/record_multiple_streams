# imports
import os                                                                       
from multiprocessing import Pool                                                
import datetime                                                                             
import time
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                     
                      
if __name__ == '__main__':
	    
	  # if playing back wav file
	  duration = '5'  #PDF = r'C:\Users\user\Desktop\File_%s.pdf' % ite

      # miclocations
	  pos = ''
	  temp = ''
	  
	  root_dirs = [r'D:\july_15_epoch_tests'+pos+temp, r'E:\july_15_epoch_tests'+pos+temp]

    		  	  
	  #  ***************** TEST AUDIO *************************
	  if False:
	      n_epochs = 1

	      
		  #temp = '20000Hz'

		  #temp = 'USV_6'
		  #temp = 'USV_9'
		  #temp = 'USV_10'
		  #temp = 'USV_17'

		  # TONES
	      wav_fname = os.path.join(r"C:\data\data\waves\audiocheck.net_sin_7000Hz_0dBFS_.1s.wav")
		  #wav_fname = os.path.join(r"C:\data\data\waves\audiocheck.net_sin_20000Hz_0dBFS_.1s.wav")

		  # USVs
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_6.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_9_7Khz_clean.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_10_harmonics.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-15_03_51_56_415333_snippet_17.wav"

	  # ***************** RECORD ANIMALS*******************
	  else:
		 	  
		  # number of epochs of recording:
		  n_epochs = 1
		      
	  
	  start_time = datetime.datetime.utcnow()
	  start_time = start_time - datetime.timedelta(hours=4)
	  start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f').replace(" ", "_").replace(":","_")
	  print ("START TIME: ", start_time)
	  
	  for root_dir in root_dirs:
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
		
	  for epoch in range(n_epochs):
		  print ("RECORDING EPOCH # :", epoch, "  duration: ", duration,  " sec")
		  processes = (
			### #r'c:\data\record_multiple_streams\play_beeps2.py'+" "+root_dir+ " " + duration,
			#r'c:\data\record_multiple_streams\ttl_pulse.py'+" "+root_dirs[1]+ " " + duration+" "+wav_fname+" "+start_time,
			#r'c:\data\record_multiple_streams\play_wav.py'+" "+root_dirs[1]+ " " + duration+" "+wav_fname+" "+start_time,
			r'c:\data\record_multiple_streams\record_video.py'+" "+root_dirs[1]+ " " + duration+" "+start_time,
			r'c:\data\record_multiple_streams\record_audio.py'+" "+root_dirs[0]+ " " + duration+" "+start_time)                                    
			
		  with Pool(3) as pool:
			  res = pool.map(run_process, processes)
		
		  pool.close
		  
		  time.sleep(1)
