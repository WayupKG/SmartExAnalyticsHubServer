from typing import TYPE_CHECKING, Generic, TypeVar

from pydantic import BaseModel

from app.schemas.base import PaginatedResponse

if TYPE_CHECKING:
    from collections.abc import Sequence

ResultScheme = TypeVar("ResultScheme", bound=BaseModel)


class Paginator(Generic[ResultScheme]):
    def __init__(
        self,
        results: Sequence[ResultScheme],
        page: int,
        per_page: int,
        total_count: int,
    ):
        self.results = results
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def number_of_pages(self) -> int:
        quotient, remainder = divmod(self.total_count, self.per_page)
        return quotient if remainder == 0 else quotient + 1

    def get_response(self) -> PaginatedResponse[ResultScheme]:
        return PaginatedResponse(
            count=self.total_count,
            number_of_pages=self.number_of_pages,
            results=list(self.results),
        )
