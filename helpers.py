def query_builder(filters, condition):
    """
    This is an helper function to build the query
    for each rules
    """
    field_mapper = {
        "From": "from_email",
        "To": "to_email",
        "Subject": "subject",
        "Date": "received_date"
    }
    query = 'where '
    for filter in filters:

        logic_raw = filter.get('predicate')
        field_raw = filter.get('field')
        value = filter.get('value')
        time_period_unit = filter.get('time_period_unit')
        field = field_mapper.get(field_raw)

        # For Contains case
        if logic_raw == 'contains':
            sub_query = field+" "+"like '%"+value+"%'"
        # For Equal case
        elif logic_raw == 'equals':
            sub_query = field+'='+"'"+value+"'"
        # For Date range case less than
        elif field_raw == 'Date' and logic_raw == 'less than':
            sub_query = f'received_date < date("now", "-{value} {time_period_unit}")'
        elif field_raw == 'Date' and logic_raw == 'greater than':
            sub_query = f'received_date > date("now", "-{value} {time_period_unit}")'
        # Other cases
        else:
            sub_query = ''
        if sub_query != '':
            if condition == 'all':
                sub_query = sub_query +' and '
            else:
                sub_query = sub_query +' or '
        else:
            print('Got Unhandled logic, passing', logic_raw)
            pass
        query = query + sub_query
    # Removing and/or in the end of the query if any
    query = query.removesuffix(' or ')
    query = query.removesuffix(' and ')
    query = 'select id from emails '+query
    # print('Query is:', query)
    return query