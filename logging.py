# /home/thor/data_logging_v2/logging.py
import csv, os, time
from typing import Callable, Optional, Sequence, Any

def log_to_csv(
    duration_seconds: float,
    data_func: Callable[[], Optional[Any]],
    filename: str,
    interval: float = 1.0,
    fieldnames: Optional[Sequence[str]] = None,
    timestamp_field: Optional[str] = "timestamp",
    append: bool = False,
) -> int:
    if duration_seconds <= 0:
        return 0

    mode = "a" if append else "w"
    write_header = not (append and os.path.exists(filename))
    end = time.monotonic() + duration_seconds
    rows = 0
    next_time = time.monotonic()

    with open(filename, mode, newline="", encoding="utf-8") as f:
        writer = None
        while time.monotonic() < end:
            try:
                sample = data_func()
            except Exception:
                sample = None

            if sample is not None:
                if isinstance(sample, dict):
                    if timestamp_field:
                        sample = {**sample, timestamp_field: time.time()}
                    if writer is None:
                        keys = list(sample.keys()) if fieldnames is None else list(fieldnames)
                        writer = csv.DictWriter(f, fieldnames=keys)
                        if write_header:
                            writer.writeheader()
                            write_header = False
                    writer.writerow(sample)
                    rows += 1

                elif isinstance(sample, (list, tuple)):
                    # Allow list/tuple rows even when `fieldnames` not provided by
                    # auto-generating numeric column names. If `timestamp_field`
                    # is set, append the timestamp as an extra column.
                    row = list(sample)
                    if fieldnames is None:
                        # generate col0..colN-1 (and timestamp column if requested)
                        generated = [f"col{i}" for i in range(len(row))]
                        if timestamp_field:
                            generated.append(timestamp_field)
                        keys = generated
                    else:
                        keys = list(fieldnames)
                        if timestamp_field and timestamp_field not in keys:
                            # when user-supplied fieldnames don't include timestamp,
                            # add it so header and rows align
                            keys = keys + [timestamp_field]

                    # initialize writer when needed
                    if writer is None:
                        writer = csv.writer(f)
                        if write_header:
                            writer.writerow(list(keys))
                            write_header = False

                    # append timestamp value to the row if requested
                    if timestamp_field:
                        row = row + [time.time()]

                    writer.writerow(row)
                    rows += 1

            next_time += interval
            sleep = max(0.0, next_time - time.monotonic())
            # don't sleep past end
            if time.monotonic() + sleep > end:
                time.sleep(max(0.0, end - time.monotonic()))
            else:
                time.sleep(sleep)

    return rows


if __name__ == "__main__":
    import random
    def sample(): return {"t": round(20 + random.random()*5,2)}
    print("Wrote", log_to_csv(5, sample, "sample_log.csv", interval=1.0, timestamp_field=None))
