from rest_framework import serializers

from ..models import AnnualIncome, State, Industry


class AnnualIncomeSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    industry_name = serializers.CharField(source='industry.name', read_only=True)

    class Meta:
        model = AnnualIncome
        fields = ['id', 'name', 'rate', 'state_name', 'industry_name', 'is_active']