import os
from datetime import date, datetime, time, timedelta


def last_weekday(target_weekday):
    today = date.today()
    days_delta = target_weekday - today.weekday()
    if days_delta >= 0:
        days_delta -= 7

    last_weekday = today + timedelta(days=days_delta)

    return last_weekday


programs = [
    {
        "service": "radiko",
        "station": "INT",
        "name": "barakanbeat",
        "weekday": 6,
        "start": time(18, 0),
        "duration": timedelta(minutes=120),
    }
]


def get_command(program, output_dir=""):
    start = datetime.combine(last_weekday(program["weekday"]), program["start"])
    vars = dict(
        program,
        **{
            "start_str": start.strftime("%Y%m%d%H%M%S"),
            "end_str": (start + program["duration"]).strftime("%Y%m%d%H%M%S"),
        }
    )
    filename = "{service}_{station}_{name}_{start_str}.m4a".format(**vars)
    cmd = [
        "./radi.sh",
        "-t",
        vars["service"],
        "-s",
        vars["station"],
        "-d",
        vars["duration"],
        "-o",
        os.path.join(output_dir, filename),
        "-b",
        vars["start_str"],
        "-e",
        vars["end_str"],
    ]

    return " ".join(map(str, cmd))


print(get_command(programs[0]))