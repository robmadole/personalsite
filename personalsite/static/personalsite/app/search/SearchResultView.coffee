class SearchResultsView extends Backbone.View
  initialize : ->
    @options.searchResultCollection.on('reset', @render)

  template : =>
    return Handlebars.templates['results.html']

  render : =>
    @$el.html @template() {
      results : @options.searchResultCollection.toJSON()
      keyword : @options.searchKeyword.get('queryString')
    }


Handlebars.registerHelper 'resultType', (type, options) ->
  if type == @type
    return options.fn @
  else
    return options.inverse @
