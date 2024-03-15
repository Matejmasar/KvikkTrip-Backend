import sqlalchemy
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2


class Coordinate:
    """
    Container to hold a geolocation.
    """

    lat: float
    lng: float


class LatLngType(sqlalchemy.types.UserDefinedType):
    """
    Custom SQLAlchemy type to handle POINT columns.

    References:

    - https://gist.github.com/kwatch/02b1a5a8899b67df2623
    - https://docs.sqlalchemy.org/en/14/core/custom_types.html#sqlalchemy.types.UserDefinedType  # noqa
    """

    # Can do because we made the Coordinate dataclass hashable.
    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_expression(self, bindvalue):
        return sqlalchemy.func.POINT(bindvalue, type_=self)

    def bind_processor(self, dialect):
        """
        Return function to serialize a Coordinate into a database string literal.
        """

        def process(value: Coordinate | Tuple[float, float] | None) -> str | None:
            if value is None:
                return None

            if isinstance(value, tuple):
                value = Coordinate(*value)

            return f"({value.lat},{value.lng})"

        return process

    # def result_processor(self, dialect, coltype):
    #     """
    #     Return function to parse a database string result into Python data type.
    #     """

    #     def process(value: str) -> Coordinate | None:
    #         if value is None:
    #             return None

    #         if not isinstance(value, str):
    #             return None  # Or handle unsupported type appropriately

    #         try:
    #             lat, lng = value.strip("()").split(",")
    #             return Coordinate(float(lat), float(lng))
    #         except (ValueError, TypeError):
    #             return None

    #    return process

    # from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

    # def (result: PGDialect_psycopg2) -> CustomDataType:
    #     """
    #     Parse a database result into a Python data type.
    #     """
    #     # Example parsing logic
    #     # Replace this with your actual parsing logic
    #     parsed_data = CustomDataType(result)  # Example: Create CustomDataType object from result
    #     return parsed_data


        def result_processor(self, dialect, coltype):
            """
            Parse a database result into a Python data type.
            """
            # Example parsing logic
            # Replace this with your actual parsing logic
            parsed_data = LatLngType(dialect)  # Example: Create CustomDataType object from result
            return parsed_data
        
        return result_processor