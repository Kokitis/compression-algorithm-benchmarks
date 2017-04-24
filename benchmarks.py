
import isodate
import math
import os
import datetime
import shlex
import subprocess
import csv
import json

class StandardMethod:
	""" Retrieves the standard compression rate and duration for a given file."""
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, 'r') as file1:
			self.data = json.loads(file1.read())

	def updateStandard(self, filename, output_folder):
		""" Updates the standard with metrics for the given filename."""

		standard_mathod = self.getStandardMethod()

		metrics = standard_method(filename, output_folder, label = 'normal')
		
		self.data[os.path.basename(filename)] = {
			'compressionRate': metrics.compression_rate,
			'duration': metrics.duration
		}

		self.save()

		return metrics.compression_rate, metrics.duration

	def getStandardMethod(self):
		return ZIP
	def save(self):
		with open(self.filename, 'w') as file1:
			file1.write(json.dumps(self.data, sort_keys = True, indent = 4))
	def __call__(self, basename):
		compression_rate = self.data[basename]['compressionRate']
		duration = self.data[basename]['duration']

		return compression_rate, duration

BENCHMARK_FILE = os.path.join(os.getcwd(), "compression_benchmarks.tsv")
OUTPUT_FOLDER = "C:\\Users\\Deitrickc\\Documents\\UPMC Files\\Projects\\misc\\output files\\"
COMPUTER_NAME = "HP"

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
		#print(terminal_label)
		process = os.system(command)
		output = ""
	else:
		command = shlex.split(command)
		process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		output = str(process.stdout.read(),'utf-8')
		print(output)
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
		self.setUpEnvironment(kwargs)
		self.runWorkflow(input_file, output_folder)

	def __call__(self, label):
		""" Retrieves the results of the most recent run for each available configuration. """

		_last_run = self._most_recent_run.get(label)
		return _last_run

	def setUpEnvironment(self, kwargs):
		self.program = "C:\\Program Files\\PeaZip\\res\\7z\\7z.exe"
		self._most_recent_run = dict()

		self.standard_compression_ratio = kwargs.get('ratio')
		self.standard_duration = kwargs.get('duration')

		if "name" not in dir(self):
			self.name = "Undefined_Name"
			self.ext = "Undefined_Ext"
	def runCommand(self, command, label, input_file, output_folder):
		path, input_basename = os.path.split(input_file)
		output_file = os.path.join(output_folder, input_basename + self.ext)
		initial_time = datetime.datetime.now()

		command = command.format(program = self.program,
			input_folder = os.path.dirname(input_file),
			input_file = input_file,
			output_file = output_file)
		if not os.path.exists(output_file):
			Terminal(command)

		final_time = datetime.datetime.now()
		duration = final_time - initial_time

		initial_ext = os.path.splitext(input_file)[-1]
		final_ext 	= os.path.splitext(output_file)[-1]
		initial_size = os.path.getsize(input_file)
		final_size 	 = os.path.getsize(output_file)
		compression_ratio = initial_size / final_size

		score = self.calculateScore(compression_ratio, duration)

		benchmark = {
			'algorithmName': self.name,
			'compressionRatio': compression_ratio,
			'initialFileType': initial_ext,
			'initialSize': initial_size,
			'initialTime': initial_time.isoformat(),
			'finalFileType': final_ext,
			'finalSize': final_size,
			'finalTime': final_time.isoformat(),
			'duration': isodate.duration_isoformat(duration),
			'label': label,
			'computer': COMPUTER_NAME,
			'score': score
		}

		self.updateBenchmarkLog(benchmark)

		return compression_ratio, duration
	
	def runWorkflow(self, input_file, output_folder):
		"""
			Keyword Arguments
			-----------------
				'label': string
					If provided, all other commands will be skipped.
		"""
		commands = self._defineCommands()

		for label, command in commands.items():
			print("Running {0} ({1})".format(self.name, label))

			self._most_recent_run[label] = self.runCommand(command, label, input_file, output_folder)

	def _getStandardValues(self):
		if self.standard_compression_ratio is not None and self.standard_duration is not None:
			return self.standard_compression_ratio, self.standard_duration
	def calculateScore(self, rate, duration):
		""" 
			Parameters
			----------
				rate: float
					The compression rate
				duration: datetime.duration
					Compression time (will be formatted as seconds)
		"""
		use_log = False
		standard_rate, standard_duration = self._getStandardValues()
		duration = (duration.days * 3600 * 24) + duration.seconds + (duration.microseconds / 1000000)
		if duration == 0.0: return 0.0
		elif standard_rate is None or standard_duration is None:
			return 1.0
		alpha = 1
		if use_log:
			weissman = alpha * (rate / standard_rate) * (math.log(standard_duration) / math.log(duration))
		else:
			weissman = alpha * (rate / standard_rate) * (standard_duration / duration)

		return weissman

	def updateBenchmarkLog(self, new_line):
		fieldnames = sorted(new_line.keys())
		with open(BENCHMARK_FILE, 'a', newline = "") as file1:
			writer = csv.DictWriter(file1, delimiter = '\t', fieldnames = fieldnames)
			if os.path.getsize(BENCHMARK_FILE) == 0:
				writer.writeheader()
			writer.writerow(new_line)

class Zip(Algorithm):
	name = "zip"
	ext = ".zip"
	def _defineCommands(self):

		command = '\"{program}\" a -tzip -mm=Deflate -mmt=on -mx5 -mfb=32 -mpass=1 -sccUTF-8 -mem=AES256 -bb0 \"-w{input_folder}\" \"{output_file}\" \"{input_file}\"'
		commands = {
			'normal': command
		}

		return commands

def main():
	input_folder = "C:\\Users\\Deitrickc\\Documents\\UPMC Files\\Projects\\misc\\input files\\"
	output_folder = "C:\\Users\\Deitrickc\\Documents\\UPMC Files\\Projects\\misc\\output files\\"
	standard_file = "standard_algorithm_metrics.json"
	standard = StandardMethod(standard_file)
	for basename in os.listdir(input_folder):
		abs_path = os.path.join(input_folder, basename)

		standard_rate, standard_duration = standard.updateStandard(abs_path)

		for algorithm in algorithms:
			program = algorithm(abs_path, output_folder, standard_rate, standard_duration)
		


if __name__ == "__main__":
	main()
