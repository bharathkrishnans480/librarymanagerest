from rest_framework import serializers
from bookshelf.models import User,Book,IssueBook

class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'volume', 'quantity','is_available')

    def get_is_available(self, instance):
        if instance.is_available:
            return 'available'
        else:
            return 'sorry not in stock'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = [
            'email'
            'username',
            'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)





class IssueBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueBook
        fields = '__all__'
        read_only_fields = ('created_at',)
