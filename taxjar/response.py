from taxjar.data import TaxJarData
from taxjar.exceptions import TaxJarResponseError
from IPython import embed

class TaxJarResponse:
    def from_request(self, request):
        response = request.json()
        if 200 <= request.status_code <= 400:
            (type_name, values), = response.items()
            return TaxJarData.build_from_response(type_name, values)
        else:
            self.raise_response_error(response)

    def raise_response_error(self, response):
        status = response['status']
        error = response['error']
        detail = response['detail']
        error = TaxJarResponseError(str(status) + " " + error)
        error.full_response = { 'response': response, 'status_code': status, 'detail': detail }
        raise error