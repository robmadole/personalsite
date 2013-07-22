class KeywordView extends Backbone.View
  events :
    'keyup #q': 'search'

  search : (e) =>
    e.stopPropagation()

    queryString = @$el.find('#q').val()

    @options.searchKeyword.set 'queryString', queryString
