from services.interfaces.timeline_service_interface import Timeline_Service_Interface
from repos.implementations.timeline_queries import Timeline_Repo
from datetime import datetime


class Timeline_Service(Timeline_Service_Interface):
    def __init__(self):
        self.timeline_repo = Timeline_Repo()

    def get_user_timeline(self, user_id, per_page_limit, page):
        return self.__format_messages(self.timeline_repo.get_user_timeline(user_id, per_page_limit, page))

    def get_public_timeline(self, per_page_limit, page):
        return self.__format_messages(self.timeline_repo.get_public_timeline(per_page_limit, page))

    def get_follower_timeline(self, username, per_page_limit, page):
        return self.__format_messages(self.timeline_repo.get_follower_timeline(username, per_page_limit, page))

    def record_latest(self, latest):
        self.timeline_repo.record_latest(latest)

    def get_latest(self):
        return self.timeline_repo.get_latest()

    def __format_messages(self, messages):
        if messages is not None:
            for x in messages:
                x["date"] = datetime.fromtimestamp(x["pub_date"]).strftime("%H:%M:%S, %m/%d/%Y")
                x["avatar"] = self.__get_avatar(x["email"])
                x["content"] = x["text"]
                x["user"] = x["username"]
                del x["text"]
                del x["username"]
                del x["pub_date"]
                del x["pw_hash"]
            return messages
        return []

    def __get_avatar(self, email):
        import hashlib
        return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest(), 48)
