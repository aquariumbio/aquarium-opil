import opil
import sbol3

# sample space -- jellyfish table
# replicate count
# media
# control type
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

    def template_feature(self, *, id: str, name: str, description: str) -> sbol3.LocalSubComponent:
        feature = sbol3.LocalSubComponent(
            [sbol3.SBOL_LOCAL_SUBCOMPONENT], name=id)
        feature.name = name
        feature.description = description

        return feature

    def build_template(self) -> sbol3.Component:
        # TODO: is the component type correct?
        template = sbol3.Component("htc_design", sbol3.SBOL_COMPONENT)

        template.features.append(self.template_feature(
            id="replicate_count",
            name="Replicate Count",
            description="Number of replicates for the condition"
        ))
        # TODO: are there media URIs?
        template.features.append(self.template_feature(
            id="media",
            name="Media",
            description="URI for the media"
        ))
        # TODO: this looks like a component role, but not clear can specify that
        template.features.append(self.template_feature(
            id="control_type",
            name="Control Type",
            description="Indicates that this condition is a control of the given type"
        ))
        template.features.append(self.strain_feature())
        template.features.append(self.template_feature(
            id="inducer",
            name="Inducer",
            description="A list of inducers for the condition"
        ))
        template.features.append(self.template_feature(
            id="antibiotic",
            name="Antibiotic",
            description="A list of antibiotics for the condition"
        ))

        return template

    def strain_feature(self):
        return self.template_feature(
            id="strain",
            name="Strain",
            description="URI for the strain"
        )

    def build_variable_component(self):
        return []

    def build_samples(self):
        template = self.build_template()
        self.doc.add(template)

        sample_space = sbol3.CombinatorialDerivation(
            "culture_conditions",
            template,
            type_uri='http://bbn.com/synbio/opil#SampleSet'
        )
        sample_space.name = "The HTC culture condition design description"
        sample_space.variable_components = self.build_variable_component()
        self.doc.add(sample_space)
        return sample_space

    def flow_type(self):
        measurement_type = opil.MeasurementType('flow')
        measurement_type.name = "Flow Cytometry"
        measurement_type.description = "flow measurement type which is ncit:C78806"
        return measurement_type

    def plate_reader_type(self):
        measurement_type = opil.MeasurementType('plate_reader')
        measurement_type.name = "Plate Reader"
        measurement_type.description = "plate reader measurement ncit:C70661"

    def build_measurements(self):
        measurement_types = []
        measurement_types.append(self.flow_type())
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
    # replicate count
    # media
    # control type
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
