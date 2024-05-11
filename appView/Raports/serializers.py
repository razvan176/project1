from rest_framework import serializers
from .models import Pmta

# class PmtaSerializer(serializers.ModelSerializer):
#     set_name = serializers.CharField(source='set_name.set_name')  # Serialize set_name field from the related Set model

#     class Meta:
#         model = Pmta
#         fields = ['set_name', 'date', 'hour', 'number_send', 'ip', 'id_mint']