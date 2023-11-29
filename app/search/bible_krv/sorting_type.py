from enum import Enum


class SortingType(Enum):
    MATCH = (
        "MATCH",
        "정확도순",
        [
            {"_score": {"order": "desc"}},
            {"idx": {"order": "asc"}},
        ],
    )

    PAGE = (
        "PAGE",
        "페이지순",
        [
            {"idx": {"order": "asc"}},
        ],
    )

    @property
    def name(self):
        return self.value[0]

    @property
    def display_name(self):
        return self.value[1]

    @property
    def sort_query(self):
        return self.value[2]

    @classmethod
    def find_by_name(cls, name: str | None) -> "SortingType":
        if name is not None:
            name = name.strip().upper()
            for sorting_type in cls:
                if sorting_type.name == name:
                    return sorting_type

        return cls.MATCH

    @classmethod
    def options(cls):
        return [
            {
                "name": s.name,
                "display_name": s.display_name,
            }
            for s in cls
        ]

    @property
    def option(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
        }
