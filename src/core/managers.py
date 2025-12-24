from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

class RelatedObjectManager:
    """
    A utility class for managing related objects (via ForeignKey or OneToOne relations)
    within detailed views, especially in admin-style or dashboard-style interfaces.

    This manager handles:
    - Fetching related objects for a given parent object.
    - Generating update forms for each related object.
    - Optionally paginating the related queryset.
    - Creating a form for adding new related objects with pre-filled context.

    Args:
        model_class (Model): The Django model class for the related object.
        form_class (Form): The form class used for both updating and creating related objects.
        related_name (str): The related manager name from the parent model (e.g., 'items' for `invoice.items.all()`).
        init_data (dict): Additional fields to inject into the create form's initial data.
        relation_type (str): Type of relation from parent to child ('fk' for ForeignKey, 'onetoone' for OneToOneField).
        paginate_by (int, optional): Number of related objects per page. If None, pagination is disabled.

    Methods:
        get_objects_and_forms(parent_obj, request):
            Returns a tuple containing:
                - A list of related objects.
                - A dictionary of update forms keyed by object ID.
                - A `page_obj` if pagination is enabled, otherwise None.

        get_create_form(parent_obj):
            Returns a blank form for creating a related object, with the parent object pre-set in the initial data.

    Example:
        manager = RelatedObjectManager(
            model_class=InvoiceItem,
            form_class=InvoiceItemForm,
            related_name='items',
            relation_type='fk',
            init_data={'created_by': request.user},
            paginate_by=10
        )
    Output:
        'related_data': {
              'items': {
                'verbose_name': 'Invoice item',
                'verbose_name_plural': 'Invoice items',
                'model_class': <InvoiceItemModel>,
                'objects': <QuerySet [...InvoiceItem instances...]>,
                'update_forms': {5: <InvoiceItemForm>, 4: <InvoiceItemForm>},
                'create_form': <InvoiceItemForm>,
                'page_obj': None
              }
            }

    """

    def __init__(self, model_class, form_class, related_name, init_data, relation_type='fk', paginate_by=None):
        self.model_class = model_class
        self.form_class = form_class
        self.related_name = related_name
        self.init_data = init_data

        self.relation_type = relation_type
        self.paginate_by = paginate_by

    def get_objects_and_forms(self, parent_obj, request):
        related_attr = getattr(parent_obj, self.related_name)

        if self.relation_type == 'fk':
            related_qs = related_attr.all()
            if self.paginate_by:
                paginator = Paginator(related_qs, self.paginate_by)
                query_param = f'{related_qs.model._meta.model_name}_page'
                page_number = request.GET.get(query_param)
                page_obj = paginator.get_page(page_number)
                objs = page_obj.object_list
            else:
                objs = related_qs
                page_obj = None

            forms_dict = {obj.id: self.form_class(instance=obj) for obj in objs}
            return objs, forms_dict, page_obj

        elif self.relation_type == 'onetoone':
            try:
                obj = related_attr
            except ObjectDoesNotExist:
                obj = None

            form = self.form_class(instance=obj) if obj else None
            objs = [obj] if obj else []
            forms_dict = {obj.pk: form} if form else {}
            return objs, forms_dict, None

        else:
            raise ValueError(f"Unknown relation_type {self.relation_type}")

    def get_create_form(self, parent_obj):
        parent_model_name = parent_obj._meta.model_name
        initial_data = {parent_model_name: parent_obj}

        additional_initial = self.init_data or {}
        initial_data.update(additional_initial)
        return self.form_class(initial=initial_data)

    def get_model(self):
        return self.model_class

    def get_related_data(self, parent_obj, request):
        model_meta = self.model_class._meta

        objs, forms, page_obj = self.get_objects_and_forms(parent_obj, request)

        related_data = {
            self.related_name: {
                'verbose_name': model_meta.verbose_name.capitalize(),
                'verbose_name_plural': model_meta.verbose_name_plural.capitalize(),
                'model_class': self.get_model(),
                'objects': objs,
                'update_forms': forms,
                'create_form': self.get_create_form(parent_obj),
                'page_obj': page_obj,
            }
        }

        return related_data

