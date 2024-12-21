#!/usr/bin/env python3
"""
Simple script to shift time in srt subtitle file.
"""
from datetime import timedelta
import os
import re
import sys
from typing import Self


# 00:01:15,550
TIME_RE = re.compile(r'(-?\d{1,3}):(\d{2}):(\d{2}),(\d{3})')
SEP = "-->"


class SubtitleTimeParseError(Exception):
    pass


class SubtitleTime:
    """
    A simple resprentation of time delta in subtitle file (srt).

    A hand of methods are added for shifting, creating from and converting to
    subtitle time format.
    """

    __slots__ = ('hours', 'minutes', 'seconds', 'microseconds')
    def __init__(self,
        hours: int, minutes: int, seconds: int, microseconds: int
    ) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.microseconds = microseconds

    @classmethod
    def from_subtitle_time(cls, t: str) -> Self:
        match = TIME_RE.match(t.strip())
        if match is None:
            raise SubtitleTimeParseError('No time delta found')
        return cls.from_subtitile_match(match)

    @classmethod
    def from_subtitile_match(cls, m: re.Match) -> Self:
        hours, minutes, seconds, microseconds = [int(s) for s in m.groups()]

        # Verify
        if hours < 0:
            raise SubtitleTimeParseError('hours must be positive integer')
        if minutes < 0 or minutes >= 60:
            raise SubtitleTimeParseError('minutes must be in [0, 60]')
        if seconds < 0 or seconds >= 60:
            raise SubtitleTimeParseError('seconds must be in [0, 60]')
        if microseconds < 0:
            raise SubtitleTimeParseError('microseconds must positive integer')

        return cls(hours, minutes, seconds, microseconds)

    def to_subtitle_time(self):
        return f'{self.hours:0>2}:{self.minutes:0>2}:{self.seconds:0>2},{self.microseconds:0>3}'

    def __str__(self):
        return self.to_subtitle_time()

    def add_seconds(self, delta: float) -> None:
        n1, n2 = divmod(delta, 1)
        sec_delta = int(n1)
        msec_delta = int(1000 * round(n2, 3))

        microseconds = msec_delta + self.microseconds
        if microseconds >= 1000:
            self.microseconds = microseconds - 1000
            sec_delta += 1
        else:
            self.microseconds = microseconds

        seconds = sec_delta + self.seconds
        if seconds >= 60:
            self.seconds = seconds - 60
            min_detalta = 1
        else:
            self.seconds = seconds
            min_detalta = 0

        minutes = min_detalta + self.minutes
        if minutes >= 60:
            self.minutes = minutes - 60
            hour_detalta = 1
        else:
            self.minutes = minutes
            hour_detalta = 0
        
        self.hours += hour_detalta


def parse_time_span(line: str ) -> bool:
    # 00:01:15,550 --> 00:01:17,790
    parts = line.partition(SEP)
    start = TIME_RE.match(parts[0].strip())
    end = TIME_RE.match(parts[2].strip())
    if start is None or end is None:
        return None, None
    try:
        start_time = SubtitleTime.from_subtitile_match(start)
        end_time = SubtitleTime.from_subtitile_match(end)
        return start_time, end_time
    except SubtitleTimeParseError:
        return None, None


def shift_time_span(start: SubtitleTime, end: SubtitleTime, delta: float) -> str:
    start.add_seconds(delta)
    end.add_seconds(delta)
    return f'{start} {SEP} {end}\n'


def try_shift_line(line: str, delta: float) -> str | None:
    s, e = parse_time_span(line)
    if None in (s, e):
        return None
    new_line = shift_time_span(s, e, delta)
    return new_line


def usage():
    print('Usage: python3 srt_shift.py <srt_file> <seconds>')


def shift_srt(fpath: str, delta: float):
    with open(fpath, encoding='utf-8') as f:
        new_lines = []
        for line in f.readlines():
            new_time_span_line = try_shift_line(line, delta)
            new_lines.append(new_time_span_line or line)
    base_path, ext = os.path.splitext(fpath)
    new_fpath = f'{base_path}_shifted_{delta}{ext}'
    with open(new_fpath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        fpath = sys.argv[1]
        delta_str = sys.argv[2]

        if not os.path.exists(fpath):
            print('Specified srt file does not exist')
            sys.exit(127)

        try:
            delta = float(delta_str)
        except ValueError:
            delta = None
        if delta is None:
            print('Specified shift delta is not numeric')
            sys.exit(127)

        shift_srt(fpath, delta)