from dataclasses import dataclass
from pydantic import BaseModel

from typing import Optional


@dataclass
class ISimpleDescriptor():
    title: str
    description: str
    long_description: Optional[list[str]] = None

@dataclass
class IBackgroundImage():
    menu_background_image: str

@dataclass
class ICategory(ISimpleDescriptor, IBackgroundImage):
    pass

@dataclass
class IBlogEntry(ISimpleDescriptor, IBackgroundImage):
    page: Optional[str] = None

@dataclass
class INew(ISimpleDescriptor):
    date: Optional[str] = None


@dataclass
class IBlogDescriptorEntry():
    categories: list[ICategory]
    blog_entries: list[IBlogEntry]
    news: list[INew]
    website_title: str
    website_short_title: str

class BlogDescriptorEntryPydantic(BaseModel, IBlogDescriptorEntry):
    pass

    
