from rest_framework import viewsets, status
from rest_framework.response import Response
from . import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Medicine, Type_of_med
from .serializers import MedicineSerializer, CategoriesSerializer

class MedicineAPIViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    lookup_field = 'link'
    permission_classes = [IsAuthenticated]

class CategoriesAPIViewSet(viewsets.ModelViewSet):
    queryset = Type_of_med.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'link'
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('link')
        if pk:
            medicines = Medicine.objects.filter(type_of_med__link=pk)
            serializer = MedicineSerializer(medicines, many=True)
            return Response({'medicines': serializer.data})
        else:
            return Response({'error': 'No pk provided'})
