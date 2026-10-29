# Lab 9 Theory (Part A)

## 1. Shuffle volume

**(a)** 12,000,000 pairs × 40 B = 480,000,000 B = **480 MB** written to local disk by all mappers combined.

**(b)** With 4 machines each running 2 mappers and 1 reducer, each mapper's output is split evenly across the 4 reducers. The 1/4 that goes to the reducer on the same machine stays local, so 3/4 crosses the network: 480 MB × 3/4 = **360 MB**.

## 2. Failure and re-execution

**MapReduce:** The master detects that mapper 3 failed and reschedules the whole mapper 3 task on another worker, which rereads the same input split from the start. Its partial output is discarded. Reducers are not affected, because they only read output from map tasks that have finished, so they never saw the partial output. They read from the rerun once it completes.

**Spark:** Spark uses the RDD's lineage (the chain of transformations that built it) to recompute only the lost partition from its parent. If the input logs are cached in memory, it rebuilds the partition from the cached data instead of rereading the input from disk, so recovery is faster than rerunning mapper 3's whole task from scratch.

## 3. Systems reasoning

The reduce phase can't start until 90 s instead of 10 s, so the map phase takes 9 times longer. Only 7 × 10 + 90 = 160 of the 8 × 90 = 720 slot-seconds do work, so about 78% of the capacity sits idle waiting on one task.

**Mitigation:** speculative execution. The master runs a backup copy of the slow task on another machine and uses whichever finishes first.

## 4. Key skew

The job isn't done until the slowest reducer finishes, so the reduce phase takes **95 s** and sets the job's wall-clock time.

This is different from Problem 3. A straggler is slow because of the machine, so rerunning the task somewhere else fixes it. Here the reducer is slow because it has 78% of the data, so it would be slow on any machine.

**Mitigation:** a combiner. Each mapper adds up its own counts before the shuffle, so the hot reducer gets one partial count per mapper instead of millions of `(key, 1)` pairs.
