
import isodate
import math
import os
import datetime

BENCHMARK_FILE = os.path.join(os.getcwd(), "compression_benchmarks.tsv")
COMPUITER_NAME = "HP"
class Algorithm:
	def __init__(self):
		self.setUpEnvironment()
		self.runWorkflow()
	def setUpEnvironment(self):
		if "name" not in dir(self):
			self.name = "Undefined_Name"
			self.ext = "Undefined_Ext"
	def runCommand(self, command, input_file, output_file):
		initial_time = datetime.datetime.now()

		#os.system(command)

		final_time = datetime.datetime.now()
		duration = final_time - initial_time

		initial_ext = os.path.splitext(input_file)[-1]
		final_ext 	= os.path.splitext(output_file)[-1]
		initial_size = os.getsize(input_file)
		final_size 	 = os.getsize(output_file)
		compression_ratio = final_size / initial_size

		score = self.calculate_score(compression_ratio, duration)

		benchmark = {
			'algorithmName': self.name,
			'compressionRatio': compression_ratio,
			'initialFileType': initial_ext,
			'initialSize': initial_size,
			'initialTime': start.isoformat(),
			'finalFileType': final_ext,
			'finalSize': final_size,
			'finalTime': stop.isoformat(),
			'duration': isodate.parse_duration(duration),
			'computer': COMPUTER_NAME,
			'score': score
		}

		self.updateLog(benchmark)
	def _getStandardValues(self):
		return 1, 1
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
		alpha = 1
		if use_log:
			weissman = alpha * (rate / standard_rate) * (math.log(standard_duration) / math.log(duration))
		else:
			weissman = alpha * (rate / standard_rate) * (standard_duration / duration)

		return weissman

	def saveBenchmark(self, new_line):
		with open(BENCHMARK_FILE, 'a') as file1:
			writer = csv.DictWriter(file1, delimiter = '\t')
			if os.getsize(BENCHMARK_FILE) == 0:
				writer.writeheader()
			writer.writerow(new_line)

class Zip(Algorithm):
	name = "zip"
	ext = ".zip"
	def _defineCommands(self):
		commands = {
			'': ""
		}

		return commands
	def runWorkflow(self):
		pass


def debug():
	string = """paq8f	5.467600	300	1.000000
				raq8g	5.514990	420	0.720477
				paq8hkcc	5.682593	300	1.039321
				paq8hp1	5.692566	300	1.041145
				paq8hp2	5.750279	300	1.051701
				paq8hp3	5.800033	300	1.060801
				paq8hp4	5.868829	300	1.073383
				paq8hp5	5.917719	300	1.082325
				paq8hp6	5.976643	300	1.093102
				paq8hp12	6.104276	540	0.620247
				decomp8	6.261574	540	0.63623
				decomp8	6.276295	540	0.637726"""
	standard_rate = 5.467600
	standard_duration = 300

	score = lambda a, b: (a / standard_rate) * (math.log(standard_duration) / math.log(b))

	for row in string.splitlines():

		row = row.strip().split('\t')
		rate = float(row[1])
		duration = int(row[2])
		print(row[0], '\t', score(rate, duration))

if __name__ == "__main__":
	debug()
