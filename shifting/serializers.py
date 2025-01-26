from rest_framework import serializers 

from .models import DailyShift, Shifting



class DailyShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyShift
        fields = '__all__'
    
    # to representation for daily shift
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['shift'] = ShiftingSerializer(instance.shift).data
    #     return data


class ShiftingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shifting
        fields = '__all__'
    
    # to representation for daily shift 
    def to_representation(self, instance):
        print('instance ', instance)
        data = super().to_representation(instance)
        # shifts = DailyShift.objects.all()
        data['shift'] = DailyShiftSerializer(instance.shift, many=True).data
        return data
    
