#Read turbine data for ocean current
import csv

#Get Turbine Data
def ReadTurbineData(TurbineFile):
    
    File_Turbine=open(TurbineFile, "r")
    File_Turbine_csv=csv.reader(File_Turbine,delimiter=',')
    
    for EachLine in File_Turbine_csv:
    
        if File_Turbine_csv.line_num==4:
            RotorDepth=float(EachLine[1])
            
        if File_Turbine_csv.line_num==5:
            RatePower=float(EachLine[1])
    
        if File_Turbine_csv.line_num==6:
            RotorDiamater=float(EachLine[1])
            
        if File_Turbine_csv.line_num==7:
            C_Performance=float(EachLine[1])#Coeficient of performance
            
        if File_Turbine_csv.line_num==8:
            E_Gearbox=float(EachLine[1])#Gearbox Efficiency
            
        if File_Turbine_csv.line_num==9:
            E_Generator=float(EachLine[1])#Generator Efficiency
            
        if File_Turbine_csv.line_num==10:
            E_Transformer=float(EachLine[1])
                    
        if File_Turbine_csv.line_num==11:
            E_Inverter=float(EachLine[1])
            
        if File_Turbine_csv.line_num==12:
            Combined_E_Turbine=float(EachLine[1])#Combined power chain conversion efficiency
            
        if File_Turbine_csv.line_num==13:
            Availability=float(EachLine[1])
            
        if File_Turbine_csv.line_num==14:
            E_Transmission=float(EachLine[1])
            
        if File_Turbine_csv.line_num==15:
            MinDepth=float(EachLine[1])

        if File_Turbine_csv.line_num==16:
            MaxDepth=float(EachLine[1])
            
        if File_Turbine_csv.line_num==17:
            Water_rho=float(EachLine[1])
            
            
    File_Turbine.close()
            
    Turbine={"RotorDepth":RotorDepth,
             "RatePower":RatePower,
             "RotorDiamater":RotorDiamater,
             "C_Performance":C_Performance,
             "E_Gearbox":E_Gearbox,
             "E_Generator":E_Generator,
             "E_Transformer":E_Transformer,
             "E_Inverter":E_Inverter,
             "Combined_E_Turbine":Combined_E_Turbine,
             "Availability": Availability,
             "E_Transmission": E_Transmission,
             "MinDepth": MinDepth,
             "MaxDepth": MaxDepth,
             "Water_rho": Water_rho
              }    
    return Turbine