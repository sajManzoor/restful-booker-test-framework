"""Concurrency utilities for test execution"""

import concurrent.futures


class ConcurrencyUtils:
    """Utilities for running concurrent operations in tests"""
    
    @staticmethod
    def run_concurrent_operations(operations, max_workers=3):
        """Run operations concurrently and return results"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(op) for op in operations]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
