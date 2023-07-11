import arrow


# this is the Paste model
class Paste:
    id: str = None
    title: str = None
    author: str = None
    date: arrow = None
    content: str = None

    def __init__(self, data: dict = None):
        if not data:
            return

        self.id = data.get("id")
        self.title = data.get("title")
        self.author = data.get("author")
        self.date = data.get("date")
        self.content = data.get("content")

    def set_id(self, id: str):
        self.id = id

    def set_title(self, title: str):
        self.title = title

    def set_author(self, author: str):
        self.author = author

    def set_date(self, date: arrow):
        self.date = date

    def set_content(self, content: str):
        self.content = content

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "content": self.content,
        }
