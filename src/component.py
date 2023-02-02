import logging
import copy

from keboola.csvwriter import ElasticDictWriter
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from client import EHubClient, EHubClientException

from json_parser_multi import MulitCsvJsonParser

# configuration variables
KEY_FETCH_CAMPAIGNS = "fetch_campaigns"
KEY_FETCH_VOUCHERS = "fetch_vouchers"

KEY_DESTINATION = "destination_settings"
KEY_LOAD_MODE = "load_mode"

DEFAULT_LOAD_MODE = "incremental_load"

REQUIRED_PARAMETERS = [KEY_FETCH_CAMPAIGNS, KEY_FETCH_VOUCHERS]
REQUIRED_IMAGE_PARS = []


# TODO ERROR HANDLING

class Component(ComponentBase):

    def __init__(self):
        self.client = None
        self.result_writers = {}
        self.incremental = None
        super().__init__()

    def run(self):
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        self.validate_image_parameters(REQUIRED_IMAGE_PARS)
        params = self.configuration.parameters
        self.client = EHubClient()

        destination_settings = params.get(KEY_DESTINATION, {})
        load_mode = destination_settings.get(KEY_LOAD_MODE, DEFAULT_LOAD_MODE)
        self.incremental = load_mode != "full_load"

        fetch_campaigns = params.get(KEY_FETCH_CAMPAIGNS)
        fetch_vouchers = params.get(KEY_FETCH_VOUCHERS)

        if fetch_campaigns:
            self.fetch_and_write_campaigns()
        if fetch_vouchers:
            self.fetch_and_write_vouchers()

        self._close_all_result_writers()

    def fetch_and_write_vouchers(self):
        logging.info("Fetching public voucher data")
        self._initialize_result_writer("voucher")
        for page in self.client.get_public_vouchers():
            self._get_result_writer("voucher").writerows(page)

    def fetch_and_write_campaigns(self):
        logging.info("Fetching public campaign data")
        self._initialize_result_writer("campaign")
        self._initialize_result_writer("campaign_categories")
        self._initialize_result_writer("campaign_commission_groups")
        parser = MulitCsvJsonParser(dont_parse_list=['commissions'])
        for page in self.client.get_public_campaigns():
            parsed = parser.parse_data(page, "campaign")
            self._get_result_writer("campaign").writerows(parsed["campaign"])
            self._get_result_writer("campaign_categories").writerows(parsed["categories"])
            self._get_result_writer("campaign_commission_groups").writerows(parsed["commissionGroups"])

    def _initialize_result_writer(self, object_name: str) -> None:
        if object_name not in self.result_writers:
            table_schema = self.get_table_schema_by_name(object_name)
            table_definition = self.create_out_table_definition_from_schema(table_schema, incremental=self.incremental)
            writer = ElasticDictWriter(table_definition.full_path, table_definition.columns)
            self.result_writers[object_name] = {"table_definition": table_definition, "writer": writer}

    def _get_result_writer(self, object_name: str) -> ElasticDictWriter:
        return self.result_writers.get(object_name).get("writer")

    def _close_all_result_writers(self) -> None:
        for object_name in self.result_writers:
            writer = self._get_result_writer(object_name)
            table_definition = self.result_writers.get(object_name).get("table_definition")
            writer.close()
            table_definition.columns = copy.deepcopy(writer.fieldnames)
            self.write_manifest(table_definition)


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
