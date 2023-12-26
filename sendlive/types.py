# Provider tag/metadata format types
from collections.abc import Mapping, Sequence
from typing import TypeAlias

MappingTags: TypeAlias = Mapping[str, str]

TupleSequenceTags: TypeAlias = Sequence[tuple[str, str]]
