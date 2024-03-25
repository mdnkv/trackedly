from datetime import datetime, timedelta


def map_entry_as_duration(entry):
    start_date_time = datetime.combine(entry.start_date, entry.start_time)
    finish_date_time = datetime.combine(entry.finish_date, entry.finish_time)
    return finish_date_time - start_date_time


def get_total_duration(entries):
    entries_durations = list(map(lambda entry: map_entry_as_duration(entry), entries))
    total = timedelta()
    for e in entries_durations:
        total += e
    return total


def get_total_duration_as_hours(entries):
    raw_duration = get_total_duration(entries)
    return int(raw_duration.total_seconds() / 3600)
