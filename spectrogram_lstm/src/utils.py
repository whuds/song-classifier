import time

def profile(fn):
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time
        print(f'{elapsed_time} seconds')

        return ret

    return with_profiling