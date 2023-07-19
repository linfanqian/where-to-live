def search_condition_to_dict(search_condition):
    return {
        'platforms': search_condition.platforms,
        'lowest_price': search_condition.lowest_price,
        'highest_price': search_condition.highest_price,
        'location': search_condition.location,
        'building_types': search_condition.building_types,
        'include_water': search_condition.include_water,
        'include_hydro': search_condition.include_hydro,
        'include_internet': search_condition.include_internet,
        'independent_bathroom': search_condition.independent_bathroom,
        'independent_kitchen': search_condition.independent_kitchen
    }