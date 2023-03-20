from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

from tests.end2end.helpers.components.node.document_root import DocumentRoot
from tests.end2end.helpers.components.node.requirement import Requirement
from tests.end2end.helpers.components.node.section import Section
from tests.end2end.helpers.components.toc import TOC


class Screen:  # pylint: disable=invalid-name, too-many-public-methods
    def __init__(self, test_case: BaseCase) -> None:
        assert isinstance(test_case, BaseCase)
        self.test_case: BaseCase = test_case

    def assert_text(self, text: str) -> None:
        self.test_case.assert_text(text)

    def assert_no_text(self, text: str) -> None:
        self.test_case.assert_element_not_present(
            f"//*[contains(., '{text}')]", by=By.XPATH
        )

    # Assert fields content:
    # Method with the 'field_name' can be used,
    # but named methods are recommended.

    def assert_xpath_contains(self, xpath: str, text: str) -> None:
        # screen shared
        self.test_case.assert_element(
            f"{xpath}[contains(., '{text}')]", by=By.XPATH
        )

    # body

    def assert_on_screen(self, viewtype: str):
        self.test_case.assert_element(
            f'//body[@data-viewtype="{viewtype}"]',
            by=By.XPATH,
        )

    # Header.
    # Document title (all views)

    def assert_header_document_title(self, document_title: str) -> None:
        self.test_case.assert_element(
            "//*[@class='header__document_title']"
            f"[contains(., '{document_title}')]",
            by=By.XPATH,
        )

    # Empty pages.
    # Valid only for 3 views:
    # table & traceability & deep-traceability,
    # overridden for the document view.

    def assert_empty_view(
        self, placeholder: str = "document-main-placeholder"
    ) -> None:
        self.test_case.assert_element(f'//*[@data-testid="{placeholder}"]')

    def assert_not_empty_view(
        self, placeholder: str = "document-main-placeholder"
    ) -> None:
        self.test_case.assert_element_not_visible(
            f'//*[@data-testid="{placeholder}"]'
        )

    # Get:

    # DocumentRoot
    def get_root_node(self) -> DocumentRoot:
        DocumentRoot(self.test_case).assert_is_root_node()
        return DocumentRoot(self.test_case)

    # Section
    def get_section(self, node_order: int = 1) -> Section:
        Section(self.test_case, node_order).assert_is_section()
        return Section(self.test_case, node_order)

    # Requirement
    def get_requirement(self, node_order: int = 1) -> Requirement:
        Requirement(self.test_case, node_order).assert_is_requirement()
        return Requirement(self.test_case, node_order)

    # TOC
    def get_toc(self) -> TOC:
        TOC(self.test_case).assert_is_toc()
        return TOC(self.test_case)

    def assert_toc_contains(self, string: str) -> None:
        TOC(self.test_case).assert_toc_contains(string)

    def assert_toc_contains_not(self, string: str) -> None:
        TOC(self.test_case).assert_toc_contains_not(string)