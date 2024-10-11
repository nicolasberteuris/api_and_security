





















"""


class MeasureUnitViewSet(viewsets.ModelViewSet):
    
    #Comentario para API Docs en Swagger
    
    serializer_class = MeasureUnitSerializer   

    #redefinir el filtro de busqueda
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id =pk, state=True).first()
        
    #redefinir la lista
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data,status=status.HTTP_200_OK)
        
    #redefinir el post
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Unidad de medida de Producto creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    #redefinir el update
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #redefinir delete
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Unidad de medida de Producto eliminada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error: No existe una Unidad de medida de Producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST) 

class IndicatorViewSet(viewsets.ModelViewSet):
    
    #Comentario para API Docs en Swagger
    
    serializer_class = IndicatorSerializer

    #redefinir el filtro de busqueda
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id =pk, state=True).first()
        
    #redefinir la lista
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data,status=status.HTTP_200_OK)
        
    #redefinir el post
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Indicador de Producto creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    #redefinir el update
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #redefinir delete
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Indicador de Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error: No existe un Indicador de Producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST) 
    

class CategoryProductViewSet(viewsets.ModelViewSet):
    
    #Comentario para API Docs en Swagger
    
    serializer_class = CategoryProductSerializer

    #redefinir el filtro de busqueda
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id =pk, state=True).first()
        
    #redefinir la lista
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data,status=status.HTTP_200_OK)
        
    #redefinir el post
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Categoria de Producto creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    #redefinir el update
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #redefinir delete
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Categoria de Producto eliminada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error: No existe una Categoria de Producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST)

        
"""

"""
class MeasureUnitListAPIView(GeneralListAPIView):
    serializer_class = MeasureUnitSerializer    

class IndicatorListAPIView(GeneralListAPIView):
    serializer_class = IndicatorSerializer
    

class CategoryProductListAPIView(GeneralListAPIView):
    serializer_class = CategoryProductSerializer
"""





