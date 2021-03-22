from math import nan, inf
import datetime
import opil
import sbol3
from sbol3.constants import SBO_FUNCTIONAL_ENTITY, SBO_SIMPLE_CHEMICAL
from tyto import NCIT, SBO, OM

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

# example doc: https://docs.google.com/document/d/1M0Xw4477859-CaglaEVUuFeK5B2WmzJosuPiVVStx6U/edit#heading=h.juneem4wj3cn


class HTCOpilGenerator():

    def __init__(self):
        sbol3.set_homespace('http://aquarium.bio/')
        self.doc = sbol3.Document()

    def template_feature(self, *, id: str, name: str, description: str, type: str, role: str) -> sbol3.LocalSubComponent:
        feature = sbol3.LocalSubComponent([type], identity=id)
        feature.name = name
        feature.description = description
        feature.roles = [role]

        return feature

    def build_samples(self) -> opil.SampleSet:
        variable_components = []

        # TODO: is the component type correct?
        template = sbol3.Component("htc_design", SBO.functional_entity)
        template.description = "HTC Sample Design"

        # TODO: are there media URIs?
        design_component = self.template_feature(
            id="media",
            name="Media",
            description="URI for the media",
            type=SBO_FUNCTIONAL_ENTITY,
            role=NCIT.get_uri_by_term('Growth Medium')
        )
        template.features.append(design_component)
        variable = sbol3.VariableFeature(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        variable.description = "Variable for media"
        variable_components.append(variable)

        design_component = self.strain_feature()
        template.features.append(design_component)
        variable = sbol3.VariableFeature(
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
            type=SBO_SIMPLE_CHEMICAL,
            role=NCIT.Inducer
        )
        # note: using SBO.concentration_of_an_entity_pool instead of
        #  'http://purl.obolibrary.org/obo/UO_0000278'
        concentration = sbol3.Measure(
            nan,
            SBO.concentration_of_an_entity_pool,
            identity='inducer_concentration'
        )
        concentration.description = "Inducer concentration"

        design_component.measures = [concentration]
        template.features.append(design_component)

        variable = sbol3.VariableFeature(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        # TODO: remove once pysbol is updated
        variable.variant_measure = sbol3.OwnedObject(
            variable, 'http://sbols.org/v3#variantMeasure', 1, inf, initial_value=[concentration])

        variable.description = "Variable for inducer"
        variable_components.append(
            variable
        )

        design_component = self.template_feature(
            id="antibiotic",
            name="Antibiotic",
            description="The antibiotics for the condition",
            type=SBO_SIMPLE_CHEMICAL,
            role=NCIT.Antibiotic
        )
        # note: using SBO.concentration_of_an_entity_pool instead of
        #  'http://purl.obolibrary.org/obo/UO_0000278'
        concentration = sbol3.Measure(
            nan,
            SBO.concentration_of_an_entity_pool,
            identity='antibiotic_concentration'
        )
        concentration.description = "Antibiotic concentration"

        design_component.measures = [concentration]
        template.features.append(design_component)

        variable = sbol3.VariableFeature(
            cardinality=sbol3.SBOL_ONE_OR_MORE,
            variable=design_component
        )
        # TODO: remove once pysbol is updated
        variable.variant_measure = sbol3.OwnedObject(
            variable, 'http://sbols.org/v3#variantMeasure', 1, inf, initial_value=[concentration])
        variable.description = "Variable for antibiotic"
        variable_components.append(variable)

        self.doc.add(template)

        sample_space = opil.SampleSet(
            "culture_conditions"
        )
        sample_space.template = template
        sample_space.name = "HTC culture condition design"
        sample_space.variable_features = variable_components
        self.doc.add(sample_space)

        return sample_space

    def strain_feature(self):
        return self.template_feature(
            id="strain",
            name="Strain",
            description="URI for the strain",
            role=NCIT.get_uri_by_term('Organism Strain'),
            type=SBO_FUNCTIONAL_ENTITY
        )

    def build_time_interval(self, *, min: float = 0.0, max: float = 24.0):
        interval = opil.TimeInterval()
        interval.minTime = opil.Measure(min, OM.hour)
        interval.maxTime = opil.Measure(max, OM.hour)
        return [interval]

    def flow_type(self):
        measurement_type = opil.MeasurementType('flow')
        measurement_type.name = "Flow Cytometry"
        measurement_type.description = "flow measurement type which is ncit:C78806"
        measurement_type.type = NCIT.get_uri_by_term('Flow Cytometer')
        measurement_type.allowed_time = self.build_time_interval()
        return measurement_type

    def plate_reader_type(self):
        measurement_type = opil.MeasurementType('plate_reader')
        measurement_type.name = "Plate Reader"
        measurement_type.description = "plate reader measurement ncit:C70661"
        measurement_type.type = NCIT.get_uri_by_term('Microplate Reader')
        measurement_type.allowed_time = self.build_time_interval()
        # TODO: not sure about this – this is strateos number
        measurement_type.maxMeasurements = 6

        return measurement_type

    def build_measurements(self):
        measurement_types = []
        measurement_types.append(self.flow_type())
        measurement_types.append(self.plate_reader_type())
        return measurement_types

    def hours(self, value):
        return sbol3.Measure(value, OM.hour, identity="hours_{}".format(value))

    def build_measure(self, *, id: str, name: str, type: str):
        parameter = opil.MeasureParameter(id)
        parameter.name = name
        parameter.minMeasure = opil.Measure(0.0, OM.hour)
        parameter.maxMeasure = opil.Measure(24.0, OM.hour)
        parameter.maxMeasurements = 6
        parameter.required = True
        return parameter

    # added this b/c of
    def build_string_parameter(self, *, id: str, name: str, default_value: str = ''):
        param = opil.StringParameter(id)
        param.name = name
        if default_value:
            default = opil.StringValue(id + '_default')
            default.value = default_value
            param.default_value = default
        return param

    def build_flag(self, *, id: str, name: str, description: str):
        param = opil.BooleanParameter(id)
        param.name = name
        param.description = description
        return param

    def build_parameters(self):
        return [
            # plate reader parameters
            # measurement type: OD, GFP, OD&GFP
            # dilution: Optional[int] (actually restricted to a list)

            # flow parameters
            self.build_flag(
                id='calibrate_cytometer',
                name='CytometerCalibrationFlag',
                description='Indicate whether a calibration plate should be run'
            ),
            self.build_flag(
                id='discard_plate',
                name='DiscardFlag',
                description='Indicates whether measurement plates should be discarded after measurement'
            )
        ]

    def build_protocol(self):
        protocol = opil.ProtocolInterface('htc')
        protocol.name = 'High-Throughput Culturing'
        protocol.description = 'Aquarium high-throughput culturing workflow'
        protocol.allowed_samples.append(self.build_samples())
        protocol.protocol_measurement_type = self.build_measurements()
        protocol.has_parameter = self.build_parameters()

        return protocol

    def generate_protocol(self):
        protocol = self.build_protocol()
        self.doc.add(protocol)

        today = datetime.date.today()
        filename = "jellyfish_htc_{}.xml".format(today.strftime("%Y%m%d"))

        self.doc.write(filename, file_format='xml')

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
