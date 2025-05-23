# AO3 Parser
Tools for parsing AO3 pages and creating urls based on requirements.

Main advantage over similar packages is it's complete control over requests to AO3.
Instead of handling requests on it's own, it shifts this to the user, giving more room for optimization.
The main bottleneck for anyone in need of collecting larger amounts of data.
(Scraping data for AI training is discouraged)

If this is not what you're looking for, I'd recommend [ao3_api](https://github.com/wendytg/ao3_api) that handles requests on it's own.

## Installation
```bash
pip install ao3-parser
```

# Usage
An average user will find themselves using two main modules the most, `Search` and `Page`. 

## Search
Common example of using `Search` would look like this.
Just like on AO3, pages are numbered from 1 and up.

```python
import AO3Parser as AO3P
from AO3Parser import Params

search = AO3P.Search(Fandoms=["Original Work"], Sort_by=Params.Sort.Kudos,
                     Rating=Params.Rating.General_Audiences,
                     Categories=[Params.Category.Multi, Params.Category.Other],
                     Words_Count="1000-1500",
                     Date="2 weeks ago")
url = search.GetUrl(page=1)
print(f"URL: {url}")
```
```
URL: https://archiveofourown.org/works/search?commit=Search&page=1&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&work_search%5Brevised_at%5D=2+weeks+ago&work_search%5Bword_count%5D=1000-1500&work_search%5Bfandom_names%5D=Original+Work&work_search%5Brating_ids%5D=10&work_search%5Bcategory_ids%5D%5B%5D=2246&work_search%5Bcategory_ids%5D%5B%5D=24
```

The `Words_Count`, `Hits_Count`, `Kudos_Count`, `Comments_Count` and `Bookmarks_Count` parameters are string types that use AO3 type formatting.
> #### Work Search: Numerical Values
> Use the following guidelines when looking for works with a specific amount of words, hits, kudos, comments, or bookmarks. Note that periods and commas are ignored: 1.000 = 1,000 = 1000.
>
>> `10`:  
>> a single number will find works with that exact amount  
> 
>> `<100`:  
>> will find works with less than that amount 
> 
>> `>100`:  
>> will find works with more than that amount  
> 
>> `100-1000`:  
>> will find works in the range of 100 to 1000

The `Date` parameter also uses AO3 style formatting.
> #### Work Search: Date
> Create a range of times. If no range is given, then one will be calculated based on the time period specified.
>
> Allowable periods: year, week, month, day, hour
>
>> `x days ago` = 24 hour period from the beginning to the end of that day
> 
>> `x weeks ago` = 7 day period from the beginning to the end of that week
> 
>> `x months ago` = 1 month period from the beginning to the end of that month
> 
>> `x years ago` = 1 year period from the beginning to the end of that year
>
> <details><summary>Examples (taking Wednesday 25th April 2012 as the current day):</summary>
>
>> `7 days ago` (this will return all works posted/updated on Wednesday 18th April)
> 
>> `1 week ago` (this will return all works posted/updated in the week starting Monday 16th April and ending Sunday 22nd April)
> 
>> `2 months ago` (this will return all works posted/updated in the month of February)
> 
>> `3 years ago` (this will return all works posted/updated in 2010)
> 
>> `< 7 days` (this will return all works posted/updated within the past seven days)
> 
>> `> 8 weeks` (this will return all works posted/updated more than eight weeks ago)
> 
>> `13-21 months` (this will return all works posted/updated between thirteen and twenty-one months ago)
> </details>
> Note that the "ago" is optional.

## Page

```python
import AO3Parser as AO3P
import requests

search = AO3P.Search(Fandoms=["Original Work"])
url = search.GetUrl()
page_data = requests.get(url).content

page = AO3P.Page(page_data)
print(f"Total works: {page.Total_Works}")
print(f"Works on page: {len(page.Works)}")
print(f"Title of the first work: {page.Works[0].Title}")
```
```
Total works: 282069
Works on page: 20
Title of the first work: Title Of This Work
```

## Work

```python
import AO3Parser as AO3P
import requests

work_id = 123456789
url = f"https://archiveofourown.org/works/{work_id}"
work_data = requests.get(url).content

work = AO3P.Work.FromHTML(work_data)
print(f"ID of the parsed work: {work.ID}")
print(f"With the title: {work.Title}")
print(f"Published on this date: {work.Published}")
```
```
ID of the parsed work: 123456789
With the title: Title Of This Work
Published on this date: 2025-04-17 00:00:00
```

All data that is parsed from a page into works can be seen below.
```python
ID: int
Title: str
Authors: list[str]
Fandoms: list[str]
Summary: str | None

Language: str
Words: int | None
Chapters: int
Expected_Chapters: int | None
Comments: int | None
Kudos: int | None
Bookmarks: int | None
Hits: int | None
Updated: datetime

Rating: Params.Rating
Categories: list[Params.Category]
Warnings: list[Params.Warning]
Completed: bool

Relationships: list[str]
Characters: list[str]
Additional_Tags: list[str]

Published: datetime | None
```
### Notes
`Params.Category.No_Category` is not recognized as a valid ID on AO3 and should not be used with `Search`.