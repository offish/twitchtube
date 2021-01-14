import http.client as httplib
import json
import os
import random
import time

import google.oauth2.credentials
import httplib2
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from .config import PATH
from .logging import Log

log = Log()

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = f'{PATH}/twitchtube/client_secret.json'

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


# Authorize the request and store authorization credentials.
# Used to generate first auth token. Only needs to happen once.
def getAuthenticatedService(CREDENTIALS_FILE):
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    auth_url, _ = flow.authorization_url(prompt='consent')
    log.error('Please go to this URL: {}'.format(auth_url))

    code = input('Enter the authorization code: ')
    credentials = flow.fetch_token(code=code)
    saveCredentials(CREDENTIALS_FILE, credentials)

    return build(API_SERVICE_NAME, API_VERSION, credentials=flow.credentials)

# Renew credentials after each time being called.


def getAuthenticatedServiceFromStorage(CREDENTIALS_FILE):
    credentials = getCredentialsFromStorage(CREDENTIALS_FILE)
    os.remove(CREDENTIALS_FILE)
    saveCredentials(CREDENTIALS_FILE, credentials)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# Fetch youtube service from saved credentials.


def getCredentialsFromStorage(CREDENTIALS_FILE):
    credentials = json.load(open(CREDENTIALS_FILE))
    credentials = json.loads(credentials)

    with open(CLIENT_SECRETS_FILE, 'r') as json_file:
        client_config = json.load(json_file)

    if 'access_token' in credentials:
        credentials = google.oauth2.credentials.Credentials(
            credentials['access_token'],
            refresh_token=credentials['refresh_token'],
            token_uri=client_config['installed']['token_uri'],
            client_id=client_config['installed']['client_id'],
            client_secret=client_config['installed']['client_secret'])
    else:
        credentials = google.oauth2.credentials.Credentials(
            credentials['token'],
            refresh_token=credentials['_refresh_token'],
            token_uri=client_config['installed']['token_uri'],
            client_id=client_config['installed']['client_id'],
            client_secret=client_config['installed']['client_secret'])

    return credentials

# Store credentials in json file.


def saveCredentials(CREDENTIALS_FILE, credentials):
    open(CREDENTIALS_FILE, 'wb')
    with open(CREDENTIALS_FILE, 'w') as outfile:
        json.dump(json.dumps(credentials, default=lambda o: o.__dict__), outfile)


def initializeUpload(youtube, title, description, file, category, keywords, privacyStatus):
    tags = keywords.split(',')

    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category
        ),
        status=dict(
            privacyStatus=privacyStatus
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting 'chunksize' equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )

    return resumableUpload(insert_request)


def thumbnails_set(client, media_file, **kwargs):
    request = client.thumbnails().set(media_body=MediaFileUpload(
        media_file, chunksize=-1, resumable=True), **kwargs)

    # See full sample for function
    return resumable_upload_thumbnails(request)

# This method implements an exponential backoff strategy to resume a
# failed upload.


def resumableUpload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            log.info('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    log.info('Video id "%s" was successfully uploaded.\n' %
                          response['id'])
                    return response['id']
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (
                    e.resp.status, e.content)
            else:
                raise
        except(RETRIABLE_EXCEPTIONS, e):
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            log.error(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            log.warn('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)


def upload_video_to_youtube(config: dict):
    CREDENTIALS_FILE = f'{PATH}/credentials/credentials.json'


    if os.path.isfile(CREDENTIALS_FILE):
        youtube = getAuthenticatedServiceFromStorage(CREDENTIALS_FILE)
    else:
        try:
            os.makedirs(f'{PATH}/credentials')
        except FileExistsError:
            pass
        youtube = getAuthenticatedService(CREDENTIALS_FILE)

    try:
        # Upload video

        videoId = initializeUpload(
            youtube,
            title=config['title'],
            description=config['description'],
            file=config['file'],
            category=config['category'],
            keywords=config['keywords'],
            privacyStatus='private'
        )

        # Upload thumbnail
        if 'thumbnail' in config:
            thumbnails_set(youtube, config['thumbnail'], videoId=videoId)
    except HttpError as e:
        log.error('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


def resumable_upload_thumbnails(request, method='insert'):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            log.info('Uploading thumbnail...')
            status, response = request.next_chunk()
            if response is not None:
                if method == 'insert' and 'id' in response:
                    log.info(response)
                elif method != 'insert' or 'id' not in response:
                    log.info(response)
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (
                    e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            log.error(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            log.warn('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)
