from AhpAnpLib import *
from AhpAnpLib import inputs_AHPLib as input
from AhpAnpLib import structs_AHPLib as str
from AhpAnpLib import calcs_AHPLib as calc
from AhpAnpLib import ratings_AHPLib as rate

#create the model
DLCModel=str.Model("DLC_Excel Ratings Model")

#create goal cluster
cluster0=str.Cluster("1Goal",0)
#create goal node
goal_node=str.Node("GoalNode",0)
#add the goal to the goal cluster
cluster0.addNode2Cluster(goal_node) 
#add the goal cluster to the model 
DLCModel.addCluster2Model(cluster0)

#create criteria nodes
InspectionScheduling=str.Node("1InspectionScheduling",1)
CostEfficiency=str.Node("2CostEfficiency",2)
InspectorEfficiency=str.Node("3InspectorEfficiency",3)
#criteria cluster
cluster1=str.Cluster("2Criteria",1)
#add the nodes to the criteria cluster
cluster1.addMultipleNodes2Cluster(InspectionScheduling,CostEfficiency,InspectorEfficiency)
#add the cluster to the model
DLCModel.addCluster2Model(cluster1)

#Subcriteria cluster and nodes
cluster2=str.Cluster("SubCriteria",2)
sub1=str.Node("1.1FrequencyofInspections",4)
sub2=str.Node("1.2SeasonalAdjustment",5)
sub3=str.Node("2.1FuelConsumption",6)
sub4=str.Node("2.2Downtime",7)
sub5=str.Node("2.3ServiceCenterProximity",8)
sub6=str.Node("3.1TrainingApplication",9)
sub7=str.Node("3.2WorkloadManagement",10)
cluster2.addMultipleNodes2Cluster(sub1,sub2,sub3,sub4,sub5,sub6,sub7)
DLCModel.addCluster2Model(cluster2)

#set up node connections from Goal Node to all the nodes of the 2Criteria cluster
DLCModel.addNodeConnectionFromNodeToAllNodesOfCluster("GoalNode","2Criteria")
#connect 1Cost to all of its Subcriteria
DLCModel.addNodeConnectionFromNodeToAllNodesOfCluster("1InspectionScheduling","SubCriteria")

##start ratings setup
#set model type to ratings
DLCModel.setModelTypeRatings()

# Select bottom level criteria to use in the ratings model
DLCModel.rateModel.addCriteriaByName("1.1FrequencyofInspections","1.2SeasonalAdjustment","2.1FuelConsumption","2.2Downtime","2.3ServiceCenterProximity","3.1TrainingApplication","3.2WorkloadManagement")



# Add the alternatives to be used in the ratings model and add them or use existing nodes
DLCModel.rateModel.addAlternativesByName("1Comprehensive Route Optimization System","2Resource Dynamic Allocation Solution","3Smart Inspection Strategy System")



#Read/Create rating scales to use for the evaluation of the alternatives with respect to the selected criteria
#There are three ways, 1) we can create a scale with values
#2) we can create a scale defining categories only without values and then do pairwise comparisons later
#3) read existing sd model scale from rcp files

#(1)this is how we add a scale that we already know its values
CostScale=rate.RatScale("CostScale")
CostScale.defineScaleByValue(None,False,
["More than 30k per year",25],
["Between 20k and 30k per year",50], 
["Between 15k and 20k per year",75],
["Less than 10k and 15k per year",100]
)
GoodMedPoor=rate.RatScale("GoodMediumPoor_Scale")
GoodMedPoor.defineScaleByValue(None,False,
["Good", 1],
["Med",0.346681], 
["Poor",0.080125]
)

DLCModel.rateModel.assignScale2CriterionByName("1.1FrequencyofInspections","GoodMediumPoor_Scale")
#we can assign the scale to multiple criteria if it is appropriate
#later we will make judgment to calculate the priorities of the categories with respect to each criterion separtely 
DLCModel.rateModel.assignScale2CriterionByName("1.2SeasonalAdjustment","CostScale")
DLCModel.rateModel.assignScale2CriterionByName("2.1FuelConsumption","GoodMediumPoor_Scale")
DLCModel.rateModel.assignScale2CriterionByName("2.2Downtime","CostScale")
DLCModel.rateModel.assignScale2CriterionByName("2.3ServiceCenterProximity","GoodMediumPoor_Scale")
DLCModel.rateModel.assignScale2CriterionByName("3.1TrainingApplication","GoodMediumPoor_Scale")
DLCModel.rateModel.assignScale2CriterionByName("3.2WorkloadManagement","GoodMediumPoor_Scale")

# Print out model structure 
DLCModel.printStruct()

# Excel questionnaire to get criteria of the AHP model
input.export4ExcelQuestFull(DLCModel,"empty.xlsx",True)

#We import the filedin questionnaire of pairwise compairson matrices of the ratings criteria
criteriaJudgmentFile="Data result.xlsx"
criteriaPrioritiesResults="Ratings_DLC_selection_Criteria_priorities.xlsx"
calc.calcAHPMatricesSave2File(DLCModel,criteriaJudgmentFile,criteriaPrioritiesResults,True,False,True)

#Then we can export the ratings table
ratingsTableEmpty="Ratings_DLC_selection_Ratings_Table_empty.xlsx"
input.export4ExcelRatingsSetup(DLCModel, ratingsTableEmpty,True)

#Then we can use the filledin ratings table to calculate and export ratings results
ratingsTableFilledin="Ratings_Car_selection_Ratings_Table_filledin.xlsx"
ratingsTableResults="Ratings_Car_selection_Ratings_results.xlsx"
input.calcExcelRatings(DLCModel, ratingsTableFilledin, ratingsTableResults,False)