# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import datetime
# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase


def text_date_to_int(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "昨天":
        return -1
    # in other case
    return None


class ActionQueryTime(Action):

    def name(self) -> Text:
        return "action_query_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        dispatcher.utter_message(text=current_time)
        return []


class ActionQueryDate(Action):

    def name(self) -> Text:
        return "action_query_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text_date = tracker.get_slot('date') or '今天'
        int_date = text_date_to_int(text_date)
        if int_date is not None:
            target_date = datetime.datetime.now() + datetime.timedelta(days=int_date)
            dispatcher.utter_message(text=target_date.strftime('%Y-%m-%d'))
        else:
            dispatcher.utter_message(text='系统暂时不支持"{}"的日期查询'.format(text_date))
        return []


class WeatherFormAction(Action):
    def name(self) -> Text:
        return "action_weather_form_submit"

    def run(
            self, dispatch: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        city = tracker.get_slot("address")
        date_text = tracker.get_slot("date-time")
        dispatch.utter_message('Demo,暂不支持查询{}({})的天气'.format(city, date_text))
        return []


class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):
    def name(self) -> Text:
        return "action_response_query"

    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase("data.json")
        super().__init__(knowledge_base)

