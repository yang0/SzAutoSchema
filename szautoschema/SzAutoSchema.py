from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.utils import force_real_str
from drf_yasg import  openapi

class SzAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys):
        operation = super().get_operation(operation_keys)
        if not hasattr(operation, 'summary'):
            operation.summary = operation.description

        return operation
