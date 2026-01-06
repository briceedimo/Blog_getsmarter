from django.contrib import admin
from .models import Category, Article, ContactMessage

# admin.site.register(Category)
# admin.site.register(Article)
# admin.site.register(ContactMessage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser




@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author == request.user:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author == request.user:
            return True
        return False




@admin.register(ContactMessage)
class ContactMessage(admin.ModelAdmin):
    """
    Affichage sécurisé des messages de contact
    """

    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)

    # Champs en lecture seule (sécurité)
    readonly_fields = (
        'name',
        'email',
        'subject',
        'message',
        'created_at'
    )

    # Désactiver les actions dangereuses
    def has_add_permission(self, request):
        return False  # impossible d'ajouter depuis l’admin

    def has_change_permission(self, request, obj=None):
        return False  # impossible de modifier

    def has_delete_permission(self, request, obj=None):
        # Seul l'admin peut supprimer
        return request.user.is_superuser

# Register your models here.
