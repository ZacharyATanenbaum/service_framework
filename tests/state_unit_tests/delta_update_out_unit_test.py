""" File to conduct unit tests on the delta update out state """

from decimal import Decimal
from service_framework.utils.msgpack_utils import msg_pack
from service_framework.states.out.delta_update_out import DeltaUpdateOut


def test_delta_update_out__get_addresses_model__returns_pub_and_rep_requirements():
    """
    Make sure the address model is defined.
    """
    addresses_model = DeltaUpdateOut.get_addresses_model()
    required_model = {
        'required_addresses': {
            'publisher': str,
            'replyer': str,
        },
        'optional_addresses': {},
    }

    assert addresses_model == required_model


def test_delta_update_out__get_compatable_state_types__returns_proper_types():
    """
    Make sure comptable types are defined.
    """
    compatable_types = DeltaUpdateOut.get_compatable_state_types()
    required_types = {'delta_update_in'}

    for compatable in compatable_types:
        assert compatable in required_types
        required_types.remove(compatable)


def test_delta_update_out__get_creation_arguments_model__happy_case():
    """
    Make sure creation arguments are properly defined.
    """
    obtained_args = DeltaUpdateOut.get_creation_arguments_model()
    required_args = {
        'required_creation_arguments': {},
        'optional_creation_arguments': {
            'topic': str,
            'is_x_pub': bool,
            'wait_after_creation_s': float,
        },
    }
    assert obtained_args == required_args


def test_delta_update_out__get_state_type__happy_case():
    """
    Make sure the state type is defined properly.
    """
    assert DeltaUpdateOut.get_state_type() == 'delta_update_out'


def test_delta_update_out__setup_topic__returns_proper_topic_if_provided():
    """
    Make sure the topic is properly defined.
    """
    required_topic = 'TEST_TOPIC'
    model = {
        'optional_creation_arguments': {
            'topic': required_topic
        }
    }
    topic = DeltaUpdateOut._setup_topic(model)

    assert topic == required_topic


def test_delta_update_out__setup_topic__returns_no_topic_if_not_provided():
    """
    Make sure the topic still works even if not defined.
    """
    topic = DeltaUpdateOut._setup_topic({})
    assert topic == ''


def test_delta_update_out__decode_message__returns_properly_decoded_message():
    """
    Make sure a message will be properly decoded.
    """
    payload = {
        'THIS IS A TEST': Decimal('1234.43112')
    }
    binary_payload = msg_pack(payload)
    unpacked_payload = DeltaUpdateOut._decode_message(binary_payload)

    assert unpacked_payload == payload
