from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'num_pages', 
                  'cur_num_pages', 'description', 'status']
        
    def clean_num_pages(self):
        data = self.cleaned_data['num_pages']
        if data >= 0:
            return data
        else:
            raise forms.ValidationError('Number of pages must be higher than 0')
    
    def clean_cur_num_pages(self):
        data = self.cleaned_data['cur_num_pages']
        if data >= 0:
            return data
        else:
            raise forms.ValidationError('Number of pages must be higher than 0')
