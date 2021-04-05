from flask import request
from flask_restplus import Namespace, Resource
from flaskr.api.v1.config import wbxt_access_token
from flaskr.api.v1.parsers import wbxt_messages_post_args
from webexteamssdk import WebexTeamsAPI, ApiError

api = Namespace('wbxt', description='Webex Teams APIs')


@api.route("/send_message")
class wbxt_send_api(Resource):
    @api.expect(wbxt_messages_post_args, Validate=True)
    def post(self):
        '''
        Sends Message to Webex Teams Space (Room) by Room Title
        '''
        args = wbxt_messages_post_args.parse_args(request)
        # Populate the text key if not specified
        if 'text' not in args:
            args['text'] = ''

        try:
            # Initialize the webex teams API with our token
            wbxt_api = WebexTeamsAPI(access_token=wbxt_access_token)

            # Get the Rooms list (only group type, not direct)
            rooms = wbxt_api.rooms.list(type='group')

            # Search through the Rooms to match the room title
            for room in rooms:
                if args['room_name'].strip() == room.title.strip():
                    # Found the room, send a message
                    message = wbxt_api.messages.create(roomId=room.id, markdown=args['text'])
                    return {'success': True, 
                            'messages': 'Successfully sent message {}'.format(message.id), 
                            'response': ''}

            # Room was not found
            return {'success': False, 
                    'messages': 'Could not find Room "{}"'.format(args['room_name']),
                    'response': ''}

        except ApiError as e:
            # Return any API error that may have been raised
            return {'success': False,
                    'messages': 'API Error encountered',
                    'response': '{}'.format(e)}
