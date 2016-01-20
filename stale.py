#!/usr/bin/env python3


# https://github.com/department-of-veterans-affairs/appeals-pm/issues

from github3 import login

import datetime as dt
import os
import re


with open(os.path.expanduser("~/.github.key"), 'r') as fd:
    key = fd.read().strip()


def process(org, repo):
    github = login('paultag', password=key)
    repo = github.repository(org, repo)
    for issue in repo.iter_issues(state='open'):
        if not issue.title.endswith(")"):
            continue
        target = re.findall("\([^\)]*\)", issue.title)
        if target == []:
            continue
        target = target[-1]
        when = dt.datetime.strptime(target, "(%m/%d)")
        when = dt.date(dt.datetime.now().year, when.month, when.day)
        if when < dt.date.today():
            overdue(issue)


def overdue(issue):
    for label in issue.labels:
        if label.name == 'overdue':
            return
    issue.add_labels('overdue')
    issue.create_comment(
        """\
This issue appears to be overdue. I've tagged the issue 'overdue'.

Please update the Bug title and remove the overdue label if the
deadline has changed.""")


if __name__ == "__main__":
    process("department-of-veterans-affairs", "appeals-pm")
