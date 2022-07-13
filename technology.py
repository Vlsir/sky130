from google.protobuf import text_format
from protos import tech_pb2

tech = tech_pb2.Technology()
tech.name = "Sky130"

LAYER_MAP_FILE = 'S130.layermap'

def guess_layer_purpose_type(named_purpose: str) -> tech_pb2.LayerPurposeType:
    text = named_purpose.lower().strip()
    if text in ('label',):
        return tech_pb2.LayerPurposeType.LABEL
    if text in ('drawing',):
        return tech_pb2.LayerPurposeType.DRAWING
    if text in ('pin',):
        return tech_pb2.LayerPurposeType.PIN
    if text in ('blockage',):
        return tech_pb2.LayerPurposeType.OBSTRUCTION

    return tech_pb2.LayerPurposeType.UNKNOWN

with open(LAYER_MAP_FILE) as f:
    for line in f.readlines():
        if line.startswith('#') or line == '\n':
            continue

        name, purpose, number, datatype = line.strip().split()
        
        layer = tech.layers.add()
        layer.name = name
        layer.purpose.description = purpose
        layer.purpose.type = guess_layer_purpose_type(purpose)
        layer.index = int(number)
        layer.sub_index = int(datatype)

print(f'read {LAYER_MAP_FILE}')

output_name_prefix = tech.name.lower()

output_file = f'{output_name_prefix}.technology.pb'
with open(output_file, 'wb') as f:
    f.write(tech.SerializeToString())
print(f'wrote {output_file}')

output_file = f'{output_name_prefix}.technology.pb.txt'
with open(output_file, 'w') as f:
    f.write(text_format.MessageToString(tech))
print(f'wrote {output_file}')
