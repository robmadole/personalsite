class SearchResult extends Backbone.Model


class SearchCollection extends Backbone.Collection
  url : '/bookmarks/search'

  model : SearchResult

  parse : (response, options) =>
    return response.search

  search : (queryString) =>
    options =
      data:
        q: queryString
      reset: true

    return @fetch options


class SearchResultsView extends Backbone.View
  initialize : ->
    @options.searchCollection.on('reset', @render)

  render : =>
    console.log(@options.searchCollection)


class KeywordView extends Backbone.View
  events :
    'keyup #q': 'search'

  search : (e) =>
    e.stopPropagation()

    queryString = @$el.find('#q').val()

    this.options.searchCollection.search queryString


$(document).ready ->
  search = new SearchCollection()

  $('[role=search-results]').each ->
    new SearchResultsView el: this, searchCollection: search

  $('[role=search-bookmarks-form]').each ->
    new KeywordView el: this, searchCollection: search
