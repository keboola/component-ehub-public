import logging

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from client import EHubClient, EHubClientException

# configuration variables
KEY_API_TOKEN = '#api_token'

REQUIRED_PARAMETERS = [KEY_API_TOKEN]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):

    def __init__(self):
        self.client = None
        super().__init__()

    def run(self):
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        self.validate_image_parameters(REQUIRED_IMAGE_PARS)
        # params = self.configuration.parameters
        self.client = EHubClient()
        for dat in self.client.get_public_campaigns():
            print(dat)


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except EHubClientException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
