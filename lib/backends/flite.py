# -*- coding: utf-8 -*-
import os, subprocess
from base import ThreadedTTSBackend

class FliteTTSBackend(ThreadedTTSBackend):
	provider = 'Flite'
	interval = 100
	
	def __init__(self):
		self.process = None
		self.threadedInit()
		
	def threadedSay(self,text):
		if not text: return
		voice = self.currentVoice() or 'kal16'
		self.process = subprocess.Popen(['flite', '-voice', voice, '-t', text])
		self.process.wait()
		
	def threadedInterrupt(self):
		self.stopProcess()
		
	def stopProcess(self):
		if self.process:
			try:
				self.process.terminate()
				self.process.wait()
			except:
				pass
			
	def voices(self):
		return subprocess.check_output(['flite','-lv']).split(': ',1)[-1].strip().split(' ')
		
	def stop(self):
		self.process.terminate()
		
	def close(self):
		self.stopProcess()
		self.threadedClose()

	@staticmethod
	def available():
		try:
			subprocess.call(['flite', '--help'], stdout=(open(os.path.devnull, 'w')), stderr=subprocess.STDOUT)
		except (OSError, IOError):
			return False
		return True

#class FliteTTSBackend(TTSBackendBase):
#	provider = 'Flite'
#	def __init__(self):
#		import ctypes
#		self.flite = ctypes.CDLL('libflite.so.1',mode=ctypes.RTLD_GLOBAL)
#		flite_usenglish = ctypes.CDLL('libflite_usenglish.so.1',mode=ctypes.RTLD_GLOBAL) #analysis:ignore
#		flite_cmulex = ctypes.CDLL('libflite_cmulex.so.1',mode=ctypes.RTLD_GLOBAL) #analysis:ignore
#		flite_cmu_us_slt = ctypes.CDLL('libflite_cmu_us_slt.so.1')
#		self.flite.flite_init()
#		self.voice = flite_cmu_us_slt.register_cmu_us_slt()
#
#	def say(self,text,interrupt=False):
#		if not text: return
#		self.flite.flite_text_to_speech(text,self.voice,'play')
#		
#		
#	@staticmethod
#	def available():
#		try:
#			import ctypes
#			ctypes.CDLL('libflite.so.1')
#		except (OSError, IOError):
#			return False
#		return True
		
#class FliteTTSBackend(TTSBackendBase):
#	provider = 'Flite'
#
#	def say(self,text,interrupt=False):
#		if not text: return
#		voice = self.currentVoice() or 'kal16'
#		subprocess.call(['flite', '-voice', voice, '-t', text])
#		
#	def voices(self):
#		return subprocess.check_output(['flite','-lv']).split(': ',1)[-1].strip().split(' ')
#		
#	@staticmethod
#	def available():
#		try:
#			subprocess.call(['flite', '--help'], stdout=(open(os.path.devnull, 'w')), stderr=subprocess.STDOUT)
#		except (OSError, IOError):
#			return False
#		return True