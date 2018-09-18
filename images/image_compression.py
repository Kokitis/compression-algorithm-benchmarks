from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Union, Dict
import time
import subprocess
from pprint import pprint
CommandType = List[Union[str,Path]]
mebi = 1024**2
@dataclass
class Benchmark:
	name: str
	ext: str
	method: str
	initial_size: int
	final_size: int
	duration: float

	@property
	def ratio(self)->float:
		return self.final_size / self.initial_size

	@property
	def change(self)->float:
		c = (self.initial_size - self.final_size) / self.initial_size
		return c

	def to_dict(self)->Dict[str, Union[str,float,int]]:
		return {
			'name': self.name,
			#'ext': self.ext,
			'method': self.method,
			'initialSize': self.initial_size/mebi,
			'finalSize': self.final_size/mebi,
			'duration': self.duration,
			#'ratio': self.ratio,
			'change': self.change

		}



def get_command_zip(input_filename:Path, output_filename:Path)->CommandType:
	command = ["zip", output_filename, input_filename]

	return command

def compress_workflow_jpg(input_filename:Path, output_folder:Path):

	initial_size = input_filename.stat().st_size
	output_filename = output_folder / input_filename.name
	zip_command = get_command_zip(input_filename, output_filename.with_suffix('.zip'))

	start_time = time.time()
	process = subprocess.call(zip_command)
	end_time = time.time()

	duration = end_time - start_time
	final_size = output_filename.with_suffix('.zip').stat().st_size

	benchmark = Benchmark(
		name = input_filename.name,
		ext = input_filename.suffix,
		method = 'zip',
		initial_size = initial_size,
		final_size = final_size,
		duration = duration
	)

	return benchmark


if __name__ == "__main__":
	jpg_folder = Path('./jpg images')
	output_folder = Path('./temp_files')
	if not output_folder.exists():
		output_folder.mkdir()
	benchmarks = list()
	for input_filename in jpg_folder.iterdir():
		benchmarks.append(compress_workflow_jpg(input_filename, output_folder))


	benchmarks = [i.to_dict() for i in benchmarks]

	import pandas
	df = pandas.DataFrame(benchmarks)
	df = df.sort_values(by = 'change', ascending = False)
	df = df.round(3)[['name', 'method', 'change',  'duration', 'initialSize', 'finalSize']]

	print(df.to_string())
	df.to_csv(str(Path('./benchmarks.tsv')), sep = '\t', index = False)

	for fn in output_folder.iterdir():
		fn.unlink()
	output_folder.rmdir()
