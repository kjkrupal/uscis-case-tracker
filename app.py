#!/usr/bin/env python3
from aws_cdk import core
from uscis_case_tracker.uscis_case_tracker_stack import UscisCaseTrackerStack

app = core.App()
UscisCaseTrackerStack(app, "uscis-case-tracker")

app.synth()
