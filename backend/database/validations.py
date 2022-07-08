from marshmallow import validate

NOT_BLANK       = validate.Length(min=1, error='Field cannot be blank')
PASSWORD_LENGTH = validate.Length(min=10, error='Password too short')
IS_INTEGER = validate.Range(min=1, error='Value must be greater than 0')