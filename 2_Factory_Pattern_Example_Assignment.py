"""
SCENARIO
you're building ReportExporterFactory for a reporting tool that exports a 
generated report as PDF today. 
Product wants CSV and Markdown export next quarter, 
and an Excel export plus a "post straight to Slack" export are 
already on the roadmap after that.

Task: apply Factory Method to this. 
Name the Product interface and the method it requires. 
Name at least two concrete creator classes and which 
concrete product each one builds. 
Describe what the shared method on the Creator 
(something like export(report_data)) is 
responsible for, and what it explicitly does not know about.

"""

from abc import ABC, abstractmethod

# Product - what every file exported must do
class ReportExporter(ABC):

    @abstractmethod
    def create_report(self, filename):
        pass

# Once class per report type - that implements the contract
class PDFExporter(ReportExporter):

    def __init__(self):
        self._method = "Some tool that helps make pdf"

    def create_report(self, filename):
        print(f"Backend to export a PDF report {self._method}...")
        return f"PDF exported - {filename}.pdf"

class CSVExporter(ReportExporter):
    def __init__(self):
        self._method = "Some tool that helps make CSV files"
    
    def create_report(self, filename):
        print(f"Backend to export a CSV report using method {self._method}...")
        return f"CSV exported - {filename}.csv"

class ReportExporterFactory(ABC):

    @abstractmethod
    def create_exporter(self) -> ReportExporter:
        pass

    def report(self, filename):
        report_method = self.create_exporter()
        return report_method.create_report(filename)

class PDFReportExporterFactory(ReportExporterFactory):

    def create_exporter(self):
        return PDFExporter()

class CSVReportExportedFactory(ReportExporterFactory):

    def create_exporter(self):
        return CSVExporter()

reporter = PDFReportExporterFactory()
results = reporter.report("Excise_Printable")
print(results)
print("------------------------------------------------")

reporter = CSVReportExportedFactory()
results = reporter.report("Excise_Data")
print(results)
