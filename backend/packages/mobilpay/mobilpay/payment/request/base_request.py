import hashlib
import time
import random
from urllib.parse import unquote
from mobilpay.payment.request.notify import Notify
from mobilpay.util.encrypt_data import Crypto


"""
    BaseRequest class is used as a base for all the payments types
"""


class BaseRequest:

    CONFIRM_ERROR_TYPE_NONE = 0x00
    CONFIRM_ERROR_TYPE_TEMPORARY = 0x01
    CONFIRM_ERROR_TYPE_PERMANENT = 0x02

    ERROR_LOAD_X509_CERTIFICATE = 0x10000001
    ERROR_ENCRYPT_DATA = 0x10000002

    ERROR_PREPARE_MANDATORY_PROPERTIES_UNSET = 0x11000001

    ERROR_FACTORY_BY_XML_ORDER_ELEM_NOT_FOUND = 0x20000001
    ERROR_FACTORY_BY_XML_ORDER_TYPE_ATTR_NOT_FOUND = 0x20000002
    ERROR_FACTORY_BY_XML_INVALID_TYPE = 0x20000003

    ERROR_LOAD_FROM_XML_ORDER_ID_ATTR_MISSING = 0x30000001
    ERROR_LOAD_FROM_XML_SIGNATURE_ELEM_MISSING = 0x30000002

    ERROR_CONFIRM_LOAD_PRIVATE_KEY = 0x300000f0
    ERROR_CONFIRM_FAILED_DECODING_DATA = 0x300000f1
    ERROR_CONFIRM_FAILED_DECODING_ENVELOPE_KEY = 0x300000f2
    ERROR_CONFIRM_FAILED_DECRYPT_DATA = 0x300000f3
    ERROR_CONFIRM_INVALID_POST_METHOD = 0x300000f4
    ERROR_CONFIRM_INVALID_POST_PARAMETERS = 0x300000f5
    ERROR_CONFIRM_INVALID_ACTION = 0x300000f6

    VERSION_QUERY_STRING = 0x01
    VERSION_XML = 0x02
    # declare member variables
    """
        * signatue(Mandatory) - signature received from mobilpay.ro that identifies merchant account
        *
        * var string(64)

     """
    _signature = None

    """
        * service - identifier of service/product for which you're requesting a payment
        * Mandatory for Mobilpay_Payment_Request_Sms
        * Optional for Mobilpay_Payment_Request_Card
    """
    _service = None

    """
        * orderId(Mandatory) - payment transaction identifier generated by merchant helps merchant to interpret a request to confirm or return url
        * it should be unique for the specified signature
        *
        * var string(64)
    """
    _orderId = None
    _timestamp = None

    _type = None

    _objPmNotify = None

    """
        * returnUrl(Optional) - URL where the user is redirected from mobilpay.ro payment interface
        * when the transaction is canceled or confirmed. If it is not supplied the application will use
        * return URL configured in control panel
        * use it only if you want to overwrite the configured one otherwise set it's value to NULL
        * var string
    """
    _returnUrl = None

    """
        * confirmUrl(Optional) - URL of the seller that will be requested when mobilpay.ro will make
        * a decision about payment(e.g. confirmed, canceled). If it is not supplied the application will use
        * confirm URL configured in control panel
        * use it only if you want to overwrite the configured one otherwise set it's value to NULL
        *
        * var string
    """

    _confirmUrl = None

    _params = []

    """
        * outEnvKey - output envelope key
        * in this property is stored the envelope key after encrypting data to send to payment interface
        */
    """
    _outEnvKey = None

    """
        * outEncData - output encrypted data
        * in this property is stored the encrypted data to send to payment interface
        */
    """

    _outEncData = None
    _xmlDoc = None
    _requestIdentifier = None
    _objRequestParams = {}
    _objRequestInfo = None

    _objReqNotify = None

    def __init__(self):
        self._requestIdentifier = hashlib.md5(
            str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest()

    def _parse_from_xml(self, element):
        attr = element.getAttribute("id")
        if attr is None or len(str(attr)) == 0:
            raise Exception(
                "parse_from_xml failed -> empty order id ", self.ERROR_LOAD_FROM_XML_ORDER_ID_ATTR_MISSING)
        self._orderId = attr

        elems = element.getElementsByTagName("signature")
        if len(elems) != 1:
            raise Exception(
                "parse_from_xml failed -> signature is missing ", self.ERROR_LOAD_FROM_XML_SIGNATURE_ELEM_MISSING)
        signature = elems[0]
        self._signature = signature.firstChild.nodeValue

        elems = element.getElementsByTagName("url")
        if len(elems) == 1:
            url = elems[0]
            elems = url.getElementsByTagName("return")
            if len(elems) == 1:
                self._returnUrl = elems[0].firstChild.nodeValue

            elems = url.getElementsByTagName("confirm")
            if len(elems) == 1:
                self._confirmUrl = elems[0].firstChild.nodeValue

        self._params = []
        param_elems = element.getElementsByTagName("params")
        if len(param_elems) == 1:
            param_elems = param_elems[0].getElementsByTagName("param")
            for param in param_elems:
                xml_param = param
                elems = xml_param.getElementsByTagName("name")
                if len(elems) != 1:
                    continue
                param_name = elems[0].firstChild.nodeValue

                elems = xml_param.getElementsByTagName("value")

                if len(elems) != 1:
                    continue

                self._params[param_name] = unquote(
                    elems[0].firstChild.nodeValue)

        elems = element.getElementsByTagName("mobilpay")
        if len(elems) == 1:
            self._objPmNotify = Notify(elems[0])

        return self

    def _encrypt(self, x509_file_path):

        public_key = Crypto.get_rsa_key(x509_file_path)

        if public_key is False or public_key is None:
            self._outEncData = None
            self._outEnvKey = None
            error_message = "Error while loading X509 public key certificate! Reason:"

            raise Exception(
                error_message, self.ERROR_LOAD_X509_CERTIFICATE)

        src_data = self._xmlDoc.toprettyxml(
            indent="\t", newl="\n", encoding="utf-8")
        result = Crypto.encrypt(src_data, public_key)

        if result is False:
            self._outEncData = None
            self._outEnvKey = None
            error_message = "Error while encrypting data! Reason:"

            raise Exception(error_message, self.ERROR_ENCRYPT_DATA)

        self._outEncData, self._outEnvKey = result

    def get_env_key(self):
        return self._outEnvKey

    def get_enc_data(self):
        return self._outEncData

    def get_request_identifier(self):
        return self._requestIdentifier

    def set_signature(self, signature):
        self._signature = signature

    def set_order_id(self, order_id):
        self._orderId = order_id

    def get_order_id(self):
        return self._orderId

    def get_notify(self):
        return self._objPmNotify
