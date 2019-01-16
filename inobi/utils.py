import uuid
from sorl.thumbnail import get_thumbnail


def users_image_path(instance, filename):
    return 'users/{0}'.format("%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))

def get_cdn_url(image, width, height):
    size = "%sx%s" %(width, height)
    thumbnail = get_thumbnail(image, size, quality=99)
    if not thumbnail:
        return thumbnail
    return thumbnail.url