items_access_parameters = {
    'methods': {
        'GET': 0,
        'POST': (3,)
    }
}

item_access_parameters = {
    'methods': {
        'GET': 0,
        'PUT': (3,),
        'DELETE': (3,)
    }
}

offers_parameters = {
    'methods': {
        'GET': 0,
        'POST': (2,)
    }
}

offer_parameters = {
    'methods': {
        'GET': 0,
        'PUT': (2,),
        'DELETE': (2, 3)
    }
}

recommended_items_parameters = {
    'methods': {
        'GET': (1,)
    }
}

similar_items_parameters = {
    'methods': {
        'GET': 0
    }
}

users_parameters = {
    'methods': {
        'GET': (1, )
    }
}

user_parameters = {
    'methods': {
        'GET': 0,
        'PUT': (1, ),
        'DELETE': (1, 3)
    }
}

user_actions_parameters = {
    'methods': {
        'GET': (1,),
        'POST': (1,)
    }
}