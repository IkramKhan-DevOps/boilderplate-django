from django.contrib import admin
from .models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    """
    Admin interface for the Fee model.
    """
    list_display = (
        'user',
        'amount',
        'discount',
        'tax_rate',
        'total_amount',
        'status',
        'is_paid',
        'due_date',
        'payment_date',
        'created_at'
    )
    list_filter = (
        'status',
        'is_paid',
        'due_date',
        'payment_date',
        'created_at'
    )
    search_fields = ('user__username', 'user__email', 'status')
    ordering = ('-due_date', '-created_at')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    fieldsets = (
        ("Fee Information", {
            'fields': ('user', 'amount', 'discount', 'tax_rate', 'total_amount', 'status', 'is_paid')
        }),
        ("Dates", {
            'fields': ('issue_date', 'due_date', 'payment_date', 'created_at', 'updated_at')
        }),
        ("Payment Details", {
            'fields': ('payment_method',)
        }),
    )

    def get_queryset(self, request):
        """
        Optimize the queryset to prefetch related fields for better performance.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

