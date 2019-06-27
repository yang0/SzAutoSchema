from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.utils import force_real_str
from drf_yasg import  openapi

class SzAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys):
        operation = super().get_operation(operation_keys)
        if not hasattr(operation, 'summary'):
            dp = operation.description

            # 如果注释有换行符，那么summary只取一行
            index = dp.find('\n')
            if index > 0:
                operation.summary = dp[:index]
            else:
                operation.summary = operation.description

        return operation