from typing import Optional, Type, List

from langchain.tools import BaseTool
from pydantic import BaseModel
from .models import Stories, Comments, Content

from .functions import get_hn_stories
from .functions import get_relevant_comments
from .functions import get_story_content


class StoriesTool(BaseTool):
    name: str = "get_stories"
    description: str = (
        "Gets stories from Hacker News. The stories are described by \
        a 'story_id', a 'title', a 'url' and"
        " a 'score'."
    )

    def _run(self, limit: int = 5, keywords: List[str] = None, story_type: str = "top"):
        stories = get_hn_stories(limit, keywords, story_type)
        return stories

    def _arun(
        self, limit: int = 5, keywords: List[str] = None, story_type: str = "top"
    ):
        stories = get_hn_stories(limit, keywords, story_type)
        return stories

    args_schema: Optional[Type[BaseModel]] = Stories


class CommentsTool(BaseTool):
    name: str = "get_comments"
    description: str = "Gets comments from a specific Hacker News story"

    def _run(self, story_id: int, limit: int = 10):
        comments = get_relevant_comments(story_id, limit)
        return comments

    def _arun(self, story_id: int, limit: int = 10):
        comments = get_relevant_comments(story_id, limit)
        return comments

    args_schema: Optional[Type[BaseModel]] = Comments


class ContentTool(BaseTool):
    name: str = "get_content"
    description: str = "Gets the Hacker News story content from a URL"

    def _run(self, story_url: str):
        story_content = get_story_content(story_url)
        return story_content

    def _arun(self, story_url: str):
        story_content = get_story_content(story_url)
        return story_content

    args_schema: Optional[Type[BaseModel]] = Content
