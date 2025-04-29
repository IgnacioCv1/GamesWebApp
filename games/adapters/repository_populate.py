from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import read_csv_file, read_csv_file_memory

def populate_mem_repo(data_path: Path, repo: AbstractRepository, database_mode: bool, filename: str):
    read_csv_file_memory(repo, filename)
def populate(data_path: Path, repo: AbstractRepository, database_mode: bool, filename: str):
    read_csv_file(data_path, repo, database_mode, filename)
