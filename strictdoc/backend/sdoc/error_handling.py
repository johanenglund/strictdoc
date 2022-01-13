import os

from strictdoc.backend.sdoc.models.document_grammar import (
    DocumentGrammar,
    GrammarElementField,
)
from strictdoc.backend.sdoc.models.requirement import (
    Requirement,
    RequirementField,
)


class StrictDocSemanticError(Exception):
    def __init__(  # pylint: disable=too-many-arguments
        self, title, hint, example, line=None, col=None, filename=None
    ):
        super().__init__(title, hint, line, col, filename)
        self.title = title
        self.hint = hint
        self.example = example
        self.line = line
        self.col = col
        self.file_path = filename

    @staticmethod
    def unknown_requirement_type(
        requirement_type, line=None, col=None, filename=None
    ):
        return StrictDocSemanticError(
            title=f"Invalid requirement type: {requirement_type}",
            hint=None,
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def unregistered_field(field_name, line=None, col=None, filename=None):
        return StrictDocSemanticError(
            title=f"Invalid requirement field: {field_name}",
            hint=None,
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def missing_required_field(
        requirement: Requirement,
        grammar_field: GrammarElementField,
        line=None,
        col=None,
        filename=None,
    ):
        return StrictDocSemanticError(
            title=(
                f"Requirement is missing a field that is required by "
                f"grammar: {grammar_field.title}"
            ),
            hint=f"Requirement fields: [{requirement.dump_fields()}]",
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def unexpected_field_outside_grammar(  # pylint: disable=too-many-arguments
        requirement: Requirement,
        requirement_field: RequirementField,
        document_grammar: DocumentGrammar,
        line=None,
        col=None,
        filename=None,
    ):
        grammar_dump = document_grammar.dump_fields(
            requirement.requirement_type
        )
        return StrictDocSemanticError(
            title=(
                f"Unexpected field outside grammar: "
                f"{requirement_field.field_name}"
            ),
            hint=(
                f"Requirement fields: [{requirement.dump_fields()}], "
                f"Grammar fields: [{grammar_dump}]"
            ),
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def wrong_field_order(  # pylint: disable=too-many-arguments
        requirement: Requirement,
        document_grammar: DocumentGrammar,
        problematic_field: RequirementField,
        line=None,
        col=None,
        filename=None,
    ):
        assert isinstance(
            problematic_field, RequirementField
        ), f"{problematic_field}"
        requirement_dump = requirement.dump_fields()
        grammar_dump = document_grammar.dump_fields(
            requirement.requirement_type
        )
        return StrictDocSemanticError(
            title=f"Wrong field order for requirement: [{requirement_dump}]",
            hint=(
                f"Problematic field: {problematic_field.field_name}. "
                f"Compare with the document grammar: [{grammar_dump}] "
                f"for type: {requirement.requirement_type}"
            ),
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def invalid_choice_field(  # pylint: disable=too-many-arguments
        requirement: Requirement,
        document_grammar: DocumentGrammar,
        requirement_field: RequirementField,
        line=None,
        col=None,
        filename=None,
    ):
        return StrictDocSemanticError(
            title=(
                f"Requirement field has an invalid SingleChoice value: "
                f"{requirement_field.field_value}"
            ),
            hint=(
                f"Problematic field: {requirement_field.field_name}. "
                f"Compare with the document grammar: "
                f"["
                f"{document_grammar.dump_fields(requirement.requirement_type)}"
                f"] "
                f"for type: {requirement.requirement_type}"
            ),
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def invalid_multiple_choice_field(  # pylint: disable=too-many-arguments
        requirement: Requirement,
        document_grammar: DocumentGrammar,
        requirement_field: RequirementField,
        line=None,
        col=None,
        filename=None,
    ):
        return StrictDocSemanticError(
            title=(
                f"Requirement field has an invalid MultipleChoice value: "
                f"{requirement_field.field_value}"
            ),
            hint=(
                f"Problematic field: {requirement_field.field_name}. "
                f"Compare with the document grammar: "
                f"["
                f"{document_grammar.dump_fields(requirement.requirement_type)}"
                f"] "
                f"for type: {requirement.requirement_type}"
            ),
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def not_comma_separated_choices(  # pylint: disable=too-many-arguments
        requirement_field: RequirementField,
        line=None,
        col=None,
        filename=None,
    ):
        return StrictDocSemanticError(
            title=(
                f"Requirement field of type MultipleChoice is invalid: "
                f"{requirement_field.field_value}"
            ),
            hint="MultipleChoice field requires ', '-separated values.",
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def not_comma_separated_tag_field(  # pylint: disable=too-many-arguments
        requirement_field: RequirementField,
        line=None,
        col=None,
        filename=None,
    ):
        return StrictDocSemanticError(
            title=(
                f"Requirement field of type Tag is invalid: "
                f"{requirement_field.field_value}"
            ),
            hint="Tag field requires ', '-separated values.",
            example=None,
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def missing_special_fields(
        special_fields, line=None, col=None, filename=None
    ):
        example_field_components = []
        for special_field in special_fields:
            example_field_components.append(
                f"- NAME: {special_field.field_name}"
            )
            example_field_components.append("  TYPE: String")
        example_field_components.append("")
        example_field_components.append("[REQUIREMENT]")
        example_field_components.append("SPECIAL_FIELDS:")
        for special_field in special_fields:
            example_field_components.append(
                f"  {special_field.field_name}: {special_field.field_value}"
            )
        example_fields = os.linesep.join(example_field_components)
        return StrictDocSemanticError(
            "Requirements special fields are not registered document-wide.",
            (
                f"Requirement's special fields must be declared in "
                f"[DOCUMENT].SPECIAL_FIELDS: {special_fields}"
            ),
            f"[DOCUMENT]\nSPECIAL_FIELDS:\n{example_fields}",
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def field_is_missing_in_doc_config(
        field_name, field_value, line=None, col=None, filename=None
    ):
        example_field_components = []
        example_field_components.append(f"- NAME: {field_name}")
        example_field_components.append("  TYPE: String")
        example_field_components.append("")
        example_field_components.append("[REQUIREMENT]")
        example_field_components.append("SPECIAL_FIELDS:")
        example_field_components.append(f"  {field_name}: {field_value}")
        example_fields = os.linesep.join(example_field_components)
        return StrictDocSemanticError(
            f"Undeclared special field: {field_name}",
            (
                "Requirement's special fields must be declared in "
                "[DOCUMENT].SPECIAL_FIELDS"
            ),
            f"[DOCUMENT]\nSPECIAL_FIELDS:\n{example_fields}",
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def requirement_missing_special_fields(
        special_fields_required, line=None, col=None, filename=None
    ):
        missing_special_fields = ", ".join(special_fields_required)
        example_field_components = []
        example_field_components.append("[DOCUMENT]")
        example_field_components.append("SPECIAL_FIELDS:")
        for special_field in special_fields_required:
            example_field_components.append(f"- NAME: {special_field}")
            example_field_components.append("  TYPE: String")
        example_field_components.append("")
        example_field_components.append("[REQUIREMENT]")
        example_field_components.append("SPECIAL_FIELDS:")
        for special_field in special_fields_required:
            example_field_components.append(f"  {special_field}: Some value")
        example = os.linesep.join(example_field_components)

        return StrictDocSemanticError(
            (
                f"Requirement is missing required special fields: "
                f"{missing_special_fields}"
            ),
            (
                "All fields that are declared in "
                "[DOCUMENT].SPECIAL_FIELDS section as "
                "'REQUIRED: Yes' must be present in every requirement."
            ),
            f"{example}",
            line=line,
            col=col,
            filename=filename,
        )

    @staticmethod
    def requirement_missing_required_field(
        required_special_field, line=None, col=None, filename=None
    ):
        example_field_components = []
        example_field_components.append(f"- NAME: {required_special_field}")
        example_field_components.append("  TYPE: String")
        example_field_components.append("")
        example_field_components.append("[REQUIREMENT]")
        example_field_components.append("SPECIAL_FIELDS:")
        example_field_components.append(
            f"  {required_special_field}: Some value"
        )
        example_fields = os.linesep.join(example_field_components)
        return StrictDocSemanticError(
            (
                f"Requirement is missing a required special field: "
                f"{required_special_field}."
            ),
            (
                "All fields that are declared in "
                "[DOCUMENT].SPECIAL_FIELDS section as 'REQUIRED: Yes' "
                "must be present in every requirement."
            ),
            f"[DOCUMENT]\nSPECIAL_FIELDS:\n{example_fields}",
            line=line,
            col=col,
            filename=filename,
        )

    def to_print_message(self):
        message = ""
        message += f"error: could not parse file: {self.file_path}.\n"
        message += f"Semantic error: {self.title}\n"
        message += f"Location: {self.file_path}:{self.line}:{self.col}"
        if self.hint:
            message += f"\nHint: {self.hint}"
        if self.example:
            message += f"\nExample:\n{self.example}"
        return message