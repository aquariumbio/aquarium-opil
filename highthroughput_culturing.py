from math import nan
import opil
import sbol3
from sbol3 import component

# sample space -- jellyfish table
# media
# strain
# - identity (Aquarium sample name/id)
# - strain status/form e.g., Yeast Glycerol Stock (Aquarium ObjectType)
# - strain item (Aquarium item ID)
# inducer
# - name
# - concentration list
# antibiotic
# - identity (name)
# - concentration
# options - may be parameters


class HTCOpilGenerator():

    def __init__(self):
        sbol3.set_homespace('http://aquarium.bio/')
        self.doc = sbol3.Document()

    def template_feature(self, *, id: str, name: str, description: str, type: str) -> sbol3.LocalSubComponent:
        feature = sbol3.LocalSubComponent(
            [type], name=id)
        feature.name = name
        feature.description = description

        return feature

    def build_samples(self) -> sbol3.Component:
        variable_components = []

        # TODO: is the component type correct?
        template = sbol3.Component("htc_design", sbol3.SBOL_COMPONENT)
        template.description = "HTC Sample Design"

        # TODO: are there media URIs?
        design_component = self.template_feature(
            id="media",
            name="Media",
            description="URI for the media",
            type='https://identifiers.org/ncit:C85504'
        )
        template.features.append(design_component)
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        variable.description = "Variable for media"
        variable_components.append(variable)

        design_component = self.strain_feature()
        template.features.append(design_component)
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE,
            variable=design_component
        )
        variable.description = "Variable for strain"
        variable_components.append(
            variable
        )

        design_component = self.template_feature(
            id="inducer",
            name="Inducer",
            description="The inducers for the condition",
            type='https://identifiers.org/ncit:C120268'
        )
        concentration = sbol3.Measure(
            nan,
            'http://purl.obolibrary.org/obo/UO_0000278',
            name='inducer_concentration'
        )
        concentration.description = "Inducer concentration"
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=concentration
        )
        variable.description = "Variable for inducer concentration"
        variable_components.append(
            variable
        )
        design_component.measures = [concentration]
        template.features.append(design_component)
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        variable.description = "Variable for inducer"
        variable_components.append(
            variable
        )

        design_component = self.template_feature(
            id="antibiotic",
            name="Antibiotic",
            description="The antibiotics for the condition",
            type='https://identifiers.org/ncit:C258'
        )
        concentration = sbol3.Measure(
            nan,
            'http://purl.obolibrary.org/obo/UO_0000278',
            name='antibiotic_concentration'
        )
        concentration.description = "Antibiotic concentration"
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=concentration
        )
        variable.description = "Variable for antibiotic concentration"
        variable_components.append(
            variable
        )
        design_component.measures = [concentration]
        template.features.append(design_component)
        variable = sbol3.VariableComponent(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        variable.description = "Variable for antibiotic"
        variable_components.append(variable)
        self.doc.add(template)

        sample_space = sbol3.CombinatorialDerivation(
            "culture_conditions",
            template,
            type_uri='http://bbn.com/synbio/opil#SampleSet'
        )
        sample_space.name = "HTC culture condition design"
        sample_space.name = "The HTC culture condition design"
        sample_space.variable_components = variable_components
        self.doc.add(sample_space)

        return sample_space

    def strain_feature(self):
        return self.template_feature(
            id="strain",
            name="Strain",
            description="URI for the strain",
            type='https://identifiers.org/ncit:C14419'
        )

    def flow_type(self):
        measurement_type = opil.MeasurementType('flow')
        measurement_type.name = "Flow Cytometry"
        measurement_type.description = "flow measurement type which is ncit:C78806"
        measurement_type.type_uri = "https://identifiers.org/ncit:C78806"
        return measurement_type

    def plate_reader_type(self):
        measurement_type = opil.MeasurementType('plate_reader')
        measurement_type.name = "Plate Reader"
        measurement_type.description = "plate reader measurement ncit:C70661"
        measurement_type.type_uri = "https://identifiers.org/ncit:C70661"
        return measurement_type

    def build_measurements(self):
        measurement_types = []
        measurement_types.append(self.flow_type())
        measurement_types.append(self.plate_reader_type())
        return measurement_types

    def build_parameters(self):
        return []

    def build_protocol(self):
        protocol = opil.ProtocolInterface('htc')
        protocol.name = 'High-Throughput Culturing'
        protocol.description = 'Aquarium high-throughput culturing workflow'
        protocol.sample_set = self.build_samples()
        # protocol.allowed_samples = self.build_samples()
        protocol.protocol_measurement_type = self.build_measurements()
        protocol.has_parameter = self.build_parameters()

        return protocol

    def generate_protocol(self):
        protocol = self.build_protocol()
        self.doc.add(protocol)

        self.doc.write('jellyfish_htc.ttl', file_format='ttl')

    # sample space -- jellyfish table
    # media
    # strain
    # - identity (Aquarium sample name/id)
    # - strain status/form e.g., Yeast Glycerol Stock (Aquarium ObjectType)
    # - strain item (Aquarium item ID)
    # inducer
    # - name
    # - concentration list
    # antibiotic
    # - identity (name)
    # - concentration
    # options - may be parameters


def main():
    generator = HTCOpilGenerator()
    generator.generate_protocol()


if __name__ == "__main__":
    main()
