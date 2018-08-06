import time
import logging
import datetime

from mws.mws import Reports

from .utils import to_amazon_timestamp
from .base import RequestReportResponse, GetReportRequestListResponse
from .exceptions import ReportFailedError

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class AdvancedReports(Reports):
    """
    Advanced Reports class that allows to request_and_download report
    with a single function call.
    TODO: add back session support
    """

    def __init__(self, report_type, max_retries=5, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.report_type = report_type
        self.max_retries = max_retries
        super().__init__(**kwargs)

    def update_report_acknowledgements(self, report_ids=(), acknowledged=False):
        data = dict(Action='UpdateReportAcknowledgements', Acknowledged='true' if acknowledged else 'false')
        data.update(self.enumerate_param('ReportIdList.Id.', report_ids))
        return self.make_request(data)

    def _request(self, start_date=None, end_date=None, marketplaceids=()):
        """
        Send request to amazon to request new report for instances report type.

        :param start_date: Begin date range of records to include in the report.
        :param end_date: End date range of records to include in the report.
        :param marketplaceids:
        :return:
        """
        start_date = to_amazon_timestamp(start_date or (datetime.datetime.now() - datetime.timedelta(days=30)))
        end_date = to_amazon_timestamp(end_date or datetime.datetime.now())
        self.logger.debug('requesting {} between {} and {}'.format(self.report_type, start_date, end_date))
        parsed_response = self.request_report(self.report_type, start_date, end_date, marketplaceids)
        parsed_response.response.raise_for_status()
        return parsed_response.response.text

    def request(self, start_date=None, end_date=None, marketplaceids=()):
        return RequestReportResponse.load(self._request(start_date, end_date, marketplaceids))

    def _get_report_status(self, report_request_id):
        self.logger.debug('getting report request list for request id {}'.format(report_request_id))
        parsed_response = self.get_report_request_list(requestids=(report_request_id,))
        parsed_response.response.raise_for_status()
        return parsed_response.response.text

    def get_report_status(self, report_request_id):
        doc = self._get_report_status(report_request_id)
        return GetReportRequestListResponse.load(doc)

    def download(self, generated_report_id):
        self.logger.debug('downloading report for report id {}'.format(generated_report_id))
        parsed_response = self.get_report(generated_report_id)
        return parsed_response.response.text

    def poll(self, report_request_id):
        """
        Wait for report to finish processing and return the generate report id.

        :param report_request_id:
        :return:
        """
        report_status_response = self.get_report_status(report_request_id)
        report_status_info = report_status_response.report_request_info_list()[0]
        status = report_status_info.report_processing_status

        for i in range(0, self.max_retries):
            self.logger.debug('report_request_id={} report_processing_status={}'.format(report_request_id, status))
            # Completed date is `None` if report isn't finished processing, otherwise it's a datetime object
            done = bool(report_status_info.completed_date)
            if done:
                if status != '_DONE_':
                    raise ReportFailedError(report_request_id, status)
                break
            time.sleep(30)  # Wait a bit for the report status to change

            report_status_response = self.get_report_status(report_request_id)
            report_status_info = report_status_response.report_request_info_list()[0]
            status = report_status_info.report_processing_status

        else:
            raise ReportFailedError(report_request_id, status)

        return report_status_info.generated_report_id

    def request_and_download(self, start_date=None, end_date=None, marketplaceids=()):
        """
        request, wait, and download.

        :return:
        """
        requested_report_response = self.request(start_date, end_date, marketplaceids)
        report_id = self.poll(requested_report_response.request_report_result.report_request_id)
        report_contents = self.download(report_id)
        print(report_contents)
        self.update_report_acknowledgements(report_ids=(report_id,), acknowledged=True)
        return report_contents
