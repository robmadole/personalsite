from personalsite.serializer.drivers.base import Serializer
from personalsite.serializer.tool import register_for
from personalsite.parser.bookmark import Bookmark, Category, Location


@register_for(Bookmark)
class BookmarkSerializer(Serializer):
    def serialize(self):
        return {
            'id': self.instance.slug,
            'type': 'bookmark',
            'slug': self.instance.slug,
            'title': self.instance.title,
            'categories': [i.slug for i in self.instance.categories]
        }


@register_for(Category)
class CategorySerializer(Serializer):
    def serialize(self):
        return {
            'id': self.instance.slug,
            'type': 'category',
            'slug': self.instance.slug,
            'name': self.instance.name,
            'description': self.instance.description,
            'locations': [i.url for i in self.instance.locations]
        }


@register_for(Location)
class LocationSerializer(Serializer):
    def serialize(self):
        return {
            'id': self.instance.url,
            'type': 'location',
            'slug': self.instance.url,
            'href': self.instance.url,
            'url': self.instance.url,
            'description': self.instance.description,
            'categories': [i.slug for i in self.instance.categories]
        }
