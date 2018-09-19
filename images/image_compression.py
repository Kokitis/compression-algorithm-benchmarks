from pathlib import Path
from dataclasses import dataclass
from typing import List, Union, Dict
import time
import subprocess
import math
import pandas

CommandType = List[Union[str, Path]]
mebi = 1024 ** 2


@dataclass
class Benchmark:
	name: str
	ext: str
	method: str
	initial_size: int
	final_size: int
	duration: float

	@property
	def ratio(self) -> float:
		return 100 * self.final_size / self.initial_size

	@property
	def change(self) -> float:
		c = (self.initial_size - self.final_size) / self.initial_size
		return 100 * c

	@property
	def score(self) -> float:
		s =  math.exp(math.sqrt(self.duration))/(self.ratio * self.initial_size )

		return s

	def to_dict(self) -> Dict[str, Union[str, float, int]]:
		return {
			'name':        self.name,
			# 'ext': self.ext,
			'method':      self.method,
			'initialSize': self.initial_size / mebi,
			'finalSize':   self.final_size / mebi,
			'duration':    self.duration,
			# 'ratio': self.ratio,
			'change':      self.change,
			'score':       self.score

		}


def get_command_zip(input_filename: Path, output_filename: Path) -> CommandType:
	command = ["zip", output_filename, input_filename]

	return command


def get_command_optipng(input_filename, output_filename) -> CommandType:
	command = ['optipng', '-o6', '-out', output_filename, input_filename]
	return command


def run_command(command: CommandType, input_filename: Path, output_filename: Path) -> Benchmark:
	initial_size = input_filename.stat().st_size
	# output_filename = output_folder / input_filename.name

	start_time = time.time()
	process = subprocess.call(command)
	end_time = time.time()

	duration = end_time - start_time
	final_size = output_filename.stat().st_size

	benchmark = Benchmark(
		name = input_filename.name,
		ext = input_filename.suffix,
		method = command[0],
		initial_size = initial_size,
		final_size = final_size,
		duration = duration
	)

	return benchmark

def png_to_jpg(input_filename:Path, output_filename:Path)->CommandType:
	command = ['convert', input_filename, output_filename]
	return command

def compress_workflow_png(output_folder: Path):
	png_folder = Path('./png images')
	benchmarks = list()
	for input_filename in png_folder.iterdir():
		output_filename = output_folder / input_filename.with_suffix('.jpg').name

		#command = get_command_optipng(input_filename, output_filename)
		command = png_to_jpg(input_filename, output_filename)
		result = run_command(command, input_filename, output_filename)
		benchmarks.append(result)

		#remove_output_folder(output_folder)

		#command = get_command_zip(input_filename, output_filename)
		#result = run_command(command, input_filename, output_filename)
		#benchmarks.append(result)

	return benchmarks



def save_output(results: List[Benchmark]):
	df = pandas.DataFrame([i.to_dict() for i in results])
	df = df.sort_values(by = 'change', ascending = False)
	df = df.round(3)[['name', 'method','score', 'change', 'duration', 'initialSize', 'finalSize']]

	print(df.to_string())
	df.to_csv(str(Path('./benchmarks.tsv')), sep = '\t', index = False)

	groups = df.groupby(by = 'method')

	for method, group in groups:
		print(group.median())


def remove_output_folder(folder: Path):
	for fn in folder.iterdir():
		fn.unlink()


if __name__ == "__main__":
	jpg_folder = Path('./jpg images')
	output_folder = Path('./temp_files')
	if not output_folder.exists():
		output_folder.mkdir()

	results = compress_workflow_png(output_folder)
	save_output(results)

	for fn in output_folder.iterdir():
		fn.unlink()
	output_folder.rmdir()
