
from environment.environment_elements import Superadobe, InternalRobotTrack, PressurizedModule, SuperadobePath, ControlTower, PavedRoad, HumanQuitArea, CommunicationCenter, LoadingDock, LunarTransportationShed, ClearanceArea
import pandas as pd
import numpy as np

def load_environment_from_excel():
    """
    Reads the Excel file, parses each sheet, and returns a dictionary
    of lists of environment objects. Modify sheet names & column
    mappings to match your actual data.
    """
    
    # load the excel file
    xls = pd.read_excel('data/LunarBase.xlsx', sheet_name=None)
    # Store the Excel sheet names in a variable
    sheet_names = list(xls.keys())
    
        # Container to store environment objects keyed by their sheet names
    environment_data = {sheet_name: [] for sheet_name in sheet_names}

    # 1) Parse the "Superadobes" sheet
    if "Superadobes" in xls.keys():
        df_superadobes = xls["Superadobes"]
        for _, row in df_superadobes.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", "Radius", "Height", ...
            # for ID, combine Tag and row index to make it unique
                        
            elem_id = f"Superadobe_{row.name+1}"
            tag = row.get("Tag", "")
            x = row.get("Center_x", 0.0)
            y = row.get("Center_y", 0.0)
            radius = row.get("Radius", 0.0)
           

            # Create a Superadobe instance
            sa = Superadobe(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                radius=radius
                # pass extra **kwargs if needed
            )
            environment_data['Superadobes'].append(sa)
    
    # 2) Parse the "PressurizedModules" sheet

    if "PressurizedModules" in xls.keys():
        df_Pressurized_modules = xls["PressurizedModules"]
        for _, row in df_Pressurized_modules.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", "Length", "Diameter", ...
            elem_id = f"Pressurized Module_{row.name+1}"
            tag = row.get("Tag", "")
            x = row.get("Corner_x", 0.0)
            y = row.get("Corner_y", 0.0)
            length = row.get("Length", 0.0)
            width = row.get("Width", 0.0)

            # Create a PressurizedModule instance
            pm = PressurizedModule(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['PressurizedModules'].append(pm)


        
    # 3) Parse the "SuperadobePath" sheet
    if "SuperadobePaths" in xls.keys():
        df_superadobepath = xls["SuperadobePaths"]
        for _, row in df_superadobepath.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"Superadobepath_{row.name+1}"
            tag = row.get("Tag", "")
            x = row.get("Corner_x", 0.0)
            y = row.get("Corner_y", 0.0)
            length = row.get("Length", 0.0)
            width = row.get("Width", 0.0)
            # Create a SuperadobePath instance
            sap = SuperadobePath(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['SuperadobePaths'].append(sap)
 
    # 4) Parse the "ControlTowers" sheet

    if "ControlTowers" in xls.keys():
        df_control_towers=xls["ControlTowers"]
        for _,row in df_control_towers.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"ControlTower_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Center_x",0.0)
            y = row.get("Center_y",0.0)
            length = row.get("Height",0.0)
            width = row.get("Width",0.0)
            # Create a ControlTower instance
            ct = ControlTower(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['ControlTowers'].append(ct)

 # 5) Parse the "PavedRoads" sheet
    if "PavedRoads" in xls.keys():
        df_paved_roads =xls["PavedRoads"]
        for _, row in df_paved_roads.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"PavedRoad_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Corner_x",0.0)
            y = row.get("Corner_y",0.0)
            length = row.get("Length",0.0)
            width = row.get("Width",0.0)
            # Create a PavedRoad instance
            pr = PavedRoad(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['PavedRoads'].append(pr)

# 6) Parse the "HumanQuitAreas" sheet

    if "HumanQuitAreas" in xls.keys():
        df_human_quit_area = xls["HumanQuitAreas"]
        for _, row in df_human_quit_area.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"HumanQuitArea_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Corner_x",0.0)
            y = row.get("Corner_y",0.0)
            length = row.get("Length",0.0)
            width = row.get("Width",0.0)
            # Create a HumanQuitArea instance
            hqa = HumanQuitArea(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['HumanQuitAreas'].append(hqa)

# 7) Parse the "CommunicationCenters" sheet

    if "CommunicationCenters" in xls.keys():
        df_communication_center = xls["CommunicationCenters"]
        for _, row in df_communication_center.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"CommunicationCenter_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Center_x",0.0)
            y = row.get("Center_y",0.0)
            radius = row.get("Radius",0.0)
           
            # Create a CommunicationCenter instance
            cc = CommunicationCenter(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                radius=radius
                # pass extra **kwargs if needed
            )
            environment_data['CommunicationCenters'].append(cc)

# 8) Parse the "LoadingDocks" sheet
    if "LoadingDocks" in xls.keys():
        df_loading_dock = xls["LoadingDocks"]
        for _, row in df_loading_dock.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"LoadingDock_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Corner_x",0.0)
            y = row.get("Corner_y",0.0)
            length = row.get("Length",0.0)
            width = row.get("Width",0.0)
            # Create a LoadingDock instance
            ld = LoadingDock(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['LoadingDocks'].append(ld)

# 9) Parse the "LunarTransportationSheds" sheet

    if "LunarTransportationSheds" in xls.keys():
        df_lunar_transportation_shed = xls["LunarTransportationSheds"]
        for _, row in df_lunar_transportation_shed.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"LunarTrasportationShed_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Corner_x",0.0)
            y = row.get("Corner_y",0.0)
            length = row.get("Length",0.0)
            width = row.get("Width",0.0)
            # Create a LunarTrasportationShed instance
            lts = LunarTransportationShed(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['LunarTransportationSheds'].append(lts)

# 10) Parse the "ClearanceAreas" sheet
    if "ClearanceAreas" in xls.keys():
        df_clearance_area = xls["ClearanceAreas"]
        for _, row in df_clearance_area.iterrows():
            # Extract columns. Example column names:
            # "ID", "Tag", "X", "Y", ...
            elem_id = f"ClearanceArea_{row.name+1}"
            tag = row.get("Tag","")
            x = row.get("Corner_x",0.0)
            y = row.get("Corner_y",0.0)
            length = row.get("Length",0.0)
            width = row.get("Width",0.0)
            # Create a ClearanceArea instance
            ca = ClearanceArea(
                element_id=elem_id,
                tag=tag,
                x_coord=x,
                y_coord=y,
                length=length,
                width=width
                # pass extra **kwargs if needed
            )
            environment_data['ClearanceAreas'].append(ca)
# 11) Parse the "InternalRobotTracks" sheet

    if "InternalRobotTracks" in xls.keys():
        df_internal_robot_track = xls["InternalRobotTracks"]
         # Extract lines where Straight is True
        line_rows = df_internal_robot_track[df_internal_robot_track['Note'] == 'Straight']
        lines = [
            ((row['X1'] , row['Y1'] ),
            (row['X2'] , row['Y2'] ))
            for _, row in line_rows.iterrows()
        ]

        # Extract rectangles where Identification is Rect
        rect_rows = df_internal_robot_track[df_internal_robot_track['Note'] == 'Rect']
        rects = [
            (row['X1'] ,
            row['Y1'] ,
            (row['X2']) ,
            (row['Y2']))
            for _, row in rect_rows.iterrows()
        ]

        irt= InternalRobotTrack(
            element_id="InternalRobotTrack_1",
            tag="InternalRobotTrack",
            lines=lines,
            rects=rects
        )

    environment_data['InternalRobotTracks'].append(irt)

    # Return the dictionary containing all environment objects
    return environment_data
