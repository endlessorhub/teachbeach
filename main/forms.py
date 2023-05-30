import json
from django import forms
from django.conf import settings
from .models import MetaTag

class MetatagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MetatagForm, self).__init__(*args, **kwargs)

        fn = settings.BASE_DIR + '/js/src/sitemap_template.json'
        with open(fn, 'r') as json_file:
            data = json.load(json_file)
            choices = [(x['path'], x['path']) for x in data['routes']]
            choices = sorted(choices)

            self.fields['route'] = forms.ChoiceField(choices=choices)


    class Meta:
        model = MetaTag
        fields =  '__all__'
