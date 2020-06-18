# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: robotics.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()



DESCRIPTOR = _descriptor.FileDescriptor(
  name='robotics.proto',
  package='robotics',
  serialized_pb=_b('\n\x0erobotics.proto\x12\x08robotics\"X\n\rRobotics_Data\x12\r\n\x05login\x18\x01 \x01(\t\x12\x14\n\x0c\x65nc_password\x18\x02 \x01(\t\x12\x10\n\x08split_id\x18\x03 \x01(\x03\x12\x10\n\x08log_data\x18\x04 \x03(\t\"\x95\x01\n\nLoginReply\x12?\n\x11\x63onnection_status\x18\x01 \x01(\x0e\x32$.robotics.LoginReply.LoginErrorsEnum\"F\n\x0fLoginErrorsEnum\x12\x06\n\x02OK\x10\x00\x12\x19\n\x15\x42\x41\x44_LOGIN_OR_PASSWORD\x10\x01\x12\x10\n\x0c\x42\x41\x44_SPLIT_ID\x10\x02\"\x15\n\x06Signal\x12\x0b\n\x03\x65nd\x18\x01 \x01(\x05\x42\x02H\x01')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_LOGINREPLY_LOGINERRORSENUM = _descriptor.EnumDescriptor(
  name='LoginErrorsEnum',
  full_name='robotics.LoginReply.LoginErrorsEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_LOGIN_OR_PASSWORD', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_SPLIT_ID', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=198,
  serialized_end=268,
)
_sym_db.RegisterEnumDescriptor(_LOGINREPLY_LOGINERRORSENUM)


_ROBOTICS_DATA = _descriptor.Descriptor(
  name='Robotics_Data',
  full_name='robotics.Robotics_Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='login', full_name='robotics.Robotics_Data.login', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enc_password', full_name='robotics.Robotics_Data.enc_password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='split_id', full_name='robotics.Robotics_Data.split_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='log_data', full_name='robotics.Robotics_Data.log_data', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=116,
)


_LOGINREPLY = _descriptor.Descriptor(
  name='LoginReply',
  full_name='robotics.LoginReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connection_status', full_name='robotics.LoginReply.connection_status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LOGINREPLY_LOGINERRORSENUM,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=268,
)


_SIGNAL = _descriptor.Descriptor(
  name='Signal',
  full_name='robotics.Signal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='end', full_name='robotics.Signal.end', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=270,
  serialized_end=291,
)

_LOGINREPLY.fields_by_name['connection_status'].enum_type = _LOGINREPLY_LOGINERRORSENUM
_LOGINREPLY_LOGINERRORSENUM.containing_type = _LOGINREPLY
DESCRIPTOR.message_types_by_name['Robotics_Data'] = _ROBOTICS_DATA
DESCRIPTOR.message_types_by_name['LoginReply'] = _LOGINREPLY
DESCRIPTOR.message_types_by_name['Signal'] = _SIGNAL

Robotics_Data = _reflection.GeneratedProtocolMessageType('Robotics_Data', (_message.Message,), dict(
  DESCRIPTOR = _ROBOTICS_DATA,
  __module__ = 'robotics_pb2'
  # @@protoc_insertion_point(class_scope:robotics.Robotics_Data)
  ))
_sym_db.RegisterMessage(Robotics_Data)

LoginReply = _reflection.GeneratedProtocolMessageType('LoginReply', (_message.Message,), dict(
  DESCRIPTOR = _LOGINREPLY,
  __module__ = 'robotics_pb2'
  # @@protoc_insertion_point(class_scope:robotics.LoginReply)
  ))
_sym_db.RegisterMessage(LoginReply)

Signal = _reflection.GeneratedProtocolMessageType('Signal', (_message.Message,), dict(
  DESCRIPTOR = _SIGNAL,
  __module__ = 'robotics_pb2'
  # @@protoc_insertion_point(class_scope:robotics.Signal)
  ))
_sym_db.RegisterMessage(Signal)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\001'))
# @@protoc_insertion_point(module_scope)
