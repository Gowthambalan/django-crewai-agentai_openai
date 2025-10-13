# from rest_framework import serializers
# from .models import QueryLog

# class QueryLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QueryLog
#         fields = ['id', 'User_query', 'Decision', 'Response', 'Created_at']
#         read_only_fields = ['id', 'created_at']

# class QueryInputSerializer(serializers.Serializer):
#     user_query = serializers.CharField(max_length=1000, required=True)
    
#     def validate_user_query(self, value):
#         """Custom validation for user query"""
#         if len(value.strip()) < 2:
#             raise serializers.ValidationError("Query must be at least 2 characters long")
#         return value

# class QueryResponseSerializer(serializers.Serializer):
#     decision = serializers.CharField(max_length=20)
#     answer = serializers.CharField()
#     query_id = serializers.IntegerField(required=False)  # ID of saved QueryLog




from rest_framework import serializers
from .models import QueryLog

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = ['id', 'user_query', 'decision', 'response', 'created_at']
