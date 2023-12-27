# Provider tag/metadata format types
from collections.abc import Mapping, Sequence

from typing_extensions import TypeAlias  # noqa: UP035

MappingTags: TypeAlias = Mapping[str, str]  # noqa: UP040

TupleSequenceTags: TypeAlias = Sequence[tuple[str, str]]  # noqa: UP040
