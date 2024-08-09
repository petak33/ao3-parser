from .extra import Extra
from .params import Params

from datetime import datetime
import urllib.parse

class Search:
    Fandom: str
    Sort_by: Params.Sort
    Sort_Direction: Params.Direction

    Include_Ratings: list[Params.Rating]
    Include_Warnings: list[Params.Warning]
    Include_Categories: list[Params.Category]
    Exclude_Ratings: list[Params.Rating]
    Exclude_Warnings: list[Params.Warning]
    Exclude_Categories: list[Params.Category]

    Crossovers: Params.Crossovers
    Single_Chapter: bool
    Completion_Status: Params.Completion

    Words_Count: str
    Hits_Count: str
    Kudos_Count: str
    Comments_Count: str
    Bookmarks_Count: str

    Date_From: datetime
    Date_To: datetime

    def __init__(self, Fandom: str, Sort_by: Params.Sort = Params.Sort.Revised, Sort_Direction: Params.Direction = None,
                 Include_Ratings: list[Params.Rating] = None, Include_Warnings: list[Params.Warning] = None, Include_Categories: list[Params.Category] = None,
                 Exclude_Ratings: list[Params.Rating] = None, Exclude_Warnings: list[Params.Warning] = None, Exclude_Categories: list[Params.Category] = None,
                 Crossovers: Params.Crossovers = Params.Crossovers.Include, Completion_Status: Params.Completion = Params.Completion.All, Single_Chapter: bool = False,
                 Words_Count: str = None, Hits_Count: str = None, Kudos_Count: str = None, Comments_Count: str = None, Bookmarks_Count: str = None,
                 Date_From: datetime = None, Date_To: datetime = None):
        self.Fandom = Fandom
        self.Sort_by = Sort_by
        self.Sort_Direction = Sort_Direction

        self.Include_Ratings = Extra.MakeIter(Include_Ratings)
        self.Include_Warnings = Extra.MakeIter(Include_Warnings)
        self.Include_Categories = Extra.MakeIter(Include_Categories)
        self.Exclude_Ratings = Extra.MakeIter(Exclude_Ratings)
        self.Exclude_Warnings = Extra.MakeIter(Exclude_Warnings)
        self.Exclude_Categories = Extra.MakeIter(Exclude_Categories)

        self.Crossovers = Crossovers
        self.Completion_Status = Completion_Status
        self.Single_Chapter = Single_Chapter

        self.Words_Count = Words_Count
        self.Hits_Count = Hits_Count
        self.Kudos_Count = Kudos_Count
        self.Comments_Count = Comments_Count
        self.Bookmarks_Count = Bookmarks_Count

        self.Date_From = Date_From
        self.Date_To = Date_To

    def getParams(self, page=1) -> dict:
        params = {
            "page": page,
            "work_search[sort_column]": self.Sort_by.value,
            "tag_id": self.Fandom
        }
        if self.Sort_Direction:
            params["work_search[sort_direction]"] = self.Sort_Direction.value

        if self.Include_Ratings:
            params["include_work_search[rating_ids][]"] = Extra.EnumsToValues(self.Include_Ratings)
        if self.Include_Warnings:
            params["include_work_search[archive_warning_ids][]"] = Extra.EnumsToValues(self.Include_Warnings)
        if self.Include_Categories:
            params["include_work_search[category_ids][]"] = Extra.EnumsToValues(self.Include_Categories)
        if self.Exclude_Ratings:
            params["exclude_work_search[rating_ids][]"] = Extra.EnumsToValues(self.Exclude_Ratings)
        if self.Exclude_Warnings:
            params["exclude_work_search[archive_warning_ids][]"] = Extra.EnumsToValues(self.Exclude_Warnings)
        if self.Exclude_Categories:
            params["exclude_work_search[category_ids][]"] = Extra.EnumsToValues(self.Exclude_Categories)

        if self.Crossovers and self.Crossovers.value:
            params["work_search[crossover]"] = self.Crossovers.value
        if self.Completion_Status and self.Completion_Status.value:
            params["work_search[complete]"] = self.Completion_Status.value
        if self.Single_Chapter:
            params["work_search[single_chapter]"] = 1

        if self.Words_Count:
            params["work_search[word_count]"] = self.Words_Count
        if self.Hits_Count:
            params["work_search[hits]"] = self.Hits_Count
        if self.Kudos_Count:
            params["work_search[kudos_count]"] = self.Kudos_Count
        if self.Comments_Count:
            params["work_search[comments_count]"] = self.Comments_Count
        if self.Bookmarks_Count:
            params["work_search[bookmarks_count]"] = self.Bookmarks_Count

        if self.Date_From:
            params["work_search[date_from]"] = self.Date_From.strftime("%Y-%m-%d")
        if self.Date_To:
            params["work_search[date_to]"] = self.Date_To.strftime("%Y-%m-%d")

        return params

    def GetUrl(self, page=1) -> str:
        return f"https://archiveofourown.org/works?commit=Sort+and+Filter&{urllib.parse.urlencode(self.getParams(page), doseq=True)}"
