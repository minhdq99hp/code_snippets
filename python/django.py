# Return FileResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse

class HomeAPIView(APIView):
    def get(self, request, pk, format=None):
        task = get_object_or_404(Task, id=pk)

        return FileResponse(open(task.file.path, 'rb'))

