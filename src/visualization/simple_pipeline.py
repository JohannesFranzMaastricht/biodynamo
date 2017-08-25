from paraview.simple import *
from paraview import vtk
from paraview import coprocessing

#Code generated from cpstate.py to create the CoProcessor.
#ParaView 5.3.0 64 bits

## Default filter name for data-feedback
propFilterName = "ProgrammableFilter1"

# Read propagation python script
propDiameterFilterScript = ''
try:
    with open('./prop_diameter_filter.py', 'r') as f:
        propDiameterFilterScript = f.read()
except IOError as err:
    # print 'Error: ' + err.strerror
    pass;

#CoProcessor definition
def CreateCoProcessor():
    def _CreatePipeline(coprocessor, datadescription):
        class Pipeline :
            #state file generated using paraview version 5.3.0
            global propDiameterFilterScript

            #disable automatic camera reset on 'Show'
            paraview.simple._DisableFirstRenderCameraReset()

            #create a new 'XML Unstructured Grid Reader'
            #create a producer from a simulation input
            biodynamoInput = coprocessor.CreateProducer(datadescription, 'input')

            # create new Programmable filter for propagating user changes
            propDiameterFilter = ProgrammableFilter(guiName="back_propagation", Input=biodynamoInput)
            propDiameterFilter.CopyArrays = True
            propDiameterFilter.Script = propDiameterFilterScript

            #create a new 'Glyph'
            #glyph1 = Glyph(Input = propDiameterFilter, GlyphType = 'Sphere')
            glyph1 = Glyph(guiName="cells", GlyphType = 'Sphere')
            glyph1.Scalars = [ 'POINTS', 'Diameter' ]
            glyph1.Vectors = [ 'POINTS', 'None' ]
            glyph1.ScaleMode = 'scalar'
            glyph1.GlyphMode = 'All Points'
            glyph1.GlyphTransform = 'Transform2'

            #finally, restore active source
            SetActiveSource(glyph1)

        return Pipeline()

    class CoProcessor(coprocessing.CoProcessor):
        def CreatePipeline(self, datadescription):
            self.Pipeline = _CreatePipeline(self, datadescription)

    coprocessor = CoProcessor()

    #these are the frequencies at which the coprocessor updates.
    freqs = { 'input' : [10, 100]}
    coprocessor.SetUpdateFrequencies(freqs)
    return coprocessor

#---------------------------------------------------------------------------------------
#Global variables that will hold the pipeline for each timestep
#Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
#It will be automatically setup when coprocessor.UpdateProducers() is called the
#first time.
coprocessor = CreateCoProcessor()

#---------------------------------------------------------------------------------------
#Enable Live - Visualizaton with ParaView
coprocessor.EnableLiveVisualization(True, 1)

#------------------------------- Data Selection method ---------------------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor


    if datadescription.GetForceOutput() == True:
#We are just going to request all fields and meshes from the simulation
#code / adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

#setup requests for all inputs based on the requirements of the
#pipeline.
    coprocessor.LoadRequestedData(datadescription)

#--------------------------------- Processing method ----------------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    #Update the coprocessor by providing it the newly generated simulation data.
    #If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    #Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    #Write image capture(Last arg : rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable = False)

    #Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)

    UpdatePipeline()

    # ---------------------------------------------------------------------------
    # global propFilterName

    # # Fetch filter object
    # propFilter = FindSource(propFilterName)
    # if not propFilter:
    #     print 'Warning: Filter "%s" cannot be found in PV filters' % propFilterName
    #     return

    # try:
    #     realFilter = servermanager.Fetch(propFilter)
    # except Exception as ex:
    #     print "Error: " + ex.strerror
    #     return

    # if not realFilter:
    #     print 'Warning: Filter "%s" cannot be fetched from the PV client' % propFilterName
    #     return

    # # Fetch all propagation arrays (ArrayName = "Prop*")
    # filterFieldData = realFilter.GetFieldData()
    # propArrays = [  filterFieldData.GetArray(i).GetName()[len("PropIdx"):]
    #     for i in range(filterFieldData.GetNumberOfArrays())
    #     if filterFieldData.GetArray(i).GetName().startswith("PropIdx")
    # ]

    # if not propArrays:
    #     # No changes made by the user
    #     return

    # propIdxArrays = {
    #         arrayName: filterFieldData.GetArray("PropIdx" + arrayName)
    #         for arrayName in propArrays
    # }
    # propValsArrays = {
    #         arrayName: filterFieldData.GetArray("PropVals" + arrayName)
    #         for arrayName in propArrays
    # }

    # # Debugging
    # #for arrayName in propArrays:
    # #    idxArray, valArray = propIdxArrays[arrayName], propValsArrays[arrayName]
    # #    print '%s:  %s' % ("PropIdx" + arrayName,
    # #            [ idxArray.GetValue(i) for i in range(idxArray.GetSize()) ])
    # #    print '%s: %s' % ("PropVals" + arrayName,
    # #            [ valArray.GetValue(i) for i in range(valArray.GetSize()) ])
    # # ----------------------------

    # # Serialize data
    # userData = vtk.vtkFieldData()
    # for arrayName in propArrays:
    #     userData.AddArray(propIdxArrays[arrayName])
    #     userData.AddArray(propValsArrays[arrayName])

    # # Create array of propagation array names
    # propArrayNames = vtk.vtkStringArray()
    # propArrayNames.SetName("PropArrays")
    # propArrayNames.SetNumberOfValues(len(propArrays))
    # for j, arrayName in enumerate(propArrays):
    #     propArrayNames.SetValue(j, arrayName)

    # userData.AddArray(propArrayNames)

    # # Set data to be propagated back to the cpp adapter
    # datadescription.SetUserData(userData)

    # # Clear script changes
    # global propDiameterFilterScript
    # propFilter.Script = propDiameterFilterScript
    # propFilter.UpdatePipeline()