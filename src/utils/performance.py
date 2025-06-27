# src/utils/performance.py
"""Utilities για μέτρηση performance"""

import time
import functools
import psutil
import os
from typing import Callable, Any, Tuple


class Timer:
    """Context manager για μέτρηση χρόνου εκτέλεσης"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time
        print(f"{self.name} took {self.elapsed:.6f} seconds")


def measure_time(func: Callable) -> Callable:
    """Decorator για μέτρηση χρόνου εκτέλεσης συνάρτησης"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"{func.__name__} took {elapsed:.6f} seconds")
        return result
    
    return wrapper


def measure_time_and_memory(func: Callable) -> Callable:
    """Decorator για μέτρηση χρόνου και μνήμης"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Μέτρηση αρχικής μνήμης
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Εκτέλεση και μέτρηση χρόνου
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        # Μέτρηση τελικής μνήμης
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before
        
        elapsed = end - start
        print(f"{func.__name__}:")
        print(f"  Time: {elapsed:.6f} seconds")
        print(f"  Memory: {mem_used:.2f} MB")
        
        return result
    
    return wrapper


def benchmark_function(func: Callable, *args, n_runs: int = 10, **kwargs) -> Tuple[float, float]:
    """
    Τρέχει μια συνάρτηση n φορές και επιστρέφει μέσο χρόνο και τυπική απόκλιση.
    
    Returns:
        (mean_time, std_time)
    """
    import numpy as np
    
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        times.append(end - start)
    
    return np.mean(times), np.std(times)


def profile_complexity(func: Callable, input_sizes: list, generator: Callable, n_runs: int = 5):
    """
    Μετράει την πολυπλοκότητα μιας συνάρτησης για διάφορα μεγέθη input.
    
    Args:
        func: Η συνάρτηση προς μέτρηση
        input_sizes: Λίστα με μεγέθη input
        generator: Συνάρτηση που παράγει input δεδομένου μεγέθους
        n_runs: Πόσες φορές να τρέξει για κάθε μέγεθος
    
    Returns:
        Dict με input_sizes και αντίστοιχους χρόνους
    """
    results = {
        'sizes': input_sizes,
        'times': [],
        'std_devs': []
    }
    
    for size in input_sizes:
        print(f"Testing size: {size}")
        data = generator(size)
        mean_time, std_time = benchmark_function(func, data, n_runs=n_runs)
        results['times'].append(mean_time)
        results['std_devs'].append(std_time)
    
    return results