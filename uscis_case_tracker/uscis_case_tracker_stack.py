import os
import subprocess
import configparser
from aws_cdk import core
from aws_cdk import aws_lambda as function
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_iam as iam


class UscisCaseTrackerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        tracker_lambda_name = "uscis-case-tracker-function"

        dependencies_layer = self.create_dependencies_layer(
            self.stack_name, tracker_lambda_name
        )

        configs = self.get_configs()

        tracker_lambda = function.Function(
            self,
            tracker_lambda_name,
            handler="tracker.handler",
            runtime=function.Runtime.PYTHON_3_8,
            code=function.Code.asset("src/lambdas"),
            layers=[dependencies_layer],
        )
        tracker_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["ses:SendEmail", "ses:SendRawEmail", "ses:SendTemplatedEmail"],
                resources=[
                    f"arn:aws:ses:us-east-1:{core.Stack.of(self).account}:identity/{configs['email']}",
                ],
            )
        )
        tracker_lambda.add_environment("CASE_NUMBER", configs["case_number"])
        tracker_lambda.add_environment("EMAIL", configs["email"])

        events.Schedule.cron()
        tracker_rule = events.Rule(
            self,
            "uscis-case-tracker-rule",
            schedule=events.Schedule.expression(f"cron({configs['schedule_cron']})"),
        )
        tracker_rule.add_target(targets.LambdaFunction(tracker_lambda))

    def get_configs(self):
        config = configparser.ConfigParser()
        config.read("environment.ini")
        return config.defaults()

    def create_dependencies_layer(self, stack_name, function_name):
        requirements_file = "src/requirements.txt"
        output_dir = f"layer/{function_name}"

        if not os.environ.get("SKIP_PIP"):
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}/python".split()
            )

        layer_id = f"{stack_name}-{function_name}-dependencies"
        layer_code = function.Code.from_asset(output_dir)
        return function.LayerVersion(self, layer_id, code=layer_code)
