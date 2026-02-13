import uuid

import sqlalchemy


def build_model_filters(model, query, field, extra_columns=None):
    if extra_columns is None:
        extra_columns = {}
    filters = []
    if query:
        # The field exists as an exposed column
        if model.__mapper__.has_property(field):
            column = getattr(model, field)

            if type(column.type) == sqlalchemy.sql.sqltypes.Integer:
                _filter = column.op("=")(query)
            elif isinstance(column.type, sqlalchemy.UUID) or isinstance(
                column.type, sqlalchemy.dialects.postgresql.UUID
            ):
                try:
                    _filter = column.op("=")(uuid.UUID(str(query)))
                except (ValueError, TypeError):
                    _filter = sqlalchemy.sql.false()
            else:
                _filter = column.like(f"%{query}%")
            filters.append(_filter)
        else:
            if field in extra_columns:
                column = extra_columns[field]
                if type(column.type) == sqlalchemy.sql.sqltypes.Integer:
                    _filter = column.op("=")(query)
                elif isinstance(column.type, sqlalchemy.UUID) or isinstance(
                    column.type, sqlalchemy.dialects.postgresql.UUID
                ):
                    try:
                        _filter = column.op("=")(uuid.UUID(str(query)))
                    except (ValueError, TypeError):
                        _filter = sqlalchemy.sql.false()
                else:
                    _filter = column.like(f"%{query}%")
                filters.append(_filter)
    return filters
