def enumerate_dict(param, dic):
    """
    Builds a dictionary of an enumerated parameter. Takes any dictionary and returns
    a dictionary recursively
    ie. enumerate_list('MarketplaceIdList.Id', (123, 345, 4343))
        returns
        {
            MarketplaceIdList.Id.1: 123,
            MarketplaceIdList.Id.2: 345,
            MarketplaceIdList.Id.3: 4343
        }
    Args:
        param (`str`): the beginning of the key in the returned dictionary
        values(`list`): the values in the returned dictionary
    """

    params = {}
    if dic is not None:
        if not param.endswith('.'):
            param = "{}.".format(param)
        for key, value in dic.items():
            if isinstance(value, list):
                for sub_key, sub_value in enumerate_list(param=key, values=value).items():
                    params['{}{}'.format(key, sub_key)] = sub_value
            elif isinstance(value, dict):
                for sub_key, sub_value in enumerate_dict(param=key, dic=value).items():
                    params['{}{}'.format(key, sub_key)] = sub_value
            else:
                params['{}{}'.format(param, key)] = value
    return params


def enumerate_list(param, values):
    """
    Builds a dictionary of an enumerated parameter. Takes any iterable and returns a dictionary.
    ie. enumerate_list('MarketplaceIdList.Id', (123, 345, 4343))
        returns
        {
            MarketplaceIdList.Id.1: 123,
            MarketplaceIdList.Id.2: 345,
            MarketplaceIdList.Id.3: 4343
        }
    Args:
        param (`str`): the beginning of the key in the returned dictionary
        values(`list`): the values in the returned dictionary
    Returns:
        :obj:`DictWrapper`
    """
    params = {}
    if values is not None:
        if not param.endswith('.'):
            param = "{}.".format(param)
        for num, value in enumerate(values):
            if isinstance(value, list):
                for sub_key, sub_value in enumerate_dict(num, dic=values).items():
                    params['{}{}'.format(param, (num + 1))] = sub_value
            elif isinstance(value, dict):
                for sub_key, sub_value in enumerate_dict(num, dic=values).items():
                    params['{}{}'.format(param, (num + 1))] = sub_value
            else:
                params['{}{}'.format(param, (num + 1))] = value
    return params
