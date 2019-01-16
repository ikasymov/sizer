import json

from django.http import JsonResponse
from django.http import QueryDict

from utils import status

def only_application_json(method='PUT'):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.content_type == 'application/json':
                if request.method == 'GET':
                    return func(request, *args, **kwargs)
                try:
                    querydict = QueryDict(mutable=True)
                    querydict.update(json.loads(request.body))
                    setattr(request, method, querydict)
                    return func(request, *args, **kwargs)
                except ValueError as e:
                    return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        data={'success': False, 'message': e.message})
            else:
                return JsonResponse({'success': False, 'message': 'Allowed only application/json'})

        return inner

    return decorator