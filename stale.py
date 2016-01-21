#!/usr/bin/env python3


from github3 import login

import datetime as dt
import time
import os
import re


KEY = os.environ['GITHUB_ACCESS_TOKEN']
USER = os.environ['GITHUB_USER_NAME']


def process(org, repo):
    github = login(USER, password=KEY)
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
    print("Overdue: {}".format(issue.title))
    for label in issue.labels:
        if label.name == 'overdue':
            return
    print("  (marked as overdue)")
    issue.add_labels('overdue')
    issue.create_comment(
        """\
This issue appears to be overdue. I've tagged the issue 'overdue'.

Please update the Bug title and remove the overdue label if the
deadline has changed.""")


def main(stayalive=False):
    while True:
        process_repos()
        if not stayalive:
            break
        time.sleep(86400)


def process_repos():
    process("department-of-veterans-affairs", "appeals-pm")
    process("department-of-veterans-affairs", "test-pm")


if __name__ == "__main__":
    process("department-of-veterans-affairs", "appeals-pm")
