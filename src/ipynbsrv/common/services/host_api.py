import json
import requests
from requests.exceptions import RequestException


class RequestService(object):
    '''
    '''

    '''
    '''
    CONTAINERS_ENDPOINT = 'containers'

    '''
    '''
    CONTAINERS_IMAGES_ENDPOINT = 'images'

    '''
    '''
    CONTAINERS_SNAPSHOTS_ENDPOINT = 'snapshots'

    '''
    '''
    def __init__(self, url):
        self._url = url

    def clone_container(self, container):
        '''
        '''
        raise NotImplementedError

    def delete_container(self, container):
        '''
        '''
        try:
            res = requests.delete(url='%s/%s/%s' % (self._url, RequestService.CONTAINERS_ENDPOINT, container))
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def delete_container_image(self, image):
        '''
        '''
        try:
            res = requests.delete(url='%s/%s/%s' % (self._url, RequestService.CONTAINERS_IMAGES_ENDPOINT, image))
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)

    def delete_container_snapshot(self, container, snapshot):
        '''
        '''
        try:
            res = requests.delete(url='%s/%s/%s/%s/%s' % (
                self._url, RequestService.CONTAINERS_ENDPOINT, container,
                RequestService.CONTAINERS_SNAPSHOT_ENDPOINT, snapshot
            ))
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def exec_in_container(self, container, command):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/exec' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({
                    'command': command
                })
            )
            if res.status_code == 200:
                return res.content.get('output')  # TODO: check API response
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container(self, container):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s' % (self._url, RequestService.CONTAINERS_ENDPOINT, container))
            if res.status_code == 200:
                container = json.loads(res.content)
                return {
                    'pk': container.get('pk'),
                    'status': container.get('status')
                }
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container_image(self, image):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s/%s' % (
                self._url, RequestService.CONTAINERS_ENDPOINT, RequestService.CONTAINERS_IMAGES_ENDPOINT, image
            ))
            if res.status_code == 200:
                image = json.loads(res.content)
                return {
                    'pk': image.get('pk')
                }
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container_images(self):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s' % (self._url, RequestService.CONTAINERS_ENDPOINT, RequestService.CONTAINERS_IMAGES_ENDPOINT))
            if res.status_code == 200:
                images = []
                for image in json.loads(res.content):
                    images.append({
                        'pk': image.get('pk')
                    })

                return images
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container_logs(self, container):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s/logs' % (self._url, RequestService.CONTAINERS_ENDPOINT, container))
            if res.status_code == 200:
                return json.loads(res.content)
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container_snapshot(self, container, snapshot):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s/%s/%s' % (
                self._url, RequestService.CONTAINERS_ENDPOINT, container,
                RequestService.CONTAINERS_SNAPSHOT_ENDPOINT, snapshot
            ))
            if res.status_code == 200:
                snapshot = json.loads(res.content)
                return {
                    'pk': snapshot.get('pk')
                }
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_container_snapshots(self, container):
        '''
        '''
        try:
            res = requests.get(url='%s/%s/%s/%s' % (
                self._url, RequestService.CONTAINERS_ENDPOINT, container,
                RequestService.CONTAINERS_SNAPSHOT_ENDPOINT
            ))
            if res.status_code == 200:
                snapshots = []
                for snapshot in json.loads(res.content):
                    snapshots.append({
                        'pk': snapshot.get('pk'),
                    })

                return snapshots
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def get_containers(self):
        '''
        '''
        try:
            res = requests.get(url='%s/%s' % (self._url, RequestService.CONTAINERS_ENDPOINT))
            if res.status_code == 200:
                containers = []
                for container in json.loads(res.content):
                    containers.append({
                        'pk': container.get('pk'),
                        'status': container.get('status')
                    })

                return containers
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def restart_container(self, container):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/restart' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({})
            )
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)

    def resume_container(self, container):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/resume' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({})
            )
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def start_container(self, container):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/start' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({})
            )
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def stop_container(self, container):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/stop' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({})
            )
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex

    def suspend_container(self, container):
        '''
        '''
        try:
            res = requests.post(
                url='%s/%s/%s/suspend' % (self._url, RequestService.CONTAINERS_ENDPOINT, container),
                data=json.dumps({})
            )
            if res.status_code == 204:
                return True
            else:
                raise RequestException
        except RequestException as ex:
            print "Status code: %i, Error: %s" % (res.status_code, res.content)
            raise ex
