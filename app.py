#!/usr/bin/env python3

from aws_cdk import App

from eda_service.component import EdaServiceStack

app = App()
EdaServiceStack(app, "eda-service")

app.synth()
