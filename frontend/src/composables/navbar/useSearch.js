export function useSearch() {
  // typical component logic where it will based on the selection of user and redirect to search page
  const handleSelection = (selection) => {
    // Set the search input to the selected item's name
    const itemName = getItemNameByType(selection.item, selection.type)

    // Call goSearch to navigate to search page
    goSearch(itemName)
  }

  const getItemNameByType = (item, type) => {
    // console.log('getItemNameByType called with:', { item, type })

    if (!item) {
      console.warn('Item is null or undefined')
      return 'Unknown Item'
    }

    switch (type) {
      case 'listings':
        return item.listingName || item.name
      case 'venues':
        return item.venueName || item.name
      case 'producers':
        return item.producerName || item.name
      default:
        // Fallback: try common name properties
        return item.name || item.listingName || item.venueName || item.producerName
    }
  }

  const goSearch = (itemName) => {
    if (!itemName || itemName.trim() === "" || itemName === "Unknown Item") {
      console.warn('Invalid item name for search:', itemName)
      return
    }

    // Remove any '/' from search input
    //const cleanItemName = itemName.replace(/\//g, "")
    const cleanItemName = encodeURIComponent(itemName.trim())
    // console.log('Clean item name:', cleanItemName)

    // If already on search page, refresh the page with new search input
    if (window.location.pathname.split("/")[1] === "search") {
      // console.log('Already on search page, redirecting to:', `/search/${cleanItemName}`)
      window.location.href = `/search/${cleanItemName}`
    } else {
      // Re-route to search page using window.location (since we don't have router in setup)
      // console.log('Redirecting to search page:', `/search/${cleanItemName}`)
      window.location.href = `/search/${cleanItemName}`
    }
  }

  return { handleSelection }
}