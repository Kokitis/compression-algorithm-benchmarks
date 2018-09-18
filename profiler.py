from pathlib import Path
import math

from dataclasses import dataclass
from pytools import timetools
from pytools.datatools import datadict
import subprocess
from typing import List
from pprint import pprint

@datadict
@dataclass
class Metric:
	start: timetools.Timestamp
	end: timetools.Timestamp
	start_size: int
	end_size: int

	@property
	def duration(self) -> timetools.Duration:
		return self.end - self.start
	@property
	def ratio(self) -> float:
		return self.start_size / self.end_size


DATA_FOLDER = Path(__file__).with_name('data')


def compute_weissmann_score(r: int, t: int, r_index: int, t_index: int):
	alpha = 1.0

	score = alpha * (r / r_index) * (math.log(t_index) / math.log(t))

	return score


def compress_file(filename: Path, command_name: str, output_folder: Path) -> Metric:
	output_filename = output_folder / (filename.name + '.' + command_name)
	command = get_command(command_name, filename, output_filename)
	start_time = timetools.now()
	process = subprocess.call(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	end_time = timetools.now()
	if not output_filename.exists():
		raise FileNotFoundError(output_filename)

	start_size = filename.stat().st_size
	end_size = output_filename.stat().st_size

	metric = Metric(
		start_time,
		end_time,
		start_size,
		end_size
	)
	return metric


def get_command(key, input_file: Path, output_file: Path) -> List:
	return ["tar", "-cvf", output_file, input_file]


def workflow():
	output_folder = DATA_FOLDER.with_name('compressed_files')
	if not output_folder.exists(): output_folder.mkdir()

	input_files = [f for f in DATA_FOLDER.iterdir() if f.is_file()]

	commands = ["tar"]
	for filename in input_files:
		for command_name in commands:
			metric = compress_file(filename, command_name, output_folder)
			print(metric)
			print(metric.ratio)
			print(str(metric.duration))


if __name__ == "__main__":
	workflow()
