import arcpy
import os

arcpy.env.overwriteOutput = True

sr = arcpy.GetParameter(0) 


arcpy.env.workspace = arcpy.GetParameterAsText(1) 
shapefileFolder = arcpy.GetParameterAsText(2) 

filesList = os.listdir(shapefileFolder)
failList = []
count = 0.0
itemPosition = 0

for i in filesList:
	try:
		if i.endswith('.shp'):
			itemPosition += 1
			shp = os.path.join(shapefileFolder,i)
			srName = arcpy.Describe(shp).SpatialReference.name
			
			if srName == "Unknown":
				arcpy.AddMessage(str(itemPosition) + ": " + i + " is in an unknown projection.")
				failList.append(i)
				continue
			elif srName == sr.name:
				arcpy.AddMessage(str(itemPosition) + ": " + i + " is already in " + sr.name)
				count += 1
				continue

			arcpy.Project_management(shp, i[:-4] + '_prj', sr)
			arcpy.AddMessage(str(itemPosition) + ": " + i + " was projected from " + srName + " into " + sr.name)
			count += 1
	except:
		failList.append(i)

arcpy.AddMessage("*"*50)
arcpy.AddMessage(str(round((count/len([i for i in filesList if i.endswith(".shp")]))*100,2)) + "% of shapefiles were successfully projected.")
for fail in failList:
	arcpy.AddMessage("Failed: " + fail)
arcpy.AddMessage("*"*50)