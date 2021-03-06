# -*- coding: utf-8 -*-
import os, subprocess
from base import TTSBackendBase

class FestivalTTSBackend(TTSBackendBase):
	provider = 'festival'
	def __init__(self):
		self.startFestivalProcess()
		
	def voices(self):
		p = subprocess.Popen(['festival','-i'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		d = p.communicate('(voice.list)')
		l = map(str.strip,d[0].rsplit('> (',1)[-1].rsplit(')',1)[0].split('\n'))
		return l
		
	def startFestivalProcess(self):
		#LOG('Starting Festival...')
		#self.festivalProcess = subprocess.Popen(['festival'],shell=True,stdin=subprocess.PIPE)
		pass
		
	def say(self,text,interrupt=False):
		if not text: return
		##self.festivalProcess.send_signal(signal.SIGINT)
		#self.festivalProcess = subprocess.Popen(['festival'],shell=True,stdin=subprocess.PIPE)
		voice = self.currentVoice()
		if voice: voice = '(voice_{0})\n'.format(voice)
		self.festivalProcess = subprocess.Popen(['festival','--pipe'],shell=True,stdin=subprocess.PIPE)
		self.festivalProcess.communicate('{0}(SayText "{1}")\n'.format(voice,text))
		#if self.festivalProcess.poll() != None: self.startFestivalProcess()
		
	def close(self):
		#if self.festivalProcess.poll() != None: return
		#self.festivalProcess.terminate()
		pass
	
	@staticmethod
	def available():
		try:
			subprocess.call(['festival', '--help'], stdout=(open(os.path.devnull, 'w')), stderr=subprocess.STDOUT)
		except (OSError, IOError):
			return False
		return True