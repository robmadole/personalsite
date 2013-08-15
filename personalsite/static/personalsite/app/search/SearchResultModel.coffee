class SearchResultModel extends Backbone.Model
  url : =>
    @get('href')

  toJSON : =>
    _.extend(super(), {url: @url()})
