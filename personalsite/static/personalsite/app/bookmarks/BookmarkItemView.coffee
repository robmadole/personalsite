class BookmarkCardView extends Backbone.View
  events :
    'click [role=category-expander]': 'toggleCategories'

  toggleCategories: (e) ->
    e.preventDefault()

    @$('[role=categories]').toggleClass 'collapse'


$(document).ready ->
  $('[role=bookmarks] [role=card]').each ->
    new BookmarkCardView el: this
