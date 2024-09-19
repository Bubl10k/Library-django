from django import forms

from .models import Collection

class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="")
    

class CollectionCreateForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title']
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if Collection.objects.filter(title=title).exists():
            raise forms.ValidationError('Collection with this title already exists.')
        return title
    

class CollectionSelectForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.all(),
        label="Choose a Collection",
        empty_label="Select a collection",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
