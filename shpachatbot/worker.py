from concurrent import futures
from typing import Callable, Iterable

from tqdm import tqdm


def worker_start(worker_func: Callable, worker_itr: Iterable, workers: int = 8, enable_tqdm: bool = True):
    with futures.ProcessPoolExecutor(max_workers=workers) as executor:
        if enable_tqdm:
            return list(tqdm(executor.map(worker_func, worker_itr), total=len(worker_itr)))
        return list(executor.map(worker_func, worker_itr))
