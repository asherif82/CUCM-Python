from flask import request
from flask_restplus import Namespace, Resource
from flaskr.api.v1.config import default_cms, default_cucm
from flaskr.cms.v1.cms import CMS
from flaskr.uds.v1.uds import UDS
from flaskr.api.v1.parsers import cms_spaces_get_args, cms_spaces_post_args

api = Namespace('cms', description='Cisco Meeting Server REST API')


@api.route("/system/status")
class cms_system_status_api(Resource):
    def get(self):
        """
        Retrieves CMS system status.
        """
        cms = CMS(default_cms['host'], default_cms['username'],
                  default_cms['password'], port=default_cms['port'])
        return cms.get_system_status()


@api.route("/version")
class cms_version_api(Resource):
    # @api.expect(system_status_data)
    def get(self):
        """
        Retrieves the version of the CMS system software.

        Use this method to query for the CMS software version.
        """
        cms = CMS(default_cms['host'], default_cms['username'], default_cms['password'], port=default_cms['port'])
        cms_status = cms.get_system_status()
        if cms_status['success']:
            return cms_status['response']['status']['softwareVersion']
        return cms_status

def get_matched_uri(space_list, uri):
    """
    Returns pkid of the Space where the URI or Secondary URI match the searched uri
    """
    for space in space_list:
        try:
            if uri == space['uri']:
                return space['@id']
        except KeyError:
            pass
        try:
            if uri == space['secondaryUri']:
                return space['@id']
        except KeyError:
            pass
    return None


@api.route("/spaces")
# @api.route("/spaces")
class cms_spaces_api(Resource):

    @api.expect(cms_spaces_get_args)
    def get(self):
        """
        Retrieves all CMS Spaces.
        """
        args = request.args.to_dict()
        cms = CMS(default_cms['host'], default_cms['username'], default_cms['password'], port=default_cms['port'])
        try:
            if not args['match_uri']:
                # return get_coSpaces with regular filtering, if any
                return cms.get_coSpaces(parameters=args)
        except KeyError:
            pass
        # Need to search using exact matching 
        args['offset'] = 0
        matched_spaces = cms.get_coSpaces(parameters=args)
        try:
            total_matches = int(matched_spaces['response']['coSpaces']['@total'])
            if total_matches == 0:
                # No match found
                return matched_spaces
            elif total_matches == len(matched_spaces['response']['coSpaces']['coSpace']):
                # Received all matches back
                pkid = get_matched_uri(space_list=matched_spaces['response']['coSpaces']['coSpace'],
                                       uri=args['filter'])
                if pkid:
                    return cms.get_coSpace(id=pkid)
                else:
                    return {'success':False,
                            'message': 'No match found for URI "{}"'.format(args['filter']),
                            'response': ''}
            else:
                # The list of results was not the complete set of results
                all_spaces = matched_spaces['response']['coSpaces']['coSpace']

                while total_matches > len(all_spaces):
                    pkid = get_matched_uri(space_list=matched_spaces['response']['coSpaces']['coSpace'],
                                           uri=args['filter'])
                    if pkid:
                        return cms.get_coSpace(id=pkid)
                    args['offset'] = len(all_spaces)
                    matched_spaces = cms.get_coSpaces(parameters=args)
                    all_spaces += matched_spaces['response']['coSpaces']['coSpace']
            return {'success': False,
                    'message': 'No match found for URI "{}"'.format(args['filter']),
                    'response': ''}
        except KeyError:
            pass
        return matched_spaces
        

    @api.expect(cms_spaces_post_args)
    def post(self, host=default_cms['host'], port=default_cms['port'], username=default_cms['username'],
             password=default_cms['password']):
        """
        Creates a new CMS Space.
        """
        args = request.args.to_dict()

        cms = CMS(default_cms['host'], default_cms['username'],
                  default_cms['password'], port=default_cms['port'])
        try:
            if args['userid']:
                cucm_uds = UDS(default_cucm['host'])
                user = cucm_uds.get_user(parameters={'username': args['userid']})

                payload = {}
                if user['success']:
                    if user['response']['users']['@totalCount'] == '1':
                        payload['name'] = "{}'s Space".format(user['response']['users']['user'][0]['displayName'])
                        payload['uri'] = user['response']['users']['user'][0]['userName']
                        payload['secondaryUri'] = user['response']['users']['user'][0]['phoneNumber']
                        # Overwrite payload with whatever values were passed via args
                        payload.update(args)

                        return cms.create_coSpace(payload=payload)
                    else:
                        return {'success': False,
                                'message': 'Found {} users with userid "{}"'.format(
                                    user['response']['users']['@totalCount'], args['userid'])}
                else:
                    # User lookup failed completely
                    return user
        except KeyError:
            return cms.create_coSpace(payload=args)


@api.route("/spaces/<id>")
@api.param('id', 'The object id of the Space')
class cms_space_api(Resource):
    def get(self, id):
        """
        Retrieves a CMS Space by object id.
        """
        cms = CMS(default_cms['host'], default_cms['username'], default_cms['password'], port=default_cms['port'])
        return cms.get_coSpace(id=id)

    @api.expect(cms_spaces_get_args)
    def put(self, id):
        """
        Edits a CMS space by object id
        """
        args = request.args.to_dict()
        cms = CMS(default_cms['host'], default_cms['username'],
                  default_cms['password'], port=default_cms['port'])
        return cms.update_coSpace(id=id, payload=args)

    def delete(self, id):
        """
        Removes a CMS space by object id
        """
        cms = CMS(default_cms['host'], default_cms['username'],
                  default_cms['password'], port=default_cms['port'])
        return cms.delete_coSpace(id=id)
