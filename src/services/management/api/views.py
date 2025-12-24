from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .serializers import AnnualIncomeSerializer
from ..models import AnnualIncome, State, Industry


class AnnualIncomeFilterAPIView(RetrieveAPIView):
    """
    PARAM: state_id, industry_id (required)
    RETURN: only matched AnnualIncome object single
    AUTH: open
    """
    serializer_class = AnnualIncomeSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """
        Override get_object to ensure the object is fetched based on state_id and industry_id.
        """
        state_id = self.kwargs.get('state_id')
        industry_id = self.kwargs.get('industry_id')

        # Validate required parameters
        if not state_id or not industry_id:
            raise ValidationError("Both state_id and industry_id are required")

        state = get_object_or_404(State.objects.all(), id=state_id)
        industry = get_object_or_404(Industry.objects.all(), id=industry_id)

        # Get the actual AnnualIncome object based on state and industry
        annual_income = get_object_or_404(
            AnnualIncome,
            state=state,
            industry=industry,
        )

        return annual_income