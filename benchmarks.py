
import isodate
import math
import os
import datetime
import shlex
import subprocess
import csv
from pprint import pprint
import time
BENCHMARK_FILE = os.path.join(os.getcwd(), "compression_benchmarks.tsv")
STANDARD_BENCHMARK_FILENAME = "standard_benchmarks.tsv"
OUTPUT_FOLDER = "C:\\Users\\Deitrickc\\Documents\\UPMC Files\\Projects\\misc\\output files\\"
COMPUTER_NAME = os.getenv('COMPUTERNAME')
OVERWRITE_FILES = True #Whether to overwrite existing files (True) or skip over them (False)

def readCSV(filename, **kwargs):
	delimiter = kwargs.get('delimiter', kwargs.get('sep', '\t'))
	if os.path.exists(filename):
		with open(filename, 'r') as file1:
			reader = csv.DictReader(file1, delimiter = delimiter)
			reader = list(reader)
	else:
		headers = []
		reader = []

	if kwargs.get('fieldnames', False):
		return reader, headers
	else:
		return reader

def writeCSV(table, filename, **kwargs):
	#pprint(table)
	if len(table) == 0: return None
	if kwargs.get('fieldnames') is None:
		fieldnames = sorted(table[0].keys())
	delimiter = kwargs.get('delimiter', kwargs.get('sep', '\t'))
	with open(filename, 'w', newline = "") as file1:
		writer = csv.DictWriter(file1, delimiter = delimiter, fieldnames = fieldnames)
		writer.writeheader()
		writer.writerows(table)

def Terminal(command, label = "", filename = None):
	""" Calls the system shell.
		Parameters
		----------
			command: string
				The command to run.
			label: string
				Used to mark output in the console.
			filename: string
				If not None, will output to console as a file.
	"""
	if False:
		#print(command)
		process = os.system(command)
		output = ""
	else:
		command = shlex.split(command)
		process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		output = str(process.stdout.read(),'utf-8')
		#print(output)
		#updateConsoleLog(filename, command, output, label)
	return output

class Algorithm:
	def __init__(self, input_file, output_folder, **kwargs):
		"""
			Keyword Arguments
			-----------------
				label: string
					If a valid label is passed, only one configuration of the algorithm will be run.
					The results of this will be available from the self.getLastRun() method.
				ratio: float; default None
					the standard ratio to use when calculating the Weissman score.
				duration: int, float; default None
					The standard duration to use when calculating the Weissman score.
		"""
		self.tag = kwargs.get('tag', "")
		if self.tag != "": self.tag += '.'
		print("\tBenchmarking the algorithm used for", self.ext, 'files.')
		self.setUpEnvironment(kwargs)
		self.runWorkflow(input_file, output_folder, use_label = kwargs.get('label'))

	def __call__(self, label = None):
		""" Retrieves the results of the most recent run for each available configuration. """
		if label is None:
			_last_run = self._most_recent_run
		else:
			_last_run = self._most_recent_run.get(label)
		return _last_run

	def getResults(self, label = None):

		if label is None:
			return self._most_recent_run
		else:
			return self._most_recent_run[label]

	def setUpEnvironment(self, kwargs):
		#self.program = "C:/Program Files/PeaZip/res/7z/7z.exe"
		self.program = self.getProgramLocation()
		self.options = self.getAvailableOptions()
		self._most_recent_run = dict()
		self._last_run_label = None
		if "name" not in dir(self):
			self.name = "Undefined_Name"
			self.ext = "Undefined_Ext"
	def runCommand(self, label, input_file, output_folder):
		path, input_basename = os.path.split(input_file)
		output_file = os.path.join(output_folder, self.tag + input_basename + '.' + label + self.ext)
		initial_time = datetime.datetime.now()
		#start = time.time()

		command = self.getAlgorithmCommand(label, input_file, output_file)

		print("\t\tUsing settings as", label, end = ".")
		if not os.path.exists(output_file) or OVERWRITE_FILES:
			Terminal(command)
		else:
			print("\tThe file already existed.")
			return None

		final_time = datetime.datetime.now()
		#stop = time.time()
		duration = final_time - initial_time
		iso_duration = isodate.duration_isoformat(duration)
		print("\tFinished in", iso_duration)
		#duration = stop - start

		initial_ext = os.path.splitext(input_file)[-1]
		final_ext 	= os.path.splitext(output_file)[-1]
		initial_size = os.path.getsize(input_file)
		final_size 	 = os.path.getsize(output_file)
		compression_ratio = initial_size / final_size

		benchmark = {
			'algorithmName': self.name,
			'compressionRatio': compression_ratio,
			'initialFileType': initial_ext,
			'initialSize': initial_size,
			'initialTime': initial_time.isoformat(),
			'finalFileType': final_ext,
			'finalSize': final_size,
			'finalTime': final_time.isoformat(),
			'duration': iso_duration,
			'label': label,
			'computer': COMPUTER_NAME,
			'filename': os.path.basename(input_file)
		}

		return benchmark
	
	def runWorkflow(self, input_file, output_folder, use_label = None):
		"""
			Keyword Arguments
			-----------------
				'label': string
					If provided, all other commands will be skipped.
		"""
		#commands = self._defineCommands()
		available_labels = sorted(self.options.keys())
		if use_label is not None: 
			available_labels = [i for i in available_labels if i == use_label]
		for label in available_labels:

			self._most_recent_run[label] = self.runCommand(label, input_file, output_folder)
			self._last_run_label = label
	def getAlgorithmCommand(self, label, input_file, output_file):
		template = self.getCommandTemplate()
		command = template.format(
			program = self.program, 
			options = self.options[label], 
			input_file = input_file, 
			output_file = output_file,
			output_folder = os.path.dirname(output_file))

		return command
	def getCommandTemplate(self):
		return '{program} {options} "{output_file}" "{input_file}"'
	def getProgramLocation(self):
		return '\"F:\\Program Files\\PeaZip\\res\\7z\\7z.exe\"'
