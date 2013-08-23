class SearchResultCollection extends Backbone.Collection
  url : '/bookmarks/search'

  model : SearchResultModel

  parse : (response, options) =>
    @links = response.links

    return response.search

  search : (queryString) =>
    options =
      data:
        q: queryString
      reset: true

    if @xhr
      @xhr.abort()

    @xhr = @fetch options

    return @xhr
