import copy
import json
import logging

from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run


log = logging.getLogger()

zappa_prompts = {
    "aws_region": "us-east-1",
    "profile_name": "default",
    "slim_handler": False,
    "s3_bucket": None,
    "timeout_seconds": 30,
    "certificate_arn": None,
    "domain": None,
    "vpc_config": {"SubnetIds": [None], "SecurityGroupIds": [None],},
}


zappa_settings = {
    "django_settings": "backend.settings",
    "project_name": ,
    # TODO how match runtimes, or at least raise an error
    "runtime": "python3.7",
}


def update_zappa_prompts(updates):
    prompts = copy.deepcopy(zappa_prompts)
    prompts.update(updates)
    return prompts


class ZappaSettings:
    filename = "zappa_settings.json"

    def update(self, env, updates):
        current = self.load()
        current[env] = updates
        self.dump(current)

        # Now certify the domain with the certificate manager.
        print("Certifying the domain with the certificate manager...")
        run(["zappa", "certify", env])

    def dump(self, data):
        with use_dir(Projects.BACKEND):
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=2)

    def load(self):
        with use_dir(Projects.BACKEND):
            try:
                with open(self.filename) as f:
                    return json.load(f)
            except FileNotFoundError:
                return {}

    def get_env_settings(self, env):
        current = self.load()
        env_data = current.get(env, {})
        if "extends" in env_data:
            # Make sure to include any settings this env might extend, but don't
            # overwrite the custom settings.
            base_data = current[env_data["extends"]]
            base_data.update(env_data)
            return base_data
        return env_data