class Z7(Algorithm):
	name = "7z"
	ext = ".7z"
	def getAvailableOptions(self):
		options = {
			'fastest': 	"a -t7z -m0=LZMA2 -mmt=on -mx1 -md=64k -mfb=32 -ms=8m -mqs=on -sccUTF-8 -bb0",
			'normal': 	"a -t7z -m0=LZMA2 -mmt=on -mx5 -md=16m -mfb=32 -ms=2g -mqs=on -sccUTF-8 -bb0",
			'ultra': 	"a -t7z -m0=LZMA2 -mmt=on -mx9 -md=64m -mfb=64 -ms=4g -mqs=on -sccUTF-8 -bb0"
		}
		return options

class Arc(Algorithm):
	name = 'arc'
	ext = '.arc'
	def getProgramLocation(self):
		return '\"F:\\Program Files\\PeaZip\\res\\arc\\arc.exe\"'
	def getAvailableOptions(self):
		options = {
			'fastest': "a -m0 -s -rr -ae=aes",
			'normal': "a -m4 -s -rr -ae=aes",
			'ultra': "a -m9 -s -rr -ae=aes"
		}
		return options

class Pea(Algorithm):
	name = 'pea'
	ext = '.pea'
	def getProgramLocation(self):
		return '\"F:\\Program Files\\PeaZip\\res\\pea.exe\"'
	def getAvailableOptions(self):
		options = {
			'normal': '0 PCOMPRESS2 SHA3_256 CRC32 RIPEMD160 BATCH FROMCL'
		}
		return options
	def getCommandTemplate(self):
		template = '{program} PEA "{output_folder}" {options} "{input_file}"'
		return template

class Zip(Algorithm):
	name = "zip"
	ext = ".zip"
	def getAvailableOptions(self):
		options = {
			'fastest': 	"a -tzip -mm=Deflate -mmt=on -mx1 -mfb=32 -mpass=1 -sccUTF-8 -mem=AES256 -bb0",
			'normal': 	"a -tzip -mm=Deflate -mmt=on -mx5 -mfb=32 -mpass=1 -sccUTF-8 -mem=AES256 -bb0",
			'ultra': 	"a -tzip -mm=Deflate -mmt=on -mx9 -mfb=128 -mpass=10 -sccUTF-8 -mem=AES256 -bb0"
		}
		return options

class XZ(Algorithm):
	name = 'xz'
	ext = '.xz'
	def getAvailableOptions(self):
		options = {
			'fastest': 	"a -txz -mx1 -md=64k -mfb=32 -sccUTF-8 -bb0",
			'normal': 	"a -txz -mx5 -md=16k -mfb=32 -sccUTF-8 -bb0",
			'ultra': 	"a -txz -mx9 -md=64k -mfb=64 -sccUTF-8 -bb0"
		}
		return options
class Tar(Algorithm):
	name = 'tar'
	ext = '.tar'
	def getAvailableOptions(self):
		options = {
			'store': "a -ttar -mx0 -sccUTF-8 -bb0"
		}
		return options
