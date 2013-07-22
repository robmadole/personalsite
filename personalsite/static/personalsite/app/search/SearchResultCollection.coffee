class SearchResultCollection extends Backbone.Collection
  url : '/bookmarks/search'

  model : SearchResultModel

  parse : (response, options) =>
    return response.search

  search : (queryString) =>
    options =
      data:
        q: queryString
      reset: true

    return @fetch options
