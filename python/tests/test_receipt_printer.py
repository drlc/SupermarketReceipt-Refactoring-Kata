
import pytest
from receipt import Receipt
from receipt_printer import ReceiptPrinter


@pytest.fixture
def printer():
    return ReceiptPrinter()

class TestReceiptPrinterPresentTotal:
    #omitted for brevity
    pass

class TestReceiptPrinterPrintDiscount:
    #omitted for brevity
    pass

class TestReceiptPrinterPrintQuantity:
    #omitted for brevity
    pass

class TestReceiptPrinterPrintPrice:
    #omitted for brevity
    pass

class TestReceiptPrinterFormatLineWithWhiteSpace:
    #omitted for brevity
    pass

class TestReceiptPrinterPrintReceiptItem:
    #omitted for brevity
    pass

class TestReceiptPrinterPrintReceipt:

    @pytest.fixture
    def receipt(self, mocker):
        return mocker.Mock()
    
    @pytest.fixture(autouse=True)
    def print_item(self, printer, mocker):
        printer.print_receipt_item = mocker.Mock()

    @pytest.fixture(autouse=True)
    def print_discount(self, printer, mocker):
        printer.print_discount = mocker.Mock()

    @pytest.fixture(autouse=True)
    def present_total(self, printer, mocker):
        printer.present_total = mocker.Mock()
        printer.present_total.return_value = "total-mock"

    def test_empty_receipt(
            self, printer: ReceiptPrinter, receipt: Receipt
    ):  
        # given
        receipt.items = []
        receipt.discounts = []
        # when
        res = printer.print_receipt(receipt)
        # then
        assert res == "\ntotal-mock"
        printer.present_total.assert_called_once_with(receipt)

    def test_with_one_item_no_discounts(
            self, printer: ReceiptPrinter, receipt: Receipt
    ):  
        #omitted for brevity
        pass

    def test_with_multiple_items_no_discounts(
            self, printer: ReceiptPrinter, receipt: Receipt
    ):  
        #omitted for brevity
        pass

    def test_with_items_and_one_discount(
            self, printer: ReceiptPrinter, receipt: Receipt
    ):  
        #omitted for brevity
        pass

    def test_with_items_and_multiple_discount(
            self, printer: ReceiptPrinter, receipt: Receipt
    ):  
        #omitted for brevity
        pass