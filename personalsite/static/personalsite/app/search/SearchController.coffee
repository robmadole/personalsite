class SearchController
  constructor : (searchForm, searchResults) ->
    searchKeyword          = new SearchKeywordModel()
    searchResultCollection = new SearchResultCollection()

    @$searchFormElement    = searchForm
    @$searchResultsElement = searchResults

    searchKeyword.on 'change:queryString', (searchKeyword, queryString) ->
      searchResultCollection.search(queryString)

    new KeywordView(
      el                     : @$searchFormElement,
      searchKeyword          : searchKeyword,
      searchResultCollection : searchResultCollection
    )

    new SearchResultsView(
      el                     : @$searchResultsElement,
      searchKeyword          : searchKeyword,
      searchResultCollection : searchResultCollection,
    )


$(document).ready ->
  new SearchController $('[role=search-bookmarks-form]'), $('[role=search-results]')
