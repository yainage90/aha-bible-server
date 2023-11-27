from elasticsearch_dsl import analyzer, char_filter, token_filter, tokenizer

INDEX_ANALYZER_NAME = "index_analyzer"
SEARCH_ANALYZER_NAME = "search_analyzer"


class KrAnalysis:
    clean_char_filter: char_filter

    nori_tokenizer: tokenizer

    synonym_filter: token_filter

    index_analyzer: analyzer
    search_analyzer: analyzer

    def __init__(self):
        self.clean_char_filter = self._create_clean_char_filter()
        self.synonym_filter = None
        self.nori_tokenizer = self._create_nori_tokenizer()
        self.synonym_filter = self._create_synonym_filter()
        self.index_analyzer = self._create_index_analyzer()
        self.search_analyzer = self._create_search_analyzer()

    def _create_clean_char_filter(self):
        return char_filter(
            "clean",
            type="pattern_replace",
            pattern="[^\\p{L}\\p{Nd}\\p{Blank}]",
            replacement="",
        )

    def _create_nori_tokenizer(self):
        return tokenizer(
            "custom_tokenizer",
            type="nori_tokenizer",
            decompound_mode="discard",
            user_dictionary_rules=[],
        )

    def _create_synonym_filter(self):
        return token_filter(
            "synonym_filter",
            type="synonym_graph",
            synonyms=[],
        )

    def _create_index_analyzer(self):
        return analyzer(
            INDEX_ANALYZER_NAME,
            type="custom",
            char_filter=[
                self.clean_char_filter,
            ],
            tokenizer=self.nori_tokenizer,
            filter=["lowercase"],
        )

    def _create_search_analyzer(self):
        return analyzer(
            SEARCH_ANALYZER_NAME,
            type="custom",
            char_filter=[
                self.clean_char_filter,
            ],
            tokenizer=self.nori_tokenizer,
            filter=[
                "lowercase",
                self.synonym_filter,
            ],
        )

    def analyzers(self):
        return [
            self.index_analyzer,
            self.search_analyzer,
        ]
