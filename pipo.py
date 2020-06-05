#!/usr/bin/python3

import sys
import pandas as pd
import datetime as dt
import numpy as np


NAME = "Melvin Kallmayer"


HELP = """{0} -- punch in, punch out

    USAGE:
      {0} [-md] INFILE

      where INFILE is a ;-seperated list of format
        
        date;start;stop     [HEADER]
        date1;start1;stop1
        date2;start2;stop2
        .
        .
        .
        dateN;startN;stopN

      holding start and stop times for respective days

    OPTIONS:

      -md  enable markdown-friendly output
""".format(sys.argv[0])


OUTSTR = """---
geometry: a4paper
header-includes:
    - \\pagenumbering{gobble}
---
```
================================================================


{0} - {1}
{2}



{3}

Total: {4}h






-------------------------------- ({2})


================================================================
```
"""


def main(markdown_friendly, infile):
    # read table
    work_df = pd.read_csv(infile, sep=';')
    times_start = pd.to_datetime(work_df['start'])
    times_stop = pd.to_datetime(work_df['stop'])
    # calc start-stop time offsets
    work_df['diff'] = times_stop - times_start
    # sum up total time worked
    total = work_df['diff'].sum().total_seconds() / 3600

    # output
    df_str     = work_df.to_string(index=False, justify='left')
    if (markdown_friendly):
        # to stdout in md format
        start_d = work_df['date'].values[0]
        stop_d  = work_df['date'].values[-1]
        print(OUTSTR.format(start_d, stop_d, NAME, df_str, total, gobble='{gobble}'))
    else:
        # to stdout in unformatted text
        time_str   = "Total number of hours worked: {}.".format(total)
        for s in [df_str, time_str]:
            print(s)

    return


if __name__ == "__main__":
    # parameter logic
    argc = len(sys.argv)

    markdown_friendly = False
    if (argc > 1):
        if ('h' in sys.argv[1]):
            print(HELP)
        else:
            markdown_friendly = '-md' in sys.argv
            infile = sys.argv[-1]
            main(markdown_friendly, infile)
    else:
        print(HELP)


