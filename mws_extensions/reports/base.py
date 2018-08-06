import logging
from lxml import etree
from functools import partial

from .utils import from_amazon_timestamp


def first_element_or_none(element_list):
    """
    Return the first element or None from an lxml selector result.
    :param element_list: lxml selector result
    :return:
    """
    if element_list:
        return element_list[0]
    return


def first_element(f):
    """
    function wrapper for _first_element_or_none.
    This is equivalent to using `return _first_element_or_none(xpath())`.
    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        return first_element_or_none(f(*args, **kwargs))
    return inner


def parse_bool(f):
    """
    Parse boolean from string.
    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        r = f(*args, **kwargs)
        if not r:
            return None
        return r.lower() == 'true'
    return inner


def parse_date(f):
    """
    Parse date from amazon timestamp.
    :param f:
    :return:
    """

    def inner(*args, **kwargs):
        ts = f(*args, **kwargs)
        if ts:
            return from_amazon_timestamp(ts)
        return
    return inner


class BaseElementWrapper(object):

    namespaces = {}
    # Used to create a dict from the instance attributes specified here.
    attrs = []
    orm_class = None

    def __init__(self, element):
        """
        :param element: Etree object of response body
        """
        # Assign placeholder element so that the partial on the elements xpath will not throw an error.
        if element is None:
            element = etree.fromstring('<Empty />')
        self.element = element

        self.xpath = partial(self.element.xpath, namespaces=self.namespaces)
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_namespace(self, ns_dict):
        """
        Use this method to assign the namespace after the class has been instantiated.
        Otherwise the xpath method of this class will not update with the new namespace.
        :param ns_dict:
        :return:
        """
        self.namespaces = ns_dict
        self.xpath = partial(self.element.xpath, namespaces=ns_dict)

    def to_dict(self):
        d = {}
        for attr in self.attrs:
            result = self.__getattribute__(attr)
            # If attribute is callable, then call the method and store the result
            if callable(result):
                result = result()

            if isinstance(result, list):
                l = []
                for x in result:
                    if hasattr(x, 'to_dict'):
                        l.append(x.to_dict())
                    else:
                        l.append(x)
                d[attr] = l
            else:
                if hasattr(result, 'to_dict'):
                    d[attr] = result.to_dict()
                else:
                    d[attr] = result
        return d

    @property
    def __dict__(self):
        return self.to_dict()

    def __str__(self):
        return etree.tostring(self.element)

    @classmethod
    def string_to_element(cls, s):
        if not s:
            s = '<Empty />'
        return etree.fromstring(s)

    @classmethod
    def load(cls, xml_string):
        return cls(cls.string_to_element(xml_string))


class GetReportRequestListResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['request_id', 'has_next', 'next_token', 'report_request_info_list']

    @property
    @first_element
    def request_id(self):
        return self.xpath('//a:RequestId/text()')

    @property
    @parse_bool
    @first_element
    def has_next(self):
        return self.xpath('//a:HasNext/text()')

    @property
    @first_element
    def next_token(self):
        return self.xpath('//a:NextToken/text()')

    def report_request_info_list(self):
        return [ReportRequestInfo(x) for x in self.xpath('//a:ReportRequestInfo')]


class RequestReportResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['request_report_result', 'request_id']

    @property
    def request_report_result(self):
        return ReportRequestInfo(self._request_report_result)

    @property
    @first_element
    def _request_report_result(self):
        return self.xpath('./a:RequestReportResult/a:ReportRequestInfo')

    @property
    @first_element
    def request_id(self):
        return self.xpath('//a:RequestId/text()')


class ReportRequestInfo(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = [
        'report_request_id',
        'report_type',
        'start_date',
        'end_date',
        'scheduled',
        'submitted_date',
        'report_processing_status',
        'generated_report_id',
        'completed_date',
        'started_processing_date'
    ]

    @property
    @first_element
    def report_request_id(self):
        return self.xpath('./a:ReportRequestId/text()')

    @property
    @first_element
    def report_type(self):
        return self.xpath('./a:ReportType/text()')

    @property
    @parse_date
    @first_element
    def start_date(self):
        return self.xpath('./a:StartDate/text()')

    @property
    @parse_date
    @first_element
    def end_date(self):
        return self.xpath('./a:EndDate/text()')

    @property
    @parse_bool
    @first_element
    def scheduled(self):
        return self.xpath('./a:Scheduled/text()')

    @property
    @parse_date
    @first_element
    def submitted_date(self):
        return self.xpath('./a:SubmittedDate/text()')

    @property
    @first_element
    def report_processing_status(self):
        return self.xpath('./a:ReportProcessingStatus/text()')

    @property
    @first_element
    def generated_report_id(self):
        return self.xpath('./a:GeneratedReportId/text()')

    @property
    @parse_date
    @first_element
    def completed_date(self):
        return self.xpath('./a:CompletedDate/text()')

    @property
    @parse_date
    @first_element
    def started_processing_date(self):
        return self.xpath('./a:StartedProcessingDate/text()')


class ReportInfo(BaseElementWrapper):

    namespaces = {
        'a': 'http://mws.amazonaws.com/doc/2009-01-01/'
    }

    attrs = {
        'report_type',
        'acknowledged',
        'acknowledged_date',
        'report_id',
        'report_request_id',
        'available_date'
    }

    @property
    @first_element
    def report_type(self):
        return self.xpath('./a:ReportType/text()')

    @property
    @parse_bool
    @first_element
    def acknowledged(self):
        return self.xpath('./a:Acknowledged/text()')

    @property
    @parse_date
    @first_element
    def acknowledged_date(self):
        return self.xpath('./a:AcknowledgedDate/text()')

    @property
    @first_element
    def report_id(self):
        return self.xpath('./a:ReportId/text()')

    @property
    @first_element
    def report_request_id(self):
        return self.xpath('./a:ReportRequestId/text()')

    @property
    @parse_date
    @first_element
    def available_date(self):
        return self.xpath('./a:AvailableDate/text()')

    def __repr__(self):
        return '<{} report_type={} report_id={} available_date={}>'.format(
            self.__class__.__name__,
            self.report_type,
            self.report_id,
            self.available_date
        )


class GetReportListResponse(BaseElementWrapper):

    namespaces = {
        'a': 'http://mws.amazonaws.com/doc/2009-01-01/'
    }

    attrs = {
        'has_next',
        'next_token',
        'request_id',
        'report_info_list'
    }

    @property
    @parse_bool
    @first_element
    def has_next(self):
        return self.xpath('./a:GetReportListResult/a:HasNext/text()')

    @property
    @first_element
    def next_token(self):
        return self.xpath('./a:GetReportListResult/a:NextToken/text()')

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def report_info_list(self):
        return [ReportInfo(x) for x in self.xpath('./a:GetReportListResult//a:ReportInfo')]

    def __repr__(self):
        return '<{} has_next={} report_info_list={}>'.format(
            self.__class__.__name__,
            self.has_next,
            self.report_info_list()
        )
