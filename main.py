import requests
import urllib
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    # https://query1.finance.yahoo.com/v8/finance/chart/${symbol}.JK?range=1d

    def on_event(self, event, extension):
        items = []

        if event.get_keyword() == "en2id":
            text = event.get_argument()
            query = urllib.urlencode({"text": text})
            url = "https://en2id-server.vercel.app/en-id?" + query
            response = requests.request("GET", url)
            data = response.json()

            if data["text"] is not None:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s' % data["text"],
                                                 description='',
                                                 on_enter=OpenUrlAction('https://translate.google.co.id/?hl=en&sl=en&tl=id&%s&op=translate' % query)))

        if event.get_keyword() == "id2en":
            text = event.get_argument()
            query = text.replace(" ", "+")
            # url = "https://en2id-server.vercel.app/id-en?" + query
            # response = requests.request("GET", url)
            # data = response.json()

            items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s' % query,
                                                 description=''
                                                 ))
            # if data["text"] is not None:
            #     items.append(ExtensionResultItem(icon='images/icon.png',
            #                                      name='%s' % data["text"],
            #                                      description='',
            #                                      on_enter=OpenUrlAction('https://translate.google.co.id/?hl=id&sl=id&tl=en&%s&op=translate' % query)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
