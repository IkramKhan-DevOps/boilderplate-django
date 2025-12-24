from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from root.model_lookup import MODEL_CLASS_LOOKUP
from src.services.accounts.models import User

ROLE_MODEL_PERMISSIONS = {
    # 'client': {
    #     **{
    #         model: ['view', 'add', 'change']
    #         for model in MODEL_CLASS_LOOKUP[''].keys()
    #     },
    # },
}


@receiver(post_save, sender=User)
def assign_role_permissions(sender, instance, created, **kwargs):
    if not created:
        return

    role = instance.user_type
    if role not in ROLE_MODEL_PERMISSIONS:
        return

    role_perms = ROLE_MODEL_PERMISSIONS[role]
    permissions_to_add = []

    for model_name, perms in role_perms.items():
        model_class = None
        for models_dict in MODEL_CLASS_LOOKUP.values():
            if model_name in models_dict:
                model_class = models_dict[model_name]
                break

        if not model_class:
            continue

        try:
            content_type = ContentType.objects.get_for_model(model_class)

            codenames = [f"{perm_code}_{model_class._meta.model_name}" for perm_code in perms]
            permissions = Permission.objects.filter(
                codename__in=codenames
            )
            permissions_to_add.extend(permissions)

            for codename in codenames:
                if not permissions.filter(codename=codename).exists():
                    print(f"[WARNING] Permission '{codename}' does not exist for model '{model_name}'")
        except ContentType.DoesNotExist:
            print(f"[ERROR] ContentType for model '{model_name}' does not exist.")
            continue

    if permissions_to_add:
        instance.user_permissions.add(*permissions_to_add)
        print(f"[DEBUG] Assigned {len(permissions_to_add)} permissions to user '{instance.username}'")
    else:
        print(f"[DEBUG] No permissions assigned to user '{instance.username}'")
