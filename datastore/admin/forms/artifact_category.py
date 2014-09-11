from datastore.models import ArtifactCategory
from django.forms import ModelForm
from django.utils.text import slugify


class ArtifactCategoryForm(ModelForm):

    def save(self, commit):
        c = self.clean()
        self.instance.slug = slugify(c['friendly_name'])
        return super(ArtifactCategoryForm, self).save(commit)

    class Meta:
        model = ArtifactCategory
        fields = ('friendly_name', 'installer_type', 'extension',)
