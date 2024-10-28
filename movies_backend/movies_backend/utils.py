from drf_yasg import openapi


def get_header_param():
    header_param = openapi.Parameter('Authorization', openapi.IN_HEADER, description='Token \'token_number\'', type=openapi.IN_HEADER)

    return [header_param]

def get_scraping_error_property():
    scraping_property = openapi.Schema(type=openapi.TYPE_STRING, description="Couldn't scrap required parameters")

    return scraping_property

def get_serializer_error_property():
    serializer_property = openapi.Schema(type=openapi.TYPE_STRING, description="Serializer errors")

    return serializer_property

def get_request_data_error_property():
    request_data_property = openapi.Schema(type=openapi.TYPE_STRING, description="Provided wrong request data")

    return request_data_property

def get_title_error_property():
    title_property = openapi.Schema(type=openapi.TYPE_STRING, description="There is no media named title in the database.")

    return title_property

def get_server_error_property():
    server_property = openapi.Schema(type=openapi.TYPE_STRING, description="There is no media named title in the database.")

    return server_property