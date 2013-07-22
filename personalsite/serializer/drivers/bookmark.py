from flask import url_for, request

from personalsite.serializer.drivers.base import Serializer
from personalsite.serializer.tool import register_for
from personalsite.parser.bookmark import Bookmark, Category, Location


@register_for(Bookmark)
class BookmarkSerializer(Serializer):
    def serialize(self):
        return {
            u'id': self.instance.slug,
            u'type': u'bookmark',
            u'href': u'{}{}'.format(
                request.url_root,
                url_for('bookmark_detail', slug=self.instance.slug)
            ),
            u'slug': self.instance.slug,
            u'title': self.instance.title,
            u'links': {
                u'categories': [i.slug for i in self.instance.categories]
            }
        }


@register_for(Category)
class CategorySerializer(Serializer):
    def serialize(self):
        return {
            u'id': self.instance.slug,
            u'type': u'category',
            u'href': u'{}{}'.format(
                request.url_root,
                url_for('category_detail', slug=self.instance.slug)
            ),
            u'slug': self.instance.slug,
            u'name': self.instance.name,
            u'description': self.instance.description,
            u'links': {
                u'locations': [i.url for i in self.instance.locations]
            }
        }


@register_for(Location)
class LocationSerializer(Serializer):
    def serialize(self):
        return {
            u'id': self.instance.url,
            u'type': u'location',
            u'slug': self.instance.url,
            u'href': self.instance.url,
            u'url': self.instance.url,
            u'description': self.instance.description,
            u'links': {
                u'categories': [i.slug for i in self.instance.categories]
            }
        }
