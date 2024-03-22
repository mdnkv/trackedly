from datetime import datetime


def map_entry_as_duration(entry):
    start_date_time = datetime.combine(entry.start_date, entry.start_time)
    finish_date_time = datetime.combine(entry.finish_date, entry.finish_time)
    return finish_date_time - start_date_time
