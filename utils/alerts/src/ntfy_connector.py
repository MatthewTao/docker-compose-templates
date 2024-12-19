import urllib.request
import urllib.parse


class NtfyConnectorStd:
    """
    Only uses standard lib
    Sometimes it's just nice to not have any other dependency
    """

    def __init__(self, topic: str, base_url: str = "https://ntfy.sh/"):
        self.topic = topic
        self.url = f"{base_url}{topic}"

    def push_notification(
        self, message: str, title: str = "", priority: str = "", tags: str = ""
    ):
        arguments = {
            "url": self.url,
            "data": message.encode(encoding="utf-8"),
            "method": "POST",
        }
        request = urllib.request.Request(**arguments)

        if title or priority or tags:
            # Create the header if this exists
            header = {}
            if title:
                request.add_header("Title", title)
            if priority:
                request.add_header("Priority", priority)
            if tags:
                request.add_header("Tags", tags)

        with urllib.request.urlopen(request) as response:
            # Read the response data
            response_data = response.read()
            # print(response_data.decode("utf-8"))
