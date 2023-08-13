import re
from datetime import datetime
import requests
import textwrap


class CultureInfoSlack:

    @staticmethod
    def eventTypeSelection():
        return [
            "音樂",
            "戲劇",
            "舞蹈",
            "親子",
            "獨立音樂",
            "展覽",
            "講座",
            "電影",
            "綜藝",
            "演唱會",
            "研習課",
            "閱讀"
        ]

    @staticmethod
    def locationSelection():
        return [
            "臺北",
            "基隆",
            "新北",
            "桃園",
            "新竹",
            "苗栗",
            "臺中",
            "彰化",
            "南投",
            "花蓮",
            "臺東",
            "雲林",
            "嘉義",
            "臺南",
            "高雄",
            "屏東",
            "金門",
            "澎湖"
        ]

    @staticmethod
    def eventTypeToCategory():
        return {
            "音樂": 1,
            "戲劇": 2,
            "舞蹈": 3,
            "親子": 4,
            "獨立音樂": 5,
            "展覽": 6,
            "講座": 7,
            "電影": 8,
            "綜藝": 11,
            "演唱會": 17,
            "研習課": 19,
            "閱讀": 200
        }

    def __init__(self, app):
        self.app = app
        self.cultureInfoHandler()

    def cultureInfoHandler(self):
        @self.app.message(re.compile(r"(event|concert|exhibition)"))
        def userSelect(client, message, logger):
            try:
                # region __Step 1 : Emoji reaction
                client.reactions_add(
                    name="eyes",
                    channel=message["channel"],
                    timestamp=message["ts"]
                )
                # endregion

                # region __Step 2 : Block - Print Title
                printSelectionTitle = {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":calendar: Taiwan Event :calendar:"
                    }
                }
                printSlectionContext = {
                    "type": "context",
                    "elements": [
                        {
                            "text": "Required Selection : Event Type | Location | Date",
                            "type": "mrkdwn"
                        }
                    ]
                }
                # endregion

                # region __Step 2 : Block - Event type dropdown list
                eventTypeSelection = self.eventTypeSelection()
                eventTypeOptions = []
                for eventValue in eventTypeSelection:
                    eventOption = {
                        "text": {
                            "type": "plain_text",
                            "text": eventValue,
                            "emoji": True
                        },
                        "value": eventValue.lower().replace(' ', '-')
                    }
                    eventTypeOptions.append(eventOption)
                    eventTypeMenu = {
                        "type": "input",
                        "block_id": "eventtype-selection",
                        "element": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select an event type"
                            },
                            "action_id": "select-eventtype",
                            "options": eventTypeOptions,
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Event Type"
                        }
                    }
                # endregion

                # region __Step 2 : Block - Location dropdown list
                locationSelection = self.locationSelection()
                locationOptions = []
                for locationValue in locationSelection:
                    locationOption = {
                        "text": {
                            "type": "plain_text",
                            "text": locationValue,
                            "emoji": True
                        },
                        "value": locationValue.lower().replace(' ', '-')
                    }
                    locationOptions.append(locationOption)
                    locationMenu = {
                        "type": "input",
                        "block_id": "location-selection",
                        "element": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select the location"
                            },
                            "action_id": "select-location",
                            "options": locationOptions,
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Location"
                        }
                    }
                # endregion

                # region Step 2 : Block - Date
                currentYearMonth = datetime.now().strftime("%Y/%m")
                dateInputBlock = {
                    "type": "input",
                    "block_id": "date-selection",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "select-date",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter a year and month (YYYY/mm/dd)"
                        },
                        "initial_value": currentYearMonth
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Date"
                    }
                }
                # endregion

                # region __Step 2 : Block - Button Send
                buttonSend = {
                    "type": "actions",
                    "block_id": "send-selection",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Send"
                            },
                            "action_id": "send-selection",
                            "style": "primary"
                        }
                    ]
                }
                # endregion

                # region __Step 2, reply message of options
                client.chat_postMessage(
                    channel=message["channel"],
                    blocks=[
                        printSelectionTitle,
                        printSlectionContext,
                        eventTypeMenu,
                        locationMenu,
                        dateInputBlock,
                        buttonSend])
                # endregion

            except Exception as e:
                logger.error(f"Error: {e}")

        @self.app.action("send-selection")
        def userSendSelection(ack, body, client, logger):
            # Acknowledge the action request
            ack()
            user_id = body["user"]["id"]
            # Store the user's selection in the userSelections dictionary
            userSelections[user_id] = body["state"]

            # region __Step 3 : Detect event type chosen
            selectedEventType = body["state"]["values"]["eventtype-selection"]["select-eventtype"]["selected_option"][
                "value"]
            eventTypeToCategory = self.eventTypeToCategory()
            selectedCategory = eventTypeToCategory.get(selectedEventType)
            if selectedCategory is None:
                logger.info("Invalid event type selected.")
                response_message = "Invalid event type selected."
                client.chat_postMessage(
                    channel=body["channel"]["id"],
                    thread_ts=body["message"]["ts"],
                    text=response_message
                )
                return
            # endregion

            # region __Step 3 : Detect location chosen
            selectedLocation = body["state"]["values"]["location-selection"]["select-location"]["selected_option"][
                "value"]
            if selectedLocation is None:
                logger.info("Invalid location selected.")
                response_message = "Invalid location selected."
                client.chat_postMessage(
                    channel=body["channel"]["id"],
                    thread_ts=body["message"]["ts"],
                    text=response_message
                )
                return
            # endregion

            # region __Step 3 : Detect date inputted
            selectedDate = body["state"]["values"]["date-selection"]["select-date"]["value"]
            if selectedDate is None:
                logger.info("Invalid date.")
                response_message = "Invalid date."
                client.chat_postMessage(
                    channel=body["channel"]["id"],
                    thread_ts=body["message"]["ts"],
                    text=response_message
                )
                return
            # endregion

            # region __Step 4 : Request open api
            response = requests.get(
                "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do",
                params={"method": "doFindTypeJ", "category": selectedCategory}
            )
            # endregion

            # region __Step 5 : Response
            if response.status_code == 200:
                resp = response.json()
                finalResultList = []
                for respListOfBegin in resp:
                    showInfo = respListOfBegin['showInfo']
                    for showInfoList in showInfo:
                        if selectedLocation in showInfoList['location'] and selectedDate in showInfoList['time']:
                            category = respListOfBegin['category']
                            title = respListOfBegin['title']
                            time = datetime.strptime(
                                showInfoList['time'], "%Y/%m/%d %H:%M:%S")
                            price = showInfoList['price']
                            location = showInfoList['location']
                            locationName = showInfoList['locationName']
                            onSales = showInfoList['onSales']
                            finalResultList.append({'category': category,
                                                    'title': title,
                                                    'time': time,
                                                    'price': price,
                                                    'location': location,
                                                    'locationName': locationName,
                                                    'onSales': onSales})
                finalResultSort = sorted(
                    finalResultList,
                    key=lambda x: x['time'],
                    reverse=False)

                response_message = ""
                for finalPrint in finalResultSort:
                    response_message += textwrap.dedent("""\
                            >*{title}*
                             •  Time:  {time}
                             •  Location Name: {locationName}
                             •  On Sales: {onSales}
                             •  Price: {price}
                             •  Location: {location}

                            """).format(
                        category=finalPrint['category'],
                        title=finalPrint['title'],
                        time=finalPrint['time'],
                        locationName=finalPrint['locationName'],
                        price=finalPrint['price'] or "NA",
                        onSales=finalPrint['onSales'],
                        location=finalPrint['location'])

                response_message = response_message.strip()
                logger.info(response_message)

                # Send the response message
                client.chat_postMessage(
                    channel=body["channel"]["id"],
                    thread_ts=body["message"]["ts"],
                    text=response_message or "No event"
                )
            else:
                response_message = "Error"
                logger.error(response.json())
                client.chat_postMessage(
                    channel=body["channel"]["id"],
                    thread_ts=body["message"]["ts"],
                    text=response_message
                )
            # endregion

            # Clear the user's selection
            del userSelections[user_id]

        # Dictionary to store user selections
        userSelections = {}