class Gzip(Algorithm):
	name = 'gzip'
	ext = '.gzip'
	def getAvailableOptions(self):
		options = {
			'fastest': 	"a -tgzip -mx1 -mfb=8 -sccUTF-8 -bb0",
			'normal': 	"a -tgzip -mx5 -mfb=32 -sccUTF-8 -bb0",
			'ultra': 	"a -tgzip -mx9 -mfb=128 -sccUTF-8 -bb0"
		}

		return options

class Pipeline:
	def __init__(self, input_folder, output_folder):
		algorithms = [Z7, Arc, Gzip, Tar, Zip, XZ]
		self.standard_benchmarks = self._loadStandardBenchmarks()
		print("Running {0} algorithms...".format(len(algorithms)))
		for index, fn in enumerate(os.listdir(input_folder)):
			print(str(index+1) + ". Running the algorithms on ", fn)
			input_file = os.path.join(input_folder, fn)
			self.runAlgorithms(input_file, output_folder, algorithms)

	def _loadStandardBenchmarks(self):
		table = readCSV(STANDARD_BENCHMARK_FILENAME)
		benchmarks = dict()
		for row in table:
			benchmarks[row['filename']] = row

		return benchmarks

	def _saveStandardBenchmarks(self):
		writeCSV(list(self.standard_benchmarks.values()), STANDARD_BENCHMARK_FILENAME)

	def _updateStandardBenchmarks(self, basename, results):

		self.standard_benchmarks[basename] = results
		self._saveStandardBenchmarks()

	def getStandardValues(self, input_file, output_folder):
		basename = os.path.split(input_file)[-1]
		standard_results = self.standard_benchmarks.get(basename)
		if standard_results is None:
			standard_program = Zip(input_file, output_folder, label = 'normal', tag = 'benchmark')
			standard_results = standard_program.getResults('normal')
			self._updateStandardBenchmarks(basename, standard_results)

		return standard_results
	@staticmethod
	def convertDuration(duration, transform = None):
		if isinstance(duration, str):
			duration = isodate.parse_duration(duration)
		duration = (duration.days * 3600 * 24) + duration.seconds + (duration.microseconds / 1000000)
		duration = duration / 60
		if transform == 'log':
			duration = math.log(duration)
		if transform == 'sqrt':
			duration = math.sqrt(duration)
			duration = math.sqrt(duration) #fourth root scales better

		return duration

	def calculateWeissmanScore(self, ratio, duration, sratio, sduration):
		duration = self.convertDuration(duration, 'sqrt')
		sduration = self.convertDuration(sduration, 'sqrt')

		if True:
			duration = math.sqrt(duration)

		alpha = 1

		score = alpha * (ratio / float(sratio)) * (sduration / duration)
		return score
	def parseResults(self, results, standard_ratio, standard_duration):
		for label, result in results.items():
			if result is None: continue
			result['label'] = label
			score = self.calculateWeissmanScore(
				result['compressionRatio'],
				result['duration'],
				standard_ratio,
				standard_duration)
			result['score'] = score
			yield result
	def runAlgorithms(self, input_file, output_folder, algorithms):
		standard_benchmark = self.getStandardValues(input_file, output_folder)
		print('\tStandard Ratio: {:.3f}\tStandard Duration: {}'.format(float(standard_benchmark['compressionRatio']), standard_benchmark['duration']))
		for algorithm in algorithms:
			
			program = algorithm(input_file, output_folder)
			results = program.getResults()
			results = self.parseResults(results, standard_benchmark['compressionRatio'], 
				isodate.parse_duration(standard_benchmark['duration']))
			self.updateLogFile(list(results))
	def updateLogFile(self, rows):
		if isinstance(rows, dict):
			rows = [rows]
		if len(rows) == 0:
			return None
		fieldnames = sorted(rows[0].keys())
		with open(BENCHMARK_FILE, 'a', newline = "") as file1:
			writer = csv.DictWriter(file1, delimiter = '\t', fieldnames = fieldnames)

			if not os.path.exists(BENCHMARK_FILE) or os.path.getsize(BENCHMARK_FILE) == 0:
				writer.writeheader()
			writer.writerows(rows)

def main():
	base_folder = "D:\\Proginoskes\\Documents\\Github Sandbox\\compression-algorithm-benchmarks\\"
	input_folder = os.path.join(base_folder, "input_files")
	output_folder = os.path.join(base_folder, "output_files")
	standard_file = "standard_algorithm_metrics.json"
	standard = Pipeline(input_folder, output_folder)
		

def debug():
	for k, v in sorted(os.environ.items()):
		print('{:<20}\t{}'.format(k, v))
if __name__ == "__main__":
	main()
	#debug()