from distutils.core import setup
import py2exe

setup(console=['BratsEvaluate.py'],
	  data_files=[('', ['RegistrationMetrics.exe',]),])