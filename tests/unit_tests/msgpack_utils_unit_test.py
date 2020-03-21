""" Test the Message Pack Utils """

from decimal import Decimal
from uuid import uuid4

from service_framework.utils import msgpack_utils


def test_msgpack_utils__custom_encode__can_encode_decimals():
    """
    Make sure the custom encoder can encode decimal objects
    """
    to_test = Decimal('123.456')
    encoded = msgpack_utils.custom_encode(to_test)
    assert encoded == {'__decimal__': True, 'as_str': str(to_test)}


def test_msgpack_utils__custom_encode__can_encode_sets():
    """
    Make sure the custom encoder can encode set objects
    """
    to_test = set(['hi', 'bye'])
    encoded = msgpack_utils.custom_encode(to_test)
    assert encoded == {'__set__': True, 'value': list(to_test)}


def test_msgpack_utils__custom_encode__can_encode_uuids():
    """
    Make sure the custom encoder can encode uuid objects
    """
    to_test = uuid4()
    encoded = msgpack_utils.custom_encode(to_test)
    assert encoded == {'__uuid__': True, 'as_str': str(to_test)}


def test_msgpack_utils__custom_encode__do_nothing_for_regular_obj():
    """
    Make sure the custom encoder only encodes specific object types.
    """
    to_test = 'Test!'
    encoded = msgpack_utils.custom_encode(to_test)
    assert encoded == to_test


def test_msgpack_utils__custom_decode__can_decode_decimals():
    """
    Make sure the custom decoder can decode decimal objects
    """
    to_test = Decimal('11.01')
    encoded = {'__decimal__': True, 'as_str': str(to_test)}
    decoded = msgpack_utils.custom_decode(encoded)
    assert to_test == decoded


def test_msgpack_utils__custom_decode__can_decode_sets():
    """
    Make sure the custom decoder can decode set objects
    """
    to_test = set(['thisisatest', 'stillatest'])
    encoded = {'__set__': True, 'value': list(to_test)}
    decoded = msgpack_utils.custom_decode(encoded)
    assert to_test == decoded


def test_msgpack_utils__custom_decode__can_decode_uuids():
    """
    Make sure the custom decoder can decode uuid objects
    """
    to_test = uuid4()
    encoded = {'__uuid__': True, 'as_str': str(to_test)}
    decoded = msgpack_utils.custom_decode(encoded)
    assert to_test == decoded


def test_msgpack_utils__custom_decode__do_nothing_for_regular_obj():
    """
    Make sure the custom decoder will do nothing to a non-specified object.
    """
    to_test = 'Regular Object Test...'
    decoded = msgpack_utils.custom_decode(to_test)
    assert to_test == decoded


def test_msgpack_utils__msg_pack__will_pack_and_unpack_decimal_object():
    """
    Make sure the function can pack a decimal object.
    """
    to_test = {
        'regular_key': 'This is a regular obj...',
        'decimal_key': Decimal('22.2'),
    }

    encoded = msgpack_utils.msg_pack(to_test)
    decoded = msgpack_utils.msg_unpack(encoded)
    assert to_test == decoded


def test_msgpack_utils__msg_pack__will_pack_and_unpack_uuid_object():
    """
    Make sure the function can pack a decimal object.
    """
    to_test = {
        'regular_key': 'This is a regular obj...',
        'uuid_key': uuid4(),
    }

    encoded = msgpack_utils.msg_pack(to_test)
    decoded = msgpack_utils.msg_unpack(encoded)
    assert to_test == decoded
