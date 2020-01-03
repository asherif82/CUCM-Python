from flask_restplus import reqparse

"""
Arguments for all API functions. Functions that have parameters will have this a decorator such as
    @api.expect(user_filter_args, validate=True)
To document and limit what can be entered on the /api/v1/ Swagger web page
"""

### Cisco Meeting Server API Arguments
cms_spaces_post_args = reqparse.RequestParser()
cms_spaces_post_args.add_argument('name', type=str, required=False, help='Name of the Space')
cms_spaces_post_args.add_argument('uri', type=str, required=False, 
                                  help='User URI part for SIP call to reach Space')
cms_spaces_post_args.add_argument('secondaryUri', type=str, required=False, 
                                  help='Secondary URI for SIP call to reach Space')
cms_spaces_post_args.add_argument('passcode', type=str, required=False, 
                                  help='Security code for this Space')
cms_spaces_post_args.add_argument('defaultLayout', type=str, required=False, 
                                  help='Default Layout for this Space',
                                  choices=['automatic', 'allEqual', 'speakerOnly', 'telepresence', 
                                  'stacked', 'allEqualQuarters'],
                                  default='automatic')

cms_spaces_get_args = reqparse.RequestParser()
cms_spaces_get_args.add_argument('filter', type=str, required=False, help='Search string')
cms_spaces_get_args.add_argument('limit', type=int, required=False, help='How many results to return. \
  Note that CMS has an internal limit of 10 even though a larger limit can be requested', default=10)
cms_spaces_get_args.add_argument('offset', type=int, required=False,
                                  help='Return results starting with the offset specified', default=0)

### Cisco Unity Connection API Arguments

cuc_importldap_post_args = reqparse.RequestParser()
cuc_importldap_post_args.add_argument('templateAlias', type=str, required=True,
                                      help='User template alias',
                                      default='voicemailusertemplate')
cuc_importldap_post_args.add_argument('pkid', type=str, required=True,
                                      help='PKID of the user to be imported')
cuc_importldap_post_args.add_argument('IsVmEnrolled', type=str, required=False,
                                      help='Play initial enrollment conversation (to record a name, request \
                                            password, etc)',
                                      choices=['true', 'false'], default='true')
cuc_importldap_post_args.add_argument('ListInDirectory', type=str, required=False,
                                      help='List in the Unity Connection Auto Attendant Directory',
                                      choices=['true', 'false'], default='true')

cuc_users_get_args = reqparse.RequestParser()
cuc_users_get_args.add_argument('column', type=str, required=False,
                                help='Column to search', default='alias')
cuc_users_get_args.add_argument('match_type', type=str, required=False, choices=[
                                'startswith', 'is'], help='Order of return values', default='is')
cuc_users_get_args.add_argument('search', type=str, required=False, help='Query string')
cuc_users_get_args.add_argument('sortorder', type=str, required=False, choices=[
                                'asc', 'desc'], help='Order of return values', default='asc')
cuc_users_get_args.add_argument('rowsPerPage', type=int, required=False,
                                help='Number of rows to return', default=100)
cuc_users_get_args.add_argument('pageNumber', type=int, required=False,
                                help='Page # to return', default=1)

cuc_users_put_args = reqparse.RequestParser()
cuc_users_put_args.add_argument('ListInDirectory', type=str, required=False,
                                help='List in the Unity Connection Auto Attendant Directory',
                                choices=['true', 'false'], default='true')
cuc_users_put_args.add_argument('IsVmEnrolled', type=str, required=False,
                                help='Play initial enrollment conversation (to record a name, request new \
                                      password, etc)',
                                choices=['true', 'false'], default='true')

cuc_pin_cred_put_args = reqparse.RequestParser()
cuc_pin_cred_put_args.add_argument('Credentials', type=int, required=True, help='PIN of the voicemail box')
cuc_pin_cred_put_args.add_argument('ResetMailbox', type=bool, required=False, help='Reset mailbox', default=True)

### Webex Teams API Arguments
wbxt_rooms_get_args = reqparse.RequestParser()
wbxt_rooms_get_args.add_argument('teamId', type=str, required=False, help='List rooms associated with a team, by ID')
wbxt_rooms_get_args.add_argument('type', type=str, required=False, help='List rooms by type',
                                 choices=['direct', 'group'])
wbxt_rooms_get_args.add_argument('sortBy', type=str, required=False, help='Sort results',
                                 choices=['id', 'lastactivity', 'created'])
wbxt_rooms_get_args.add_argument('max', type=int, required=False,
                                 help='Maximum number of rooms in the response', default=100)


wbxt_messages_post_args = reqparse.RequestParser()
wbxt_messages_post_args.add_argument('roomId', type=str, required=True, help='The room ID of the message')
wbxt_messages_post_args.add_argument('text', type=str, required=False, help='The message, in plain text')
wbxt_messages_post_args.add_argument('markdown', type=str, required=False,
                                     help='The message, in Markdown format. The maximum message length is 7439 bytes')
