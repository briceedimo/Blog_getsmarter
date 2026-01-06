from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    """
    Formulaire sécurisé pour la création et la modification d’articles.
    """

    class Meta:
        model = Article

        # Champs autorisés côté formulaire
        fields = ['title', 'content', 'category', 'status', 'image']

        # Personnalisation des labels (optionnel mais propre)
        labels = {
            'title': 'Titre',
            'content': 'Contenu',
            'category': 'Catégorie',
            'status': 'Statut',
        }

        # Widgets (rendu + sécurité)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded p-2',
                'placeholder': 'Titre de l’article'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border rounded p-2',
                'rows': 6,
                'placeholder': 'Contenu de l’article'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border rounded p-2'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full border rounded p-2'
            }),
        }
