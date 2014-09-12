from datastore.models import Build, MetadataCategory, Tag
from django.contrib import admin
from django import forms


class BuildForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BuildForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        for c in MetadataCategory.objects.all():
            r = c.required
            name = c.friendly_name
            if r:
                name += " *"

            field = forms.CharField(label=name, readonly=True)
            if not instance is None:
                metas = instance.metadata.filter(category=c)
                if metas.count() != 0:
                    field.initial = metas[0]
            self.fields["category_%s" % c.pk] = field

        for t in Tag.objects.all():
            field = forms.BooleanField(required=False, label=t.value)
            if not instance is None and instance.tags.filter(pk=t.pk).exists():
                field.initial = True
            self.fields["tag_%s" % t.pk] = field


    def save(self, *args, **kwargs):
        cleaned = self.clean()
        commit = kwargs['commit']
        self.instance.save()
        for name, value in cleaned.iteritems():
            if "category" in name:
                cat_id = int(name.split("_")[1])
                has_meta_of_type = self.instance.metadata.filter(category__pk=cat_id).exists()
                if not has_meta_of_type and not value is None:
                    self.instance.metadata.add(value)
                    continue
                elif has_meta_of_type:
                    meta = self.instance.metadata.get(category__pk=cat_id)
                    if meta.value != value.value:
                        self.instance.metadata.remove(meta)
                        self.instance.metadata.add(value)
                        continue
            elif "tag" in name:
                tag_id = int(name.split("_")[1])
                has_tag = self.instance.tags.filter(pk=tag_id).exists()
                if has_tag and value == False:
                    self.instance.tags.remove(self.instance.tags.get(pk=tag_id))
                elif not has_tag and value == True:
                    self.instance.tags.add(Tag.objects.get(pk=tag_id))
        return super(BuildForm, self).save(commit=commit)
    
    class Meta:
        model = Build
        fields = ('name',)


