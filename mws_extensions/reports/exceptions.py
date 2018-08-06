class ReportFailedError(ValueError):

    def __init__(self, report_request_id, status, *args):
        self.status = status
        self.report_request_id = report_request_id
        self.message = 'GetReportRequestList for report_request_id={} returned {}'.format(self.report_request_id, self.status)
        super(ReportFailedError, self).__init__(self.message, *args)
