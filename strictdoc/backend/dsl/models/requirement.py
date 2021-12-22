from typing import Optional, List

from strictdoc.backend.dsl.document_reference import DocumentReference
from strictdoc.backend.dsl.models.node import Node
from strictdoc.backend.dsl.models.reference import Reference
from strictdoc.backend.dsl.models.special_field import SpecialField


class RequirementContext:
    def __init__(self):
        self.title_number_string = None


class Requirement(Node):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        requirement_type: str,
        statement: Optional[str],
        statement_multiline: Optional[str],
        uid,
        level: Optional[str],
        status,
        tags,
        references: List[Reference],
        title: Optional[str],
        body,
        rationale,
        rationale_multiline,
        comments,
        special_fields: List[SpecialField],
        requirements=None,
    ):
        assert parent
        assert isinstance(requirement_type, str)

        self.parent = parent

        self.requirement_type: str = requirement_type

        # TODO: Why textX creates empty uid when the sdoc doesn't declare the
        # UID field?
        self.uid = (
            uid.strip() if (isinstance(uid, str) and len(uid) > 0) else None
        )
        self.level: Optional[str] = level
        self.status = status
        self.tags = tags

        assert isinstance(references, List)
        self.references: List[Reference] = references

        self.title = title
        self.statement: Optional[str] = statement
        self.rationale = rationale
        self.comments = comments
        self.special_fields = special_fields
        self.requirements = requirements

        # For multiline fields:
        # Due to the details of how matching single vs multistring lines is
        # implemented, the rstrip() is done to simplify SDoc code generation.
        self.statement_multiline: Optional[str] = (
            statement_multiline.rstrip() if statement_multiline else None
        )
        self.body = body.rstrip() if body else None
        self.rationale_multiline = (
            rationale_multiline.rstrip() if rationale_multiline else None
        )

        # TODO: Is it worth to move this to dedicated Presenter* classes to
        # keep this class textx-only?
        self.ng_level = None
        self.ng_document_reference: Optional[DocumentReference] = None
        self.context = RequirementContext()

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"ng_level: {self.ng_level}, "
            f"uid: {self.uid}, "
            f"title_or_none: {self.title}, "
            f"statement: {self.statement}"
            ")"
        )

    def __repr__(self):
        return self.__str__()

    @property
    def has_meta(self):
        return (
            self.uid is not None
            or (self.tags is not None and len(self.tags) > 0)
            or self.status is not None
        )

    @property
    def is_requirement(self):
        return True

    @property
    def is_section(self):
        return False

    @property
    def is_composite_requirement(self):
        return False

    @property
    def document(self):
        return self.ng_document_reference.get_document()

    def get_requirement_references(self):
        if not self.references or len(self.references) == 0:
            return []
        references = []
        for reference in self.references:
            if reference.ref_type != "Parent":
                continue
            references.append(reference)
        return references

    def get_statement_single_or_multiline(self):
        if self.statement:
            return self.statement
        if self.statement_multiline:
            return self.statement_multiline
        return None

    def get_rationale_single_or_multiline(self):
        if self.rationale:
            return self.rationale
        if self.rationale_multiline:
            return self.rationale_multiline
        return None

    def switch_to_multiline_statement(self):
        if self.statement:
            assert self.statement_multiline is None
            self.statement_multiline = self.statement
            self.statement = None


class CompositeRequirement(Requirement):
    def __init__(self, parent, **fields):
        super().__init__(parent, **fields)
        self.ng_sections = []
        self.ng_document_reference: Optional[DocumentReference] = None
        self.ng_has_requirements = False

    @property
    def is_composite_requirement(self):
        return True

    @property
    def document(self):
        return self.ng_document_reference.get_document()


class Body:
    def __init__(self, parent, content):
        self.parent = parent
        self.content = content.strip()

    def __str__(self):
        return f"Body({self.content})"

    def __repr__(self):
        return self.__str__()


class RequirementComment:
    def __init__(self, parent, comment_single, comment_multiline):
        self.parent = parent
        self.comment_single = comment_single

        # Due to the details of how matching single vs multistring lines is
        # implemented, the rstrip() is done to simplify SDoc code generation.
        self.comment_multiline = (
            comment_multiline.rstrip() if comment_multiline else None
        )

    def __str__(self):
        return (
            f"Comment("
            f"comment_single: {self.comment_single}, "
            f"comment_multiline: {self.comment_multiline}"
            f")"
        )

    def __repr__(self):
        return self.__str__()

    def get_comment(self):
        comment = (
            self.comment_single
            if self.comment_single
            else self.comment_multiline
        )
        return comment
