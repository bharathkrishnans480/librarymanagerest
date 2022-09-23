from django.shortcuts import render
from rest_framework.response import Response
from .models import Book,IssueBook,User
from rest_framework import generics
from .serializers import BookSerializer,UserSerializer,IssueBookSerializer
from rest_framework.permissions import BasePermission,IsAuthenticated


# Create your views here.

class WriteByAdminOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if request.method=='GET':
            return True
        if request.method=='POST' or request.method=='PUT' or request.method=='DELETE':
            if user.is_superuser:
                return True
        return False



class AllBooksView(generics.ListAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()
class BookCreateView(generics.CreateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = BookSerializer
class BookView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class BookUpdateView(generics.UpdateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class DeleteBookView(generics.DestroyAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    queryset = Book.objects.all()

class CreateStudentView(generics.CreateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = UserSerializer

class ListAllStudentsView(generics.ListAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser = False)

class StudentView(generics.RetrieveAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser = False)

class UpdateStudentView(generics.UpdateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser = False)

class StudentRemoveView(generics.DestroyAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    queryset = User.objects.filter(is_superuser = False)

class CreateBookIssue(generics.CreateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)

    def create(self, request, *args, **kwargs):
        serializer = IssueBookSerializer(data=request.data)
        try:
            book = Book.objects.get(id = request.data.get('book'))
            required_quantity = request.data.get('quantity')

            if not book.is_available:
                return Response('This book is Out of stock')
            if required_quantity>book.quantity:
                return Response('Quantity should be less than or equal to the available quantity')

            elif serializer.is_valid():
                book.quantity-=required_quantity
                book.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except:
            return Response('No such book available')
class IssueBookListView(generics.ListAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)
    serializer_class = IssueBookSerializer
    queryset = IssueBook.objects.all()


class IssueBookQuantityUpdateView(generics.UpdateAPIView):
    permission_classes = (WriteByAdminOnlyPermissions,)

    def update(self, request, *args, **kwargs):

        try:
            book = Book.objects.get(id=request.data.get('book'))
            instance = IssueBook.objects.get(id=kwargs.get('pk'))
            serializer = IssueBookSerializer(data=request.data, instance=instance)
            required_quantity = request.data.get('quantity')
            if not book.is_available and required_quantity > instance.quantity:
                return Response('This book is Out of stock')
            if required_quantity > book.quantity + instance.quantity:
                return Response('sorry limit reached')

            elif serializer.is_valid():
                if required_quantity > instance.quantity:
                    book.quantity -= required_quantity - instance.quantity
                    book.save()
                elif required_quantity < instance.quantity:
                    book.quantity += instance.quantity - required_quantity
                    book.save()

                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except:
            return Response('book unavailable')