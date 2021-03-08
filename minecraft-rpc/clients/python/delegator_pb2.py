# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: delegator.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='delegator.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x64\x65legator.proto\"W\n\x0cServerConfig\x12\x1d\n\tworldType\x18\x01 \x01(\x0e\x32\n.WorldType\x12\x13\n\x0bmaxHeapSize\x18\x02 \x01(\x05\x12\x13\n\x0bminHeapSize\x18\x03 \x01(\x05\"(\n\x05Ports\x12\x0f\n\x07rpcPort\x18\x01 \x01(\x05\x12\x0e\n\x06mcPort\x18\x02 \x01(\x05\"!\n\x04Port\x12\x0c\n\x04port\x18\x01 \x01(\x05\x12\x0b\n\x03msg\x18\x02 \x01(\t\"\x07\n\x05\x45mpty*\"\n\tWorldType\x12\x08\n\x04\x46LAT\x10\x00\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x01\x32V\n\tDelegator\x12)\n\x0eSpawnNewServer\x12\r.ServerConfig\x1a\x06.Ports\"\x00\x12\x1e\n\x0b\x43loseServer\x12\x05.Port\x1a\x06.Empty\"\x00\x62\x06proto3'
)

_WORLDTYPE = _descriptor.EnumDescriptor(
  name='WorldType',
  full_name='WorldType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FLAT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEFAULT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=194,
  serialized_end=228,
)
_sym_db.RegisterEnumDescriptor(_WORLDTYPE)

WorldType = enum_type_wrapper.EnumTypeWrapper(_WORLDTYPE)
FLAT = 0
DEFAULT = 1



_SERVERCONFIG = _descriptor.Descriptor(
  name='ServerConfig',
  full_name='ServerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldType', full_name='ServerConfig.worldType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maxHeapSize', full_name='ServerConfig.maxHeapSize', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='minHeapSize', full_name='ServerConfig.minHeapSize', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=106,
)


_PORTS = _descriptor.Descriptor(
  name='Ports',
  full_name='Ports',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rpcPort', full_name='Ports.rpcPort', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mcPort', full_name='Ports.mcPort', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=148,
)


_PORT = _descriptor.Descriptor(
  name='Port',
  full_name='Port',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='Port.port', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='msg', full_name='Port.msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=183,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=185,
  serialized_end=192,
)

_SERVERCONFIG.fields_by_name['worldType'].enum_type = _WORLDTYPE
DESCRIPTOR.message_types_by_name['ServerConfig'] = _SERVERCONFIG
DESCRIPTOR.message_types_by_name['Ports'] = _PORTS
DESCRIPTOR.message_types_by_name['Port'] = _PORT
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.enum_types_by_name['WorldType'] = _WORLDTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerConfig = _reflection.GeneratedProtocolMessageType('ServerConfig', (_message.Message,), {
  'DESCRIPTOR' : _SERVERCONFIG,
  '__module__' : 'delegator_pb2'
  # @@protoc_insertion_point(class_scope:ServerConfig)
  })
_sym_db.RegisterMessage(ServerConfig)

Ports = _reflection.GeneratedProtocolMessageType('Ports', (_message.Message,), {
  'DESCRIPTOR' : _PORTS,
  '__module__' : 'delegator_pb2'
  # @@protoc_insertion_point(class_scope:Ports)
  })
_sym_db.RegisterMessage(Ports)

Port = _reflection.GeneratedProtocolMessageType('Port', (_message.Message,), {
  'DESCRIPTOR' : _PORT,
  '__module__' : 'delegator_pb2'
  # @@protoc_insertion_point(class_scope:Port)
  })
_sym_db.RegisterMessage(Port)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'delegator_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)



_DELEGATOR = _descriptor.ServiceDescriptor(
  name='Delegator',
  full_name='Delegator',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=230,
  serialized_end=316,
  methods=[
  _descriptor.MethodDescriptor(
    name='SpawnNewServer',
    full_name='Delegator.SpawnNewServer',
    index=0,
    containing_service=None,
    input_type=_SERVERCONFIG,
    output_type=_PORTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CloseServer',
    full_name='Delegator.CloseServer',
    index=1,
    containing_service=None,
    input_type=_PORT,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DELEGATOR)

DESCRIPTOR.services_by_name['Delegator'] = _DELEGATOR

# @@protoc_insertion_point(module_scope)
