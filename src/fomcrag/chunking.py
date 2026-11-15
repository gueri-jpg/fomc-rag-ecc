"""Deterministic word windows; never cross a physical PDF page."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .preprocessing import LEXICAL_VERSION, WORD, lexical_tokens, raw_offset
from .storage import fingerprint


@dataclass(frozen=True)
class ChunkConfig:
    window_words: int = 256
    overlap_words: int = 40
    algorithm: str = "page-word-window-v1"

    def __post_init__(self) -> None:
        if type(self.window_words) is not int or type(self.overlap_words) is not int:
            raise ValueError("Window and overlap must be integers")
        if not 0 <= self.overlap_words < self.window_words:
            raise ValueError("Require window > overlap >= 0")

    @property
    def version(self) -> str:
        return f"words{self.window_words}_overlap{self.overlap_words}_v1"


def chunk_page(page: dict, config: ChunkConfig, corpus_version: str) -> list[dict]:
    words = list(WORD.finditer(page["text"]))
    chunks = []
    index_version = fingerprint([corpus_version, asdict(config), LEXICAL_VERSION])
    for start in range(0, len(words), config.window_words - config.overlap_words):
        end = min(start + config.window_words, len(words))
        char_start, char_end = words[start].start(), words[end - 1].end()
        text = page["text"][char_start:char_end]
        identity = [page["pdf_sha256"], page["document"], page["page"], char_start, char_end,
                    page["text_sha256"], corpus_version, asdict(config)]
        keep = ("document", "document_id", "source_pdf", "source_path", "meeting_date", "year",
                "document_type", "doc_type", "pdf_sha256", "page_id", "page", "page_start", "page_end")
        chunk = {key: page[key] for key in keep}
        chunk.update(chunk_id=fingerprint(identity), char_start=char_start, char_end=char_end,
                     raw_char_start=raw_offset(page["raw_offset_runs"], char_start),
                     raw_char_end=raw_offset(page["raw_offset_runs"], char_end - 1) + 1,
                     word_start=start, word_end=end, word_count=end - start,
                     text=text, bm25_tokens=lexical_tokens(text), lexical_version=LEXICAL_VERSION,
                     chunking_version=config.version, chunking_config=asdict(config),
                     corpus_version=corpus_version, index_version=index_version)
        chunks.append(chunk)
        if end == len(words):
            break
    return chunks
