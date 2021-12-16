import pydicom
import nibabel as nib
from nibabel.testing import data_path
import os
import Type as TP
class DicomFileHandler:

    def readByte(self,name):
        result = []
        with open(name, "rb") as f:
            byte = f.read(1)
            while byte:
                result.append(byte)
                byte = f.read(1)
        return result,self.getNameOfFile(name)


    
    def writeDicomByte(self,path,name,byteArray):
        with open(self.createDcmName(path,name),"wb") as f:
            f.write(byteArray)


    def readNifti(self,name):
        filePath = os.path.join(data_path, name)
        return nib.load(filePath),self.getNameOfFile(name)

    def readDicomPydicom(self,name):
        file =   pydicom.dcmread(name)
        return file,self.getNameOfFile(name)


    def writeFilePyDicom(self,path,name,result):
        result.save_as(self.createDcmName(path,name))

    def getNameOfFile(self,name):
        return name.split('/')[-1].split('.')[0] + "_result"

    
    def getFileType(self,name):
        stringType = self.getFileTypeName(name)
        if(stringType == "dcm"):
            return TP.Type.DICOM
        elif(stringType == "nii"):
            return TP.Type.NIFTI
        else:
            raise Exception("the app dose not support this kind of format")

    def getFileTypeName(self,name):
        return name.split('/')[-1].split('.')[1]
    

    def createDcmName(self,path,name):
        return path+"/"+name+".dcm"


DicomHandler = DicomFileHandler()