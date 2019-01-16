from sizer.models import Photo

def get_photo_detail(pk):
    return Photo.objects.select_related('user').get(pk=pk)