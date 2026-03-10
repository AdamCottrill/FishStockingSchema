def validate(data_in, schema):
    valid_data = []
    errors = []

    try:
        data = schema(**data_in)
        if data:
            valid_data.append(data)
    except Exception as e:
        # validation error
        errors.append(e)

    return {"data": valid_data, "errors": errors}
