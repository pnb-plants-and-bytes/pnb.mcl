from pathlib import Path
from lxml import etree
from pnb.mcl.metamodel.standard import Model
from pnb.mcl.io.xmi import read_xmi
from pnb.mcl.io.xml import XmlExporter
from pnb.mcl.io.rdf import RdfExporter


THIS_DIR = Path(__file__).parent
DEXPI_PROCESS_1_0 = read_xmi(THIS_DIR / 'DEXPI Process 1.0.xmi')

print(DEXPI_PROCESS_1_0)
print()

print(DEXPI_PROCESS_1_0.PhysicalQuantities)
print()

DataTypes = DEXPI_PROCESS_1_0.DataTypes
PhysicalQuantities = DEXPI_PROCESS_1_0.PhysicalQuantities
Process = DEXPI_PROCESS_1_0.Process

M = Model(
    'ExampleProcess',
    'http://www.example.org/ExampleProcess')

M.add(Process.Pumping(
    name='P1',
    Method=Process.PumpingMethod.PositiveDisplacement,
    VolumeFlow=PhysicalQuantities.QualifiedPhysicalQuantity(
        Mode=PhysicalQuantities.QuantityMode.Design,
        Provenance=PhysicalQuantities.QuantityProvenance.Estimated,
        Range=PhysicalQuantities.QuantityRange.Normal),
    Ports=[
        P1_XL2:=Process.MaterialPort(
            Direction=Process.PortDirection.Outlet,
            Identifier='XL2')]))


M.add(Process.Pumping(
    name='P2',
    Method=Process.PumpingMethod.PositiveDisplacement,
    VolumeFlow=PhysicalQuantities.QualifiedPhysicalQuantity(
        Mode=PhysicalQuantities.QuantityMode.Design,
        Provenance=PhysicalQuantities.QuantityProvenance.Estimated,
        Range=PhysicalQuantities.QuantityRange.Normal),
    Ports=[
        P2_XL1:=Process.MaterialPort(
            Direction=Process.PortDirection.Inlet,
            Identifier='XL1')]))

M.add(Process.ProcessConnection(
    Source=P1_XL2,
    Target=P2_XL1))

print(etree.tostring(XmlExporter(M).xml, pretty_print=True, encoding='unicode'))
print()

print(RdfExporter(M).graph.serialize(format='n3'))
print()
