# Return FileResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse

class HomeAPIView(APIView):
    def get(self, request, pk, format=None):
        task = get_object_or_404(Task, id=pk)

        # get data from another view
        resonse = SomeAPIView.as_view()(request=request._request).data

        return FileResponse(open(task.file.path, 'rb'))



import django

if django.utils.timezone.is_naive(publish_date):
    publish_date = django.utils.timezone.make_aware(publish_date)

