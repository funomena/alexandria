from datastore.models import *
from django.db.models import Q


def get_build_query_set(metadata, base_list):
	q_list = None
	print metadata
	all_meta_cats = MetaDataCategory.objects.prefetch_related('values').filter(slug__in = metadata.keys())
	print len(all_meta_cats)
	for meta_cat in all_meta_cats:
		meta_value = metadata.get(meta_cat.slug, None)
		if meta_value:
			q_subset = 	Q(metadata__category__slug = meta_cat.slug, metadata__value = meta_value)
			
			if q_list is None:
				q_list = base_list.filter(q_subset).distinct()
			else:
				q_list &= base_list.filter(q_subset).distinct()

	return q_list
