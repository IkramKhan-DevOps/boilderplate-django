from src.core.mixins import CoreListViewMixin, CoreDetailViewMixin, CoreCreateViewMixin, CoreUpdateViewMixin, \
    CoreDeleteViewMixin


class GenericListViewMixin(CoreListViewMixin):
    permission_prefix = 'management'


class GenericDetailViewMixin(CoreDetailViewMixin):
    permission_prefix = 'management'


class GenericCreateViewMixin(CoreCreateViewMixin):
    permission_prefix = 'management'


class GenericUpdateViewMixin(CoreUpdateViewMixin):
    permission_prefix = 'management'


class GenericDeleteViewMixin(CoreDeleteViewMixin):
    permission_prefix = 'management'
