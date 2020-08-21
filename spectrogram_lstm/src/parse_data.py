import numpy as np

def create_batch_from_file(label, samples, rate, starts):
    starts = np.asarray(starts)
    if len(samples.shape) > 1:
        raise "samples be of shape (n,) where 'n' is the number of samples"

    split_locations = (starts * rate).astype(int)
    batches = np.split(samples, split_locations)
    labels = list([label for _ in batches])

    return labels, batches